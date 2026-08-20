"""
MeteoRisco — Configurações via pydantic-settings

Carrega variáveis do .env automaticamente.
Uso: from src.config.settings import settings
"""
from pathlib import Path
from typing import Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ─── LLM ──────────────────────────────────────────────────────────────────
    llm_provider: Optional[str] = Field(
        default=None,
        description="Provedor LLM: 'gemini' | 'openai' | 'anthropic'. Pendente aprovação do grupo.",
    )
    gemini_api_key: Optional[str] = Field(default=None)
    openai_api_key: Optional[str] = Field(default=None)
    anthropic_api_key: Optional[str] = Field(default=None)
    llm_model: Optional[str] = Field(
        default=None,
        description="Nome do modelo LLM. Ex: 'gemini-2.0-flash', 'gpt-4o-mini'.",
    )

    # ─── Open-Meteo ───────────────────────────────────────────────────────────
    open_meteo_base_url: str = Field(
        default="https://api.open-meteo.com/v1/forecast"
    )
    open_meteo_timeout_seconds: int = Field(default=30)

    # ─── Pipeline ─────────────────────────────────────────────────────────────
    weather_mode: str = Field(
        default="live",
        description="'live' usa API real; 'fixture' usa dados offline",
    )
    forecast_hours: int = Field(
        default=48,
        description="Janela de previsão em horas (máx 384 = 16 dias)",
    )

    # ─── Paths ────────────────────────────────────────────────────────────────
    domain_dir: Path = Field(default=Path("domain"))
    fixtures_dir: Path = Field(default=Path("fixtures"))
    traces_dir: Path = Field(default=Path("traces"))

    # ─── Logging ──────────────────────────────────────────────────────────────
    log_level: str = Field(default="INFO")

    @property
    def llm_api_key(self) -> Optional[str]:
        """Retorna a API key do provider configurado."""
        if self.llm_provider == "gemini":
            return self.gemini_api_key
        elif self.llm_provider == "openai":
            return self.openai_api_key
        elif self.llm_provider == "anthropic":
            return self.anthropic_api_key
        return None

    @property
    def has_llm(self) -> bool:
        """True se o provider LLM está configurado."""
        return bool(self.llm_provider and self.llm_api_key)


# Singleton — importe este objeto diretamente
settings = Settings()
