import pytest
from datetime import datetime, timezone
from src.contracts.weather import WeatherSignal, WeatherMetrics, LocationRef
from src.contracts.risk import HazardType, SeverityLevel
from src.skills.apply_risk_matrix import apply_risk_matrix

@pytest.fixture
def base_location():
    return LocationRef(
        id="sao_paulo",
        city="São Paulo",
        state="SP",
        region="sudeste",
        latitude=-23.5505,
        longitude=-46.6333,
        timezone="America/Sao_Paulo"
    )

def test_apply_risk_matrix_no_hazard(base_location):
    metrics = WeatherMetrics(
        precipitation_mm_h=0.0,
        wind_gusts_10m_kmh=10.0,
        weather_code=0,
        cape_j_kg=0.0,
        lifted_index=0.0
    )
    signal = WeatherSignal(
        location=base_location,
        forecast_generated_at=datetime.now(timezone.utc),
        forecast_valid_from=datetime.now(timezone.utc),
        forecast_valid_until=datetime.now(timezone.utc),
        metrics=metrics
    )

    assessment = apply_risk_matrix(signal)
    assert assessment.hazard_type == HazardType.NO_HAZARD
    assert assessment.severity is None
    assert len(assessment.impacted_lines) == 0
