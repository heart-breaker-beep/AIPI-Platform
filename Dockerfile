# ============================================================
# AIPI Platform 运行时镜像
# ------------------------------------------------------------
# 构建：docker build -t aipi:latest .
# 启动：docker compose up -d   （见 docker-compose.yml）
#
# 镜像只跑应用本身；MySQL / Qdrant 由 compose 提供。
# ============================================================

FROM python:3.11-slim-bookworm


# ------------------------------------------------------------
# 运行环境
# ------------------------------------------------------------
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TZ=Asia/Shanghai

WORKDIR /app


# ------------------------------------------------------------
# 系统依赖
# ------------------------------------------------------------
#   build-essential —— asyncmy 等 C 扩展没有匹配 wheel 时兜底编译，
#                      装完即卸，不留在最终镜像里
#   curl            —— 容器 healthcheck 用
#   tzdata          —— 上面设的 TZ 需要它，否则忽略
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      curl \
      tzdata \
 && rm -rf /var/lib/apt/lists/*


# ------------------------------------------------------------
# Python 依赖
# ------------------------------------------------------------
# 先只拷依赖清单：源码改动不会让这一层缓存失效，
# 重建时能省掉整轮 pip install。
COPY requirements.docker.txt ./

RUN pip install --upgrade pip \
 && pip install -r requirements.docker.txt \
 && apt-get purge -y --auto-remove build-essential \
 && rm -rf /var/lib/apt/lists/*


# ------------------------------------------------------------
# 应用代码
# ------------------------------------------------------------
COPY alembic.ini ./
COPY alembic ./alembic
COPY app ./app


# ------------------------------------------------------------
# 启动脚本
# ------------------------------------------------------------
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh


# ------------------------------------------------------------
# 非 root 运行
# ------------------------------------------------------------
# 报告输出目录要跟着一起建好并授权，
# 否则挂载卷时容器内用户写不进去。
RUN groupadd --gid 1000 aipi \
 && useradd --uid 1000 --gid 1000 --create-home aipi \
 && mkdir -p /app/reports /app/test_reports \
 && chown -R aipi:aipi /app

USER aipi


# ------------------------------------------------------------
# 端口与健康检查
# ------------------------------------------------------------
EXPOSE 8000

# /health 只读配置、不碰数据库，用它探活不会误判。
HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=4 \
  CMD curl -fsS http://127.0.0.1:8000/health || exit 1


ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
