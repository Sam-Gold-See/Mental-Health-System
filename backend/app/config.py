import os

from pydantic import Field
import pydantic_settings
from pydantic import SecretStr


class Config(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env.development"
        if os.getenv("ENV", "dev") == "dev"
        else ".env.production"
    )

    # 数据库配置
    DB_URL: str = Field(...)

    # JWT配置
    JWT_SECRET_KEY: SecretStr = Field(...)
    JWT_ALGORITHM: str = Field(...)
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(...)
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(...)


# 创建配置实例
config = Config()
