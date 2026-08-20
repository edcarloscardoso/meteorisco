"""
MeteoRisco — Agente 2: Analista MeteoRisco

Missão: Transformar sinais meteorológicos (WeatherSignal) em avaliações
de risco securitário (RiskAssessment). Entrada → saída: WeatherSignal → RiskAssessment.

Skills permitidas: apply_risk_matrix (classify_hazard)
Skills proibidas: LLM para decisão de elegibilidade

Por que separado:
  A interpretação do evento no contexto de risco securitário é semanticamente
  distinta da aquisição dos dados. Thresholds, classificação e justificativa
  são responsabilidades de domínio, não de I/O.
"""
import logging
from datetime import datetime, timezone

from src.contracts.weather import WeatherSignal
from src.contracts.risk import RiskAssessment
from src.contracts.cycle import AgentTrace
from src.skills.apply_risk_matrix import apply_risk_matrix

logger = logging.getLogger(__name__)


class AnalistaMeteoRisco:
    """Agente responsável por classificar ameaças climáticas no contexto de risco."""

    NAME = "AnalistaMeteoRisco"

    def run(self, signal: WeatherSignal) -> tuple[RiskAssessment, AgentTrace]:
        """
        Classifica o WeatherSignal como RiskAssessment.

        Args:
            signal: WeatherSignal produzido pelo Scout.

        Returns:
            (RiskAssessment, AgentTrace)
        """
        t_start = datetime.now(timezone.utc)

        try:
            assessment = apply_risk_matrix(signal)

            t_end = datetime.now(timezone.utc)
            duration_ms = (t_end - t_start).total_seconds() * 1000

            has_hazard = assessment.has_hazard
            trace = AgentTrace(
                agent_name=self.NAME,
                t_start=t_start,
                t_end=t_end,
                duration_ms=duration_ms,
                status="ok",
                summary=(
                    f"Avaliação: hazard={assessment.hazard_type} | "
                    f"severity={assessment.severity} | "
                    f"ramos={assessment.impacted_lines}. "
                    f"{'⚠️ Evento relevante identificado.' if has_hazard else '✅ Nenhum evento relevante.'}"
                ),
            )

            logger.info(
                f"[{self.NAME}] OK | "
                f"hazard={assessment.hazard_type} | severity={assessment.severity}"
            )
            return assessment, trace

        except Exception as exc:
            t_end = datetime.now(timezone.utc)
            duration_ms = (t_end - t_start).total_seconds() * 1000
            logger.error(f"[{self.NAME}] ERRO: {exc}")

            trace = AgentTrace(
                agent_name=self.NAME,
                t_start=t_start,
                t_end=t_end,
                duration_ms=duration_ms,
                status="error",
                summary="Falha na classificação de risco",
                error=str(exc),
            )
            raise
