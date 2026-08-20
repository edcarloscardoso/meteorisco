"""
MeteoRisco — Skill: normalize_weather

Transforma o payload bruto da Open-Meteo em WeatherSignal normalizado.
Aplica lógica de agregação da janela de previsão (pior caso nas próximas N horas).

DECISÃO TÉCNICA:
- Semântica temporal correta (v1.1): forecast_generated_at ≠ forecast_valid_from.
- Extrai o PIOR CASO da janela de previsão configurada (max precipitation, max gusts, etc.).
- Preserva distinção entre dados fornecidos pela API e inferências do MeteoRisco.

Determinístico. Testável unitariamente sem LLM e sem HTTP.
"""
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

from src.contracts.weather import WeatherSignal, WeatherMetrics, LocationRef

logger = logging.getLogger(__name__)


def normalize_weather(
    raw_payload: dict,
    location: dict,
    forecast_window_hours: int = 24,
) -> WeatherSignal:
    """
    Normaliza o payload bruto da Open-Meteo em WeatherSignal.

    Estratégia de agregação: extrai o PIOR CASO (máximo de risco)
    dentro da janela de previsão especificada (próximas N horas).
    Isso garante que o pipeline alerta para o pico de severidade previsto.

    Args:
        raw_payload: Dict retornado por fetch_weather.
        location: Dict da localidade conforme locations.yaml.
        forecast_window_hours: Horas de previsão a considerar (padrão: 24h).

    Returns:
        WeatherSignal com campos temporais corretos e métricas normalizadas.
    """
    is_fixture = raw_payload.get("_is_fixture", False)
    fetched_at_str = raw_payload.get("_fetched_at")

    forecast_generated_at = (
        datetime.fromisoformat(fetched_at_str)
        if fetched_at_str
        else datetime.now(timezone.utc)
    )
    # Garantir timezone awareness
    if forecast_generated_at.tzinfo is None:
        forecast_generated_at = forecast_generated_at.replace(tzinfo=timezone.utc)

    forecast_valid_from = forecast_generated_at
    forecast_valid_until = forecast_generated_at + timedelta(hours=forecast_window_hours)

    hourly = raw_payload.get("hourly", {})
    metrics = _aggregate_worst_case(hourly, forecast_window_hours)

    location_ref = LocationRef(
        id=location["id"],
        city=location["city"],
        state=location["state"],
        region=location["region"],
        latitude=location["latitude"],
        longitude=location["longitude"],
        timezone=location["timezone"],
    )

    signal = WeatherSignal(
        location=location_ref,
        source="open-meteo",
        forecast_generated_at=forecast_generated_at,
        forecast_valid_from=forecast_valid_from,
        forecast_valid_until=forecast_valid_until,
        metrics=metrics,
        is_fixture=is_fixture,
    )

    logger.debug(
        f"[normalize_weather] {location['id']} | "
        f"chuva={metrics.precipitation_mm_h}mm/h | "
        f"rajadas={metrics.wind_gusts_10m_kmh}km/h | "
        f"wmo={metrics.weather_code} | "
        f"cape={metrics.cape_j_kg}J/kg | "
        f"janela={forecast_window_hours}h | fixture={is_fixture}"
    )

    return signal


def _aggregate_worst_case(hourly: dict, window_hours: int) -> WeatherMetrics:
    """
    Extrai o pior caso (máximo de risco) nas primeiras 'window_hours' do forecast.
    Retorna WeatherMetrics com os valores de pico.
    """
    # Limita ao número de horas da janela
    limit = min(window_hours, len(hourly.get("time", [])))

    def safe_max(key: str) -> Optional[float]:
        """Retorna o máximo de uma série, ignorando None."""
        values = hourly.get(key, [])[:limit]
        valid = [v for v in values if v is not None]
        return max(valid) if valid else None

    def safe_min(key: str) -> Optional[float]:
        """Retorna o mínimo de uma série, ignorando None."""
        values = hourly.get(key, [])[:limit]
        valid = [v for v in values if v is not None]
        return min(valid) if valid else None

    def worst_weather_code(key: str = "weather_code") -> Optional[int]:
        """
        Retorna o código WMO mais severo da janela.
        Maior código = condição mais severa na escala WMO.
        """
        values = hourly.get(key, [])[:limit]
        valid = [int(v) for v in values if v is not None]
        return max(valid) if valid else None

    return WeatherMetrics(
        precipitation_mm_h=safe_max("precipitation"),
        precipitation_probability_pct=safe_max("precipitation_probability"),
        wind_gusts_10m_kmh=safe_max("wind_gusts_10m"),
        wind_speed_10m_kmh=safe_max("wind_speed_10m"),
        weather_code=worst_weather_code("weather_code"),
        cape_j_kg=safe_max("cape"),
        lifted_index=safe_min("lifted_index"),  # Mais negativo = mais instável
        temperature_2m_celsius=safe_max("temperature_2m"),
    )
