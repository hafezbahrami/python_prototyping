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
    return AppConfig(
        app_name=os.getenv("APP_NAME", "basic-service"),
        app_version=os.getenv("APP_VERSION", "0.0.0"),
        env=os.getenv("ENV", "prod"),
    )


APP_CONFIG = load_config()
