from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Config(BaseSettings):
    app_name: str
    host: str
    port: int
    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str
    token_secret_key: str
    token_algorithm: str
    token_expiration_in_minutes: int
    queue_url: str
    queue_region: str
    

    model_config = SettingsConfigDict(env_file=f"{os.getcwd()}/.env")
    