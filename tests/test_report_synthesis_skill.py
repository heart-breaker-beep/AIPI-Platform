"""
ReportSynthesisSkill / LLMChatTool / SynthesisNode 测试。

覆盖三条关键路径：

1. 正常路径：LLM 返回合法 JSON → 规整成 summary + dimensions
2. 降级路径：无 Key / 调用异常 / 非法 JSON → available=False 且不抛异常
3. 约束路径：prompt 中「只归纳不推测」的规则必须存在，
   且事实里缺失的维度必须以 available=False 呈现给 LLM

全程不发起任何真实网络请求：
LLM 通过 llm_chat 工具注入假实现。
"""

import json

import pytest

from app.skills.report_synthesis_skill import (
    ReportSynthesisSkill,
)
from app.tools.llm_chat_tool import LLMChatTool
from app.workflow.nodes.synthesis_node import (
    SynthesisNode,
)
from app.workflow.state import WorkflowState

VALID_REPLY = json.dumps(
    {
        "summary": {
            "one_line": "这是一个 LangGraph 发票审批 Agent。",
            "core_design": [
                "draft-only + human-in-the-loop",
                "单 Agent 状态机",
            ],
            "technology_choices": ["FastAPI + LangGraph"],
            "highlights": ["有审计轨迹"],
            "risks": ["RAG 维度数据不足"],
            "use_cases": ["参考其 human-in-the-loop 设计"],
        },
        "dimensions": {
            "agents": "单 Agent + 显式状态机。",
            "workflow": "LangGraph StateGraph。",
            "skills": "数据不足：README 未声明 skills。",
            "tools": "4 个校验工具。",
            "rag": "数据不足：README 未声明 rag。",
            "memory": "SQLite checkpoint 持久化。",
        },
    },
    ensure_ascii=False,
)


class FakeLLMTool:
    """假的 llm_chat 工具。"""

    def __init__(
        self,
        content=VALID_REPLY,
        available=True,
        reason=None,
    ):
        self.content = content
        self.available = available
        self.reason = reason
        self.calls = []

    async def execute(
        self,
        messages,
        **kwargs,
    ):
        self.calls.append(messages)

        if not self.available:
            return {
                "available": False,
                "reason": self.reason,
            }

        return {
            "available": True,
            "content": self.content,
        }


class FakeContext:

    def __init__(self, tool=None):
        self.tools = {}

        if tool is not None:
            self.tools["llm_chat"] = tool


def build_data():
    """一份接近真实结构的 state.data。"""

    return {
        "question": "分析这个项目",
        "repository": {
            "name": "enterprise-finance-agent",
            "full_name": "demo/enterprise-finance-agent",
            "description": "Enterprise finance workflow agent.",
            "language": "Python",
            "topics": ["langgraph"],
            "stargazers_count": 1,
            "forks_count": 1,
            "open_issues_count": 0,
            "license": {"name": "MIT License"},
            "size": 64,
            "created_at": "2026-07-22T02:17:59Z",
            "pushed_at": "2026-07-22T02:31:46Z",
        },
        "readme": "# Demo\n- supplier lookup\n",
        "technology_stack": {
            "llm": ["OpenAI"],
            "database": ["SQLAlchemy"],
            "frameworks": ["FastAPI", "LangGraph"],
            "embedding": [],
            "deployment": [],
        },
        "directory_structure": {
            "available": True,
            "total_files": 107,
            "by_extension": {".py": 88},
        },
        "project_structure": {
            "available": True,
            "basis": "readme+topics",
            "dimensions": {
                "agents": {
                    "declared": True,
                    "items": ["Agent may extract fields"],
                    "topics": [],
                    "evidence": [
                        {
                            "file_path": "README.md",
                            "line_start": 10,
                            "text": "- agent state model",
                        }
                    ],
                },
                "rag": {
                    "declared": False,
                    "reason": "README 中没有 rag 相关声明。",
                    "items": [],
                    "topics": [],
                    "evidence": [],
                },
            },
        },
        "modules": [
            {
                "file_path": "docker-compose.yml",
                "content": "services:\n  api:\n",
            }
        ],
        "evidence": [
            {
                "file_path": "README.md",
                "line_start": 1,
                "line_end": 30,
                "content": "x" * 400,
            }
        ],
    }


