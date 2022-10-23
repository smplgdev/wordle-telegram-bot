from pydantic import SecretStr, BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    ADMINS: list
    PG_USERNAME: str
    PG_PASSWORD: str
    PG_DATABASE: str
    ip: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


config = Settings()
