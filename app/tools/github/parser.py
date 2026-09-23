"""GitHub Repository URL 解析工具。"""

from urllib.parse import urlparse


def parse_github_url(url: str) -> tuple[str, str]:
    """解析 GitHub URL，返回 owner 和 repository name。"""

    parsed = urlparse(url)

    if parsed.netloc.lower() != "github.com":
        raise ValueError("只支持 GitHub Repository URL")

    parts = [
        part
        for part in parsed.path.strip("/").split("/")
        if part
    ]

    if len(parts) < 2:
        raise ValueError("无效的 GitHub Repository URL")

    owner = parts[0]
    name = parts[1]

    if name.endswith(".git"):
        name = name[:-4]

    return owner, name