# ----------------------------------------------------------------
# ReportSynthesisSkill
# ----------------------------------------------------------------


@pytest.mark.asyncio
async def test_synthesis_returns_normalized_result():

    tool = FakeLLMTool()

    skill = ReportSynthesisSkill()

    result = await skill.execute(
        FakeContext(tool),
        build_data(),
    )

    assert result["available"] is True

    assert result["reason"] is None

    assert (
        result["summary"]["one_line"]
        == "这是一个 LangGraph 发票审批 Agent。"
    )

    assert result["summary"]["core_design"] == [
        "draft-only + human-in-the-loop",
        "单 Agent 状态机",
    ]

    # dimensions 只保留已知维度。
    assert set(result["dimensions"]) == {
        "agents",
        "workflow",
        "skills",
        "tools",
        "rag",
        "memory",
    }

    assert (
        result["dimensions"]["rag"]
        == "数据不足：README 未声明 rag。"
    )


@pytest.mark.asyncio
async def test_synthesis_unavailable_when_tool_missing():
    """没有注册 llm_chat 工具时必须降级而不是抛异常。"""

    skill = ReportSynthesisSkill()

    result = await skill.execute(
        FakeContext(),
        build_data(),
    )

    assert result["available"] is False

    assert "llm_chat" in result["reason"]


@pytest.mark.asyncio
async def test_synthesis_unavailable_when_llm_unavailable():
    """LLM 侧失败的原因必须原样透传，便于排查。"""

    tool = FakeLLMTool(
        available=False,
        reason="未配置 LLM_API_KEY，无法调用 LLM。",
    )

    skill = ReportSynthesisSkill()

    result = await skill.execute(
        FakeContext(tool),
        build_data(),
    )

    assert result["available"] is False

    assert (
        result["reason"]
        == "未配置 LLM_API_KEY，无法调用 LLM。"
    )


@pytest.mark.asyncio
async def test_synthesis_unavailable_on_invalid_json():

    tool = FakeLLMTool(
        content="这不是 JSON，只是一段解释文字。"
    )

    skill = ReportSynthesisSkill()

    result = await skill.execute(
        FakeContext(tool),
        build_data(),
    )

    assert result["available"] is False

    assert "JSON" in result["reason"]


@pytest.mark.asyncio
async def test_synthesis_parses_fenced_json():
    """LLM 用 markdown 代码块包裹、并在前后加解释文字时仍要能解析。"""

    tool = FakeLLMTool(
        content=(
            "好的，以下是结果：\n"
            "```json\n"
            f"{VALID_REPLY}\n"
            "```\n"
            "希望对你有帮助。"
        )
    )

    skill = ReportSynthesisSkill()

    result = await skill.execute(
        FakeContext(tool),
        build_data(),
    )

    assert result["available"] is True

    assert len(result["dimensions"]) == 6


@pytest.mark.asyncio
async def test_synthesis_prompt_forbids_speculation():
    """
    prompt 必须带上「只归纳不推测」的约束。

    这是本 Skill 的核心约束，
    被放宽会让报告重新变成「看起来合理但内容是编的」。
    """

    tool = FakeLLMTool()

    skill = ReportSynthesisSkill()

    await skill.execute(
        FakeContext(tool),
        build_data(),
    )

    messages = tool.calls[0]

    system = messages[0]["content"]

    user = messages[1]["content"]

    assert messages[0]["role"] == "system"

    assert "只能使用" in system

    assert "数据不足" in system

    assert "禁止使用你自己的外部知识" in system

    # 事实必须以 <facts> 包裹交给模型。
    assert "<facts>" in user

    assert "</facts>" in user


