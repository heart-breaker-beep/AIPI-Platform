"""
Infrastructure Layer - 基础设施层。

职责：
- 实现技术细节（Workflow 引擎、Agent、Tool、数据库）
- 向内依赖 Domain 层的接口
- 不包含业务规则

依赖方向：
API → Domain ← Infrastructure
"""
