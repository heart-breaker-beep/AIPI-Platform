"""Reader reports preserve evidence provenance across synthesis and both exports."""

import json
from types import SimpleNamespace

import pytest

from app.analysis.reporting.project_report import (
    SECTIONS,
    build_chapters,
    normalize_report,
    prepare_report_data,
    readme_sections,
    source_catalog,
)
from app.analysis.reporting.report_document import ReportDocumentBuilder
from app.analysis.skills.architecture_analysis_skill import ArchitectureAnalysisSkill
from app.analysis.skills.report_generation_skill import ReportGenerationSkill
from app.analysis.skills.report_synthesis_skill import ReportSynthesisSkill
from app.analysis.skills.technology_analysis_skill import TechnologyAnalysisSkill
from app.integrations.report_export_tool import ReportExportTool


def sample_data():
    return {
        "repository": {"full_name": "example/client", "description": "Example HTTP client", "language": "Python"},
        "question": "解释项目架构与使用方式", "branch": "main",
        "readme": "# Example client\nA small HTTP client.\n## Installation\n```sh\npip install example-client\n```\n",
        "modules": [{"file_path": "src/client.py", "start_line": 12,
                     "content": "def request(url):\n    return transport.send(url)\n", "truncated": True}],
        "project_structure": {"available": True, "code_extraction": {"available": True, "parsed_files": 1,
            "source_inventory": {"source": "git_tree", "source_files": 100, "selected_files": 2,
                                 "read_successful_files": 1, "coverage_percent": 2}}},
    }


def reply_from_facts(facts):
    sources = facts["report_sources"]
    code = next(item["id"] for item in sources if item["file"] == "src/client.py")
    install = next(item["id"] for item in sources if "pip install" in item["content"])
    return {"summary": {"one_line": "示例客户端"}, "project_report": {"sections": {
        "overview": [{"title": "项目定位", "content": "文档介绍了一个 HTTP 客户端。", "basis": "documentation", "evidence_ids": [install]}],
        "modules": [{"title": "客户端", "content": "request 将请求交给 transport。", "basis": "code",
                     "entrypoint": "src/client.py", "io": "URL → 响应", "relationships": "调用 transport.send",
                     "evidence_ids": [code]}],
        "runtime": [{"title": "发送请求", "content": "传入 URL 后调用 transport.send，并返回其结果。", "basis": "code", "evidence_ids": [code]}],
        "usage": [{"title": "安装", "content": "文档提供安装命令。", "command": "pip install example-client", "basis": "documentation", "evidence_ids": [install]}],
    }, "relations": [{"source": "request", "target": "transport.send", "label": "调用", "basis": "code", "evidence_ids": [code]}],
       "unknowns": ["运行环境版本尚未取得。"]}}


class ReplyTool:
    async def execute(self, messages, **kwargs):
        prompt = messages[-1]["content"]
        facts = json.loads(prompt.split("<facts>\n", 1)[1].split("\n</facts>", 1)[0])
        return {"available": True, "content": json.dumps(reply_from_facts(facts), ensure_ascii=False)}


@pytest.mark.asyncio
async def test_synthesis_exports_share_content_and_citations(tmp_path):
    data = sample_data()
    data["synthesis"] = await ReportSynthesisSkill().execute(SimpleNamespace(tools={"llm_chat": ReplyTool()}), data)
    result = await ReportGenerationSkill().execute(
        SimpleNamespace(tools={"report_export": ReportExportTool(str(tmp_path))}),
        {**data, "format": "both", "filename": "reader.md"},
    )
    document = json.loads((tmp_path / "reader.json").read_text(encoding="utf-8"))
    markdown = (tmp_path / "reader.md").read_text(encoding="utf-8")
    assert document["schema_version"] == 1  # Additive reader format preserves existing JSON consumers.
    assert document["report_format_version"] == 2
    assert [chapter["id"] for chapter in document["chapters"]] == [key for key, _, _ in SECTIONS] + ["appendix"]
    for chapter in document["chapters"]:
        assert chapter["body"] in markdown
    assert "src/client.py:12" in markdown
    assert "pip install example-client" in markdown
    assert "2%" in markdown and "不代表语义覆盖率" in markdown
    assert "## 04 Agent 架构" not in markdown
    assert "POST /analysis" not in markdown
    assert result["json_report"]["available"] is True
    ids = {source["id"] for source in document["synthesis"]["project_report"]["sources"]}
    for items in document["synthesis"]["project_report"]["sections"].values():
        assert all(set(item["evidence_ids"]) <= ids for item in items)
    # Checkpoint reconstruction uses the same chapter bodies.
    assert ReportDocumentBuilder.build_document(data)["chapters"] == document["chapters"]


def test_rejects_untraceable_claims_commands_and_paths():
    sources = [
        {"id": "E001", "kind": "documentation", "file": "README.md", "content": "pip install demo"},
        {"id": "E002", "kind": "path", "file": "agents/core.py", "content": "path:agents/core.py"},
    ]
    report = normalize_report({"sections": {
        "capabilities": [{"title": "Unsupported", "content": "Invented feature", "evidence_ids": ["E999"]}],
        "architecture": [{"title": "Unsupported runtime", "content": "Runs agents", "basis": "code", "evidence_ids": ["E002"]}],
        "modules": [{"title": "Entry", "content": "Documentation entry", "entrypoint": "invented.py", "evidence_ids": ["E001"]}],
        "usage": [{"title": "Start", "content": "Unverified command", "command": "python server.py", "evidence_ids": ["E001"]}],
    }, "relations": [{"source": "A", "target": "B", "basis": "code", "evidence_ids": ["E002"]}]}, sources)
    assert report["sections"]["capabilities"] == []
    assert report["sections"]["architecture"] == []
    assert report["sections"]["modules"][0]["entrypoint"] == ""
    assert "command" not in report["sections"]["usage"][0]
    assert report["relations"] == []
    assert report["validation"]["semantic_verification"] == "not_performed"


