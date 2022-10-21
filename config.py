from pydantic import SecretStr, BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


config = Settings()
