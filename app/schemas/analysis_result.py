"""
Analysis Result 数据契约。

Phase12:

Workflow执行结果
        ↓
AnalysisResult
        ↓
Report
"""

from typing import Any

from pydantic import BaseModel, Field



class ProjectOverview(BaseModel):
    """
    项目基础信息。
    """

    name: str | None = None

    description: str | None = None

    repository_url: str | None = None

    language: str | None = None



class TechnologyStack(BaseModel):
    """
    技术栈信息。
    """

    languages: list[str] = Field(
        default_factory=list
    )

    frameworks: list[str] = Field(
        default_factory=list
    )

    databases: list[str] = Field(
        default_factory=list
    )

    tools: list[str] = Field(
        default_factory=list
    )



class AgentAnalysisResult(BaseModel):
    """
    单个 Agent 分析结果。
    """

    agent_name: str


    summary: str | None = None


    facts: list[str] = Field(
        default_factory=list
    )


    evidence_ids: list[str] = Field(
        default_factory=list
    )



class AnalysisResult(BaseModel):
    """
    Phase12 标准分析结果。

    作为:

    Workflow
        ↓
    Report

    的统一数据契约。
    """


    run_id: str



    project_overview: ProjectOverview = Field(
        default_factory=ProjectOverview
    )



    technology_stack: TechnologyStack = Field(
        default_factory=TechnologyStack
    )



    agents: list[AgentAnalysisResult] = Field(
        default_factory=list
    )



    workflow: dict[str, Any] = Field(
        default_factory=dict
    )



    skills: list[str] = Field(
        default_factory=list
    )



    tools: list[str] = Field(
        default_factory=list
    )



    rag: dict[str, Any] = Field(
        default_factory=dict
    )



    memory: dict[str, Any] = Field(
        default_factory=dict
    )



    database: dict[str, Any] = Field(
        default_factory=dict
    )



    evidence: list[Any] = Field(
        default_factory=list
    )