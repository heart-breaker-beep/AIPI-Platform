"""项目统一日志配置，负责初始化日志格式并提供带 run_id 的任务日志。"""

import logging
import sys
from typing import Optional


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)


def setup_logging() -> None:
    """初始化全局日志配置。"""
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        stream=sys.stdout,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """获取指定模块的 Logger。"""
    return logging.getLogger(name)


def log_with_run_id(
    logger: logging.Logger,
    level: int,
    message: str,
    run_id: Optional[str] = None,
) -> None:
    """记录任务日志，并在存在 run_id 时关联具体任务。"""

    # run_id 是后续 Workflow、Agent、Tool、Checkpoint
    # 追踪同一次任务执行过程的重要标识。
    if run_id:
        message = f"run_id={run_id} | {message}"

    logger.log(level, message)