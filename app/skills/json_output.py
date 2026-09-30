"""
LLM JSON 输出解析。

为什么单独抽出来
================

报告综合分析（ReportSynthesisSkill）与
单模块深挖（ModuleDeepDiveSkill）都要
让 LLM 返回 JSON，
而模型的实际返回有三种常见形态：

    1. 纯 JSON
    2. ```json 代码块包裹
    3. 前后混着解释文字

更麻烦的是第四种：**被截断的 JSON**。

真实事故：综合分析要输出六个维度的判断段落，
回复一旦触到 max_tokens 上限就会被切断，
而截断的 JSON 用 json.loads 必然失败，
报告就会整章退化成「综合分析不可用」。

两处都要处理这件事，
逻辑放在一处避免两边慢慢长歪。
"""

import json


def parse_json_object(content: str):
    """
    尽最大努力把 LLM 回复解析成 dict。

    解析不出来返回 None，
    由调用方决定怎么降级 ——
    这里绝不伪造半截内容。
    """

    if not isinstance(content, str):
        return None

    text = strip_code_fence(content)

    if not text:
        return None

    try:

        parsed = json.loads(text)

    except (ValueError, TypeError):

        # 前后混入解释文字时，
        # 退回到「第一个 { 到最后一个 }」。
        start = text.find("{")

        end = text.rfind("}")

        if start == -1 or end <= start:

            # 连一对完整的 {} 都没有，
            # 基本可以认定回复被截断了。
            return repair_truncated(text)

        try:

            parsed = json.loads(
                text[start: end + 1]
            )

        except (ValueError, TypeError):

            return repair_truncated(text)

    if isinstance(parsed, dict):
        return parsed

    return None


def strip_code_fence(content: str) -> str:
    """去掉 markdown 代码块围栏。"""

    text = content.strip()

    if not text.startswith("```"):
        return text

    lines = text.splitlines()

    if lines and lines[0].startswith("```"):
        lines = lines[1:]

    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    return "\n".join(lines).strip()


def repair_truncated(text: str):
    """
    尝试修复被截断的 JSON。

    两种策略，依次尝试：

        1. 直接补上未闭合的引号与括号
        2. 回退到最后一个逗号再补括号
           （截断正好落在半个键值上时用）

    修不好就返回 None。
    """

    if not text:
        return None

    for candidate in (
        close_brackets(text),
        close_brackets(trim_to_last_comma(text)),
    ):

        if not candidate:
            continue

        try:

            parsed = json.loads(candidate)

        except (ValueError, TypeError):

            continue

        if isinstance(parsed, dict):
            return parsed

    return None


def close_brackets(text: str) -> str:
    """补上未闭合的引号与括号。"""

    stack = []

    in_string = False

    escaped = False

    for char in text:

        if in_string:

            if escaped:
                escaped = False

            elif char == "\\":
                escaped = True

            elif char == '"':
                in_string = False

            continue

        if char == '"':
            in_string = True

        elif char == "{":
            stack.append("}")

        elif char == "[":
            stack.append("]")

        elif char in "}]":

            if stack:
                stack.pop()

    repaired = text

    # 截断在字符串中间时先补引号。
    if in_string:
        repaired += '"'

    return repaired + "".join(
        reversed(stack)
    )


def trim_to_last_comma(text: str) -> str:
    """回退到最后一个逗号，丢掉残缺的尾巴。"""

    index = text.rfind(",")

    if index <= 0:
        return ""

    return text[:index]
