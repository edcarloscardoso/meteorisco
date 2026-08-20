import pytest
from datetime import datetime, timezone
from src.skills.normalize_weather import normalize_weather
from src.contracts.weather import WeatherSignal

def test_normalize_weather_worst_case():
    raw_payload = {
        "hourly": {
            "time": ["2026-08-18T20:00", "2026-08-18T21:00", "2026-08-18T22:00"],
            "precipitation": [0.0, 15.0, 5.0],
            "precipitation_probability": [10, 90, 40],
            "wind_gusts_10m": [15.0, 45.0, 65.0],
            "wind_speed_10m": [10.0, 20.0, 30.0],
            "weather_code": [0, 95, 96],
            "cape": [100.0, 1500.0, 2500.0],
            "lifted_index": [0.0, -4.0, -8.0],
            "temperature_2m": [22.0, 18.0, 16.0]
        },
        "_is_fixture": False,
        "_fetched_at": "2026-08-18T19:50:00+00:00"
    }

    location = {
        "id": "sao_paulo",
        "city": "São Paulo",
        "state": "SP",
        "region": "sudeste",
        "latitude": -23.5505,
        "longitude": -46.6333,
        "timezone": "America/Sao_Paulo"
    }

    signal = normalize_weather(raw_payload, location, forecast_window_hours=3)

    assert isinstance(signal, WeatherSignal)
    assert signal.location.id == "sao_paulo"
    assert signal.metrics.precipitation_mm_h == 15.0  # max precipitation
    assert signal.metrics.wind_gusts_10m_kmh == 65.0   # max wind gusts
    assert signal.metrics.weather_code == 96            # worst weather_code
    assert signal.metrics.cape_j_kg == 2500.0          # max cape
    assert signal.metrics.lifted_index == -8.0          # min lifted_index
    assert signal.forecast_generated_at == datetime.fromisoformat("2026-08-18T19:50:00+00:00")
