"""
Workflow 节点公共设施。

包含：
- BaseNode 的兼容再导出（项目只保留 app.workflow.node.BaseNode）
- output_marker：写 state.outputs 时的统一精简标记
"""

from app.workflow.node import BaseNode


__all__ = [
    "BaseNode",
    "output_marker",
]


def output_marker(
    name,
    result,
) -> dict:
    """
    生成 state.outputs 里的一条运行痕迹。

    为什么不存正文：outputs 在业务上没有读取方
    （只在 checkpoint 里存取），而 StateManager 的瘦身
    只覆盖 state.data —— 把完整报告 append 进 outputs，
    就会绕过体积守卫，重新把单行 checkpoint 推过
    asyncmy 的 256KB 读取上限，让这个 run 再也读不回来。

    保留名字与产出字段，足够排查「这一步到底有没有产出」。

    Args:
        name: 产出方名称（Agent 名或节点名）
        result: 节点/Agent 的原始产出

    Returns:
        精简标记
    """

    marker = {
        "agent": name,
        "type": type(result).__name__,
    }

    if isinstance(result, dict):

        marker["fields"] = sorted(
            result.keys()
        )

    return marker
