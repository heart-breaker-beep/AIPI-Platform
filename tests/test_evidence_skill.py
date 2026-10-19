"""
EvidenceAnalysisSkill 测试。
"""

import pytest

from app.analysis.skills.evidence_analysis_skill import (
    EvidenceAnalysisSkill,
)
from app.analysis.evidence.store import EvidenceStore


class FakeContext:
    """
    只需要 tools 的最小 Context。

    RAG 通路（rag_retrieval 工具）在没开 RAG 时不参与，
    这些用例只覆盖结构证据与落库行为。
    """

    tools = {}

@pytest.mark.asyncio
async def test_evidence_from_architecture_agent_output():
    """
    源码证据分支必须能读到真实的 key。

    旧实现只读 input_data["architecture"]，
    但真实数据结构里没有这个 key
    （真实 key 是 architecture_analysis_agent，
    且 PlanExecutorNode 会把 modules 拍平到顶层），
    因此这个分支以前从未执行过，
    Evidence 里只有 README、没有源码。
    """

    skill = EvidenceAnalysisSkill()

    result = await skill.execute(
        FakeContext(),
        {
            "repo_url": "https://github.com/demo/demo",
            "architecture_analysis_agent": {
                "files": ["app/main.py"],
                "modules": [
                    {
                        "file_path": "app/main.py",
                        "content": "class Demo:\n    pass\n",
                    }
                ],
            },
        },
    )

    file_paths = [
        item["file_path"]
        for item in result["evidence"]
    ]

    assert "app/main.py" in file_paths


@pytest.mark.asyncio
async def test_failed_module_read_is_not_used_as_evidence():
    """读取失败的模块不能变成空内容的假证据。"""

    skill = EvidenceAnalysisSkill()

    result = await skill.execute(
        FakeContext(),
        {
            "repo_url": "https://github.com/demo/demo",
            "modules": [
                {
                    "file_path": "app/broken.py",
                    "content": "",
                    "error": "Read timeout",
                }
            ],
        },
    )

    assert result["count"] == 0


@pytest.mark.asyncio
async def test_readme_evidence_is_truncated():
    """
    README 证据也要按同样的上限截断。

    回归点：模块证据截断到 MAX_EVIDENCE_CHARS，
    README 却是整份落库 ——
    一份上万字符的 README 比整个源码证据集合还大。
    """

    readme = "README line\n" * 400

    result = await EvidenceAnalysisSkill().execute(
        FakeContext(),
        {
            "repo_url": "https://github.com/demo/demo",
            "readme": readme,
        },
    )

    evidence = result["evidence"][0]

    assert len(evidence["content"]) == (
        EvidenceAnalysisSkill.MAX_EVIDENCE_CHARS
    )

    # 行号跟着截断后的正文走，
    # 不能标成「README:1-400」却只存了前几十行。
    assert evidence["line_end"] == len(
        evidence["content"].splitlines()
    )

    assert evidence["line_end"] < len(
        readme.splitlines()
    )


class FakeSavepoint:
    """可 async with 的假 SAVEPOINT。"""

    def __init__(
        self,
        session,
    ):

        self.session = session

    async def __aenter__(self):

        return self

    async def __aexit__(
        self,
        *exc_info,
    ):

        self.session.savepoint_exits.append(
            exc_info[0]
        )

        # 不要把异常吞掉：调用方要能记下失败原因。
        return False


class FakeSession:
    """
    只记录 add / flush / begin_nested 的假 Session。

    指定 fail_on 里的内容在 add 时抛异常，
    用来模拟「某一条证据违反约束写不进去」。
    """

    def __init__(
        self,
        fail_on=(),
    ):

        self.added = []
        self.savepoints = 0
        self.savepoint_exits = []
        self.fail_on = set(fail_on)

    def add(
        self,
        instance,
    ):

        if getattr(
            instance,
            "content",
            "",
        ) in self.fail_on:

            raise RuntimeError(
                "duplicate key"
            )

        self.added.append(instance)

    async def flush(self):

        return None

    def begin_nested(self):

        self.savepoints += 1

        return FakeSavepoint(self)


class FakePersistContext:

    def __init__(
        self,
        session,
    ):

        self.tools = {}
        self.evidence_store = EvidenceStore(session)

        self.config = {
            "repository_id": 7,
        }


@pytest.mark.asyncio
async def test_each_evidence_write_uses_its_own_savepoint():
    """
    单条证据写失败不能让整个 session 失去可用性。

    回归点：失败后继续用同一个 session，
    session 会停在「需要回滚」状态，
    之后所有写入（后面的证据、checkpoint）连锁失败 ——
    一条坏数据能把整个 run 的落库全带走。
    """

    session = FakeSession(
        fail_on=("bad",),
    )

    result = await EvidenceAnalysisSkill().execute(
        FakePersistContext(session),
        {
            "repo_url": "https://github.com/demo/demo",
            "modules": [
                {
                    "file_path": "app/bad.py",
                    "content": "bad",
                },
                {
                    "file_path": "app/good.py",
                    "content": "good",
                },
            ],
        },
    )

    # 每条写入都有自己的 SAVEPOINT。
    assert session.savepoints == 2

    # 坏的那条被记下来，好的那条照常落库。
    assert len(result["persist_failures"]) == 1

    assert result["count"] == 1

    assert [
        item["file_path"]
        for item in result["evidence"]
    ] == ["app/good.py"]
