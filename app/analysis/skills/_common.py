"""
技能层公共工具。

背景：综合分析、学习路线、模块深挖三个 LLM 技能
各自抄了一份同样的「取工具 / 拼 history / 解析 JSON」
与「值 → 限长字符串列表」逻辑，
合计四五百行以不同细节重复。

这里只收拢**行为完全一致**的部分：
把差异（上限、是否按字符截断、单条规范化函数）
做成参数，调用方传自己的值，
因此合并前后的输出逐字节相同。
"""

import json

from app.core.exceptions import ToolError
from app.core.logging import get_logger


logger = get_logger(__name__)


# 列表类字段的默认上限。
#
# 三个技能原本都写死 6（综合分析用 MAX_BULLETS = 6），
# 因此默认值取 6，避免任何一处忘记传参时行为悄悄变化。
DEFAULT_MAX_ITEMS = 6


def as_text(value) -> str:
    """
    把任意值转成去空白的字符串。

    列表/元组按「；」连接（综合分析对嵌套值的处理），
    None 变成空字符串。
    """

    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    if isinstance(
        value,
        (list, tuple),
    ):

        return "；".join(
            str(item).strip()
            for item in value
            if str(item).strip()
        )

    return str(value).strip()


def as_text_list(
    value,
    *,
    max_items: int = DEFAULT_MAX_ITEMS,
    max_chars: int | None = None,
    normalize=None,
) -> list:
    """
    把任意值规整成限长的字符串列表。

    Args:
        value: 原始值（None / 字符串 / 列表 / 其它）
        max_items: 最多保留多少条
        max_chars: 单条最多保留多少字符（None 表示不截断）
        normalize: 单条转换函数，默认 str(item).strip()。
            综合分析传自己的 _as_text（它会把嵌套列表join 起来）

    Returns:
        字符串列表
    """

    if value is None:
        return []

    if isinstance(value, str):

        text = value.strip()

        return [text] if text else []

    if not isinstance(
        value,
        (list, tuple),
    ):

        return [str(value)]

    items = []

    for item in value:

        text = (
            normalize(item)
            if normalize is not None
            else str(item).strip()
        )

        if not text:
            continue

        if max_chars is not None:
            text = text[:max_chars]

        items.append(text)

        if len(items) >= max_items:
            break

    return items


def dumps_prompt(payload) -> str:
    """
    统一的 prompt JSON 序列化。

    ensure_ascii=False：中文要在 prompt 里保持可读，
    \\uXXXX 既费 token 又影响模型理解。

    default=str：facts 里带 datetime / 枚举等非 JSON 类型时，
    退回字符串而不是抛 TypeError —— prompt 组装失败
    会把整个技能打挂，代价远高于类型损失。

    indent=2：三个技能原本都是缩进两格，
    保留它，合并前后发出去的内容逐字相同。
    """

    return json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        default=str,
    )


async def load_tree(
    tool,
    owner: str,
    repo: str,
    branch: str,
) -> list:
    """
    读取仓库文件树；拿不到时返回空列表。

    目录结构属于取材的增强信息：
    一次超时不该让整个分析失败。
    但也不能静默 —— 失败要留下日志，
    否则「没有目录结构」这件事在报告里毫无痕迹。

    合并自 architecture_analysis_skill 与 module_deep_dive_skill
    各自的一份（后者原本漏了 try/except）。
    """

    if tool is None:
        return []

    get_tree = getattr(
        tool,
        "get_tree",
        None,
    )

    if not callable(get_tree):
        return []

    try:

        tree = await get_tree(
            owner=owner,
            name=repo,
            branch=branch,
        )

    except ToolError as error:

        logger.warning(
            "repository tree unavailable | %s/%s | %s: %s",
            owner,
            repo,
            type(error).__name__,
            error,
        )

        return []

    if not isinstance(tree, list):
        return []

    return tree
