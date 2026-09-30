"""
LLM JSON 输出解析测试。

这套容错逻辑是真实事故换来的：
综合分析要输出六个维度的判断段落，
回复一旦触到 max_tokens 上限就会被切断，
而截断的 JSON 用 json.loads 必然失败，
报告整章退化成「综合分析不可用」。
"""

import json

from app.skills.json_output import (
    parse_json_object,
    strip_code_fence,
)


FULL = json.dumps(
    {
        "summary": {
            "one_line": "结论",
            "core_design": ["设计一", "设计二"],
            "highlights": ["亮点"],
        },
        "dimensions": {
            "agents": "Agent 判断段落",
            "workflow": "Workflow 判断段落",
            "rag": "RAG 判断段落",
        },
    },
    ensure_ascii=False,
    indent=2,
)


# ----------------------------------------------------------------
# 正常形态
# ----------------------------------------------------------------


def test_parses_plain_json():

    parsed = parse_json_object(FULL)

    assert parsed["summary"]["one_line"] == "结论"


def test_parses_fenced_json():

    parsed = parse_json_object(
        "```json\n" + FULL + "\n```"
    )

    assert parsed["dimensions"]["rag"] == "RAG 判断段落"


def test_parses_json_with_surrounding_prose():
    """模型在 JSON 前后加解释文字时要能救回来。"""

    parsed = parse_json_object(
        "好的，以下是分析结果：\n"
        + FULL
        + "\n希望对你有帮助。"
    )

    assert parsed["summary"]["core_design"] == [
        "设计一",
        "设计二",
    ]


def test_returns_none_for_non_json():

    assert parse_json_object("这不是 JSON") is None

    assert parse_json_object("") is None

    assert parse_json_object(None) is None


def test_returns_none_for_json_array():
    """只接受对象；顶层是数组时不算成功。"""

    assert parse_json_object("[1, 2, 3]") is None


# ----------------------------------------------------------------
# 截断修复
# ----------------------------------------------------------------


def test_repairs_truncation_inside_string():
    """截断在字符串中间 —— 补引号与括号。"""

    truncated = FULL[: len(FULL) - 30]

    parsed = parse_json_object(truncated)

    assert parsed is not None

    assert parsed["summary"]["one_line"] == "结论"


def test_repairs_truncation_between_values():
    """截断在值之后 —— 补括号。"""

    parsed = parse_json_object(FULL.rstrip()[:-1])

    assert parsed is not None

    assert parsed["summary"]["one_line"] == "结论"


def test_repairs_truncation_after_key():
    """截断在半个键值上 —— 回退到最后一个逗号。"""

    cut = FULL[: FULL.rindex('"rag"') + 6]

    parsed = parse_json_object(cut)

    assert parsed is not None

    assert parsed["summary"]["one_line"] == "结论"


def test_repairs_truncation_inside_array():

    text = json.dumps(
        {
            "summary": {
                "one_line": "x",
                "core_design": ["a", "b"],
            },
            "dimensions": {},
        },
        ensure_ascii=False,
    )

    parsed = parse_json_object(text[:55])

    assert parsed is not None

    assert parsed["summary"]["one_line"] == "x"


def test_repair_never_invents_content():
    """
    修不出来就返回 None。

    降级成「综合分析不可用」是可接受的；
    把半截内容当结论展示是不可接受的。
    """

    # 值缺失，补括号与回退逗号都救不回来。
    assert parse_json_object('{"a": , "b": 1') is None

    assert parse_json_object("纯粹的一段说明文字。") is None


def test_repair_may_yield_empty_containers():
    """
    补全后是「合法的空结构」时应当接受。

    这不是编造内容：{"summary": {}} 是真实解析出来的，
    调用方会看到 summary 为空并如实降级。
    把它当成解析失败反而会丢掉已经拿到的部分。
    """

    parsed = parse_json_object('{"summary": {')

    assert parsed == {"summary": {}}


def test_repair_handles_braces_inside_strings():
    """字符串里的花括号不能干扰配平。"""

    parsed = parse_json_object(
        '{"a": "包含 } 和 ] 的文本", "b": 1'
    )

    assert parsed is not None

    assert parsed["b"] == 1


def test_repair_handles_escaped_quotes():
    """转义引号不能让扫描器误判字符串结束。"""

    parsed = parse_json_object(
        '{"a": "带 \\" 转义引号的值", "b": 2'
    )

    assert parsed is not None

    assert parsed["b"] == 2


# ----------------------------------------------------------------
# 代码块剥离
# ----------------------------------------------------------------


def test_strip_code_fence():

    assert strip_code_fence(
        "```json\n{}\n```"
    ) == "{}"

    assert strip_code_fence("{}") == "{}"

    assert strip_code_fence(
        "```\n{}\n```"
    ) == "{}"
