"""
Tools 包。

这里刻意不做 re-export：
工具由 app/services/analysis_factory.py 按名字装配，
包级再导出一份没有任何调用方，
只会让 ruff 一直报 F401，也让人误以为改包要同步改这里。
"""
