import pytest
from unittest.mock import patch, MagicMock
from src.skills.fetch_weather import fetch_weather, _load_fixture

def test_fetch_weather_fixture_mode():
    # Testa se no modo fixture ele carrega localmente sem fazer chamada HTTP
    with patch("src.skills.fetch_weather._load_fixture") as mock_load:
        mock_load.return_value = {"hourly": {}, "_is_fixture": True}
        result = fetch_weather("sao_paulo", -23.5505, -46.6333, "America/Sao_Paulo", force_fixture=True)
        assert result["_is_fixture"] is True
        mock_load.assert_called_once_with("sao_paulo")

@patch("httpx.Client")
def test_fetch_weather_live_mode_success(mock_client_class):
    # Mock do cliente httpx
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.json.return_value = {"hourly": {"temperature_2m": [20.0]}}
    mock_response.raise_for_status = MagicMock()
    mock_client.get.return_value = mock_response
    mock_client_class.return_value.__enter__.return_value = mock_client

    result = fetch_weather("sao_paulo", -23.5505, -46.6333, "America/Sao_Paulo", force_fixture=False)
    
    assert result["_is_fixture"] is False
    assert "hourly" in result
    assert result["hourly"]["temperature_2m"] == [20.0]

@patch("httpx.Client")
def test_fetch_weather_live_mode_fallback_on_error(mock_client_class):
    # Se der erro HTTP na chamada da API, deve acionar o fallback para fixture
    mock_client = MagicMock()
    mock_client.get.side_effect = Exception("API Timeout")
    mock_client_class.return_value.__enter__.return_value = mock_client

    with patch("src.skills.fetch_weather._load_fixture") as mock_load:
        mock_load.return_value = {"hourly": {}, "_is_fixture": True, "_fallback": True}
        result = fetch_weather("sao_paulo", -23.5505, -46.6333, "America/Sao_Paulo", force_fixture=False)
        assert result["_is_fixture"] is True
        assert result["_fallback"] is True
        mock_load.assert_called_once_with("sao_paulo", fallback=True)
