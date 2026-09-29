"""
EvidenceAnalysisSkill 测试。
"""

import pytest

from app.skills.evidence_analysis_skill import (
    EvidenceAnalysisSkill,
)


class FakeQdrantTool:

    async def execute(
        self,
        **kwargs,
    ):

        return [
            {
                "text": (
                    "class BaseAgent:"
                ),
                "document_id": (
                    "agent-base"
                ),
                "chunk_index": 0,
                "file_path": (
                    "app/agents/base.py"
                ),
            }
        ]


class FakeContext:

    tools = {
        "qdrant_search":
            FakeQdrantTool()
    }


@pytest.mark.asyncio
async def test_evidence_analysis_skill():

    skill = EvidenceAnalysisSkill()

    result = await skill.execute(
        FakeContext(),
        {
            "query_vector": [
                0.1,
                0.2,
            ],
            "limit": 5,
        },
    )

    assert (
        result["count"]
        == 1
    )

    evidence = (
        result["evidence"][0]
    )

    assert (
        evidence["content"]
        == "class BaseAgent:"
    )

    assert (
        evidence["file_path"]
        == "app/agents/base.py"
    )

    # 当前索引器没有可靠行号，
    # 所以不能伪造。
    assert (
        evidence["line_start"]
        is None
    )

    assert (
        evidence["line_end"]
        is None
    )

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
