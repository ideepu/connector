from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    API_KEY: SecretStr
    BASE_URL: str = Field(default='https://sultek.data-in-stage.funnel.io', max_length=2083)
    BASE_URL_PREFIX: str = Field(default='/demo')


config = Config()
