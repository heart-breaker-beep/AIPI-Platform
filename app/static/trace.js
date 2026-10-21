/* Incremental execution timeline. Independent of action requests and status polling. */
(() => {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const labels = {
    created: "任务已创建", critic_agent: "检查分析结果",
    start: "开始分析", approve: "批准并继续", resume: "继续分析", retry: "重试分析",
    replan: "重新规划", pause: "暂停分析", cancel: "取消分析", planner_agent: "制定分析方案",
    design_gate: "等待方案确认", plan_executor: "执行项目分析", human_review: "等待结果审核",
    synthesis: "综合分析", finalizer: "生成与导出报告", end: "分析结束",
    repository_analysis_agent: "获取仓库信息", repository_analysis: "采集仓库资料",
    technology_analysis_agent: "识别技术栈", technology_analysis: "读取技术配置",
    architecture_analysis_agent: "分析代码结构", architecture_analysis: "解析关键源码",
    evidence_analysis_agent: "整理证据", evidence_analysis: "采集直接证据",
    report_synthesis: "生成报告结论", report_generation: "组织报告正文",
    llm_chat: "调用分析模型", read_file: "读取文件", github_repository: "查询仓库信息",
    repository_tree: "读取目录树", report_export: "导出报告", source_selection: "选取关键文件",
  };
  const statuses = { running: "执行中", completed: "已完成", partial: "部分完成", failed: "失败",
    unavailable: "不可用", interrupted: "已中断", waiting: "等待确认", canceled: "已取消" };
  const terminal = new Set(["COMPLETED", "FAILED", "CANCELED"]);
  let runId = null, cursor = 0, generation = 0, timer = null, controller = null;
  let runStatus = null, busy = false, follows = true, failures = 0, filter = false;
  let execution = {}, spans = new Map(), seen = new Set(), nodes = new Map(), windowEnd = null;
  let pendingFinalDrain = false, collapsedFor = null;
  let notifiedExecution = null;
  const list = $("traceList"), panel = $("tracePanel"), body = $("traceBody");

  function el(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function symbol(name) {
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("class", "ico"); svg.setAttribute("aria-hidden", "true");
    const use = document.createElementNS("http://www.w3.org/2000/svg", "use");
    use.setAttribute("href", `#i-${name}`); svg.append(use);
    return svg;
  }
  function label(span) { return span.attributes.file_path || labels[span.name] || span.name; }
  function timeText(span) {
    const ms = span.duration_ms ?? (span.status === "running" ? Date.now() - Date.parse(span.occurred_at) : null);
    return ms === null ? "" : `${Math.max(0, ms / 1000).toFixed(1)} 秒`;
  }
  function notify(text) { if ($("traceConnection").textContent !== text) $("traceConnection").textContent = text; }
  function detailsText(span) {
    const a = span.attributes;
    return [span.message, a.error_type && `错误类型：${a.error_type}`,
      a.total !== undefined && `计划文件：${a.total}`,
      a.read_successful_files !== undefined && `读取成功：${a.read_successful_files}`,
      a.selected_files !== undefined && `选取文件：${a.selected_files}`,
      a.count !== undefined && `证据条目：${a.count}`,
      a.model && `模型：${a.model}`,
      a.total_tokens !== undefined && `用量：${a.total_tokens} tokens`,
      a.attempt > 1 && `第 ${a.attempt} 次尝试`,
      a.file_path && a.branch && `分支：${a.branch}`,
    ].filter(Boolean).join(" · ");
  }
  function render() {
    const all = Array.from(spans.values());
    const exceptionIds = new Set();
    for (const span of all) {
      if (!["failed", "partial", "unavailable", "interrupted"].includes(span.status)) continue;
      let current = span;
      while (current && !exceptionIds.has(current.span_id)) {
        exceptionIds.add(current.span_id);
        current = spans.get(current.parent_span_id);
      }
    }
    const end = windowEnd === null ? all.length : Math.min(windowEnd, all.length);
    const visible = all.slice(Math.max(0, end - 250), end);
    const ids = new Set(visible.map((span) => span.span_id));
    // Preserve all retained DOM nodes, expansion state and keyboard focus.
    for (const [id, node] of nodes) {
      if (!ids.has(id)) { node.remove(); nodes.delete(id); }
    }
    for (const span of visible) {
      let node = nodes.get(span.span_id);
      if (!node) {
        node = el("details", "trace-item");
        node.dataset.span = span.span_id;
        const summary = el("summary", "trace-row");
        const mark = el("span", "trace-mark"); mark.append(symbol("clock"));
        const title = el("span", "trace-name");
        const copy = el("button", "trace-copy");
        copy.type = "button"; copy.setAttribute("aria-label", "复制文件路径");
        copy.title = "复制文件路径"; copy.append(symbol("copy"));
        copy.onclick = (event) => {
          event.preventDefault(); event.stopPropagation();
          navigator.clipboard?.writeText(spans.get(span.span_id)?.attributes.file_path || "")
            .then(() => { copy.title = "已复制"; }).catch(() => { copy.title = "复制失败，请选择路径后复制"; });
        };
        title.append(el("span", "trace-name-text"), copy);
        summary.append(mark, title,
          el("span", "trace-status"), el("time", "trace-time"));
        node.append(summary, el("p", "trace-detail"), el("div", "trace-children"));
        node.open = ["run", "node", "agent"].includes(span.category) || span.status !== "completed";
        nodes.set(span.span_id, node);
        const parent = nodes.get(span.parent_span_id);
        (parent ? parent.querySelector(":scope > .trace-children") : list).append(node);
      }
      node.dataset.status = span.status;
      const container = nodes.get(span.parent_span_id)?.querySelector(":scope > .trace-children") || list;
      if (node.parentNode !== container) container.append(node);
      const name = node.querySelector(":scope > summary .trace-name-text");
      if (name.textContent !== label(span)) name.textContent = label(span);
      node.querySelector(":scope > summary .trace-copy").hidden = !span.attributes.file_path;
      node.querySelector(":scope > summary > .trace-mark use").setAttribute("href",
        `#i-${span.status === "running" ? "clock" : span.status === "completed" ? "check" : "alert"}`);
      node.querySelector(":scope > summary > .trace-status").textContent = statuses[span.status] || span.status;
      node.querySelector(":scope > summary > .trace-time").textContent = timeText(span);
      node.querySelector(":scope > .trace-detail").textContent = detailsText(span);
      node.hidden = filter && !exceptionIds.has(span.span_id);
    }
    $("traceEarlier").hidden = end <= 250;
    $("traceLatest").hidden = windowEnd === null && follows;
    const counts = all.filter((s) => s.category === "file");
    const finished = counts.filter((s) => s.status !== "running");
    const failed = finished.filter((s) => s.status !== "completed").length;
    $("traceSummary").textContent = counts.length ? `文件读取 ${finished.length} 次 · 成功 ${finished.length - failed} · 异常 ${failed}` : "记录实际执行步骤与耗时";
    if (spans.size && follows && windowEnd === null && body.open) list.scrollTop = list.scrollHeight;
    const active = all.filter((s) => s.status === "running").at(-1);
    const latest = all.at(-1);
    if (busy || execution.status === "running") {
      $("traceActivity").textContent = active ? `${label(active)} · 已等待 ${timeText(active)}` : "等待执行事件";
      if (active) $("node").textContent = labels[active.name] || (active.category === "file" ? "读取文件" : active.name);
    } else {
      $("traceActivity").textContent = execution.status === "interrupted" ? "执行心跳已中断，请查询任务状态后再操作" :
        latest ? `最近活动：${label(latest)}` : "任务开始后将在这里显示进展";
    }
  }

  function merge(events) {
    for (const event of events) {
      if (seen.has(event.event_id)) continue;
      seen.add(event.event_id);
      if (event.event_type === "progress") {
        const parent = spans.get(event.span_id);
        if (parent) { parent.message = event.message; Object.assign(parent.attributes, event.attributes); }
        continue;
      }
      const id = event.span_id || event.event_id;
      const previous = spans.get(id);
      spans.set(id, { ...previous, ...event, span_id: id,
        occurred_at: previous?.occurred_at || event.occurred_at,
        attributes: { ...previous?.attributes, ...event.attributes },
      });
    }
    // Keep operation summaries for this run; render at most 250 DOM rows at a time.
    if (seen.size > 6000) seen = new Set(Array.from(seen).slice(-3000));
  }

  async function tick(epoch) {
    if (epoch !== generation || !runId) return;
    controller = new AbortController();
    let again = 1000;
    try {
      const response = await fetch(`/api/v1/analysis/${encodeURIComponent(runId)}/trace?after=${cursor}&limit=200`, { signal: controller.signal });
      if (!response.ok) throw new Error(String(response.status));
      const data = await response.json();
      if (epoch !== generation || data.run_id !== runId) return;
      failures = 0;
      cursor = data.next_cursor;
      execution = data.execution || {};
      const executionKey = `${execution.execution_id}:${execution.status}`;
      if (executionKey !== notifiedExecution) {
        notifiedExecution = executionKey;
        window.dispatchEvent(new CustomEvent("analysisexecution", { detail: { runId, ...execution } }));
      }
      merge(data.events || []);
      if (execution.status === "interrupted") {
        for (const span of spans.values()) {
          if (span.execution_id === execution.execution_id && span.status === "running") span.status = "interrupted";
        }
      }
      const notes = { not_recorded: "该任务暂未记录详细过程", expired: "该任务的过程记录已过期",
        unavailable: "过程记录暂不可用，请检查数据库迁移与服务状态" };
      notify(execution.gap_count ? "部分过程记录缺失，分析仍可继续" : notes[data.trace_state] || "已同步");
      render();
      if (terminal.has(runStatus) && !busy && !data.has_more && execution.status !== "running") {
        pendingFinalDrain = false;
        if (collapsedFor !== runId && runStatus === "COMPLETED") { body.open = false; collapsedFor = runId; }
        return;
      }
      if (data.has_more) again = 30;
      else if (document.hidden) again = 10000;
      else if (!busy && !["running"].includes(execution.status) && !pendingFinalDrain) again = 5000;
    } catch (error) {
      if (epoch !== generation || error.name === "AbortError") return;
      failures += 1;
      notify("过程连接中断，正在重新连接；这不代表分析失败");
      again = Math.min(15000, 1000 * 2 ** failures);
    } finally {
      if (epoch === generation) {
        controller = null;
        clearTimeout(timer);
        // Stop only after a successful final drain, not on a transient error.
        if (!terminal.has(runStatus) || busy || pendingFinalDrain || failures || execution.status === "running") {
          timer = setTimeout(() => tick(epoch), again);
        }
      }
    }
  }
  function wake() {
    clearTimeout(timer);
    // Abort the old fetch; its generation can no longer alter this timeline.
    controller?.abort();
    generation += 1;
    tick(generation);
  }
  function attach(id, status) {
    if (runId !== id) {
      controller?.abort(); clearTimeout(timer); generation += 1;
      runId = id; cursor = 0; spans.clear(); seen.clear(); nodes.clear(); list.replaceChildren();
      follows = true; windowEnd = null; failures = 0; execution = {}; busy = false;
      notifiedExecution = null;
      body.open = true; collapsedFor = null;
    }
    runStatus = status;
    pendingFinalDrain = true;
    panel.classList.remove("hidden");
    wake();
  }
  window.AnalysisTrace = {
    attach,
    isRunning(id) { return runId === id && !terminal.has(runStatus) && execution.status === "running"; },
    currentLabel() {
      const active = Array.from(spans.values()).filter((span) => span.status === "running").at(-1);
      return active ? labels[active.name] || (active.category === "file" ? "读取文件" : active.name) : "正在执行";
    },
    action(id, active) {
      if (runId !== id && !active) return;
      if (runId !== id) attach(id, null);
      busy = active; pendingFinalDrain = true;
      if (active) { body.open = true; collapsedFor = null; }
      wake();
    },
    clear() {
      generation += 1; controller?.abort(); clearTimeout(timer); runId = null;
      panel.classList.add("hidden");
    },
  };
  list.addEventListener("scroll", () => {
    follows = list.scrollHeight - list.scrollTop - list.clientHeight < 45;
    $("traceLatest").hidden = follows && windowEnd === null;
  }, { passive: true });
  $("traceLatest").onclick = () => { follows = true; windowEnd = null; render(); };
  $("traceEarlier").onclick = () => { follows = false; windowEnd = Math.max(250, (windowEnd ?? spans.size) - 250); render(); };
  $("traceFilter").onchange = (event) => { filter = event.target.value === "warning"; render(); };
  document.addEventListener("visibilitychange", () => { if (!document.hidden && runId) wake(); });
  setInterval(() => { if (runId && !document.hidden && (busy || execution.status === "running")) render(); }, 1000);
})();
