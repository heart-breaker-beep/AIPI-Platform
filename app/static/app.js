/* ============================================================
 * AIPI · GitHub 项目智能分析 —— 前端
 * ------------------------------------------------------------
 * 无构建步骤，直接由 FastAPI 以静态文件托管。
 *
 * 数据来源全部是后端已有接口：
 *   POST /api/v1/analysis                     新建分析
 *   GET  /api/v1/analysis                     历史列表
 *   GET  /api/v1/analysis/{id}                状态（轮询）
 *   POST /api/v1/analysis/{id}/{动作}          approve|pause|resume|retry
 *   GET  /api/v1/analysis/{id}/report         markdown 报告
 *   GET  /api/v1/analysis/{id}/report/json    结构化报告  ← 看板的数据源
 *   POST /api/v1/analysis/{id}/deep-dive      单模块深挖
 *   POST /api/v1/analysis/{id}/learning-path  学习路线
 *
 * 与旧版的差别：旧版把 markdown 原样贴出来，
 * 后端已经算好的项目指标、技术栈、目录统计、
 * 六个维度的实现明细、证据清单全部被丢掉了。
 * 现在这些走「数据看板」，markdown 退化成「报告原文」。
 * ============================================================ */

(() => {
  "use strict";

  const API = "/api/v1";
  const POLL_MS = 2000;

  const $ = (id) => document.getElementById(id);

  /* ============================================================
   * 通用工具
   * ============================================================ */

  const esc = (value) =>
    String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");

  const icon = (name, cls) =>
    `<svg class="ico${cls ? " " + cls : ""}"><use href="#i-${name}"/></svg>`;

  const baseName = (p) => String(p || "").split(/[\\/]/).pop();

  /** 把 31724 读成 31.7k，指标卡里更省地方。 */
  function compactNumber(value) {
    const n = Number(value);
    if (!Number.isFinite(n)) return "—";
    if (n < 1000) return String(n);
    if (n < 1e6) return (n / 1000).toFixed(n < 1e4 ? 1 : 0).replace(/\.0$/, "") + "k";
    return (n / 1e6).toFixed(1).replace(/\.0$/, "") + "M";
  }

  /*
   * 把服务端返回的时间字符串转成时间戳。
   *
   * 关键：不带时区标记的字符串，`new Date()` 会按**本地时间**解析。
   * 而服务端历史上存的是 naive UTC（datetime.utcnow），
   * 在 UTC+8 环境下会把「刚刚跑完」显示成「8 小时前」。
   *
   * 后端现在已经补上 UTC 时区（schemas.analysis._assume_utc），
   * 这里再兜一层：万一遇到不带时区的字符串（旧接口、其它端点），
   * 一律按 UTC 解释，而不是交给浏览器猜。
   */
  function parseServerTime(value) {
    if (!value) return NaN;

    const text = String(value);

    const hasZone = /(?:Z|[+-]\d{2}:?\d{2})$/.test(text);

    return new Date(hasZone ? text : text + "Z").getTime();
  }

  function formatDate(value) {
    if (!value) return "";
    const ms = parseServerTime(value);
    if (Number.isNaN(ms)) return String(value);
    const d = new Date(ms);
    const pad = (n) => String(n).padStart(2, "0");
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ` +
           `${pad(d.getHours())}:${pad(d.getMinutes())}`;
  }

  function relativeTime(value) {
    if (!value) return "";
    const then = parseServerTime(value);
    if (Number.isNaN(then)) return "";
    const s = Math.floor((Date.now() - then) / 1000);
    if (s < 60) return "刚刚";
    if (s < 3600) return Math.floor(s / 60) + " 分钟前";
    if (s < 86400) return Math.floor(s / 3600) + " 小时前";
    if (s < 2592000) return Math.floor(s / 86400) + " 天前";
    return formatDate(value).slice(0, 10);
  }

  function toast(message) {
    const el = $("toast");
    el.textContent = message;
    el.classList.add("show");
    clearTimeout(toast._t);
    toast._t = setTimeout(() => el.classList.remove("show"), 2200);
  }

  /* ============================================================
   * Markdown 渲染
   * ------------------------------------------------------------
   * 报告用到的语法是固定的几种：标题 / 表格 / 列表 / 代码块 /
   * 引用 / 行内代码 / 粗斜体 / 链接。
   * 与其从 CDN 拉 marked（离线就瞎），不如自己实现这一小撮，
   * 页面因此零外部依赖。
   * ============================================================ */

  /** 行内元素。输入会被转义，所以这里处理的是已转义文本。 */
  function mdInline(text) {
    let s = esc(text);

    // 行内代码先抠出来占位，免得里面的 * _ 被后面的规则误伤。
    const codes = [];
    s = s.replace(/`([^`]+)`/g, (_, code) => {
      codes.push(code);
      return "\u0000" + (codes.length - 1) + "\u0000";
    });

    // 链接。只放行安全协议，其余降级成纯文本。
    s = s.replace(/\[([^\]]*)\]\(([^)\s]+)\)/g, (_, label, url) => {
      const href = esc(url);
      if (!/^(https?:|\/|#|mailto:)/i.test(url)) return label;
      return `<a href="${href}" target="_blank" rel="noopener noreferrer">${label}</a>`;
    });

    s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    s = s.replace(/(^|[^*\w])\*([^*\n]+)\*/g, "$1<em>$2</em>");

    return s.replace(/\u0000(\d+)\u0000/g, (_, i) => `<code>${codes[Number(i)]}</code>`);
  }

  const mdSplitRow = (line) =>
    line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());

  const mdIsDelimiter = (line) =>
    line.includes("-") && /^\s*\|?[\s:|-]+\|[\s:|-]*$/.test(line);

  /** 列表项匹配：返回缩进宽度 / 是否有序 / 正文。 */
  function mdListItem(line) {
    const m = line.match(/^(\s*)([-*+]|\d+[.)])\s+(.*)$/);
    if (!m) return null;
    return {
      indent: m[1].replace(/\t/g, "    ").length,
      ordered: /\d/.test(m[2]),
      text: m[3],
    };
  }

  /** 递归构建列表，支持缩进嵌套。返回 [html, 下一行下标]。 */
  function mdBuildList(lines, start) {
    const base = mdListItem(lines[start]).indent;
    const ordered = mdListItem(lines[start]).ordered;
    const tag = ordered ? "ol" : "ul";

    let html = `<${tag}>`;
    let i = start;

    while (i < lines.length) {
      const item = mdListItem(lines[i]);

      if (!item) {
        // 列表项里的续行：缩进比当前层深，且不是新的项。
        if (lines[i].trim() && /^\s/.test(lines[i]) && html.endsWith("</li>")) {
          const extra = mdInline(lines[i].trim());
          html = html.replace(/<\/li>$/, ` ${extra}</li>`);
          i++;
          continue;
        }
        break;
      }

      if (item.indent < base) break;

      if (item.indent > base) {
        const [sub, next] = mdBuildList(lines, i);
        html = html.replace(/<\/li>$/, `${sub}</li>`);
        i = next;
        continue;
      }

      if (item.ordered !== ordered) break;

      html += `<li>${mdInline(item.text)}</li>`;
      i++;
    }

    return [html + `</${tag}>`, i];
  }

  function renderMarkdown(source) {
    const lines = String(source ?? "").replace(/\r\n?/g, "\n").split("\n");
    const out = [];
    let i = 0;

    while (i < lines.length) {
      const line = lines[i];

      // --- 围栏代码块 ---
      const fence = line.match(/^\s*(```|~~~)/);
      if (fence) {
        const marker = fence[1];
        const buf = [];
        i++;
        while (i < lines.length && !lines[i].trimStart().startsWith(marker)) {
          buf.push(lines[i]);
          i++;
        }
        i++; // 吃掉收尾围栏
        out.push(`<pre><code>${esc(buf.join("\n"))}</code></pre>`);
        continue;
      }

      if (!line.trim()) { i++; continue; }

      // --- 标题 ---
      const heading = line.match(/^(#{1,6})\s+(.*)$/);
      if (heading) {
        const level = heading[1].length;
        out.push(`<h${level}>${mdInline(heading[2].trim())}</h${level}>`);
        i++;
        continue;
      }

      // --- 分割线 ---
      if (/^\s*([-*_])\s*(\1\s*){2,}$/.test(line)) {
        out.push("<hr>");
        i++;
        continue;
      }

      // --- 表格：本行有 | 且下一行是分隔行 ---
      if (line.includes("|") && i + 1 < lines.length && mdIsDelimiter(lines[i + 1])) {
        const header = mdSplitRow(line);
        i += 2;

        const rows = [];
        while (i < lines.length && lines[i].includes("|") && lines[i].trim()) {
          rows.push(mdSplitRow(lines[i]));
          i++;
        }

        const head = header.map((c) => `<th>${mdInline(c)}</th>`).join("");
        const body = rows
          .map((cells) => {
            const tds = header
              .map((_, idx) => `<td>${mdInline(cells[idx] ?? "")}</td>`)
              .join("");
            return `<tr>${tds}</tr>`;
          })
          .join("");

        out.push(
          `<table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`
        );
        continue;
      }

      // --- 引用（连续行合并） ---
      if (/^\s*>/.test(line)) {
        const buf = [];
        while (i < lines.length && /^\s*>/.test(lines[i])) {
          buf.push(lines[i].replace(/^\s*>\s?/, ""));
          i++;
        }
        out.push(`<blockquote>${renderMarkdown(buf.join("\n"))}</blockquote>`);
        continue;
      }

      // --- 列表 ---
      if (mdListItem(line)) {
        const [html, next] = mdBuildList(lines, i);
        out.push(html);
        i = next;
        continue;
      }

      // --- 段落：吃到这里为止的连续普通行 ---
      const para = [];
      while (
        i < lines.length &&
        lines[i].trim() &&
        !/^(#{1,6}\s|\s*>|\s*(```|~~~))/.test(lines[i]) &&
        !mdListItem(lines[i]) &&
        !mdIsDelimiter(lines[i]) &&
        !/^\s*([-*_])\s*(\1\s*){2,}$/.test(lines[i])
      ) {
        para.push(lines[i]);
        i++;
      }
      if (para.length) out.push(`<p>${mdInline(para.join(" "))}</p>`);
      else i++; // 兜底，防止死循环
    }

    return out.join("\n");
  }

  /* ============================================================
   * API
   * ============================================================ */

  async function api(path, options) {
    let res;

    try {
      res = await fetch(API + path, options);
    } catch (e) {
      throw new Error("无法连接服务：" + e.message);
    }

    const body = await res.json().catch(() => ({}));

    if (!res.ok) {
      const detail = body.detail
        ? (typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail))
        : `${res.status} ${res.statusText}`;
      throw new Error(detail);
    }

    return body;
  }

  const post = (path) => api(path, { method: "POST" });

  /* ============================================================
   * 状态
   * ============================================================ */

  const state = {
    runId: null,
    run: null,          // 最近一次 AnalysisResponse
    doc: null,          // 结构化报告 document
    markdown: null,     // 当前展示的 markdown 正文
    mainReport: null,   // 主报告缓存，供「返回主报告」使用
    reportPath: "",
    view: "dashboard",
    dim: null,          // 当前选中的维度
    evidenceFilter: "",
    inFlight: false,    // 人工操作请求在途，轮询必须让路
    scrolledFor: null,  // 只在状态首次出现时自动滚动一次
    replanOpen: false,  // 「修改问题」面板是否展开
    timer: null,
  };

  /* 每个状态：文案、色调、需要人工做什么。 */
  const STATUS = {
    CREATED:   { text: "已创建",     tone: "running" },
    PLANNING:  { text: "规划中",     tone: "running" },
    ANALYZING: { text: "执行分析中", tone: "running" },
    RETRYING:  { text: "重试中",     tone: "running" },
    pending:   { text: "排队中",     tone: "running" },

    WAITING_DESIGN: {
      text: "已暂停 · 等你确认",
      tone: "waiting",
      head: "需要你的确认：分析方案已生成",
      body: "工作流已暂停。批准后将串行执行 5 个 Agent 的分析" +
            "（读取仓库文件、抽取架构与技术栈），大仓库约 1-2 分钟。",
      actionLabel: "批准分析方案",
    },

    WAITING_HUMAN: {
      text: "已暂停 · 等你确认",
      tone: "waiting",
      head: "需要你的确认：分析已完成，等待撰写报告",
      body: "各 Agent 已跑完。批准后将生成结论摘要与最终报告。",
      actionLabel: "批准并生成报告",
    },

    PAUSED: {
      text: "已暂停",
      tone: "waiting",
      head: "已手动暂停",
      body: "恢复后会从当前节点继续。",
      actionLabel: "恢复",
      action: "resume",
    },

    FAILED: {
      text: "失败",
      tone: "failed",
      head: "分析失败",
      body: "可以重试；若反复失败，请查看服务端终端的 traceback。",
      actionLabel: "重试",
      action: "retry",
    },

    CANCELED: {
      text: "已放弃",
      tone: "cancelled",
      head: "本次分析已放弃",
      body: "数据保留：已生成的部分仍可在历史里查看。",
    },

    COMPLETED: { text: "已完成", tone: "done" },
  };

  const CONFIRM_STEP = { WAITING_DESIGN: 1, WAITING_HUMAN: 2 };
  const TOTAL_CONFIRMS = 2;

  /* 这些状态不会再自行推进，轮询到它们就停下。
     只会因用户操作而改变，而操作都由本页发起。 */
  const RESTING_STATUSES = [
    "COMPLETED",
    "FAILED",
    "CANCELED",
    "WAITING_DESIGN",
    "WAITING_HUMAN",
    "PAUSED",
  ];

  const BASE_TITLE = "AIPI · GitHub 项目智能分析";
  const TITLE = {
    waiting: "⚠ 需要你确认",
    running: "⏳ 分析中",
    done: "✅ 报告已生成",
    failed: "❌ 分析失败",
  };

  const statusMeta = (s) => STATUS[s] || { text: s || "未知", tone: "" };

  /* 维度元信息。后端 key → 展示名。 */
  const DIMENSIONS = [
    { key: "agents",   label: "Agent 架构" },
    { key: "workflow", label: "Workflow" },
    { key: "skills",   label: "Skill" },
    { key: "tools",    label: "Tool" },
    { key: "rag",      label: "RAG" },
    { key: "memory",   label: "Memory" },
    { key: "extension", label: "扩展点" },
  ];

  /* 待执行 Agent 的中文名（设计闸门展示方案时用）。 */
  const AGENT_LABELS = {
    repository_analysis_agent: "仓库分析 · 拉取元数据与目录结构",
    architecture_analysis_agent: "架构分析 · 解析模块与调用关系",
    technology_analysis_agent: "技术栈分析 · 识别框架与依赖",
    evidence_analysis_agent: "证据提取 · 生成可追溯的源码证据",
    critic_agent: "批判审查 · 交叉校验结论与证据",
  };

  /* ============================================================
   * 主题
   * ============================================================ */

  $("themeToggle").onclick = () => {
    const next =
      document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem("aipi-theme", next); } catch (e) { /* 忽略 */ }
  };

  /* ============================================================
   * 健康检查
   * ============================================================ */

  async function checkHealth() {
    const box = $("health");
    const text = $("healthText");
    try {
      const res = await fetch("/health");
      if (!res.ok) throw new Error(String(res.status));
      const body = await res.json();
      box.classList.add("ok");
      box.classList.remove("bad");
      text.textContent = body.environment || "ok";
    } catch (e) {
      box.classList.add("bad");
      box.classList.remove("ok");
      text.textContent = "服务不可用";
    }
  }

  /* ============================================================
   * 状态面板
   * ============================================================ */

  function renderStatus(run) {
    const meta = statusMeta(run.status);

    $("statusPanel").classList.remove("hidden");
    $("emptyState").classList.add("hidden");

    const pill = $("status");
    pill.textContent = meta.text;
    pill.className = "pill " + (meta.tone || "");

    $("node").textContent = run.current_node || "";
    $("runId").textContent = "run_id " + (run.run_id || "—");

    const waiting = meta.tone === "waiting";
    const running = meta.tone === "running";
    const progress = Number(run.progress) || 0;

    $("progressText").textContent =
      progress + "%" + (waiting ? " · 已暂停" : "");

    $("progress").style.width = progress + "%";
    $("bar").className = "progress " + (waiting ? "waiting" : running ? "running" : "");

    document.title = meta.tone && TITLE[meta.tone]
      ? TITLE[meta.tone] + " · " + BASE_TITLE
      : BASE_TITLE;

    renderCallout(meta, run);
    renderStatusControls(meta, run);
  }

  function renderCallout(meta, run) {
    const callout = $("callout");
    const actions = $("actions");

    actions.innerHTML = "";

    // 设计闸门单独处理：要展示分析方案，动作也不止一个
    if (run.status === "WAITING_DESIGN") {
      renderDesignGate(run, callout, actions);
      return;
    }

    // 其它状态不涉及方案，把方案区收起来
    $("planBox").classList.add("hidden");
    $("planBox").innerHTML = "";
    $("replanBox").classList.add("hidden");

    if (!meta.actionLabel) {
      callout.classList.add("hidden");
      callout.classList.remove("pulse");
      return;
    }

    const step = CONFIRM_STEP[run.status];
    $("calloutHead").innerHTML =
      (step
        ? `<span class="step-tag">第 ${step} 步 / 共 ${TOTAL_CONFIRMS} 步</span>`
        : "") + esc(meta.head);

    $("calloutBody").textContent = meta.body;

    const btn = document.createElement("button");
    btn.className = "btn";
    btn.textContent = meta.actionLabel;
    btn.onclick = () => act(meta.action || "approve");
    actions.appendChild(btn);

    callout.classList.remove("hidden");
    callout.classList.add("pulse");

    // 只在状态第一次出现时滚过去，否则轮询会把页面反复拽走。
    const key = run.status + ":" + run.run_id;
    if (state.scrolledFor !== key) {
      state.scrolledFor = key;
      callout.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }

  /* ============================================================
   * 设计闸门
   * ------------------------------------------------------------
   * 旧版本在这里只给了一个「批准分析方案」按钮，
   * 而接口根本不返回方案内容 ——
   * 用户被要求批准一份自己看不到的东西，等于盲签。
   * 现在展示方案，并给出批准 / 暂停 / 放弃 / 修改问题四个出口。
   * ============================================================ */

  function renderDesignGate(run, callout, actions) {
    const meta = statusMeta(run.status);

    $("calloutHead").innerHTML =
      `<span class="step-tag">第 1 步 / 共 ${TOTAL_CONFIRMS} 步</span>` +
      esc(meta.head);

    $("calloutBody").textContent = meta.body;

    // 方案
    const planBox = $("planBox");
    planBox.innerHTML = renderPlan(run.research_plan);
    planBox.classList.remove("hidden");

    const add = (label, cls, onClick) => {
      const btn = document.createElement("button");
      btn.className = cls;
      btn.textContent = label;
      btn.onclick = onClick;
      actions.appendChild(btn);
    };

    add("批准分析方案", "btn", () => act("approve"));
    add("暂停", "btn btn-secondary", () => act("pause"));
    add("修改问题", "btn btn-secondary", () => {
      $("replanQuestion").value = run.question || "";
      $("replanBox").classList.remove("hidden");
      $("replanQuestion").focus();
      state.replanOpen = true;
    });
    add("放弃本次分析", "btn btn-danger-ghost", cancelRun);

    // 轮询重绘会把面板收起来，这里按用户上次的选择恢复
    $("replanBox").classList.toggle("hidden", !state.replanOpen);

    callout.classList.remove("hidden");
    callout.classList.add("pulse");

    const key = run.status + ":" + run.run_id;
    if (state.scrolledFor !== key) {
      state.scrolledFor = key;
      callout.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }

  /** 把 research_plan 渲染成可读的方案。 */
  function renderPlan(plan) {
    if (!plan || typeof plan !== "object") {
      return (
        `<div style="padding:var(--s-4)">` +
        fallback("服务端未返回分析方案，可以直接批准继续。") +
        `</div>`
      );
    }

    const rows = [];

    const row = (label, html) => {
      rows.push(
        `<div class="plan-row">
           <div class="plan-label">${esc(label)}</div>
           <div class="plan-value">${html}</div>
         </div>`
      );
    };

    row(
      "分析问题",
      esc(plan.question || "（未指定，将做全量等深分析）")
    );

    const focus = plan.focus || {};
    const dims = focus.dimensions || [];
    const dimTitles = {};
    DIMENSIONS.forEach((d) => (dimTitles[d.key] = d.label));

    row(
      "分析重点",
      dims.length
        ? `<div class="chips">${dims
            .map(
              (d) =>
                `<span class="chip accent">${esc(dimTitles[d] || d)}</span>`
            )
            .join("")}</div>`
        : `<span class="muted">未点名模块，六个维度等深分析</span>`
    );

    const tasks = plan.tasks || [];

    row(
      "待执行",
      tasks.length
        ? `<ol class="plan-steps">${tasks
            .map(
              (t, i) =>
                `<li><span class="idx">${i + 1}</span>` +
                `<span>${esc(AGENT_LABELS[t] || t)}</span></li>`
            )
            .join("")}</ol>`
        : `<span class="muted">—</span>`
    );

    if (plan.evidence_required) {
      row("证据要求", "每条结论须附源码出处（文件 + 行号）");
    }

    return rows.join("");
  }

  /** 运行中给一个「暂停」入口；其余状态靠 callout 的按钮。 */
  function renderStatusControls(meta, run) {
    const box = $("statusControls");
    box.innerHTML = "";

    const controllable = ["ANALYZING", "PLANNING", "CREATED", "RETRYING", "pending"];
    if (!controllable.includes(run.status)) return;

    const btn = document.createElement("button");
    btn.className = "btn btn-ghost btn-sm";
    btn.innerHTML = icon("pause") + " 暂停";
    btn.onclick = () => act("pause");
    box.appendChild(btn);
  }

  function showError(message) {
    $("error").textContent = message || "";
  }

  /* ============================================================
   * 轮询
   * ============================================================ */

  function stopPolling() {
    clearInterval(state.timer);
    state.timer = null;
  }

  function poll() {
    stopPolling();

    state.timer = setInterval(async () => {
      /*
       * 人工操作在途时绝不刷新。
       *
       * approve 会阻塞几十秒（要跑 5 个 Agent），
       * 而 run.status 直到请求结束才更新。
       * 期间轮询读到的仍是旧的 WAITING_*，
       * 会把「执行中」覆盖回「等你确认」，
       * 并把批准按钮重新渲染出来 ——
       * 用户看到「明明点了批准，页面还催我批准」，
       * 还能再点一次触发并发执行。
       */
      if (state.inFlight) return;

      try {
        const run = await api(`/analysis/${state.runId}`);
        state.run = run;
        renderStatus(run);

        // 停顿态停止轮询。
        //
        // 这些状态只会因为用户操作而改变，而操作都由本页发起并即时处理，
        // 继续每 2 秒轮询没有收益 ——
        // 反而会把 callout 反复重绘，用户正在里面读分析方案、
        // 或往「修改问题」框里打字时，面板会被一次次重建。
        if (RESTING_STATUSES.includes(run.status)) {
          stopPolling();

          if (run.status === "COMPLETED") {
            await loadReport(run.run_id);
          }

          loadHistory();
        }
      } catch (e) {
        stopPolling();
        showError("查询状态失败：" + e.message);
      }
    }, POLL_MS);
  }

  /* ============================================================
   * 人工动作
   * ============================================================ */

  async function act(name) {
    if (state.inFlight) return;   // 防重复提交
    state.inFlight = true;

    showError("");

    // 立刻切到「执行中」，否则用户以为点击没生效。
    $("callout").classList.add("hidden");
    $("callout").classList.remove("pulse");
    $("statusControls").innerHTML = "";
    $("status").className = "pill running";
    $("status").textContent = "执行中…";
    $("bar").className = "progress running";
    $("progressText").textContent = "正在跑，大仓库约 1-2 分钟";
    document.title = TITLE.running + " · " + BASE_TITLE;
    $("callout").scrollIntoView({ behavior: "smooth", block: "nearest" });

    try {
      const run = await post(`/analysis/${state.runId}/${name}`);
      state.inFlight = false;
      state.run = run;
      renderStatus(run);

      // 与 poll() 同一套判断：操作完落到停顿态就不必再轮询。
      if (RESTING_STATUSES.includes(run.status)) {

        if (run.status === "COMPLETED") {
          await loadReport(run.run_id);
        }

        loadHistory();

      } else {
        poll();
      }
    } catch (e) {
      state.inFlight = false;
      await handleActionFailure(name, e);
    }
  }

  /*
   * 人工操作失败后的处理。
   *
   * 关键事实：工作流逐节点落盘，每个节点跑完就存一次 checkpoint。
   * 所以请求返回 500 时，前面已完成的工作早就提交了 ——
   * 「请求失败」不等于「任务失败」。
   *
   * 真实事故：checkpoint 超过 asyncmy 的 256KB 单字段上限后，
   * 收尾阶段某次读操作崩了，请求返回 500，但任务其实已经 COMPLETED。
   * 因此这里必须立刻回读一次真实状态。
   */
  async function handleActionFailure(name, error) {
    let run;

    try {
      run = await api(`/analysis/${state.runId}`);
    } catch (e) {
      showError(
        `${name} 请求失败：${error.message}\n` +
        `重新查询状态也失败：${e.message}`
      );
      return;
    }

    state.run = run;
    renderStatus(run);

    if (run.status === "COMPLETED") {
      // 任务其实已经完成，用户要的结果拿到了，
      // 没必要再拿一个 500 去吓他。
      showError("");
      await loadReport(run.run_id);
      return;
    }

    showError(
      `${name} 请求失败：${error.message}\n\n` +
      `注意：这不代表分析失败。工作流逐节点落盘，` +
      `请求失败时已完成的部分仍然有效。\n` +
      `当前真实状态：${run.status}（${run.progress}%）\n` +
      `若状态是等待确认，可直接重新点击上面的按钮。\n` +
      `服务端终端里有完整 traceback（找 "unexpected error" 那行）。`
    );

    if (!["FAILED", "WAITING_DESIGN", "WAITING_HUMAN", "PAUSED"].includes(run.status)) {
      poll();
    }
  }

  /* ============================================================
   * 放弃 / 重新规划
   * ============================================================ */

  async function cancelRun() {
    if (state.inFlight || !state.runId) return;

    if (!confirm("确定放弃本次分析？\n\n已经产生的数据会保留，但不会再继续执行。")) {
      return;
    }

    state.inFlight = true;
    stopPolling();

    try {
      const run = await post(`/analysis/${state.runId}/cancel`);
      state.run = run;
      state.replanOpen = false;
      renderStatus(run);
      loadHistory();
    } catch (e) {
      showError("放弃失败：" + e.message);
    } finally {
      state.inFlight = false;
    }
  }

  async function replanRun() {
    if (state.inFlight || !state.runId) return;

    const question = $("replanQuestion").value.trim();

    if (!question) {
      toast("请填写新的分析问题");
      $("replanQuestion").focus();
      return;
    }

    state.inFlight = true;
    stopPolling();

    // 重新规划要重跑 Planner（含一次 LLM 调用），会有几秒无响应，
    // 先把按钮禁用并提示，免得用户以为没点上而重复点击。
    const submit = $("replanSubmit");
    submit.disabled = true;
    submit.textContent = "重新规划中…";

    try {
      const run = await api(`/analysis/${state.runId}/replan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      state.run = run;
      state.replanOpen = false;
      renderStatus(run);
      loadHistory();
      toast("已按新问题重新规划");
    } catch (e) {
      showError("重新规划失败：" + e.message);
    } finally {
      submit.disabled = false;
      submit.textContent = "用新问题重新规划";
      state.inFlight = false;
    }
  }

  $("replanSubmit").onclick = replanRun;
  $("replanCancel").onclick = () => {
    state.replanOpen = false;
    $("replanBox").classList.add("hidden");
  };

  /* ============================================================
   * 启动分析
   * ============================================================ */

  $("startForm").onsubmit = async (event) => {
    event.preventDefault();

    const repoUrl = $("repo").value.trim();
    const question = $("question").value.trim();

    if (!repoUrl) {
      toast("请填写仓库地址");
      $("repo").focus();
      return;
    }

    stopPolling();
    showError("");
    resetReport();

    const btn = $("start");
    btn.disabled = true;

    $("emptyState").classList.add("hidden");
    $("statusPanel").classList.remove("hidden");
    $("status").className = "pill running";
    $("status").textContent = "启动中…";
    $("bar").className = "progress running";
    $("callout").classList.add("hidden");
    document.title = TITLE.running + " · " + BASE_TITLE;
    state.scrolledFor = null;

    try {
      const run = await api("/analysis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          repo_url: repoUrl,
          question: question || null,
          // 按次开关。true/false 都显式传，让服务端不必猜。
          enable_rag: $("ragToggle").checked,
        }),
      });

      state.runId = run.run_id;
      state.run = run;
      state.mainReport = null;
      setHash(run.run_id);

      renderStatus(run);
      poll();
      loadHistory();
    } catch (e) {
      showError("启动失败：" + e.message);
      $("status").className = "pill failed";
      $("status").textContent = "启动失败";
    } finally {
      btn.disabled = false;
    }
  };

  /* ============================================================
   * 报告加载
   * ============================================================ */

  /** 两种接口的嵌套层级不同，这里统一取 content 与 path。 */
  function extractReport(data) {
    const outer = data.report || {};
    if (typeof outer.content === "string") {
      return { content: outer.content, path: (outer.report || {}).path || "" };
    }
    return { content: data.content || "", path: outer.path || "" };
  }

  function resetReport() {
    state.doc = null;
    state.markdown = null;
    state.mainReport = null;
    state.dim = null;
    state.evidenceFilter = "";
    state.replanOpen = false;

    $("reportArea").classList.add("hidden");
    $("viewDashboard").innerHTML = "";

    // 只清 JSON 树本身，不能清 #viewJson ——
    // 工具栏（展开/折叠按钮）和 #jsonTree 都在它里面，
    // 清掉容器会把这两个节点连同事件绑定一起丢掉。
    $("jsonTree").innerHTML = "";
    $("report").innerHTML = "";
    $("viewHint").classList.add("hidden");
    $("reportTitle").textContent = "分析报告";
    $("heroMeta").innerHTML = "";
    $("repoLink").textContent = "";
    $("repoLink").removeAttribute("href");
    $("backToMain").classList.add("hidden");
    $("download").classList.remove("hidden");
    $("downloadJson").classList.remove("hidden");
  }

  async function loadReport(forRunId) {
    const target = forRunId || state.runId;
    if (!target) return;

    try {
      // 结构化报告与 markdown 并行取，看板是主视图。
      const [mdData, jsonData] = await Promise.all([
        api(`/analysis/${target}/report`).catch(() => null),
        api(`/analysis/${target}/report/json`).catch(() => null),
      ]);

      const doc = jsonData && jsonData.document ? jsonData.document : null;
      state.doc = doc;

      let content = "";
      let path = "";

      if (mdData) {
        const parsed = extractReport(mdData);
        content = parsed.content;
        path = parsed.path;
      }

      if (!content && !doc) {
        showError("报告为空。");
        return;
      }

      state.markdown = content;
      state.reportPath = path;
      state.mainReport = { run_id: target, content, path };

      $("reportArea").classList.remove("hidden");
      $("reportTitle").textContent = "分析报告";
      $("backToMain").classList.add("hidden");
      $("download").classList.remove("hidden");
      $("downloadJson").classList.remove("hidden");

      renderHero(doc, path);
      renderMarkdownView(content);
      renderDashboard(doc);
      renderJsonTree(doc);

      // 没有结构化数据时，看板没什么可展示的，直接落到原文。
      switchView(doc ? "dashboard" : "markdown");

      document.title = TITLE.done + " · " + BASE_TITLE;

      $("reportArea").scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (e) {
      showError("获取报告失败：" + e.message);
    }
  }

  function renderMarkdownView(content) {
    $("report").innerHTML = content
      ? renderMarkdown(content)
      : '<div class="fallback">' + icon("inbox") + "<span>该 run 没有 markdown 报告文件。</span></div>";
  }

  /* ============================================================
   * 报告头
   * ============================================================ */

  function renderHero(doc, path) {
    const project = (doc && doc.project) || {};
    const link = $("repoLink");

    const fullName =
      project.full_name ||
      (doc && doc.run_id) ||
      (state.run && state.run.repo_url) ||
      "";

    if (/^https?:/.test(fullName)) {
      link.textContent = fullName;
      link.href = fullName;
    } else if (project.url) {
      link.textContent = fullName || project.url;
      link.href = project.url;
    } else if (fullName) {
      link.textContent = fullName;
      link.removeAttribute("href");
    } else {
      link.textContent = "";
      link.removeAttribute("href");
    }

    const meta = [];
    const push = (ic, text) => {
      if (text === undefined || text === null || text === "") return;
      meta.push(`<span>${icon(ic)}${esc(text)}</span>`);
    };

    push("code", project.language);
    push("scale", project.license);
    push("clock", doc && doc.generated_at ? "生成于 " + formatDate(doc.generated_at) : "");

    const dir = (doc && doc.directory) || {};
    push("file", dir.total_files ? `仓库 ${dir.total_files} 个文件` : "");
    push("file", path ? baseName(path) : "");

    $("heroMeta").innerHTML = meta.join("");
  }

  /* ============================================================
   * 数据看板
   * ============================================================ */

  function renderDashboard(doc) {
    const box = $("viewDashboard");

    if (!doc) {
      box.innerHTML =
        '<div class="panel"><div class="fallback">' +
        icon("inbox") +
        "<span>该 run 未产出结构化报告（可能是旧版本跑出来的）。" +
        "切到「报告原文」仍可阅读完整内容。</span></div></div>";
      return;
    }

    const parts = [];

    parts.push(dashboardOverview(doc));
    parts.push(dashboardTechStack(doc));
    parts.push(dashboardDirectory(doc));
    parts.push(dashboardDimensions(doc));
    parts.push(dashboardEvidence(doc));
    parts.push(dashboardSynthesis(doc));

    box.innerHTML = parts.join("");
  }

  /* ---------- 概览 ---------- */

  function dashboardOverview(doc) {
    const p = doc.project || {};
    const s = doc.synthesis || {};

    if (!p.available) {
      return panel(
        icon("search") + " 项目概览",
        fallback(p.reason || "未获取到仓库信息。")
      );
    }

    const oneLine = (s.summary && s.summary.one_line) || p.description || "";

    const stats = [
      ["star", "Stars", compactNumber(p.stars), "收藏数"],
      ["fork", "Forks", compactNumber(p.forks), "派生数"],
      ["issue", "Issues", compactNumber(p.open_issues), "未关闭"],
      ["file", "文件数", compactNumber(doc.directory && doc.directory.total_files), "仓库规模"],
      ["scale", "License", p.license || "—", "开源协议"],
      ["code", "语言", p.language || "—", "主语言"],
    ];

    const statHtml = stats
      .map(
        ([ic, label, value, sub]) => `
        <div class="stat">
          <div class="stat-label">${icon(ic)}${esc(label)}</div>
          <div class="stat-value" title="${esc(value)}">${esc(value)}</div>
          <div class="stat-sub">${esc(sub)}</div>
        </div>`
      )
      .join("");

    const topics = (p.topics || []).length
      ? `<div class="chip-group" style="margin-top:var(--s-4)">
           <div class="chip-group-label">Topics</div>
           <div class="chips">${p.topics
             .map((t) => `<span class="chip accent">${esc(t)}</span>`)
             .join("")}</div>
         </div>`
      : "";

    const dates = `
      <div class="hero-meta" style="margin-top:var(--s-4)">
        <span>${icon("clock")}创建 ${esc(formatDate(p.created_at))}</span>
        <span>${icon("refresh")}最近推送 ${esc(formatDate(p.pushed_at))}</span>
        <span>${icon("branch")}默认分支 ${esc(p.default_branch || "—")}</span>
      </div>`;

    return panel(
      icon("search") + " 项目概览",
      (oneLine ? `<div class="lede">${esc(oneLine)}</div>` : "") +
        `<div class="stat-grid" style="margin-top:var(--s-4)">${statHtml}</div>` +
        topics +
        dates
    );
  }

  /* ---------- 技术栈 ---------- */

  function dashboardTechStack(doc) {
    const stack = doc.technology_stack || {};
    const groups = [
      ["llm", "LLM"],
      ["frameworks", "框架"],
      ["database", "数据库"],
      ["embedding", "Embedding"],
      ["deployment", "部署"],
    ];

    const used = groups.filter(([key]) => (stack[key] || []).length);
    const sourceFiles = stack.source_files || [];

    if (!used.length && !sourceFiles.length) {
      return panel(
        icon("layers") + " 技术栈",
        fallback("未从仓库中识别出明确的技术栈声明。")
      );
    }

    const html = used
      .map(([key, label]) => {
        const items = stack[key] || [];
        return `
          <div class="chip-group">
            <div class="chip-group-label">${esc(label)}</div>
            <div class="chips">
              ${items.map((v) => `<span class="chip">${esc(v)}</span>`).join("")}
            </div>
          </div>`;
      })
      .join("");

    const src = sourceFiles.length
      ? `<div class="chip-group" style="margin-top:var(--s-4)">
           <div class="chip-group-label">依据文件</div>
           <div class="chips">${sourceFiles
             .map((f) => `<span class="chip mono">${esc(f)}</span>`)
             .join("")}</div>
         </div>`
      : "";

    return panel(
      icon("layers") + " 技术栈",
      `<div style="display:grid;gap:var(--s-4);grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">${html}</div>${src}`
    );
  }

  /* ---------- 目录统计 ---------- */

  function dashboardDirectory(doc) {
    const d = doc.directory || {};

    if (!d.available) {
      return panel(
        icon("folder") + " 目录结构",
        fallback(d.reason || "未获取到仓库文件树。")
      );
    }

    // 扩展名分布条：按数量降序，最多 10 条。
    const exts = Object.entries(d.by_extension || {})
      .map(([name, count]) => [name, Number(count) || 0])
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10);

    const max = exts.length ? exts[0][1] : 1;

    const extHtml = exts
      .map(
        ([name, count]) => `
        <div class="ext-row">
          <span class="ext-name">${esc(name)}</span>
          <span class="ext-track">
            <span class="ext-fill" style="width:${Math.max(2, (count / max) * 100).toFixed(1)}%"></span>
          </span>
          <span class="ext-count">${esc(count)}</span>
        </div>`
      )
      .join("");

    const dirs = (d.top_level_dirs || [])
      .map(
        (item) => `
        <div class="detail-card">
          <div class="detail-top">
            <span class="detail-kind">${esc(item.name)}</span>
            <span class="detail-meta" style="margin:0">
              ${esc(item.file_count)} 个文件
            </span>
          </div>
        </div>`
      )
      .join("");

    const keyFiles = (d.key_files || []).length
      ? `<div class="chip-group" style="margin-top:var(--s-4)">
           <div class="chip-group-label">关键文件</div>
           <div class="chips">${d.key_files
             .map((f) => `<span class="chip mono">${esc(f)}</span>`)
             .join("")}</div>
         </div>`
      : "";

    const modules = (doc.modules || []).length
      ? `<div class="chip-group" style="margin-top:var(--s-4)">
           <div class="chip-group-label">本次采集源码（${doc.modules.length}）</div>
           <div class="chips">${doc.modules
             .slice(0, 40)
             .map(
               (m) =>
                 `<span class="chip mono" title="${esc(m.file_path)}${m.truncated ? " · 已截断" : ""}">${esc(
                   m.file_path
                 )}</span>`
             )
             .join("")}</div>
         </div>`
      : "";

    return panel(
      icon("folder") + " 目录结构",
      `<div class="stat-grid">
         <div class="stat">
           <div class="stat-label">${icon("file")}文件总数</div>
           <div class="stat-value">${esc(compactNumber(d.total_files))}</div>
           <div class="stat-sub">来源：${esc(d.source || "—")}</div>
         </div>
         <div class="stat">
           <div class="stat-label">${icon("folder")}顶层目录</div>
           <div class="stat-value">${esc((d.top_level_dirs || []).length)}</div>
           <div class="stat-sub">一级目录数</div>
         </div>
         <div class="stat">
           <div class="stat-label">${icon("code")}文件类型</div>
           <div class="stat-value">${esc(Object.keys(d.by_extension || {}).length)}</div>
           <div class="stat-sub">不同扩展名</div>
         </div>
       </div>` +
        (extHtml ? `<div class="ext-list">${extHtml}</div>` : "") +
        (dirs
          ? `<div class="details" open><summary>顶层目录分布</summary>
               <div class="detail-grid">${dirs}</div>
             </div>`
          : "") +
        keyFiles +
        modules
    );
  }

  /* ---------- 六维度 ---------- */

  function dashboardDimensions(doc) {
    const all = doc.dimensions || {};

    if (all._available === false) {
      return panel(
        icon("layers") + " 模块维度",
        fallback(all._reason || "未产出项目结构。")
      );
    }

    if (!Object.keys(all).length) {
      return panel(
        icon("layers") + " 模块维度",
        fallback("该 run 未产出模块维度分析。")
      );
    }

    // 首次进入默认选中第一个有内容的维度。
    if (!state.dim || !(state.dim in all)) {
      const first = DIMENSIONS.find((d) => all[d.key]) ||
        { key: Object.keys(all)[0] };
      state.dim = first.key;
    }

    const tabs = DIMENSIONS.filter((d) => all[d.key])
      .map((d) => {
        const entry = all[d.key];
        const count = (entry.details || []).length;
        return `
          <button class="dim-tab${state.dim === d.key ? " is-active" : ""}"
                  data-dim="${esc(d.key)}">
            ${esc(d.label)}
            ${count ? `<span class="dim-count">${count}</span>` : ""}
          </button>`;
      })
      .join("");

    const body = dimensionBody(state.dim, all[state.dim]);

    return panel(
      icon("layers") +
        " 模块维度 " +
        `<span class="count">${Object.keys(all).length} 个模块</span>`,
      `<div class="dim-tabs">${tabs}</div><div id="dimBody">${body}</div>`
    );
  }

  function dimensionBody(key, entry) {
    if (!entry) return fallback("没有这个维度的数据。");

    const declared = entry.declared;
    const items = entry.items || [];
    const codeEvidence = entry.code_evidence || [];
    const evidence = entry.evidence || [];
    const details = entry.details || [];
    const repo = githubBase();

    const head = `
      <div class="dim-head">
        <span class="chip ${declared ? "success" : "warn"}">
          ${declared ? "已在仓库中声明" : "未声明"}
        </span>
        ${entry.declared_by
          ? `<span class="dim-sub">依据：${esc(entry.declared_by)}</span>`
          : ""}
        <span class="dim-sub">实现明细 ${details.length} · 代码证据 ${codeEvidence.length}</span>
      </div>`;

    if (!declared && entry.reason) {
      return head + fallback(entry.reason);
    }

    // 概述条目
    const itemsHtml = items.length
      ? `<div class="chip-group">
           <div class="chip-group-label">识别到的条目</div>
           <div class="chips">${items
             .map((v) => `<span class="chip">${esc(v)}</span>`)
             .join("")}</div>
         </div>`
      : "";

    // 代码证据：直接给出签名行 + GitHub 行号链接
    const codeHtml = codeEvidence.length
      ? `<div class="chip-group" style="margin-top:var(--s-4)">
           <div class="chip-group-label">代码证据</div>
           <div class="evidence-lines">${codeEvidence
             .map((e) => evidenceLine(e, repo))
             .join("")}</div>
         </div>`
      : "";

    // 声明来源证据
    const declHtml = evidence.length
      ? `<div class="chip-group" style="margin-top:var(--s-4)">
           <div class="chip-group-label">声明出处</div>
           <div class="evidence-lines">${evidence
             .map((e) => evidenceLine(e, repo))
             .join("")}</div>
         </div>`
      : "";

    // 实现明细
    const detailHtml = details.length
      ? `<details class="details">
           <summary>展开实现明细（${details.length} 项）</summary>
           <div class="detail-grid">${details
             .map((d) => detailCard(d, repo))
             .join("")}</div>
         </details>`
      : "";

    if (!itemsHtml && !codeHtml && !declHtml && !detailHtml) {
      return head + fallback("该维度已声明，但没有抽取到实现细节。");
    }

    return head + itemsHtml + codeHtml + declHtml + detailHtml;
  }

  function evidenceLine(e, repo) {
    const line = e.line_start || e.line || "";
    const path = e.file_path || "";
    const text = e.text || e.content || "";
    const url = repo && path ? `${repo}/blob/HEAD/${path}#L${line}` : "";

    return `
      <div class="evidence-line">
        <span class="ln">${esc(path)}${line ? ":" + esc(line) : ""}</span>
        <span class="src">${esc(String(text).slice(0, 220))}</span>
        ${url ? `<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">↗</a>` : ""}
      </div>`;
  }

  function detailCard(d, repo) {
    const kind = String(d.kind || "item").toLowerCase();
    const url =
      repo && d.file_path
        ? `${repo}/blob/HEAD/${d.file_path}#L${d.line || 1}`
        : "";

    const methods = (d.methods || []).length
      ? subChips("方法", d.methods)
      : "";
    const calls = (d.calls || []).length ? subChips("调用", d.calls) : "";
    const literals = (d.literals || []).length
      ? subChips("关键常量", d.literals)
      : "";

    return `
      <div class="detail-card">
        <div class="detail-top">
          <span class="detail-kind ${esc(kind)}">${esc(d.kind || "—")}</span>
          <span class="detail-name">${esc(d.name || "—")}</span>
        </div>
        ${d.signature ? `<div class="detail-sig">${esc(d.signature)}</div>` : ""}
        <div class="detail-meta">
          <span>${esc(d.file_path || "")}${d.line ? ":" + esc(d.line) : ""}</span>
          ${url ? `<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">在 GitHub 查看 ↗</a>` : ""}
        </div>
        ${methods}${calls}${literals}
      </div>`;
  }

  function subChips(label, values) {
    return `
      <div class="detail-sub">
        <div class="detail-sub-label">${esc(label)}</div>
        <div class="chips">${values
          .slice(0, 24)
          .map((v) => `<span class="chip mono">${esc(v)}</span>`)
          .join("")}</div>
      </div>`;
  }

  /* 由仓库地址拼出 GitHub 文件链接前缀。 */
  function githubBase() {
    const doc = state.doc;
    const url = doc && doc.project && doc.project.url;
    if (url) return String(url).replace(/\/$/, "");

    const raw = (state.run && state.run.repo_url) || "";
    return /^https?:\/\//.test(raw) ? raw.replace(/\/$/, "") : "";
  }

  /* ---------- 证据清单 ---------- */

  function dashboardEvidence(doc) {
    const all = doc.evidence || [];
    const repo = githubBase();

    if (!all.length) {
      return panel(
        icon("shield") + " 证据清单",
        fallback("该 run 没有采集到证据条目。")
      );
    }

    const filter = state.evidenceFilter.trim().toLowerCase();
    const rows = filter
      ? all.filter((e) =>
          `${e.file_path || ""} ${e.content || ""} ${e.source_type || ""}`
            .toLowerCase()
            .includes(filter)
        )
      : all;

    const body = rows.length
      ? rows.map((e) => evidenceRow(e, repo)).join("")
      : `<tr><td colspan="5" style="text-align:center;padding:var(--s-6);color:var(--c-text-3)">
           没有匹配「${esc(state.evidenceFilter)}」的证据
         </td></tr>`;

    return panel(
      icon("shield") +
        " 证据清单 " +
        `<span class="count">${rows.length} / ${all.length} 条</span>`,
      `<div class="evidence-toolbar">
         <div class="search-box">
           ${icon("search")}
           <input id="evidenceSearch" type="text" placeholder="按文件路径或内容筛选…"
                  value="${esc(state.evidenceFilter)}">
         </div>
       </div>
       <div class="table-wrap evidence-scroll">
         <table class="data">
           <thead>
             <tr>
               <th style="width:34%">文件</th>
               <th style="width:12%">行号</th>
               <th style="width:12%">来源</th>
               <th style="width:14%">校验</th>
               <th></th>
             </tr>
           </thead>
           <tbody>${body}</tbody>
         </table>
       </div>`
    );
  }

  function evidenceRow(e, repo) {
    const path = e.file_path || "—";
    const start = e.line_start;
    const end = e.line_end;
    const range =
      start && end && end !== start ? `${start}-${end}` : start ? String(start) : "—";

    const url = repo && e.file_path
      ? `${repo}/blob/HEAD/${e.file_path}#L${start || 1}`
      : "";

    const status = e.verification_status;
    const verifyChip = status
      ? `<span class="chip success">${esc(status)}</span>`
      : `<span class="chip">未校验</span>`;

    const snippet = e.content
      ? `<tr class="evidence-detail hidden"><td colspan="5">
           <div class="evidence-snippet">${esc(String(e.content).slice(0, 4000))}</div>
         </td></tr>`
      : "";

    return `
      <tr class="evidence-row">
        <td class="file-cell">
          ${url ? `<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(path)}</a>` : esc(path)}
        </td>
        <td class="num">${esc(range)}</td>
        <td>${esc(e.source_type || "—")}</td>
        <td>${verifyChip}</td>
        <td style="text-align:right">
          ${e.content ? '<button class="btn btn-ghost btn-sm evidence-toggle">查看</button>' : ""}
        </td>
      </tr>
      ${snippet}`;
  }

  /* ---------- 综合结论 ---------- */

  const INSIGHT_SECTIONS = [
    ["core_design", "核心设计", "layers", "design"],
    ["technology_choices", "技术选型", "code", ""],
    ["highlights", "亮点", "zap", "highlight"],
    ["risks", "风险与局限", "alert", "risk"],
    ["use_cases", "适用场景", "book", "use"],
  ];

  function dashboardSynthesis(doc) {
    const s = doc.synthesis || {};

    if (!s.available) {
      return panel(
        icon("zap") + " 综合结论",
        fallback(s.reason || "未产出综合分析。")
      );
    }

    const summary = s.summary || {};

    const cards = INSIGHT_SECTIONS.map(([key, label, ic, cls]) => {
      const list = summary[key];
      if (!Array.isArray(list) || !list.length) return "";

      return `
        <div class="insight-card ${cls}">
          <div class="insight-head">${icon(ic)}${esc(label)}
            <span class="count" style="margin-left:auto">${list.length}</span>
          </div>
          <ul class="insight-list">
            ${list.map((t) => `<li>${esc(t)}</li>`).join("")}
          </ul>
        </div>`;
    }).join("");

    return panel(
      icon("zap") + " 综合结论",
      cards || fallback("综合分析已生成，但没有可展示的要点。")
    );
  }

  /* ---------- 小工具 ---------- */

  function panel(title, body) {
    return `<section class="panel">
      <h2 class="section-title">${title}</h2>
      ${body}
    </section>`;
  }

  function fallback(text) {
    return `<div class="fallback">${icon("alert")}<span>${esc(text)}</span></div>`;
  }

  /* ============================================================
   * JSON 树
   * ============================================================ */

  function renderJsonTree(doc) {
    const box = $("jsonTree");
    box.innerHTML = "";

    if (!doc) {
      box.innerHTML = `<div class="fallback">${icon("inbox")}<span>没有结构化报告。</span></div>`;
      return;
    }

    box.appendChild(jsonNode(null, doc, 0));
  }

  function jsonNode(key, value, depth) {
    const wrap = document.createElement("div");
    wrap.className = "jt-node";
    const row = document.createElement("div");
    row.className = "jt-row";

    if (key !== null) {
      const k = document.createElement("span");
      k.className = "jt-key";
      k.textContent = `"${key}"`;
      row.appendChild(k);
      row.appendChild(document.createTextNode(":"));
    }

    if (value === null) {
      row.insertAdjacentHTML("beforeend", `<span class="jt-null">null</span>`);
      wrap.appendChild(row);
      return wrap;
    }

    if (Array.isArray(value)) {
      const children = document.createElement("div");
      children.className = "jt-children" + (depth >= 1 ? " collapsed" : "");

      const toggle = document.createElement("button");
      toggle.className = "jt-toggle";
      toggle.innerHTML =
        `<span class="jt-count">[ ${value.length} 项 ]</span>`;
      toggle.onclick = () => children.classList.toggle("collapsed");
      row.appendChild(toggle);

      value.forEach((item, idx) => children.appendChild(jsonNode(idx, item, depth + 1)));

      wrap.appendChild(row);
      if (value.length) wrap.appendChild(children);
      return wrap;
    }

    if (typeof value === "object") {
      const keys = Object.keys(value);
      const children = document.createElement("div");
      children.className = "jt-children" + (depth >= 1 ? " collapsed" : "");

      const toggle = document.createElement("button");
      toggle.className = "jt-toggle";
      toggle.innerHTML = `<span class="jt-count">{ ${keys.length} 项 }</span>`;
      toggle.onclick = () => children.classList.toggle("collapsed");
      row.appendChild(toggle);

      keys.forEach((k) => children.appendChild(jsonNode(k, value[k], depth + 1)));

      wrap.appendChild(row);
      if (keys.length) wrap.appendChild(children);
      return wrap;
    }

    const cls =
      typeof value === "string" ? "jt-str"
      : typeof value === "number" ? "jt-num"
      : typeof value === "boolean" ? "jt-bool"
      : "jt-null";

    const text = typeof value === "string" ? `"${value}"` : String(value);
    const span = document.createElement("span");
    span.className = cls;
    span.textContent = text.length > 400 ? text.slice(0, 400) + "…" : text;
    row.appendChild(span);

    wrap.appendChild(row);
    return wrap;
  }

  $("jsonExpand").onclick = () => {
    document.querySelectorAll("#jsonTree .jt-children").forEach((el) =>
      el.classList.remove("collapsed")
    );
  };
  $("jsonCollapse").onclick = () => {
    document.querySelectorAll("#jsonTree .jt-children").forEach((el) =>
      el.classList.add("collapsed")
    );
  };

  /* ============================================================
   * 视图切换
   * ============================================================ */

  function switchView(view) {
    state.view = view;

    $("viewDashboard").classList.toggle("hidden", view !== "dashboard");
    $("viewMarkdown").classList.toggle("hidden", view !== "markdown");
    $("viewJson").classList.toggle("hidden", view !== "json");

    document.querySelectorAll("#tabs .tab").forEach((tab) => {
      tab.classList.toggle("is-active", tab.dataset.view === view);
    });
  }

  $("tabs").addEventListener("click", (event) => {
    const tab = event.target.closest(".tab");
    if (tab) switchView(tab.dataset.view);
  });

  function setHint(text, warn) {
    const el = $("viewHint");
    if (!text) {
      el.classList.add("hidden");
      el.innerHTML = "";
      return;
    }
    el.className = "view-hint" + (warn ? " warn" : "");
    el.innerHTML = icon(warn ? "alert" : "zap") + `<span>${esc(text)}</span>`;
  }

  /* ============================================================
   * 看板内的交互（事件委托）
   * ============================================================ */

  $("viewDashboard").addEventListener("click", (event) => {
    // 维度切换
    const dimTab = event.target.closest(".dim-tab");
    if (dimTab) {
      state.dim = dimTab.dataset.dim;
      document.querySelectorAll("#viewDashboard .dim-tab").forEach((el) =>
        el.classList.toggle("is-active", el === dimTab)
      );
      const body = $("dimBody");
      if (body) body.innerHTML = dimensionBody(state.dim, state.doc.dimensions[state.dim]);
      return;
    }

    // 证据展开
    const toggle = event.target.closest(".evidence-toggle");
    if (toggle) {
      const row = toggle.closest("tr");
      const detail = row.nextElementSibling;
      if (detail && detail.classList.contains("evidence-detail")) {
        detail.classList.toggle("hidden");
        toggle.textContent = detail.classList.contains("hidden") ? "查看" : "收起";
      }
    }
  });

  // 证据筛选：输入时只重绘证据区块，避免整页重建、输入框失焦。
  $("viewDashboard").addEventListener("input", (event) => {
    if (event.target.id !== "evidenceSearch") return;

    state.evidenceFilter = event.target.value;
    const section = event.target.closest("section.panel");
    if (!section || !state.doc) return;

    const fresh = document.createElement("div");
    fresh.innerHTML = dashboardEvidence(state.doc);
    section.replaceWith(fresh.firstElementChild);

    const input = $("evidenceSearch");
    if (input) {
      input.focus();
      input.setSelectionRange(input.value.length, input.value.length);
    }
  });

  /* ============================================================
   * 深挖 / 学习路线
   * ============================================================ */

  const dropdown = $("deepDiveMenu");
  dropdown.querySelector("button").onclick = (e) => {
    e.stopPropagation();
    dropdown.classList.toggle("open");
  };
  document.addEventListener("click", () => dropdown.classList.remove("open"));

  dropdown.querySelectorAll(".dropdown-menu button").forEach((btn) => {
    btn.onclick = () => {
      dropdown.classList.remove("open");
      deepDive(btn.dataset.module);
    };
  });

  async function deepDive(module) {
    if (!state.runId) return;

    setHint(`正在深挖 ${module}（会重新联网读取更多文件，约 30 秒）…`);
    dropdown.querySelector("button").disabled = true;

    try {
      const data = await post(
        `/analysis/${state.runId}/deep-dive?module=${encodeURIComponent(module)}`
      );

      const { content, path } = extractReport(data);

      setHint(
        `已深挖 ${module}：读取 ${(data.files_read || []).length} 个文件，` +
        `展开 ${data.details || 0} 项实现明细`
      );

      $("reportTitle").textContent = "深挖报告 · " + module;

      // 深挖结果只有 markdown，没有结构化文档，直接切到原文视图。
      if (state.mainReport) $("backToMain").classList.remove("hidden");
      $("download").classList.add("hidden");
      $("downloadJson").classList.add("hidden");

      state.markdown = content;
      state.reportPath = path;

      renderMarkdownView(content);
      switchView("markdown");

      $("reportArea").scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (e) {
      setHint("");
      showError("深挖失败：" + e.message);
    } finally {
      dropdown.querySelector("button").disabled = false;
    }
  }

  $("learningPath").onclick = async () => {
    if (!state.runId) return;

    const btn = $("learningPath");
    setHint("正在生成学习路线（约 10 秒）…");
    btn.disabled = true;

    try {
      const data = await post(`/analysis/${state.runId}/learning-path`);

      if (!data.available) {
        setHint("");
        showError("学习路线不可用：" + (data.reason || "未知原因"));
        return;
      }

      const path = (data.report || {}).path || "";

      setHint("学习路线已生成，独立文件，未修改主报告");
      $("reportTitle").textContent = "学习路线";

      if (state.mainReport) $("backToMain").classList.remove("hidden");
      $("download").classList.add("hidden");
      $("downloadJson").classList.add("hidden");

      state.markdown = data.content || "";
      state.reportPath = path;

      renderMarkdownView(state.markdown);
      switchView("markdown");

      $("reportArea").scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (e) {
      setHint("");
      showError("生成学习路线失败：" + e.message);
    } finally {
      btn.disabled = false;
    }
  };

  $("backToMain").onclick = () => {
    if (!state.mainReport) return;

    setHint("");
    $("reportTitle").textContent = "分析报告";
    $("backToMain").classList.add("hidden");
    $("download").classList.remove("hidden");
    $("downloadJson").classList.remove("hidden");

    state.markdown = state.mainReport.content;
    state.reportPath = state.mainReport.path;

    renderMarkdownView(state.markdown);
    switchView(state.doc ? "dashboard" : "markdown");
  };

  /* ============================================================
   * 下载 / 复制
   * ============================================================ */

  function downloadBlob(content, filename, mime) {
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }

  $("download").onclick = () => {
    const content = (state.mainReport && state.mainReport.content) || state.markdown;
    if (!content) return;
    const name = baseName(state.mainReport && state.mainReport.path) || "report.md";
    downloadBlob(content, name, "text/markdown;charset=utf-8");
  };

  $("downloadJson").onclick = async () => {
    if (!state.runId) return;
    try {
      const data = await api(`/analysis/${state.runId}/report/json`);
      if (!data.document) {
        showError("结构化报告为空。");
        return;
      }
      downloadBlob(
        JSON.stringify(data.document, null, 2),
        `${state.runId}_analysis.json`,
        "application/json;charset=utf-8"
      );
    } catch (e) {
      showError("获取结构化报告失败：" + e.message);
    }
  };

  $("copyPath").onclick = async () => {
    const text = state.reportPath;
    if (!text) {
      toast("没有可复制的路径");
      return;
    }

    try {
      await navigator.clipboard.writeText(text);
      toast("路径已复制");
    } catch (e) {
      // http 页面或旧浏览器下 clipboard 不可用，退回手动复制。
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand("copy"); toast("路径已复制"); }
      catch (err) { toast("复制失败，请手动复制"); }
      document.body.removeChild(ta);
    }
  };

  /* ============================================================
   * 历史记录
   * ============================================================ */

  async function loadHistory() {
    const box = $("history");

    try {
      const runs = await api("/analysis?limit=30");

      if (!runs.length) {
        box.innerHTML = '<div class="history-placeholder">还没有分析记录</div>';
        return;
      }

      box.innerHTML = runs
        .map((run) => {
          const meta = statusMeta(run.status);
          const name =
            String(run.repo_url || "").split("/").slice(-2).join("/").split("?")[0] ||
            run.run_id.slice(0, 8);

          return `
            <div class="hist-item${run.run_id === state.runId ? " active" : ""}"
                 data-run="${esc(run.run_id)}">
              <span class="hist-dot ${esc(meta.tone || "")}"></span>
              <div class="hist-body">
                <div class="hist-name" title="${esc(run.repo_url || "")}">${esc(name)}</div>
                <div class="hist-meta">${esc(meta.text)} · ${esc(run.progress || 0)}%</div>
              </div>
              <span class="hist-time">${esc(relativeTime(run.created_at))}</span>
            </div>`;
        })
        .join("");
    } catch (e) {
      box.innerHTML = '<div class="history-placeholder">历史记录加载失败</div>';
    }
  }

  /* 打开一条历史记录。只读不写：不 approve、不重跑。 */
  async function openRun(runId) {
    stopPolling();

    state.runId = runId;
    state.mainReport = null;
    state.scrolledFor = null;
    setHash(runId);

    showError("");
    resetReport();

    try {
      const run = await api(`/analysis/${runId}`);
      state.run = run;
      renderStatus(run);

      if (run.status === "COMPLETED") {
        // 已完成的 run 只取报告：再起轮询只会让 loadReport 白跑第二遍。
        await loadReport(runId);
      } else if (
        ["WAITING_DESIGN", "WAITING_HUMAN", "ANALYZING", "PAUSED", "PLANNING",
         "CREATED", "RETRYING", "pending"].includes(run.status)
      ) {
        poll();
      }
    } catch (e) {
      showError("打开记录失败：" + e.message);
    }

    loadHistory();
  }

  $("history").addEventListener("click", (event) => {
    const item = event.target.closest(".hist-item");
    if (item) openRun(item.dataset.run);
  });

  $("refreshHistory").onclick = loadHistory;

  /* ---------- RAG 开关 ---------- */

  /*
   * 选择存 localStorage：RAG 是一个「我这次想不想等」的决定，
   * 每次进来都要重设一遍会很烦。
   * 默认值由服务端配置决定，首次访问时不给前端预设。
   */
  try {
    const saved = localStorage.getItem("aipi-rag");

    if (saved !== null) {
      $("ragToggle").checked = saved === "1";
    }
  } catch (e) { /* 隐私模式忽略 */ }

  function syncRagWarning() {
    $("ragWarning").classList.toggle("hidden", !$("ragToggle").checked);
  }

  $("ragToggle").onchange = () => {
    try {
      localStorage.setItem("aipi-rag", $("ragToggle").checked ? "1" : "0");
    } catch (e) { /* 忽略 */ }
    syncRagWarning();
  };

  syncRagWarning();

  /* ============================================================
   * 深链 #/run/<id>
   * ------------------------------------------------------------
   * 刷新页面不该丢掉正在看的分析，
   * 一个 run 的地址也应该能直接发给别人。
   * 用 replaceState 而不是直接改 hash，
   * 免得切换时往「后退」历史里塞一堆条目。
   * ============================================================ */

  function runIdFromHash() {
    const m = location.hash.match(/^#\/run\/([A-Za-z0-9_-]+)$/);
    return m ? m[1] : null;
  }

  function setHash(runId) {
    const next = runId ? `#/run/${runId}` : location.pathname + location.search;
    if (location.hash !== next) {
      history.replaceState(null, "", next);
    }
  }

  window.addEventListener("hashchange", () => {
    const id = runIdFromHash();
    if (id && id !== state.runId) openRun(id);
  });

  /* ============================================================
   * 启动
   * ============================================================ */

  checkHealth();
  setInterval(checkHealth, 30000);

  const deepLink = runIdFromHash();
  if (deepLink) openRun(deepLink);
  else loadHistory();

})();
