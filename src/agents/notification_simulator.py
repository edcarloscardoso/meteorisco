"""
MeteoRisco — Notification Simulator

Missão: Executar simulação de envio após aprovação do operador (human-in-the-loop).
Entrada → saída: AuditResult[] (aprovados) → NotificationLog[].

Não é um "agente" com LLM — é um componente especializado de simulação.
Skills permitidas: simulate_notify
"""
import logging
from datetime import datetime, timezone

from src.contracts.message import MessageDraft
from src.contracts.audit import AuditResult, AuditStatus
from src.contracts.notification import NotificationLog
from src.contracts.cycle import AgentTrace
from src.skills.simulate_notify import simulate_notify

logger = logging.getLogger(__name__)


class NotificationSimulator:
    """Componente responsável por simular envio de mensagens aprovadas."""

    NAME = "NotificationSimulator"

    def run(
        self,
        drafts: list[MessageDraft],
        audit_results: list[AuditResult],
        approved_by: str = "operador",
        operator_rejections: list[str] | None = None,
    ) -> tuple[list[NotificationLog], AgentTrace]:
        """
        Simula envio para mensagens aprovadas pelo auditor E pelo operador.

        Args:
            drafts: Lista de MessageDraft do Redator.
            audit_results: Lista de AuditResult do Auditor.
            approved_by: Identificador do aprovador (operador).
            operator_rejections: IDs de segurados que o operador rejeitou manualmente.

        Returns:
            (list[NotificationLog], AgentTrace)
        """
        t_start = datetime.now(timezone.utc)
        operator_rejections = operator_rejections or []

        try:
            # Mapeia insured_id → AuditResult
            audit_map = {r.insured_id: r for r in audit_results}

            logs = []
            skipped_blocked = 0
            skipped_operator = 0

            for draft in drafts:
                audit = audit_map.get(draft.insured_id)
                if not audit:
                    logger.warning(
                        f"[{self.NAME}] Sem AuditResult para {draft.insured_id}. Pulando."
                    )
                    continue

                # Verificar rejeição manual do operador
                if draft.insured_id in operator_rejections:
                    skipped_operator += 1
                    logger.info(
                        f"[{self.NAME}] Operador rejeitou {draft.insured_id}. Sem envio."
                    )
                    continue

                # Verificar bloqueio do auditor
                if audit.status == AuditStatus.BLOCKED:
                    skipped_blocked += 1
                    continue

                # Simular envio
                log = simulate_notify(
                    draft=draft,
                    audit=audit,
                    approved_by=approved_by,
                )
                if log:
                    logs.append(log)

            t_end = datetime.now(timezone.utc)
            duration_ms = (t_end - t_start).total_seconds() * 1000

            trace = AgentTrace(
                agent_name=self.NAME,
                t_start=t_start,
                t_end=t_end,
                duration_ms=duration_ms,
                status="ok",
                summary=(
                    f"Simulações realizadas: {len(logs)} | "
                    f"Bloqueados pelo auditor: {skipped_blocked} | "
                    f"Rejeitados pelo operador: {skipped_operator}"
                ),
            )

            logger.info(
                f"[{self.NAME}] OK | simulados={len(logs)} | "
                f"bloqueados={skipped_blocked} | rejeitados={skipped_operator}"
            )
            return logs, trace

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
                summary="Falha na simulação de notificação",
                error=str(exc),
            )
            raise
