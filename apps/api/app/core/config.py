from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Market Bias Intelligence System API"
    environment: str = Field(default="dev")
    db_url: str = Field(default="postgresql+psycopg://postgres:postgres@localhost:5432/mbis")
    redis_url: str = Field(default="redis://localhost:6379/0")
    market_data_provider: str = Field(default="mock")
    news_provider: str = Field(default="mock")
    calendar_provider: str = Field(default="mock")


settings = Settings()
