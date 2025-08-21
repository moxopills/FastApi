from enum import StrEnum

from pydantic_settings import BaseSettings


class Env(StrEnum):
    local = "local"
    stage = "stage"
    prod = "prod"


class Config(BaseSettings):
    env: Env = Env.local

    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "hjpsm21300"
    MYSQL_DB: str = "FastAPIProject"
    MYSQL_CONNECT_TIMEOUT: int = 5
    MYSQL_MAX_SIZE: int = 30
