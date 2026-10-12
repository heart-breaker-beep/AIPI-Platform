"""
Analysis Domain - 分析任务领域。

职责：
- 分析任务的业务编排
- Workflow 生命周期管理
- 不涉及具体技术实现（Agent/Tool/Database）

这里的 __all__ 只导出领域内的类型。
组合根（create_analysis_service）已移到 app/services/analysis_factory.py ——
它必须同时认识 domain 与 infrastructure，
留在本目录会让 domain 反向依赖 infrastructure。
"""

from .service import AnalysisService
from .workflow import AnalysisWorkflowOrchestrator

__all__ = [
    "AnalysisService",
    "AnalysisWorkflowOrchestrator",
]
