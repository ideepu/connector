from src.config import Config
from tests import conftest


class TestConfig:
    def test_init(self):
        config = Config()
        assert config.API_KEY.get_secret_value() == conftest.TEST_API_KEY
        assert config.BASE_URL == conftest.TEST_BASE_URL
        assert config.BASE_URL_PREFIX == conftest.TEST_BASE_URL_PREFIX
