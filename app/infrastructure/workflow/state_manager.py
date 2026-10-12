"""
State Manager - WorkflowState 瘦身策略管理。

职责：
- 管理 WorkflowState 的瘦身策略（业务规则）
- 决定哪些字段可以丢弃、保留多少
- 返回瘦身后的 data 字典

与 CheckpointRepository 的分工：
- StateManager：业务逻辑，决定"什么可以丢"、"保留多少"
- CheckpointRepository：数据访问，只负责存储和读取

从 CheckpointRepository 中抽取的逻辑：
- _fit_state_data() -> prepare_for_persistence()
- _trim() -> _trim_field()
- _size() -> _estimate_size()
- TRIM_ORDER, MAX_STATE_BYTES 等常量
"""

import copy
import json

# 导出常量供测试使用
MAX_STATE_BYTES = 180_000


class StateManager:
    """WorkflowState 管理器 - 负责瘦身策略。"""

    # 单行 state_data 的安全上限（字节）。
    #
    # 为什么必须设：列类型是 JSON，而 asyncmy 驱动
    # 读取大字段时的缓冲区分片会失败，
    # 报错是客户端的
    #
    #     Lost connection to MySQL server during query
    #     (Existing exports of data: object cannot be re-sized)
    #
    # 实测临界点与 MySQL 的 sort_buffer_size
    # （默认 262,144 = 256KB）吻合：
    # 224KB 能读，264KB 读不了。
    #
    # 一旦写进去一个超限的 state_data，
    # **这个 run 就再也读不回来了** ——
    # 恢复、取报告、深挖全部 500。
    # 所以必须在写入前拦住，而不是读取时补救。
    #
    # 留足余量取 180KB。
    MAX_STATE_BYTES = 180_000

    # 超限时按「最不值得留」的顺序逐项瘦身。
    #
    # 顺序是有讲究的：
    #
    #   final_report.content  报告正文已经写到 reports/*.md，
    #                         存进 state 纯属重复，
    #                         而且它正好是压垮骆驼的最后一根稻草
    #                         （finalizer 那一步 +20KB）。
    #   readme                原始 README，已被抽取成结构，
    #                         保留开头足够人工核对。
    #   evidence              证据正文，报告第 12 章展示用。
    #   modules               源码片段，报告第 11 章展示用 ——
    #                         最后才动它，因为删了报告就空了。
    TRIM_ORDER = (
        "final_report.content",
        "readme",
        "evidence",
        "modules",
    )

    # 瘦身后各字段保留的规模
    MAX_README_CHARS = 4_000
    MAX_EVIDENCE = 20
    MAX_MODULES = 4

    # state.outputs 的安全上限（字节）。
    #
    # outputs 在业务上没有读取方（只在 checkpoint 里存取），
    # 节点写入时应该只 append 精简标记
    # （见 nodes/base.py 的 output_marker）。
    # 这里是兜底：任何一个节点把大对象写进来，
    # 都不该让整行 checkpoint 越过读取上限。
    #
    # 2 万字节足够装几十条标记。
    MAX_OUTPUTS_BYTES = 20_000

    @classmethod
    def prepare_for_persistence(
        cls,
        data: dict,
        max_bytes: int | None = None,
    ) -> tuple[dict, dict]:
        """
        瘦身 state.data 以适应数据库限制。

        Args:
            data: 原始 state.data
            max_bytes: 最大字节数限制（默认 180KB）

        Returns:
            (瘦身后的 data, 瘦身记录)

        瘦身记录格式：
        {
            "original_bytes": 原始大小,
            "final_bytes": 瘦身后大小,
            "limit_bytes": 限制大小,
            "dropped_bytes": {"字段路径": 减少的字节数}
        }
        """
        if not isinstance(data, dict):
            return data, {}

        if max_bytes is None:
            max_bytes = cls.MAX_STATE_BYTES

        # 深拷贝，避免修改原始数据
        data = copy.deepcopy(data)

        size = cls._estimate_size(data)

        if size <= max_bytes:
            return data, {}

        dropped = {}

        for path in cls.TRIM_ORDER:
            before = cls._estimate_size(data)

            cls._trim_field(data, path)

            after = cls._estimate_size(data)

            if after < before:
                dropped[path] = before - after

            if after <= max_bytes:
                break

        return data, {
            "original_bytes": size,
            "final_bytes": cls._estimate_size(data),
            "limit_bytes": max_bytes,
            "dropped_bytes": dropped,
        }

    @classmethod
    def prepare_outputs(
        cls,
        outputs: list,
        max_bytes: int | None = None,
    ) -> list:
        """
        瘦身 state.outputs。

        与 data 的逐字段瘦身不同：outputs 里的条目没有读取方，
        超限时整体降级为标记即可，不需要排优先级。

        Args:
            outputs: 原始 state.outputs
            max_bytes: 最大字节数限制（默认 20KB）

        Returns:
            瘦身后的 outputs（未超限时原样返回）
        """

        if not isinstance(outputs, list) or not outputs:
            return outputs

        if max_bytes is None:
            max_bytes = cls.MAX_OUTPUTS_BYTES

        if cls._estimate_size(outputs) <= max_bytes:
            return outputs

        return [
            cls._outputs_marker(item)
            for item in outputs
        ]

    @classmethod
    def _outputs_marker(cls, item):
        """把一条 outputs 降级为标记。"""

        if not isinstance(item, dict):
            return {"type": type(item).__name__}

        marker = {
            "type": "dict",
            "keys": sorted(
                str(key) for key in item
            ),
        }

        # 已经是 output_marker 产出的标记时保留 agent 名，
        # 否则排查时看不出这条是谁写的。
        agent = item.get("agent")

        if isinstance(agent, str):
            marker["agent"] = agent

        return marker

    @staticmethod
    def _estimate_size(value) -> int:
        """
        按实际落库的序列化方式估算字节数。

        Args:
            value: 待估算的值

        Returns:
            估算的字节数
        """
        try:
            return len(
                json.dumps(
                    value,
                    ensure_ascii=False,
                    default=str,
                ).encode("utf-8")
            )
        except (TypeError, ValueError):
            return 0

    @classmethod
    def _trim_field(
        cls,
        data: dict,
        path: str,
    ) -> None:
        """
        按路径瘦身一个字段（就地修改）。

        Args:
            data: state.data 字典
            path: 字段路径（支持 "." 嵌套，如 "final_report.content"）
        """
        if path == "final_report.content":
            report = data.get("final_report")

            if isinstance(report, dict):
                # 报告正文已经写在 reports/*.md，
                # 这里只留文件信息，
                # 取报告时由 orchestrator 回读文件。
                report.pop("content", None)

            return

        if path == "readme":
            readme = data.get("readme")

            if isinstance(readme, str) and len(readme) > cls.MAX_README_CHARS:
                data["readme"] = readme[: cls.MAX_README_CHARS]

            return

        if path == "evidence":
            cls._trim_list(
                data,
                "evidence",
                cls.MAX_EVIDENCE,
                ("content",),
            )

            # evidence_analysis_agent 里是同一份数据
            cls._trim_list(
                data,
                "evidence_analysis_agent",
                cls.MAX_EVIDENCE,
                ("content",),
                nested="evidence",
            )

            return

        if path == "modules":
            cls._trim_list(
                data,
                "modules",
                cls.MAX_MODULES,
                ("content",),
            )

    @staticmethod
    def _trim_list(
        data: dict,
        key: str,
        keep: int,
        drop_keys: tuple,
        nested: str | None = None,
    ) -> None:
        """
        截断一个列表字段，并去掉指定子字段（就地修改）。

        Args:
            data: state.data 字典
            key: 列表字段的键名
            keep: 保留多少条
            drop_keys: 要删除的子字段名（针对列表中的字典项）
            nested: 如果值是嵌套字典，先按此键提取列表
        """
        value = data.get(key)

        if nested and isinstance(value, dict):
            value = value.get(nested)

        if not isinstance(value, list):
            return

        # 截断列表
        if len(value) > keep:
            del value[keep:]

        # 删除子字段
        for item in value:
            if isinstance(item, dict):
                for drop in drop_keys:
                    item.pop(drop, None)

    @classmethod
    def add_trim_metadata(cls, data: dict, trims: dict) -> dict:
        """
        在 data 中添加瘦身元数据。

        Args:
            data: state.data 字典
            trims: 瘦身记录

        Returns:
            添加了元数据的 data（就地修改 + 返回）
        """
        if trims:
            # 下划线开头，FinalizerNode 组装报告输入时
            # 会跳过这类键，不会污染报告。
            data["_trimmed"] = trims

        return data

    # 测试兼容别名
    @classmethod
    def fit_state_data(cls, data: dict) -> tuple[dict, dict]:
        """
        测试兼容别名，调用 prepare_for_persistence。

        Args:
            data: state.data 字典

        Returns:
            (瘦身后的 data, 瘦身记录)
        """
        return cls.prepare_for_persistence(data)

    @staticmethod
    def _size(data) -> int:
        """
        测试兼容别名，调用 _estimate_size。

        Args:
            data: 要估算的数据

        Returns:
            序列化后的字节数
        """
        return StateManager._estimate_size(data)
