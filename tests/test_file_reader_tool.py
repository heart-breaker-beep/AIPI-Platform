"""
FileReaderTool 测试。

覆盖：

1. httpx 超时转换为带 URL 的 ToolError
2. 其他 httpx 错误同样转换为 ToolError
3. 保持 404 → master fallback 的既有行为
4. 保持正常读取行为
"""

import httpx
import pytest

from app.core.exceptions import ToolError
from app.tools.file_reader_tool import (
    FileReaderTool,
)


BASE = "https://raw.githubusercontent.com"

EXPECTED_MAIN = (
    f"{BASE}/openai/openai-python/"
    "main/requirements.txt"
)

EXPECTED_MASTER = (
    f"{BASE}/openai/openai-python/"
    "master/requirements.txt"
)


class FakeResponse:
    """最小可用的 httpx Response 替身。"""

    def __init__(
        self,
        status_code,
        text="",
    ):

        self.status_code = status_code

        self.text = text


class FakeAsyncClient:
    """
    假 httpx.AsyncClient。

    支持两种模式：

    - error 不为 None：get() 直接抛异常
    - 否则按 responses 顺序返回
    """

    def __init__(
        self,
        responses=None,
        error=None,
    ):

        self.responses = list(
            responses or []
        )

        self.error = error

        self.urls = []

    async def __aenter__(self):

        return self

    async def __aexit__(
        self,
        *exc_info,
    ):

        return False

    async def get(
        self,
        url,
        timeout=None,
    ):

        self.urls.append(url)

        if self.error is not None:

            raise self.error

        if not self.responses:

            return FakeResponse(404)

        return self.responses.pop(0)


def install_client(
    monkeypatch,
    client,
):
    """把假 Client 注入 FileReaderTool 使用的 httpx 模块。"""

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda *args, **kwargs: client,
    )

    return client


@pytest.mark.asyncio
async def test_timeout_is_converted_to_tool_error(
    monkeypatch,
):
    """
    httpx.ReadTimeout 必须转换成 ToolError，
    并且错误信息包含 URL。

    httpx.ReadTimeout('') 的 str() 为空字符串，
    直接向上抛出会产生 errors == [""]。
    """

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            error=httpx.ReadTimeout("")
        ),
    )

    with pytest.raises(ToolError) as excinfo:

        await FileReaderTool().execute(
            owner="openai",
            name="openai-python",
            file_path="requirements.txt",
        )

    message = str(excinfo.value)

    assert "Read timeout" in message

    assert EXPECTED_MAIN in message

    assert message.strip() != ""

    assert client.urls == [EXPECTED_MAIN]


@pytest.mark.asyncio
async def test_connect_error_is_converted_to_tool_error(
    monkeypatch,
):
    """非超时的 httpx 错误同样转换成 ToolError。"""

    install_client(
        monkeypatch,
        FakeAsyncClient(
            error=httpx.ConnectError(
                "connection refused"
            )
        ),
    )

    with pytest.raises(ToolError) as excinfo:

        await FileReaderTool().execute(
            owner="openai",
            name="openai-python",
            file_path="requirements.txt",
        )

    message = str(excinfo.value)

    assert "Read failed" in message

    assert EXPECTED_MAIN in message

    assert "connection refused" in message


@pytest.mark.asyncio
async def test_404_on_main_falls_back_to_master(
    monkeypatch,
):
    """main 返回 404 时回退 master，两者都 404 则返回空字符串。"""

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            responses=[
                FakeResponse(404),
                FakeResponse(404),
            ]
        ),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
    )

    assert result == ""

    assert client.urls == [
        EXPECTED_MAIN,
        EXPECTED_MASTER,
    ]


@pytest.mark.asyncio
async def test_404_on_master_returns_empty_without_retry(
    monkeypatch,
):
    """分支已经是 master 时不再回退，直接返回空字符串。"""

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            responses=[
                FakeResponse(404),
            ]
        ),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
        branch="master",
    )

    assert result == ""

    assert client.urls == [EXPECTED_MASTER]


@pytest.mark.asyncio
async def test_master_fallback_success(
    monkeypatch,
):
    """main 404 但 master 命中时返回 master 内容。"""

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            responses=[
                FakeResponse(404),
                FakeResponse(
                    200,
                    "fastapi==0.1.0",
                ),
            ]
        ),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
    )

    assert result == "fastapi==0.1.0"

    assert client.urls == [
        EXPECTED_MAIN,
        EXPECTED_MASTER,
    ]


@pytest.mark.asyncio
async def test_success_returns_text_unchanged(
    monkeypatch,
):
    """200 时原样返回文本，且不回退 master。"""

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            responses=[
                FakeResponse(
                    200,
                    "fastapi==0.1.0",
                ),
            ]
        ),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
    )

    assert result == "fastapi==0.1.0"

    assert client.urls == [EXPECTED_MAIN]
