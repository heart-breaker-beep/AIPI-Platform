"""
MySQL Query Tool。

负责:
    - Agent 查询业务数据
    - 封装数据库访问能力
"""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.tools.base import BaseTool

class MySQLQueryTool(BaseTool):

    """
    MySQL 查询工具。

    Agent 不直接操作数据库。
    """
    name = "mysql_query"

    def __init__(
        self,
        session: AsyncSession
    ):

        self.session = session

    async def execute(
        self,
        sql: str,
        params: dict | None = None,
    ):


        """
        执行查询。
        Args:

            sql:
                SQL语句

            params:
                参数
        """


        try:

            result = await self.session.execute(
                text(sql),
                params or {}
            )


            rows = result.mappings().all()


            return [
                dict(row)
                for row in rows
            ]

        except Exception as e:

            raise RuntimeError(
                f"MySQL query failed: {e}"
            )