@pytest.mark.asyncio
async def test_synthesis_facts_expose_missing_dimensions():
    """
    事实摘要里缺失的维度必须以 available=False + reason 呈现。

    否则 LLM 会把「没采集到」误读成「项目没有这个能力」，
    进而写出「该项目未使用 RAG」这种错误结论。
    """

    tool = FakeLLMTool()

    skill = ReportSynthesisSkill()

    await skill.execute(
        FakeContext(tool),
        build_data(),
    )

    user = tool.calls[0][1]["content"]

    facts = json.loads(
        user[
            user.index("<facts>")
            + len("<facts>"):
            user.index("</facts>")
        ]
    )

    declared = facts["declared_structure"]

    assert declared["agents"]["available"] is True

    assert declared["rag"]["available"] is False

    assert (
        declared["rag"]["reason"]
        == "README 中没有 rag 相关声明。"
    )

    # 没有采集到的维度（本次数据里没有 skills）也必须显式标注。
    assert declared["skills"]["available"] is False

    # README 是主要事实来源，必须带上。
    assert facts["readme"]["available"] is True

    # 真实读到的源码也要给到，用于交叉验证 README 自述。
    assert (
        facts["source_files"][0]["file_path"]
        == "docker-compose.yml"
    )


@pytest.mark.asyncio
async def test_synthesis_survives_broken_data():
    """state.data 结构异常时不能抛异常。"""

    skill = ReportSynthesisSkill()

    tool = FakeLLMTool()

    result = await skill.execute(
        FakeContext(tool),
        {
            "repository": "not-a-dict",
            "readme": 123,
            "project_structure": None,
            "modules": "not-a-list",
            "evidence": None,
        },
    )

    assert result["available"] is True


# ----------------------------------------------------------------
# LLMChatTool
# ----------------------------------------------------------------


@pytest.mark.asyncio
async def test_llm_chat_tool_without_api_key(monkeypatch):
    """
    没有配置 API Key 时必须返回 available=False，
    而不是抛异常让整个 Workflow 失败。
    """

    import app.tools.llm_chat_tool as module

    class FakeSettings:
        LLM_API_KEY = ""
        LLM_MODEL = "deepseek-chat"
        LLM_BASE_URL = "https://api.deepseek.com"
        LLM_TIMEOUT = 60.0

    monkeypatch.setattr(
        module,
        "get_settings",
        lambda: FakeSettings(),
    )

    tool = LLMChatTool()

    result = await tool.execute(
        messages=[
            {"role": "user", "content": "hi"}
        ]
    )

    assert result["available"] is False

    assert "LLM_API_KEY" in result["reason"]


@pytest.mark.asyncio
async def test_llm_chat_tool_wraps_llm_error():
    """LLM 抛异常时必须转成 available=False 并带上原因。"""

    class ExplodingLLM:

        async def chat(self, messages, **kwargs):
            raise RuntimeError("connection reset")

    tool = LLMChatTool(llm=ExplodingLLM())

    result = await tool.execute(
        messages=[
            {"role": "user", "content": "hi"}
        ]
    )

    assert result["available"] is False

    assert "connection reset" in result["reason"]


@pytest.mark.asyncio
async def test_llm_chat_tool_rejects_empty_content():
    """LLM 返回空内容算失败，不能当成合法回答。"""

    class EmptyLLM:

        async def chat(self, messages, **kwargs):
            return "   "

    tool = LLMChatTool(llm=EmptyLLM())

    result = await tool.execute(
        messages=[
            {"role": "user", "content": "hi"}
        ]
    )

    assert result["available"] is False


@pytest.mark.asyncio
async def test_llm_chat_tool_uses_injected_llm():
    """注入 LLM 时不应读取配置、不应创建网络客户端。"""

    class EchoLLM:

        def __init__(self):
            self.seen = None

        async def chat(self, messages, **kwargs):
            self.seen = messages
            return "ok"

    llm = EchoLLM()

    tool = LLMChatTool(llm=llm)

    result = await tool.execute(
        messages=[
            {"role": "user", "content": "hello"}
        ]
    )

    assert result == {
        "available": True,
        "content": "ok",
    }

    assert llm.seen[0]["content"] == "hello"


# ----------------------------------------------------------------
# SynthesisNode
# ----------------------------------------------------------------


class FakeSkill:

    def __init__(
        self,
        result=None,
        error=None,
    ):
        self.result = result
        self.error = error
        self.calls = []

    async def execute(
        self,
        context,
        input_data,
    ):
        self.calls.append(input_data)

        if self.error is not None:
            raise self.error

        return self.result


