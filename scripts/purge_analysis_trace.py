"""Delete only expired trace events for ended runs; keep reports and stream metadata."""

import argparse
import asyncio

from app.persistence.repositories.analysis_trace import AnalysisTraceRepository
from app.persistence.session import AsyncSessionLocal, engine


async def main(days):
    try:
        await AnalysisTraceRepository(AsyncSessionLocal).purge(days)
        print(f"Trace events for ended runs older than {days} days cleaned.")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=30)
    args = parser.parse_args()
    if args.days < 1:
        parser.error("--days must be at least 1")
    asyncio.run(main(args.days))
