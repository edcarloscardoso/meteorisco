"""
MeteoRisco — Skill: simulate_notify

Simula o envio de mensagens aprovadas pelo operador (human-in-the-loop).
Produz NotificationLog com payload, canal, timestamp e status "simulated".

IMPORTANTE: Nenhuma mensagem real é enviada.
FORA DE ESCOPO do MVP: SMS, e-mail, WhatsApp, push reais.

Determinístico. Sem LLM. Testável unitariamente.
"""
import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from src.contracts.message import MessageDraft
from src.contracts.audit import AuditResult, AuditStatus
from src.contracts.notification import NotificationLog, NotificationStatus
from src.config import settings

logger = logging.getLogger(__name__)


def simulate_notify(
    draft: MessageDraft,
    audit: AuditResult,
    approved_by: str = "operador",
    justification: str | None = None,
) -> NotificationLog | None:
    """
    Simula o envio de uma mensagem aprovada e registra em NotificationLog.

    Pré-condição: audit.status deve ser APPROVED ou REVISED.
    Se BLOCKED → retorna None (não simula).

    Args:
        draft: MessageDraft com o conteúdo da mensagem.
        audit: AuditResult com o resultado da auditoria.
        approved_by: Identificador de quem aprovou (operador, sistema, etc.).
        justification: Justificativa opcional da aprovação.

    Returns:
        NotificationLog se enviado com sucesso.
        None se mensagem estava bloqueada.
    """
    if audit.status == AuditStatus.BLOCKED:
        logger.warning(
            f"[simulate_notify] Mensagem de {draft.insured_id} BLOQUEADA pelo auditor. "
            f"Envio simulado cancelado. Razão: {audit.silence_reason}"
        )
        return None

    timestamp = datetime.now(timezone.utc)
    payload_ref = _build_payload_ref(draft, timestamp)

    # Persistir log em arquivo (opcional, traces/)
    _persist_trace(draft, audit, timestamp, approved_by)

    log = NotificationLog(
        insured_id=draft.insured_id,
        insured_name=draft.insured_name,
        channel=draft.channel,
        status=NotificationStatus.SIMULATED,
        payload_ref=payload_ref,
        timestamp=timestamp,
        message_subject=draft.subject,
        message_body_preview=draft.body[:200] if draft.body else "",
        approved_by=approved_by,
        justification=justification or f"Aprovado via {approved_by}",
    )

    logger.info(
        f"[simulate_notify] ✅ SIMULADO | {draft.insured_id} | "
        f"canal={draft.channel} | ref={payload_ref[:12]}..."
    )

    return log


def _build_payload_ref(draft: MessageDraft, timestamp: datetime) -> str:
    """Gera um hash de referência para o payload da mensagem."""
    content = f"{draft.insured_id}:{draft.channel}:{timestamp.isoformat()}:{draft.body[:100]}"
    return hashlib.sha256(content.encode()).hexdigest()[:32]


def _persist_trace(
    draft: MessageDraft,
    audit: AuditResult,
    timestamp: datetime,
    approved_by: str,
) -> None:
    """
    Persiste o log de notificação simulada em traces/ (opcional).
    Não bloqueia se o diretório não existir.
    """
    try:
        traces_dir = settings.traces_dir
        traces_dir.mkdir(parents=True, exist_ok=True)

        trace_file = traces_dir / f"notification_{timestamp.strftime('%Y%m%d')}.jsonl"
        entry = {
            "timestamp": timestamp.isoformat(),
            "insured_id": draft.insured_id,
            "channel": draft.channel,
            "severity": draft.severity,
            "audit_status": audit.status.value,
            "approved_by": approved_by,
            "body_preview": draft.body[:100] if draft.body else "",
        }
        with trace_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as exc:
        logger.debug(f"[simulate_notify] Não foi possível persistir trace: {exc}")
