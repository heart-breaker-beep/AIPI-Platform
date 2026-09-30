"""
Workflow Checkpoint 数据访问层。
"""

import json

from sqlalchemy import (
    delete,
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.checkpoint import Checkpoint
from app.workflow.state import WorkflowState

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

# 瘦身后各字段保留的规模。
READ_README_CHARS = 4_000

READ_EVIDENCE = 20

READ_MODULES = 4


class CheckpointRepository:
    """负责 checkpoints 表的数据访问。"""

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:

        self.session = session

    async def save(
        self,
        state: WorkflowState,
    ) -> Checkpoint:
        """
        保存 WorkflowState 快照。

        收进来的 state 是 CheckpointManager
        deepcopy 过的快照，
        因此这里瘦身不会影响内存里的运行状态。
        """

        data, trims = self._fit_state_data(
            state.data
        )

        if trims:

            # 下划线开头，FinalizerNode 组装报告输入时
            # 会跳过这类键，不会污染报告。
            data["_trimmed"] = trims

        checkpoint = Checkpoint(
            run_id=state.run_id,
            checkpoint_version=(
                state.checkpoint_version
            ),
            status=state.status,
            current_node=state.current_node,
            state_data=data,
            outputs=state.outputs,
            errors=state.errors,
            retry_count=state.retry_count,
            pause_reason=state.pause_reason,
            human_approved=state.human_approved,
        )

        self.session.add(
            checkpoint
        )

        await self.session.flush()

        return checkpoint

    @classmethod
    def _fit_state_data(
        cls,
        data,
    ):
        """
        把 state_data 压到安全上限以内。

        返回 (可能被瘦身过的 data, 瘦身记录)。
        """

        if not isinstance(data, dict):
            return data, {}

        size = cls._size(data)

        if size <= MAX_STATE_BYTES:
            return data, {}

        dropped = {}

        for path in TRIM_ORDER:

            before = cls._size(data)

            cls._trim(data, path)

            after = cls._size(data)

            if after < before:

                dropped[path] = (
                    before - after
                )

            if after <= MAX_STATE_BYTES:
                break

        return data, {
            "original_bytes": size,
            "final_bytes": cls._size(data),
            "limit_bytes": MAX_STATE_BYTES,
            "dropped_bytes": dropped,
        }

    @staticmethod
    def _size(value) -> int:
        """按实际落库的序列化方式估算字节数。"""

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
    def _trim(
        cls,
        data: dict,
        path: str,
    ) -> None:
        """按路径瘦身一个字段。"""

        if path == "final_report.content":

            report = data.get("final_report")

            if isinstance(report, dict):

                # 报告正文已经写在 reports/*.md，
                # 这里只留文件信息，
                # 取报告时由 runner 回读文件。
                report.pop("content", None)

            return

        if path == "readme":

            readme = data.get("readme")

            if isinstance(readme, str) and len(
                readme
            ) > READ_README_CHARS:

                data["readme"] = (
                    readme[:READ_README_CHARS]
                )

            return

        if path == "evidence":

            cls._trim_list(
                data,
                "evidence",
                READ_EVIDENCE,
                ("content",),
            )

            # evidence_analysis_agent 里是同一份数据。
            cls._trim_list(
                data,
                "evidence_analysis_agent",
                READ_EVIDENCE,
                ("content",),
                nested="evidence",
            )

            return

        if path == "modules":

            cls._trim_list(
                data,
                "modules",
                READ_MODULES,
                ("content",),
            )

    @staticmethod
    def _trim_list(
        data: dict,
        key: str,
        keep: int,
        drop_keys,
        nested=None,
    ) -> None:
        """截断一个列表字段，并去掉指定子字段。"""

        value = data.get(key)

        if nested and isinstance(value, dict):

            value = value.get(nested)

        if not isinstance(value, list):
            return

        if len(value) > keep:

            del value[keep:]

        for item in value:

            if isinstance(item, dict):

                for drop in drop_keys:
                    item.pop(drop, None)

    async def get_latest(
        self,
        run_id: str,
    ) -> WorkflowState | None:
        """
        获取指定 run 的最新 Checkpoint。

        实现说明：

        不能用 ORDER BY checkpoint_version DESC LIMIT 1。

        state_data 是可能达到数百 KB 的 JSON
        （包含目录结构、关键源码、Evidence、报告），
        MySQL 在对这种大行排序时会报：

            OperationalError 1038
            Out of sort memory,
            consider increasing server sort buffer size

        因此改成两步：

            1. 只查最大版本号（只读整数列，不需要排序大行）
            2. 按 (run_id, version) 精确取行（等值查询，不排序）
        """

        version_result = await self.session.execute(
            select(
                func.max(
                    Checkpoint.checkpoint_version
                )
            ).where(
                Checkpoint.run_id == run_id
            )
        )

        latest_version = (
            version_result.scalar_one_or_none()
        )

        if latest_version is None:
            return None

        result = await self.session.execute(
            select(Checkpoint)
            .where(
                Checkpoint.run_id == run_id,
                Checkpoint.checkpoint_version
                == latest_version,
            )
            .limit(1)
        )

        checkpoint = (
            result.scalar_one_or_none()
        )

        if checkpoint is None:
            return None

        return WorkflowState(
            run_id=checkpoint.run_id,
            status=checkpoint.status,
            current_node=checkpoint.current_node,
            data=checkpoint.state_data or {},
            outputs=checkpoint.outputs or [],
            errors=checkpoint.errors or [],
            retry_count=checkpoint.retry_count,
            pause_reason=checkpoint.pause_reason,
            human_approved=checkpoint.human_approved,
            checkpoint_version=checkpoint.checkpoint_version,
        )

    async def delete(
        self,
        run_id: str,
    ) -> None:
        """删除指定 run 的全部 Checkpoint。"""

        await self.session.execute(
            delete(Checkpoint).where(
                Checkpoint.run_id == run_id
            )
        )

        await self.session.flush()