def test_practical_readme_sections_keep_original_lines_and_ignore_fenced_headings():
    content = "# Demo\n" + "intro\n" * 3000 + "## Install\n```sh\n# not a heading\npip install demo\n```\n## Development\nRun make test.\n"
    sections = readme_sections(content)
    install = next(item for item in sections if item["title"] == "Install")
    assert install["line_start"] == 3002
    assert "# not a heading" in install["content"]
    assert "pip install demo" in install["content"]
    assert any(item["title"] == "Development" for item in sections)
    assert sum(len(item["content"]) for item in sections) <= 10000


def test_import_and_path_signals_do_not_become_implementation_sources():
    catalog = source_catalog({"declared_structure": {"tools": {"code_scope": "implementation",
        "code_evidence": [{"file": "tools.py", "line": 1, "text": "import tool_library"},
                          {"file": "tools.py", "text": "path:tools.py"}]}}})
    assert [item["kind"] for item in catalog] == ["dependency", "path"]


@pytest.mark.asyncio
async def test_llm_failure_still_exports_scope_without_fabricating_sections(tmp_path):
    data = sample_data()
    data["synthesis"] = await ReportSynthesisSkill().execute(SimpleNamespace(tools={}), data)
    assert data["synthesis"]["available"] is False
    doc = ReportDocumentBuilder.build_document(data)
    assert doc["report_format_version"] == 2
    assert all(not items for items in doc["synthesis"]["project_report"]["sections"].values())
    body = ReportGenerationSkill._build_report(data)
    assert "数据不足" in body and "源码文件 / 选取 / 读取成功" in body
    assert "Example HTTP client" in body


def test_old_checkpoints_keep_legacy_report_without_invented_reader_sections():
    doc = ReportDocumentBuilder.build_document(sample_data())
    assert doc["report_format_version"] == 1
    assert "chapters" not in doc
    assert "## 00 结论摘要" in ReportDocumentBuilder.to_markdown(sample_data())
    assert len(build_chapters(prepare_report_data(sample_data()))) == 10


def test_foundational_files_are_not_crowded_out_by_topic_sampling():
    paths = [f"src/agents/agent_{number}.py" for number in range(50)] + [
        "src/client.py", "src/_base_client.py", "src/main.py", "tests/main.py",
    ]
    selected = ArchitectureAnalysisSkill()._report_read_candidates(paths)
    assert {"src/client.py", "src/_base_client.py", "src/main.py"} <= set(selected)
    assert len(selected) == ArchitectureAnalysisSkill.MAX_MODULES
    assert "tests/main.py" not in selected


def test_repeated_explanations_are_kept_in_one_chapter():
    source = {"id": "E001", "kind": "documentation", "file": "README.md", "content": "docs"}
    item = {"title": "A | B", "content": "Documented behavior", "basis": "documentation", "evidence_ids": ["E001"]}
    report = normalize_report({"sections": {"overview": [item], "capabilities": [item]}}, [source])
    assert len(report["sections"]["overview"]) == 1
    assert report["sections"]["capabilities"] == []


@pytest.mark.asyncio
async def test_document_and_config_collection_reaches_synthesis(monkeypatch):
    files = {"src/client.py": "def request():\n    return 1\n",
             "CONTRIBUTING.md": "# Development\nRun make test.\n",
             "package.json": '{"scripts":{"test":"node --test"}}'}

    class Reader:
        async def execute(self, **kwargs):
            return files.get(kwargs["file_path"], "")

    skill = ArchitectureAnalysisSkill()

    async def tree(*args):
        return [{"path": name, "type": "blob"} for name in files]

    monkeypatch.setattr(skill, "_load_tree", tree)
    context = SimpleNamespace(tools={"file_reader": Reader()})
    data = {"owner": "example", "repo": "client", "branch": "dev"}
    architecture = await skill.execute(context, data)
    technology = await TechnologyAnalysisSkill().execute(context, data)
    facts = ReportSynthesisSkill()._build_facts({**data, **architecture, **technology})
    sources = facts["report_sources"]
    assert any(item["file"] == "CONTRIBUTING.md" and "make test" in item["content"] for item in sources)
    assert any(item["file"] == "package.json" and "node --test" in item["content"] for item in sources)
    assert architecture["analysis_ref"] == "dev"
    assert architecture["source_inventory"]["read_successful_files"] == 1


def test_module_table_preserves_literal_pipes_without_adding_columns():
    data = sample_data()
    facts = ReportSynthesisSkill()._build_facts(data)
    reply = reply_from_facts(facts)["project_report"]
    reply["sections"]["modules"][0]["content"] = "输入 A | B，返回响应。"
    data["synthesis"] = {"available": True, "project_report": normalize_report(reply, facts["report_sources"])}
    chapter = next(item for item in build_chapters(data) if item["id"] == "modules")
    row = chapter["body"].splitlines()[2]
    assert "&#124;" in row
    assert row.count("|") == 6


def test_command_prefix_is_not_accepted_as_a_complete_documented_command():
    source = {"id": "E001", "kind": "documentation", "file": "README.md",
              "content": "pip install demo[server]\n"}
    report = normalize_report({"sections": {"usage": [{"title": "安装", "content": "文档安装方法。",
        "command": "pip install demo", "evidence_ids": ["E001"]}]}}, [source])
    assert "command" not in report["sections"]["usage"][0]
