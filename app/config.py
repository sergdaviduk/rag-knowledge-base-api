from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/rag"
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4.1-mini"
    embedding_dimensions: int = 1536
    top_k: int = 5

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
