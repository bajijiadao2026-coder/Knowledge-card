from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    coze_api_token: str = ""
    coze_workflow_id: str = ""

    kimi_api_key: str = ""
    claude_api_key: str = ""

    database_url: str = "sqlite:///./knowledge_cards.db"
    app_secret_key: str = "change-me"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
