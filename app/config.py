from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_host: str
    database_user: str
    database_password: str
    database_port: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file="../.env",     # from app/ to FastAPI/.env
        env_file_encoding="utf-8",
        extra="ignore",
    )

vars = Settings()