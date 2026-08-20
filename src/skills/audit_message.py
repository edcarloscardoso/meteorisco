"""
MeteoRisco — Skill: audit_message

Verifica conformidade de um MessageDraft ao playbook.yaml.
Híbrida: regras hard determinísticas + checagens de estrutura.

PRINCÍPIO: Quem redige não pode ser quem audita.
O Auditor é completamente independente do Redator.

Checagens implementadas:
1. Frases proibidas (regras hard do playbook.prohibitions.forbidden_phrases)
2. Temas proibidos (promessa de cobertura, alarmismo, etc.)
3. Elementos obrigatórios (pelo menos uma ação prática)
4. Comprimento por canal

Determinístico nas regras hard. Testável unitariamente.
"""
import logging
import re
from datetime import datetime, timezone

from src.contracts.message import MessageDraft
from src.contracts.audit import AuditResult, AuditStatus
from src.skills.load_domain import load_playbook

logger = logging.getLogger(__name__)

_DEFAULT_FORBIDDEN_PATTERNS = [
    (r"garantimos (a |que a )?indenização", "promessa_de_cobertura"),
    (r"sua apólice cobre", "promessa_de_cobertura"),
    (r"você (será|vai ser) indenizado", "promessa_de_cobertura"),
    (r"com certeza (vai|irá) granizar", "over_claiming_granizo"),
    (r"granizo (confirmado|detectado|observado)", "over_claiming_granizo"),
    (r"evacuação (obrigatória|imediata)", "alarmismo_excessivo"),
    (r"risco de morte", "alarmismo_excessivo"),
    (r"não temos responsabilidade", "linguagem_inadequada"),
]


def audit_message(draft: MessageDraft) -> AuditResult:
    """
    Audita um MessageDraft contra o playbook e retorna AuditResult.
    """
    playbook = load_playbook()
    violations = []
    violation_details = []

    body = draft.body or ""
    subject = draft.subject or ""
    full_text = f"{subject} {body}".lower()

    # 1. Frases proibidas do playbook
    forbidden_phrases = _get_forbidden_patterns(playbook)
    for pattern, category in forbidden_phrases:
        match = re.search(pattern, full_text, re.IGNORECASE)
        if match:
            violations.append(category)
            violation_details.append(
                f"Padrão proibido detectado ({category}): '...{match.group()}...'"
            )
            logger.warning(
                f"[audit_message] Violação '{category}' na msg de {draft.insured_id}: "
                f"'{match.group()}'"
            )

    # 2. Elementos obrigatórios: pelo menos uma ação prática
    if not draft.actions:
        violations.append("ausencia_de_acoes")
        violation_details.append(
            "Mensagem não contém nenhuma ação prática para o segurado."
        )

    # 3. Linguagem de granizo: verificar se usa linguagem modelada
    if draft.severity in ("orange", "red") and "granizo" in body.lower():
        if not any(
            term in body.lower()
            for term in [
                "previsão", "possibilidade", "prevista", "modelada",
                "modelo", "potencial", "indicação"
            ]
        ):
            violations.append("granizo_sem_ressalva_epistemica")
            violation_details.append(
                "Mensagem menciona granizo sem ressalva epistemológica "
                "(ex: 'previsão de granizo', 'possibilidade prevista pelo modelo')."
            )

    # 4. Verificar comprimento por canal
    channel_limits = _get_channel_limits(playbook)
    limit = channel_limits.get(draft.channel)
    if limit and len(body) > limit:
        violations.append(f"mensagem_muito_longa_{draft.channel}")
        violation_details.append(
            f"Mensagem ({len(body)} chars) excede limite do canal "
            f"{draft.channel} ({limit} chars)."
        )

    # 5. Determinar status
    # Qualquer frase proibida, promessa de cobertura, alarmismo ou ausência de ressalva bloqueia
    blocking_categories = {
        "promessa_de_cobertura",
        "over_claiming_granizo",
        "alarmismo_excessivo",
        "linguagem_inadequada",
        "frase_proibida",
    }
    has_blocking = any(v in blocking_categories for v in violations)

    if has_blocking:
        status = AuditStatus.BLOCKED
        silence_reason = f"Violação grave de conteúdo: {', '.join(v for v in violations if v in blocking_categories)}"
    elif violations:
        status = AuditStatus.REVISED
        silence_reason = None
    else:
        status = AuditStatus.APPROVED
        silence_reason = None

    message_id = f"{draft.insured_id}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"

    result = AuditResult(
        message_id=message_id,
        insured_id=draft.insured_id,
        insured_name=draft.insured_name,
        status=status,
        violations=list(set(violations)),
        violation_details=violation_details,
        notes=_build_notes(status, violations),
        silence_reason=silence_reason,
        original_body_preview=body[:200] if body else None,
    )

    logger.info(
        f"[audit_message] {draft.insured_id} → {status} | "
        f"violações={violations}"
    )

    return result


def _get_forbidden_patterns(playbook: dict) -> list[tuple]:
    """
    Extrai padrões de frases proibidas do playbook.
    """
    prohibitions = playbook.get("prohibitions", {})
    phrases = prohibitions.get("forbidden_phrases", [])

    patterns = []
    for item in phrases:
        pattern = item.get("pattern", "")
        reason = item.get("reason", "frase_proibida")
        if pattern and not pattern.startswith("TODO"):
            # Mapear temas conhecidos
            theme = "frase_proibida"
            if "indenização" in pattern or "apólice" in pattern:
                theme = "promessa_de_cobertura"
            elif "graniz" in pattern:
                theme = "over_claiming_granizo"
            elif "evacuação" in pattern or "morte" in pattern:
                theme = "alarmismo_excessivo"
            patterns.append((pattern, theme))

    if not patterns:
        return _DEFAULT_FORBIDDEN_PATTERNS

    return patterns


def _get_channel_limits(playbook: dict) -> dict:
    """Retorna limites de caracteres por canal do playbook."""
    channels = playbook.get("channels", {})
    limits = {}
    for channel, config in channels.items():
        max_len = config.get("max_length")
        if max_len and isinstance(max_len, int):
            limits[channel] = max_len
    return limits


def _build_notes(status: AuditStatus, violations: list) -> str:
    """Gera nota legível da auditoria."""
    if status == AuditStatus.APPROVED:
        return "Mensagem aprovada. Nenhuma violação ao playbook detectada."
    elif status == AuditStatus.REVISED:
        return (
            f"Mensagem aprovada com ressalvas. "
            f"Violações não-bloqueantes: {', '.join(violations)}. "
            f"Revisar antes do envio simulado."
        )
    else:
        return (
            f"Mensagem BLOQUEADA. Violações graves detectadas: {', '.join(violations)}. "
            f"Não simular envio."
        )
