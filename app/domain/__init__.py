"""
Domain Layer - 核心领域层。

职责：
- 定义业务规则和编排逻辑
- 不依赖任何基础设施实现
- 只定义接口，由 Infrastructure 层实现

依赖方向：
API → Domain ← Infrastructure
"""
