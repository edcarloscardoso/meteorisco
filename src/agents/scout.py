"""
MeteoRisco — Agente 1: Scout Climático

Missão: Obter e normalizar previsões meteorológicas da Open-Meteo para
uma localidade-piloto. Entrada → saída: Localidade → WeatherSignal.

Skills permitidas: fetch_weather, normalize_weather
Skills proibidas: LLM (I/O externo não passa por LLM)

Por que separado:
  I/O externo, normalização, tratamento de falhas e fallback possuem
  responsabilidade própria. A aquisição do dado não deve estar misturada
  à interpretação do risco.
"""
import logging
from datetime import datetime, timezone

from src.contracts.weather import WeatherSignal
from src.contracts.cycle import AgentTrace
from src.skills.fetch_weather import fetch_weather
from src.skills.normalize_weather import normalize_weather
from src.skills.load_domain import get_location_by_id
from src.config import settings

logger = logging.getLogger(__name__)


class ScoutClimatico:
    """Agente responsável por obter e normalizar o sinal meteorológico."""

    NAME = "ScoutClimático"

    def run(
        self,
        location_id: str,
        force_fixture: bool = False,
    ) -> tuple[WeatherSignal, AgentTrace]:
        """
        Executa o Scout para a localidade informada.

        Args:
            location_id: ID da localidade-piloto (ex: 'sao_paulo').
            force_fixture: Força uso de fixture offline.

        Returns:
            (WeatherSignal, AgentTrace) — sinal normalizado + trace de execução.
        """
        t_start = datetime.now(timezone.utc)
        is_fallback = False

        try:
            # Carrega configuração da localidade
            location = get_location_by_id(location_id)

            # Obtém previsão (live ou fixture)
            raw = fetch_weather(
                location_id=location_id,
                latitude=location["latitude"],
                longitude=location["longitude"],
                timezone_str=location["timezone"],
                force_fixture=force_fixture,
            )

            is_fallback = raw.get("_is_fixture", False)

            # Normaliza em WeatherSignal
            signal = normalize_weather(
                raw_payload=raw,
                location=location,
                forecast_window_hours=settings.forecast_hours,
            )

            t_end = datetime.now(timezone.utc)
            duration_ms = (t_end - t_start).total_seconds() * 1000

            trace = AgentTrace(
                agent_name=self.NAME,
                t_start=t_start,
                t_end=t_end,
                duration_ms=duration_ms,
                status="ok",
                summary=(
                    f"Previsão obtida para {location['city']}/{location['state']} "
                    f"({'fixture' if is_fallback else 'API real'}). "
                    f"Pico: chuva={signal.metrics.precipitation_mm_h}mm/h, "
                    f"rajadas={signal.metrics.wind_gusts_10m_kmh}km/h, "
                    f"WMO={signal.metrics.weather_code}, "
                    f"CAPE={signal.metrics.cape_j_kg}J/kg"
                ),
                is_fallback=is_fallback,
            )

            logger.info(f"[{self.NAME}] OK | {location_id} | fixture={is_fallback}")
            return signal, trace

        except Exception as exc:
            t_end = datetime.now(timezone.utc)
            duration_ms = (t_end - t_start).total_seconds() * 1000
            logger.error(f"[{self.NAME}] ERRO | {location_id}: {exc}")

            trace = AgentTrace(
                agent_name=self.NAME,
                t_start=t_start,
                t_end=t_end,
                duration_ms=duration_ms,
                status="error",
                summary=f"Falha ao obter previsão para {location_id}",
                error=str(exc),
                is_fallback=True,
            )
            raise
