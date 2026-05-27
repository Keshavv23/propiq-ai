from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    supabase_url: str
    supabase_anon_key: str
    supabase_service_key: str
    groq_api_key: str
    telegram_bot_token: str
    resend_api_key: str
    chroma_persist_path: str = "./chroma_store"

    class Config:
        env_file = ".env"

settings = Settings()