from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class SystemSettings(BaseSettings):
    SECRET_KEY: str = Field(validation_alias="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    GOOGLE_CLIENT_ID:str = Field(validation_alias="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET:str = Field(validation_alias="GOOGLE_CLIENT_SECRET")

    DB_URL: str = Field(validation_alias="DB_URL")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = SystemSettings()  # type: ignore
# TODO: Check for this later
