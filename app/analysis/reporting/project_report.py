"""Versioned, evidence-backed content for the project understanding report.

Synthesis owns explanations. This contract owns sources, bounds, validation and
the chapters consumed by both the Markdown exporter and the reading interface.
Citation validation checks provenance, not the semantic truth of a claim.
"""

import json
import re

VERSION = 2
SECTIONS = (
    ("overview", "01 项目速览", "说明项目类型、解决的问题、目标用户、适用边界"),
    ("capabilities", "02 核心功能", "按用户任务解释功能，说明输入、处理、产出与前置条件"),
    ("architecture", "03 整体架构", "解释系统边界、层次职责、依赖方向和外部系统；有依据时描述协作关系"),
    ("modules", "04 核心模块与源码入口", "解释模块职责、真实源码入口、输入输出、调用方与依赖方"),
    ("runtime", "05 核心运行流程", "选择一条有依据的主链路，按执行顺序说明入口、处理、输出与异常分支"),
    ("technology", "06 技术栈与数据管理", "解释语言、框架、依赖、外部服务、存储和部署条件各自的用途及依据"),
    ("usage", "07 安装、配置与使用", "按环境要求、安装、配置、最小示例、预期结果组织，保留前置条件与工作目录"),
    ("development", "08 源码阅读与二次开发", "给出有文件依据的阅读顺序、扩展入口、构建与测试方式，建议明确标注为建议"),
    ("assessment", "09 设计评价与待确认事项", "解释有依据的设计特点与取舍、使用限制、已观察问题；不凭空打分或断言样本外能力缺失"),
)
ORIGINS = {
    "code": "源码观察", "documentation": "文档声明", "metadata": "仓库信息",
    "dependency": "依赖线索", "path": "路径线索", "suggestion": "分析建议", "excerpt": "采集片段",
}


def mapping(value):
    return value if isinstance(value, dict) else {}


def records(value):
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def clean(value, limit=800):
    return value.strip()[:limit] if isinstance(value, str) else ""


