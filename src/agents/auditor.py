"""
MeteoRisco — Agente 5: Auditor de Decisão

Missão: Verificar conformidade de cada MessageDraft ao playbook, bloquear
mensagens inadequadas e registrar trilha de decisão. Entrada → saída: MessageDraft[] → AuditResult[].

Skills permitidas: audit_message
Skills proibidas: LLM para decisão de bloqueio (deve ser determinístico)

Por que separado:
  Governança precisa ser independente da geração da mensagem.
  Quem redige não pode ser quem audita. Separação de responsabilidades.
"""
import logging
from datetime import datetime, timezone

from src.contracts.message import MessageDraft
from src.contracts.audit import AuditResult
from src.contracts.cycle import AgentTrace
from src.skills.audit_message import audit_message

logger = logging.getLogger(__name__)


class AuditordDeDecisao:
    """Agente responsável por auditar conformidade das mensagens ao playbook."""

    NAME = "AuditordDeDecisão"

    def run(
        self, drafts: list[MessageDraft]
    ) -> tuple[list[AuditResult], AgentTrace]:
        """
        Audita cada MessageDraft contra o playbook.

        Args:
            drafts: Lista de MessageDraft do Redator.

        Returns:
            (list[AuditResult], AgentTrace)
        """
        t_start = datetime.now(timezone.utc)

        try:
            results = []
            blocked_count = 0
            revised_count = 0
            approved_count = 0

            for draft in drafts:
                result = audit_message(draft)
                results.append(result)

                from src.contracts.audit import AuditStatus
                if result.status == AuditStatus.BLOCKED:
                    blocked_count += 1
                elif result.status == AuditStatus.REVISED:
                    revised_count += 1
                else:
                    approved_count += 1

            t_end = datetime.now(timezone.utc)
            duration_ms = (t_end - t_start).total_seconds() * 1000

            trace = AgentTrace(
                agent_name=self.NAME,
                t_start=t_start,
                t_end=t_end,
                duration_ms=duration_ms,
                status="ok",
                summary=(
                    f"Auditoria de {len(results)} mensagens: "
                    f"✅ aprovadas={approved_count} | "
                    f"⚠️ revisão={revised_count} | "
                    f"🚫 bloqueadas={blocked_count}"
                ),
            )

            logger.info(
                f"[{self.NAME}] OK | "
                f"aprovadas={approved_count} | "
                f"revisão={revised_count} | bloqueadas={blocked_count}"
            )
            return results, trace

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
                summary="Falha na auditoria",
                error=str(exc),
            )
            raise
