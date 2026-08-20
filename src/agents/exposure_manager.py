"""
MeteoRisco — Agente 3: Gestor de Exposição

Missão: Cruzar o RiskAssessment com a carteira sintética e regras de
negócio para selecionar segurados elegíveis. Entrada → saída: RiskAssessment → AudienceSelection.

Skills permitidas: select_insureds, apply_risk_matrix (regras de supressão)
Skills proibidas: LLM — elegibilidade é SEMPRE determinística

Por que separado:
  Elegibilidade é uma decisão de negócio determinística e não deve ficar
  escondida em prompt de LLM. Essa separação garante auditabilidade e testabilidade.
  [DECISÃO TOMADA] Nunca permitir que LLM substitua a matriz determinística de elegibilidade.
"""
import logging
from datetime import datetime, timezone

from src.contracts.risk import RiskAssessment
from src.contracts.audience import AudienceSelection
from src.contracts.cycle import AgentTrace
from src.skills.select_insureds import select_insureds

logger = logging.getLogger(__name__)


class GestorDeExposicao:
    """Agente responsável por selecionar segurados elegíveis com regras determinísticas."""

    NAME = "GestorDeExposição"

    def run(
        self, risk: RiskAssessment, location_id: str
    ) -> tuple[AudienceSelection, AgentTrace]:
        """
        Seleciona segurados elegíveis para o ciclo preventivo.

        Args:
            risk: RiskAssessment do Analista.
            location_id: ID da localidade do ciclo.

        Returns:
            (AudienceSelection, AgentTrace)
        """
        t_start = datetime.now(timezone.utc)

        try:
            selection = select_insureds(risk=risk, location_id=location_id)

            t_end = datetime.now(timezone.utc)
            duration_ms = (t_end - t_start).total_seconds() * 1000

            trace = AgentTrace(
                agent_name=self.NAME,
                t_start=t_start,
                t_end=t_end,
                duration_ms=duration_ms,
                status="ok",
                summary=(
                    f"Seleção completa: {selection.total_eligible} elegíveis | "
                    f"{selection.total_suppressed} suprimidos. "
                    f"Regras aplicadas: {selection.applied_matrix_rules}"
                ),
            )

            logger.info(
                f"[{self.NAME}] OK | "
                f"elegíveis={selection.total_eligible} | suprimidos={selection.total_suppressed}"
            )
            return selection, trace

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
                summary="Falha na seleção de segurados",
                error=str(exc),
            )
            raise