@pytest.mark.asyncio
async def test_synthesis_node_writes_state_data():

    skill = FakeSkill(
        result={
            "available": True,
            "reason": None,
            "summary": {"one_line": "结论"},
            "dimensions": {},
        }
    )

    node = SynthesisNode(skill=skill)

    state = WorkflowState(run_id="synthesis-node")

    state.data = {
        "repository": {"name": "demo"},
        "_internal": "should be skipped",
    }

    result = await node.execute(state, FakeContext())

    assert result.data["synthesis"]["available"] is True

    assert len(result.outputs) == 1

    # 下划线开头的内部键不转发。
    assert "_internal" not in skill.calls[0]


@pytest.mark.asyncio
async def test_synthesis_node_degrades_on_skill_error():
    """
    Skill 抛异常时节点必须降级。

    否则综合分析这一章的失败会让
    整个 Analysis Workflow 变成 FAILED。
    """

    node = SynthesisNode(
        skill=FakeSkill(
            error=RuntimeError("boom")
        )
    )

    state = WorkflowState(run_id="synthesis-node-error")

    state.data = {}

    result = await node.execute(state, FakeContext())

    assert result.data["synthesis"]["available"] is False

    assert "boom" in result.data["synthesis"]["reason"]


# ----------------------------------------------------------------
# 跨 run 历史记忆注入
# ----------------------------------------------------------------


class FakeContextManager:
    """假的 ContextManager，只实现 build_history。"""

    def __init__(
        self,
        text=(
            "<history>\n"
            "- (2026-01-01) 问题：上次问的是什么"
            " ｜ 状态：COMPLETED\n"
            "</history>"
        ),
    ):
        self.text = text
        self.calls = []

    async def build_history(self, **kwargs):
        self.calls.append(kwargs)
        return self.text


class FakeContextWithMemory(FakeContext):
    """带 context_manager 的 context。"""

    def __init__(
        self,
        tool=None,
        manager=None,
    ):
        super().__init__(tool)

        self.context_manager = manager

        self.config = {"repository_id": 42}


@pytest.mark.asyncio
async def test_synthesis_injects_history_before_facts():
    """有历史记忆时要注入 user message，且排在 <facts> 之前。"""

    tool = FakeLLMTool()

    manager = FakeContextManager()

    skill = ReportSynthesisSkill()

    await skill.execute(
        FakeContextWithMemory(tool, manager),
        {
            **build_data(),
            "run_id": "run-1",
            "repository_id": 42,
        },
    )

    user = tool.calls[0][1]["content"]

    assert "<history>" in user

    # 不可信内容在前、权威事实在后。
    assert user.index("<history>") < user.index("<facts>")

    assert manager.calls[0]["repository_id"] == 42


@pytest.mark.asyncio
async def test_synthesis_without_context_manager_has_no_history():
    """
    无 context_manager 时不注入也不报错。

    tests/test_workflow.py 等手搭的 context 就是这种形态，
    改动前的输出必须完全保持。
    """

    tool = FakeLLMTool()

    result = await ReportSynthesisSkill().execute(
        FakeContext(tool),
        build_data(),
    )

    assert result["available"] is True

    user = tool.calls[0][1]["content"]

    assert "<history>" not in user


@pytest.mark.asyncio
async def test_synthesis_survives_context_manager_failure():
    """历史记忆构建失败不能让综合分析失败。"""

    class BrokenContextManager:
        async def build_history(self, **kwargs):
            raise RuntimeError("history db down")

    tool = FakeLLMTool()

    result = await ReportSynthesisSkill().execute(
        FakeContextWithMemory(tool, BrokenContextManager()),
        {
            **build_data(),
            "run_id": "run-1",
            "repository_id": 42,
        },
    )

    assert result["available"] is True

    assert "<history>" not in tool.calls[0][1]["content"]


def test_synthesis_system_prompt_states_history_trust():
    """
    system prompt 必须声明 <history> 可信度低于 <facts>。

    否则模型要么忽略历史，要么把上一轮的结论
    当成本轮的事实 —— 两种都违背「只归纳不推测」。
    """

    prompt = ReportSynthesisSkill._system_prompt()

    assert "<history>" in prompt

    assert "以 <facts> 为准" in prompt

    # 原有的防幻觉约束不能被挤掉。
    assert "只能使用" in prompt

    assert "数据不足" in prompt
