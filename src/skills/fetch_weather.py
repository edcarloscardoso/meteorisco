"""
MeteoRisco — Skill: fetch_weather

Integração com a Open-Meteo Forecast API (https://open-meteo.com/).
Obtém previsões horárias para lat/lon de uma localidade-piloto.

Variáveis obtidas (confirmadas no Data Feasibility Study — 15/08/2026):
  - precipitation (mm/h)
  - wind_gusts_10m (km/h)
  - weather_code (WMO)
  - cape (J/kg) — indicador de convecção
  - lifted_index — instabilidade atmosférica
  - wind_speed_10m (km/h) — contexto
  - temperature_2m (°C) — contexto

FALLBACK: Se API indisponível ou modo fixture, carrega JSON do diretório fixtures/.
Determinístico (I/O externo). Testável com mock HTTP.
"""
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import httpx

from src.config import settings

logger = logging.getLogger(__name__)

# Variáveis horárias a solicitar à Open-Meteo
HOURLY_VARIABLES = [
    "precipitation",
    "wind_gusts_10m",
    "wind_speed_10m",
    "weather_code",
    "cape",
    "lifted_index",
    "temperature_2m",
    "precipitation_probability",
]

# Mapeamento location_id → nome do arquivo fixture
FIXTURE_MAP = {
    "belem": "open_meteo_belem.json",
    "recife": "open_meteo_recife.json",
    "brasilia": "open_meteo_brasilia.json",
    "sao_paulo": "open_meteo_sao_paulo.json",
    "porto_alegre": "open_meteo_porto_alegre.json",
}

EXTREME_FIXTURE_MAP = {
    "belem": "extreme_meteo_belem.json",
    "recife": "extreme_meteo_recife.json",
    "brasilia": "extreme_meteo_brasilia.json",
    "sao_paulo": "extreme_meteo_sao_paulo.json",
    "porto_alegre": "extreme_meteo_porto_alegre.json",
}


def fetch_weather(
    location_id: str,
    latitude: float,
    longitude: float,
    timezone_str: str,
    forecast_hours: Optional[int] = None,
    force_fixture: bool = False,
    force_extreme: bool = False,
) -> dict:
    """
    Obtém previsão meteorológica para a localidade informada.

    Args:
        location_id: ID da localidade (ex: 'sao_paulo') — usado para fallback fixture.
        latitude: Latitude da coordenada de referência.
        longitude: Longitude da coordenada de referência.
        timezone_str: Timezone IANA (ex: 'America/Sao_Paulo').
        forecast_hours: Horas de previsão (padrão: settings.forecast_hours).
        force_fixture: Se True, usa fixture offline (open_meteo_*.json).
        force_extreme: Se True, usa fixture extrema offline (extreme_meteo_*.json).

    Returns:
        Dict com o payload bruto da Open-Meteo (ou fixture equivalente).
        Inclui campo '_is_fixture' indicando a fonte.
    """
    hours = forecast_hours or settings.forecast_hours
    use_fixture = force_fixture or force_extreme or settings.weather_mode == "fixture"

    if use_fixture:
        logger.info(f"[fetch_weather] Modo FIXTURE (extreme={force_extreme}) para {location_id}")
        if force_extreme:
            return _load_fixture(location_id, extreme=True)
        return _load_fixture(location_id)

    try:
        payload = _call_open_meteo(latitude, longitude, timezone_str, hours)
        payload["_is_fixture"] = False
        payload["_fetched_at"] = datetime.now(timezone.utc).isoformat()
        logger.info(
            f"[fetch_weather] Open-Meteo OK para {location_id} "
            f"({hours}h de previsão)"
        )
        return payload
    except Exception as exc:
        logger.warning(
            f"[fetch_weather] API indisponível para {location_id}: {exc}. "
            f"Ativando fallback com fixture."
        )
        return _load_fixture(location_id, fallback=True)


def _call_open_meteo(
    latitude: float,
    longitude: float,
    timezone_str: str,
    forecast_hours: int,
) -> dict:
    """Realiza a chamada HTTP à Open-Meteo Forecast API."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ",".join(HOURLY_VARIABLES),
        "timezone": timezone_str,
        "forecast_hours": forecast_hours,
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm",
    }

    with httpx.Client(timeout=settings.open_meteo_timeout_seconds) as client:
        response = client.get(settings.open_meteo_base_url, params=params)
        response.raise_for_status()
        return response.json()


def _load_fixture(location_id: str, fallback: bool = False, extreme: bool = False) -> dict:
    """
    Carrega fixture estática para uma localidade.
    Raises FileNotFoundError se a fixture não existir.
    """
    fixture_map = EXTREME_FIXTURE_MAP if extreme else FIXTURE_MAP
    fixture_filename = fixture_map.get(location_id)
    if not fixture_filename:
        raise ValueError(
            f"Nenhuma fixture definida para '{location_id}'. "
            f"Fixtures disponíveis: {list(fixture_map.keys())}"
        )

    fixture_path = settings.fixtures_dir / fixture_filename
    if not fixture_path.exists():
        raise FileNotFoundError(
            f"Fixture não encontrada: {fixture_path}. "
            f"Execute scripts/capture_fixtures.py para capturar dados reais."
        )

    with fixture_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    data["_is_fixture"] = True
    data["_fallback"] = fallback
    data["_fetched_at"] = datetime.now(timezone.utc).isoformat()

    source = "fallback" if fallback else "fixture"
    logger.info(f"[fetch_weather] Usando {source}: {fixture_path.name}")
    return data