def readme_sections(content, budget=10000):
    """Preserve line numbers and sample practical sections beyond a long intro."""
    if not isinstance(content, str) or not content.strip():
        return []
    sections, lines, heading, start, fence = [], [], "项目介绍", 1, None
    for number, line in enumerate(content.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
        match = re.match(r"^#{1,4}\s+(.+)", line) if fence is None else None
        if match and lines:
            sections.append((start, heading, "\n".join(lines)))
            start, lines = number, []
        if match:
            heading = match.group(1)
        lines.append(line)
    if lines:
        sections.append((start, heading, "\n".join(lines)))
    practical = re.compile(
        r"install|quick|start|usage|example|config|require|architect|develop|"
        r"contribut|test|deploy|build|auth|feature|安装|使用|入门|配置|开发|架构|部署|测试", re.IGNORECASE,
    )
    ranked = sorted(enumerate(sections), key=lambda pair: (
        0 if pair[0] == 0 else 1 if practical.search(pair[1][1]) else 2, pair[0],
    ))
    selected = []
    for _, (start, title, body) in ranked[:12]:
        if budget <= 0:
            break
        excerpt = body[:min(1800, budget)]
        selected.append({
            "title": title, "file": "README.md", "line_start": start,
            "line_end": start + len(excerpt.splitlines()) - 1,
            "content": excerpt, "truncated": len(excerpt) < len(body),
        })
        budget -= len(excerpt)
    return sorted(selected, key=lambda item: item["line_start"])


def source_catalog(facts):
    """Bound the source index and assign stable IDs before asking the model."""
    sources, seen, remaining = [], set(), 48000

    def file_kind(path):
        path = clean(path, 400).lower()
        if path.endswith((".md", ".rst")):
            return "documentation"
        if path.endswith((".py", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".go", ".java", ".rs",
                          ".rb", ".php", ".cs", ".kt", ".swift", ".vue")):
            return "code"
        return "dependency"

    def add(kind, path, start, content, end=None, truncated=False):
        nonlocal remaining
        if not content or len(sources) >= 75 or remaining <= 0:
            return
        if not isinstance(content, str):
            content = json.dumps(content, ensure_ascii=False, default=str)
        limit = min(1800, remaining)
        shortened = len(content) > limit
        content = content[:limit]
        path = clean(path, 400)
        start = start if type(start) is int and start > 0 else None
        end = end if type(end) is int and start and end >= start else None
        if shortened and start:
            end = start + len(content.splitlines()) - 1
        identity = (kind, path, start, content)
        if identity in seen:
            return
        seen.add(identity)
        remaining -= len(content)
        sources.append({
            "id": f"E{len(sources) + 1:03d}", "kind": kind, "file": path,
            "line_start": start, "line_end": end, "content": content,
            "truncated": bool(truncated or shortened),
        })

    for key, kind in (("project_overview", "metadata"), ("technology_stack", "dependency"),
                      ("directory_structure", "path"), ("code_extraction", "scope")):
        value = mapping(facts.get(key))
        if value and value.get("available") is not False:
            # Config text has separate file/line entries; don't duplicate it in
            # an unlocated JSON source that could be mistaken for implementation.
            value = {name: item for name, item in value.items() if name != "configuration_evidence"}
            add(kind, "", None, value)
    for item in records(facts.get("readme_sections")):
        add("documentation", item.get("file"), item.get("line_start"), item.get("content"),
            item.get("line_end"), item.get("truncated"))
    for item in records(facts.get("source_files")):
        if item.get("error"):
            continue
        add(file_kind(item.get("file_path")), item.get("file_path"), item.get("start_line", 1), item.get("content"),
            truncated=item.get("truncated"))
    for item in records(facts.get("report_materials")):
        add(item.get("kind", "documentation"), item.get("file_path"), item.get("start_line", 1),
            item.get("content"), truncated=item.get("truncated"))
    for entry in mapping(facts.get("declared_structure")).values():
        if not isinstance(entry, dict):
            continue
        kind = {"path_only": "path", "dependency_only": "dependency"}.get(entry.get("code_scope"), "code")
        for item in records(entry.get("code_evidence"))[:5]:
            snippet = clean(item.get("text"), 1800)
            item_kind = "path" if snippet.startswith("path:") else "dependency" if snippet.startswith(("import ", "from ")) else kind
            add(item_kind, item.get("file"), item.get("line"), snippet)
        for item in records(entry.get("readme_evidence"))[:3]:
            add("documentation", "README.md", item.get("line"), item.get("text"))
        for item in records(entry.get("details"))[:2]:
            add("code", item.get("file"), item.get("line"), item)
    for item in records(facts.get("evidence")):
        path = clean(item.get("file_path"), 400)
        kind = "documentation" if path.lower().endswith((".md", ".rst")) else "excerpt"
        add(kind, path, item.get("line_start"), item.get("content"), item.get("line_end"))
    return sources


def normalize_report(raw, sources):
    """Check citations, source strength, repeated content, commands and modules."""
    raw = mapping(raw)
    sources = records(sources)
    source_map = {item["id"]: item for item in sources if isinstance(item.get("id"), str)}
    sections, notices, seen = {}, [], set()

    def refs(value):
        return list(dict.fromkeys(
            ref for ref in value if isinstance(ref, str) and ref in source_map
        ))[:4] if isinstance(value, list) else []

    def origin(value, ids):
        kinds = {source_map[ref].get("kind") for ref in ids}
        if value == "suggestion":
            return value
        if value in kinds and value in ORIGINS:
            return value
        return next((kind for kind in ("code", "documentation", "dependency", "metadata", "path", "excerpt")
                     if kind in kinds), "metadata")

    for key, label, instruction in SECTIONS:
        incoming = mapping(raw.get("sections")).get(key)
        accepted = []
        for item in records(incoming)[:5]:
            title, content = clean(item.get("title"), 100), clean(item.get("content"), 700)
            if not title or not content:
                continue
            ids = refs(item.get("evidence_ids"))
            if not ids:
                notices.append(f"{label}：有说明缺少有效证据引用，已省略。")
                continue
            identity = re.sub(r"\s+", "", content).casefold()
            if identity in seen:
                notices.append(f"{label}：重复说明已合并到首次出现的章节。")
                continue
            basis = origin(item.get("basis"), ids)
            if item.get("basis") == "code" and basis != "code":
                notices.append(f"{label}：有源码结论仅引用了文档或其他线索，已省略；实现仍待确认。")
                continue
            if key in ("runtime", "architecture") and not any(
                source_map[ref].get("kind") in ("code", "documentation") for ref in ids
            ):
                notices.append(f"{label}：只有目录、元数据或依赖线索，无法据此说明运行关系。")
                continue
            seen.add(identity)
            entry = {"title": title, "content": content, "basis": basis, "evidence_ids": ids}
            if key == "modules":
                known = {source_map[ref].get("file") for ref in ids}
                entry["entrypoint"] = clean(item.get("entrypoint"), 400)
                if entry["entrypoint"] not in known:
                    entry["entrypoint"] = ""
                    notices.append(f"{label}：有源码入口无法与引用文件对应，未展示该路径。")
                entry["io"] = clean(item.get("io"), 220)
                entry["relationships"] = clean(item.get("relationships"), 260)
            command = clean(item.get("command"), 1800)
            if command and key in ("usage", "development"):
                if any(command_is_quoted(command, source_map[ref].get("content", "")) for ref in ids):
                    entry["command"] = command
                else:
                    notices.append(f"{label}：命令未能与引用原文对应，已省略。")
            accepted.append(entry)
        sections[key] = accepted
        if not accepted:
            notices.append(f"{label}：数据不足，需要补充材料以{instruction}。")

    relations = []
    for item in records(raw.get("relations"))[:10]:
        ids = refs(item.get("evidence_ids"))
        ids = [ref for ref in ids if source_map[ref].get("kind") in ("code", "documentation")]
        source, target = clean(item.get("source"), 70), clean(item.get("target"), 70)
        if item.get("basis") == "code" and not any(source_map[ref].get("kind") == "code" for ref in ids):
            notices.append("组件关系：有源码关系缺少源码引用，已省略。")
            continue
        if source and target and ids:
            relations.append({"source": source, "target": target, "label": clean(item.get("label"), 80),
                              "basis": origin(item.get("basis"), ids), "evidence_ids": ids})
    unknowns = raw.get("unknowns")
    if isinstance(unknowns, list):
        notices.extend(clean(item, 300) for item in unknowns[:10] if clean(item, 300))
    return {"version": VERSION, "sections": sections, "sources": sources, "relations": relations,
            "notices": list(dict.fromkeys(notices)),
            "validation": {"citations_checked": True, "semantic_verification": "not_performed"}}


def command_is_quoted(command, content):
    """Require complete lines or an exact quoted value, not a command prefix."""
    if re.search(r"(?m)^[ \t]*" + re.escape(command) + r"[ \t]*$", content):
        return True
    return any(delimiter + command + delimiter in content for delimiter in ("`", '"', "'"))


def output_instruction():
    sections = {}
    for key, _, instruction in SECTIONS:
        entry = {"title": "简短主题", "content": instruction, "basis": "documentation",
                 "evidence_ids": ["E001"]}
        if key == "modules":
            entry.update(entrypoint="引用中的真实文件路径", io="输入与输出", relationships="调用方和依赖方")
        if key in ("usage", "development"):
            entry["command"] = "引用原文中的命令或示例代码；没有则为空"
        sections[key] = [entry]
    schema = {"summary": {"one_line": "一句话项目定位", "core_design": [], "technology_choices": [],
                          "highlights": [], "risks": [], "use_cases": []},
              "dimensions": {},
              "project_report": {"sections": sections,
                  "relations": [{"source": "组件名称", "target": "组件名称", "label": "关系",
                                 "basis": "code", "evidence_ids": ["E001"]}],
                  "unknowns": ["尚未确认的事项以及缺少的材料"]}}
    return (
        "按以下 JSON 结构输出：\n" + json.dumps(schema, ensure_ascii=False, indent=2)
        + "\nproject_report 为正文，每节最多 5 项，每项 content 建议 50–120 字；"
        "缺少依据的章节返回空数组，并写明 unknowns，不补凑条数。"
        "先识别项目类型（SDK/服务/CLI/框架/应用等），按该类型解释整体项目，再在对应章节深入用户关注点。"
        "无需给每个项目套用 Agent、Workflow、RAG 等维度。"
        "每项 evidence_ids 只能引用 facts.report_sources 中的 ID，引用必须直接支持该项说明。"
        "basis 可用 code/documentation/metadata/dependency/path/suggestion；"
        "目录、依赖导入、类名不证明完整能力或实际调用，源码片段也不代表整个仓库。"
        "只有文档明确描述或源码明确调用的关系才能填 relations，目录关系不能填。"
        "运行流程的步骤按执行顺序给出，不能把 import 顺序当调用顺序。"
        "建议标注 suggestion，问题与待验证风险分清；未发现不等于不存在。"
        "content 使用纯文本，不放标题、表格、HTML、代码块或自行生成的命令；"
        "命令和最小示例只放 command，逐字摘录引用中的原文，保留执行条件，禁止编造配置或凭据。"
        "modules.entrypoint 必须等于本项引用的真实文件路径。"
        "各章避免重复；summary 每个列表最多两条供历史摘要使用；dimensions 仅保留有依据的相关维度。"
        "返回前检查说明、来源标识、证据和流程是否一致；没有依据的结论改为空或待确认事项。"
    )


def inline(value):
    """Prevent source text from injecting Markdown structure or table columns."""
    value = clean(value, 3000)
    value = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"([`*\[\]\\])", r"\\\1", " ".join(value.splitlines())).replace("|", "&#124;")


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |",
                      "| " + " | ".join("---" for _ in headers) + " |"]
                     + ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows])


