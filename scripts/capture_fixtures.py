"""
MeteoRisco — Script de Captura de Fixtures

Este script faz chamadas reais à Open-Meteo Forecast API para as 5 cidades-piloto
e salva os dados brutos em fixtures/.

Para permitir testes consistentes de eventos extremos (chuva severa, vento forte e granizo),
o script cria duas versões por localidade:
  1. open_meteo_{cidade}.json: dados reais atuais da API.
  2. extreme_meteo_{cidade}.json: dados modificados artificialmente com valores severos
     (ex: precipitação > 20mm/h, ventos > 80km/h, WMO 99, CAPE > 2000 J/kg)
     para testar as regras determinísticas e evals de risco sem depender do clima real do dia.
"""
import os
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
import httpx

# Configuração simples de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configurações do piloto (do locations.yaml)
CITIES = {
    "belem": {"lat": -1.4558, "lon": -48.4902, "tz": "America/Belem"},
    "recife": {"lat": -8.0476, "lon": -34.8770, "tz": "America/Recife"},
    "brasilia": {"lat": -15.7975, "lon": -47.8919, "tz": "America/Sao_Paulo"},
    "sao_paulo": {"lat": -23.5505, "lon": -46.6333, "tz": "America/Sao_Paulo"},
    "porto_alegre": {"lat": -30.0346, "lon": -51.2177, "tz": "America/Sao_Paulo"},
}

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

def fetch_and_save():
    fixtures_dir = Path(__file__).parent.parent / "fixtures"
    fixtures_dir.mkdir(exist_ok=True)

    url = "https://api.open-meteo.com/v1/forecast"

    with httpx.Client(timeout=30) as client:
        for city_id, info in CITIES.items():
            params = {
                "latitude": info["lat"],
                "longitude": info["lon"],
                "hourly": ",".join(HOURLY_VARIABLES),
                "timezone": info["tz"],
                "forecast_hours": 48,
                "wind_speed_unit": "kmh",
                "precipitation_unit": "mm",
            }
            
            try:
                logger.info(f"Fazendo chamada para {city_id}...")
                response = client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                # Salvar real
                real_file = fixtures_dir / f"open_meteo_{city_id}.json"
                with real_file.open("w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                logger.info(f"Fixture real salva: {real_file.name}")
                
                # Gerar extremo para teste
                extreme_data = generate_extreme_data(data, city_id)
                extreme_file = fixtures_dir / f"extreme_meteo_{city_id}.json"
                with extreme_file.open("w", encoding="utf-8") as f:
                    json.dump(extreme_data, f, indent=2, ensure_ascii=False)
                logger.info(f"Fixture extrema salva: {extreme_file.name}")
                
            except Exception as exc:
                logger.error(f"Erro ao capturar dados de {city_id}: {exc}")

def generate_extreme_data(base_data: dict, city_id: str) -> dict:
    """Gera uma cópia dos dados com picos severos no início do forecast (horas 3 a 6)."""
    import copy
    data = copy.deepcopy(base_data)
    hourly = data.get("hourly", {})
    
    # Injetar pico de tempestade severa / granizo / vento forte
    # Belo pico de 5h a 8h do forecast
    limit = len(hourly.get("time", []))
    for idx in range(min(3, limit), min(8, limit)):
        # Configurar cenários dependendo do tipo desejado de teste
        if city_id == "sao_paulo":
            # Granizo + Vento forte em SP
            hourly["precipitation"][idx] = 18.5
            hourly["wind_gusts_10m"][idx] = 75.0
            hourly["weather_code"][idx] = 99  # Tempestade severa com granizo forte
            hourly["cape"][idx] = 2200.0      # Altamente instável
            hourly["lifted_index"][idx] = -6.5
        elif city_id == "porto_alegre":
            # Tempestade/Vento muito severo no Sul
            hourly["precipitation"][idx] = 12.0
            hourly["wind_gusts_10m"][idx] = 95.0 # Vendaval severo
            hourly["weather_code"][idx] = 95  # Tempestade sem granizo
            hourly["cape"][idx] = 1500.0
            hourly["lifted_index"][idx] = -4.0
        elif city_id == "belem":
            # Chuva equatorial convectiva massiva
            hourly["precipitation"][idx] = 35.0  # Alagamento repentino
            hourly["wind_gusts_10m"][idx] = 45.0
            hourly["weather_code"][idx] = 96  # Tempestade com granizo leve
            hourly["cape"][idx] = 2800.0
            hourly["lifted_index"][idx] = -8.0
        else:
            # Padrão chuva laranja
            hourly["precipitation"][idx] = 15.0
            hourly["wind_gusts_10m"][idx] = 60.0
            hourly["weather_code"][idx] = 95
            hourly["cape"][idx] = 1000.0
            hourly["lifted_index"][idx] = -3.0
            
    return data

if __name__ == "__main__":
    fetch_and_save()
