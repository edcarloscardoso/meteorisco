"""
MeteoRisco — Agente 4: Redator Preventivo

Missão: Transformar a decisão de comunicação (AudienceSelection) em mensagens
personalizadas e acionáveis (MessageDraft[]). Entrada → saída: AudienceSelection → MessageDraft[].

Skills permitidas: draft_message (usa LLM + playbook)
Skills proibidas: Decisões de elegibilidade (responsabilidade do Gestor)

Por que separado:
  É a etapa em que LLM agrega maior valor — geração de linguagem personalizada.
  A geração de comunicação não pode ser confundida com a decisão de quem recebe.
  O Redator não sabe POR QUE alguém foi selecionado — apenas COMO comunicar.
"""
import logging
from datetime import datetime, timezone

from src.contracts.risk import RiskAssessment
from src.contracts.audience import AudienceSelection
from src.contracts.message import MessageDraft
from src.contracts.cycle import AgentTrace
from src.skills.draft_message import draft_message

logger = logging.getLogger(__name__)


class RedatorPreventivo:
    """Agente responsável por gerar mensagens preventivas personalizadas via LLM."""

    NAME = "RedatorPreventivo"

    def run(
        self,
        selection: AudienceSelection,
        risk: RiskAssessment,
    ) -> tuple[list[MessageDraft], AgentTrace]:
        """
        Gera uma mensagem para cada segurado elegível na AudienceSelection.

        Args:
            selection: AudienceSelection do Gestor.
            risk: RiskAssessment para contexto de severidade e evento.

        Returns:
            (list[MessageDraft], AgentTrace)
        """
        t_start = datetime.now(timezone.utc)

        try:
            drafts = []
            fallback_count = 0

            for item in selection.items:
                draft = draft_message(audience_item=item, risk=risk)
                drafts.append(draft)
                if draft.model_meta and draft.model_meta.is_fallback:
                    fallback_count += 1

            t_end = datetime.now(timezone.utc)
            duration_ms = (t_end - t_start).total_seconds() * 1000

            llm_count = len(drafts) - fallback_count
            trace = AgentTrace(
                agent_name=self.NAME,
                t_start=t_start,
                t_end=t_end,
                duration_ms=duration_ms,
                status="ok",
                summary=(
                    f"{len(drafts)} mensagens geradas | "
                    f"LLM: {llm_count} | Template/fallback: {fallback_count}"
                ),
                is_fallback=fallback_count > 0,
            )

            logger.info(
                f"[{self.NAME}] OK | "
                f"{len(drafts)} mensagens | {fallback_count} via template"
            )
            return drafts, trace

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
                summary="Falha na geração de mensagens",
                error=str(exc),
            )
            raise
