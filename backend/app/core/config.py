from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="")
    SUPABASE_JWT_SECRET: str = Field(default="")
    ANTHROPIC_API_KEY: str = Field(default="")
    ABSTRACT_API_KEY: str = Field(default="")
    RESEND_API_KEY: str = Field(default="")
    FROM_EMAIL: str = Field(default="onboarding@resend.dev")
    SUPABASE_URL: str = Field(default="")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
