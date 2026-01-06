import os
from dataclasses import dataclass

@dataclass
class AppConfig:
    app_name: str
    app_version: str
    env: str

    @property
    def is_dev(self) -> bool:
        return self.env == "dev"


def load_config() -> AppConfig:
    # Example:
    # postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/basic_service
    database_url = os.getenv("DATABASE_URL", "")

    if not database_url:
        raise RuntimeError("DATABASE_URL is required")    

    return AppConfig(
        app_name=os.getenv("APP_NAME", "basic-service"),
        app_version=os.getenv("APP_VERSION", "0.0.0"),
        env=os.getenv("ENV", "prod"),
        database_url=database_url,
    )


APP_CONFIG = load_config()
