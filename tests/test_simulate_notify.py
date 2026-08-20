import pytest
from src.contracts.message import MessageDraft, ModelMeta
from src.contracts.audit import AuditResult, AuditStatus
from src.skills.simulate_notify import simulate_notify
from src.contracts.notification import NotificationStatus

def test_simulate_notify_success():
    draft = MessageDraft(
        insured_id="INS001",
        insured_name="Ana Souza",
        channel="app",
        severity="orange",
        line_of_business="residential",
        body="Olá Ana. Previsão de chuva.",
        actions=["Ação 1"],
        model_meta=ModelMeta(provider="template", model="offline-template-v1", is_fallback=True)
    )
    audit = AuditResult(
        message_id="msg_001",
        insured_id="INS001",
        insured_name="Ana Souza",
        status=AuditStatus.APPROVED
    )

    log = simulate_notify(draft, audit)
    assert log is not None
    assert log.status == NotificationStatus.SIMULATED
    assert log.insured_id == "INS001"

def test_simulate_notify_blocked():
    draft = MessageDraft(
        insured_id="INS001",
        insured_name="Ana Souza",
        channel="app",
        severity="orange",
        line_of_business="residential",
        body="Garantimos a indenização.",
        actions=["Ação 1"],
        model_meta=ModelMeta(provider="template", model="offline-template-v1", is_fallback=True)
    )
    audit = AuditResult(
        message_id="msg_001",
        insured_id="INS001",
        insured_name="Ana Souza",
        status=AuditStatus.BLOCKED,
        silence_reason="Violação grave"
    )

    log = simulate_notify(draft, audit)
    assert log is None
