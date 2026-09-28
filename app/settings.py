from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    gemini_api_key: str = ""
    gemini_flash_model: str = "gemini-3.8-flash"
    gemini_pro_model: str = "gemini-2.5-pro"

    image_provider: str = "placeholder"
    image_model: str = "stable-diffusion-v1-5/stable-diffusion-v1-5"
    image_device: str = "auto"
    image_steps: int = 20

    gemini_image_model: str = "gemini-3.1-flash-image"
    hf_token: str = ""

    max_panels: int = 5
    max_prompt_length: int = 2000

    cors_origins: str = "*"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )

    @property
    def static_dir(self) -> Path:
        return BASE_DIR / "static"

    @property
    def panels_dir(self) -> Path:
        return self.static_dir / "panels"

    @property
    def exports_dir(self) -> Path:
        return self.static_dir / "exports"

    @property
    def templates_dir(self) -> Path:
        return BASE_DIR / "templates"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()