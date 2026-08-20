"""
MeteoRisco — Contrato: WeatherSignal

Saída do Scout Climático. Representa previsões meteorológicas normalizadas
obtidas da Open-Meteo. Usa semântica de PREVISÃO (forecast), não observação.

Campos temporais (v1.1 — semântica corrigida):
  - forecast_generated_at: quando a API foi consultada
  - forecast_valid_from:   início da janela temporal da previsão
  - forecast_valid_until:  fim da janela temporal da previsão
"""
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field


class LocationRef(BaseModel):
    """Referência à localidade-piloto conforme locations.yaml."""
    id: str = Field(description="Identificador único (ex: 'sao_paulo')")
    city: str = Field(description="Nome da cidade")
    state: str = Field(description="UF (ex: 'SP')")
    region: str = Field(description="Região brasileira")
    latitude: float
    longitude: float
    timezone: str


class WeatherMetrics(BaseModel):
    """
    Métricas meteorológicas fornecidas pela Open-Meteo.
    Todos os valores são PREVISTOS pelo modelo numérico (NWP), não observados.

    IMPORTANTE (decisão epistemológica do projeto):
    - weather_code WMO 96/99 indica POTENCIAL de granizo pelo modelo — não granizo observado.
    - cape e lifted_index são indicadores de convecção — inferência do MeteoRisco.
    """
    # Precipitação
    precipitation_mm_h: Optional[float] = Field(
        None, description="Precipitação prevista (mm/h)"
    )
    precipitation_probability_pct: Optional[float] = Field(
        None, description="Probabilidade de precipitação (%)"
    )

    # Vento
    wind_gusts_10m_kmh: Optional[float] = Field(
        None, description="Rajadas de vento a 10m (km/h)"
    )
    wind_speed_10m_kmh: Optional[float] = Field(
        None, description="Velocidade do vento a 10m (km/h)"
    )

    # Condição geral (WMO Weather Interpretation Codes)
    weather_code: Optional[int] = Field(
        None,
        description=(
            "Código WMO de condição climática prevista. "
            "95=tempestade, 96=tempestade c/ granizo leve, 99=tempestade c/ granizo forte. "
            "Classificação modelada, não observação direta de granizo."
        ),
    )

    # Termodinâmica (convecção)
    cape_j_kg: Optional[float] = Field(
        None,
        description="CAPE — Energia Potencial Convectiva Disponível (J/kg). Indicador de convecção.",
    )
    lifted_index: Optional[float] = Field(
        None,
        description="Lifted Index — valores negativos indicam instabilidade atmosférica.",
    )

    # Temperatura (contexto)
    temperature_2m_celsius: Optional[float] = Field(
        None, description="Temperatura a 2m (°C)"
    )


class WeatherSignal(BaseModel):
    """
    Contrato de saída do Scout Climático.
    Representa o sinal meteorológico normalizado para uma localidade e janela temporal.
    """
    location: LocationRef
    source: str = Field(default="open-meteo", description="Fonte dos dados meteorológicos")

    # Semântica temporal correta (v1.1)
    forecast_generated_at: datetime = Field(
        description="Momento em que a previsão foi obtida da API (quando consultamos)"
    )
    forecast_valid_from: datetime = Field(
        description="Início da janela temporal para a qual a previsão é válida"
    )
    forecast_valid_until: datetime = Field(
        description="Fim da janela temporal para a qual a previsão é válida"
    )

    metrics: WeatherMetrics = Field(
        description="Dados meteorológicos previstos pelo modelo numérico (NWP)"
    )

    # Modo de operação (transparência de fallback)
    is_fixture: bool = Field(
        default=False,
        description="True se os dados vêm de fixture estática (modo offline/fallback)",
    )
    raw_ref: Optional[Any] = Field(
        default=None,
        description="Referência opcional ao payload bruto da API (para auditoria)",
    )
