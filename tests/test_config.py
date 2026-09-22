"""配置模块测试。"""

from app.core.config import get_settings


def test_settings_load():
    """测试配置是否能够正常加载。"""

    settings = get_settings()

    assert settings.APP_NAME
    assert settings.APP_ENV
    assert settings.LLM_PROVIDER