def citations(ids):
    return " ".join(f"[{ref}](#{ref.lower()})" for ref in ids)


def code_block(content, language="text"):
    longest = max((len(match.group()) for match in re.finditer(r"`+", content)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}{language}\n{content}\n{fence}"


def prepare_report_data(data):
    """Opt new exports into v2, including honest degradation without an LLM."""
    data = dict(mapping(data))
    synthesis = dict(mapping(data.get("synthesis")))
    if mapping(synthesis.get("project_report")).get("version") != VERSION:
        facts = {
            "project_overview": mapping(data.get("repository")),
            "technology_stack": mapping(data.get("technology_stack")),
            "directory_structure": mapping(data.get("directory_structure")),
            "code_extraction": mapping(mapping(data.get("project_structure")).get("code_extraction")),
            "readme_sections": readme_sections(data.get("readme")),
            "source_files": records(data.get("modules")),
            "report_materials": records(data.get("report_materials")) + records(
                mapping(data.get("technology_stack")).get("configuration_evidence")),
        }
        synthesis["project_report"] = normalize_report({}, source_catalog(facts))
    data["synthesis"] = synthesis
    data["report_format_version"] = VERSION
    return data


def build_chapters(data):
    """Canonical reader chapters; no model calls and no invented fallback claims."""
    report = mapping(mapping(data.get("synthesis")).get("project_report"))
    sections = mapping(report.get("sections"))
    repo = mapping(data.get("repository"))
    structure = mapping(data.get("project_structure"))
    extraction = mapping(structure.get("code_extraction"))
    inventory = mapping(extraction.get("source_inventory"))
    architecture = mapping(data.get("architecture") or data.get("architecture_analysis_agent"))
    directory = mapping(data.get("directory_structure") or architecture.get("directory_structure"))
    chapters = []
    for key, title, instruction in SECTIONS:
        entries = records(sections.get(key))
        parts = []
        if key == "overview":
            if data.get("question"):
                parts.append("**本次问题**：" + inline(data["question"]))
            if not entries and repo.get("description"):
                parts.append(inline(repo["description"]) + "（仓库描述）")
        if key == "modules" and entries:
            parts.append(table(["模块 / 职责", "源码入口", "输入与输出", "协作关系", "来源 / 证据"], [
                (f"**{inline(item.get('title'))}**：{inline(item.get('content'))}",
                 inline(item.get("entrypoint")) or "尚未确认", inline(item.get("io")) or "尚未确认",
                 inline(item.get("relationships")) or "尚未确认",
                 ORIGINS.get(item.get("basis"), "待确认") + " " + citations(item.get("evidence_ids", [])))
                for item in entries]))
        else:
            for number, item in enumerate(entries, 1):
                label = f"{number}. " if key == "runtime" else ""
                parts.append(f"### {label}{inline(item.get('title'))}\n\n"
                             f"{inline(item.get('content'))}\n\n"
                             f"*{ORIGINS.get(item.get('basis'), '待确认')}* · {citations(item.get('evidence_ids', []))}")
                if item.get("command"):
                    parts.append(code_block(item["command"]))
        if not entries:
            if key == "architecture" and report.get("relations"):
                parts.append("已采集部分组件关系，整体分层与设计说明尚未确认。")
            else:
                parts.append("数据不足：尚未形成有证据支持的说明，需要补充材料以" + instruction + "。")
        if key == "overview":
            license_value = repo.get("license")
            license_name = license_value.get("name") if isinstance(license_value, dict) else license_value
            values = [("仓库", repo.get("full_name") or repo.get("name")), ("主语言", repo.get("language")),
                      ("许可证", license_name), ("默认分支", repo.get("default_branch")),
                      ("Stars / Forks / Open Issues", " / ".join(str(repo.get(field, "—")) for field in
                       ("stargazers_count", "forks_count", "open_issues_count"))),
                      ("最近推送", repo.get("pushed_at")), ("元数据采集时间", data.get("repository_collected_at") or "未记录"),
                      ("仓库地址", repo.get("html_url"))]
            parts.append(table(["仓库信息", "值"], [(name, inline(str(value)) if value is not None else "尚未确认")
                                                       for name, value in values]))
        if key == "architecture":
            relations = records(report.get("relations"))
            if relations:
                parts.append("### 已采集的组件关系\n\n" + table(["上游", "关系", "下游", "来源 / 证据"], [
                    (inline(item["source"]), inline(item["label"]), inline(item["target"]),
                     ORIGINS.get(item["basis"], "待确认") + " " + citations(item["evidence_ids"]))
                    for item in relations]))
            if directory.get("available"):
                dirs = records(directory.get("top_level_dirs"))[:15]
                if dirs:
                    parts.append("### 目录分布\n\n目录分布只表示文件组织，不代表调用关系。\n\n" + table(
                        ["顶层目录", "文件数"], [(inline(item.get("name")), item.get("file_count", "—")) for item in dirs]))
        if key == "technology" and not entries:
            stack = mapping(data.get("technology_stack"))
            detected = [(label, ", ".join(str(item) for item in stack[name])) for name, label in
                        (("frameworks", "框架线索"), ("llm", "模型服务线索"), ("database", "数据库 / ORM 线索"),
                         ("embedding", "向量存储线索"), ("deployment", "部署线索"))
                        if isinstance(stack.get(name), list) and stack[name]]
            if detected:
                parts.append("以下为依赖扫描线索，用途与实际调用尚未确认。\n\n" + table(
                    ["类别", "检测结果"], [(label, inline(value)) for label, value in detected]))
        if key == "assessment":
            notices = report.get("notices") if isinstance(report.get("notices"), list) else []
            if not mapping(data.get("synthesis")).get("available"):
                notices = [mapping(data.get("synthesis")).get("reason") or "综合分析不可用，当前仅展示已采集事实。", *notices]
            if notices:
                parts.append("### 待确认与内容检查\n\n" + "\n".join("- " + inline(item) for item in notices))
        chapter = {"id": key, "title": title, "body": "\n\n".join(parts)}
        if key == "architecture":
            chapter["relations"] = records(report.get("relations"))
        chapters.append(chapter)

    scope = [("分析分支 / ref", data.get("analysis_ref") or data.get("branch") or "未记录"),
             ("提交 SHA", data.get("commit_sha") or "未取得；不能保证分析期间分支未变化"),
             ("目录文件总数", directory.get("total_files", "未记录")),
             ("源码清单来源", inventory.get("source", "未记录")),
             ("源码文件 / 选取 / 读取成功", " / ".join(str(inventory.get(key, "未记录")) for key in
              ("source_files", "selected_files", "read_successful_files"))),
             ("解析文件数", extraction.get("parsed_files", "未记录"))]
    if inventory.get("source") == "git_tree":
        scope.append(("文件选取比例（不代表语义覆盖率）", str(inventory.get("coverage_percent", "未记录")) + "%"))
    readme = data.get("readme")
    scope.append(("当前保留的 README 字符数", len(readme) if isinstance(readme, str) else "未记录"))
    parts = [table(["分析范围", "记录"], [(label, inline(str(value))) for label, value in scope]),
             "分析结论限于本次已读取的样本；README 按章节选取，源码按文件选取，片段的截断情况见证据标记。未发现某项能力不等于项目没有该能力。证据编号已核对来源，结论语义仍需结合原文复核。"]
    failures = [f"{item.get('file_path', '未知文件')}：{item.get('error')}" for item in records(data.get("modules")) if item.get("error")]
    failures.extend(f"{item.get('file_path', '未知文件')}：{item.get('error')}"
                    for item in records(data.get("report_materials")) if item.get("error"))
    failures.extend(f"{path}：{reason}" for path, reason in mapping(mapping(data.get("technology_stack")).get("read_failures")).items())
    if data.get("readme_error"):
        failures.append("README：" + str(data["readme_error"]))
    failures.extend(f"{item.get('file_path', '未知文件')}：{item.get('reason') or item.get('error') or '解析失败'}"
                    for item in records(extraction.get("unparsed")))
    if failures:
        parts.append("### 读取或解析失败\n\n" + "\n".join("- " + inline(item) for item in failures))
    used_ids = {ref for entries in sections.values() for item in records(entries) for ref in item.get("evidence_ids", [])}
    used_ids.update(ref for relation in records(report.get("relations")) for ref in relation.get("evidence_ids", []))
    for source in records(report.get("sources")):
        if used_ids and source.get("id") not in used_ids and source.get("kind") != "scope":
            continue
        location = source.get("file") or "采集记录"
        if source.get("line_start"):
            location += f":{source['line_start']}"
            if source.get("line_end") and source["line_end"] != source["line_start"]:
                location += f"–{source['line_end']}"
        kind = ORIGINS.get(source.get("kind"), {"scope": "采样记录", "excerpt": "采集片段"}.get(source.get("kind"), "采集记录"))
        parts.append(f"### {source['id']}\n\n{kind} · {inline(location)}"
                     + (" · 片段已截断" if source.get("truncated") else "")
                     + "\n\n" + code_block(source.get("content", "")))
    if not report.get("sources"):
        parts.append("尚未建立证据索引；当前内容不足以支持完整项目判断。")
    chapters.append({"id": "appendix", "title": "附录：证据与分析范围", "body": "\n\n".join(parts)})
    return chapters


def to_markdown(chapters):
    contents = "\n".join(f"- [{chapter['title']}](#{chapter['id']})" for chapter in chapters)
    return "## 阅读目录\n\n" + contents + "\n\n" + "\n\n".join(
        f"<a id=\"{chapter['id']}\"></a>\n\n## {chapter['title']}\n\n{chapter['body']}" for chapter in chapters)
