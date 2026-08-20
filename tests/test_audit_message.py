import pytest
from src.contracts.message import MessageDraft, ModelMeta
from src.contracts.audit import AuditStatus
from src.skills.audit_message import audit_message

def test_audit_message_approved():
    draft = MessageDraft(
        insured_id="INS001",
        insured_name="Ana Souza",
        channel="app",
        severity="orange",
        line_of_business="residential",
        body="Olá Ana. Há previsão de chuva intensa em sua região. Verifique as calhas e recolha objetos externos.",
        actions=["Verifique as calhas", "Recolha objetos externos"],
        model_meta=ModelMeta(provider="template", model="offline-template-v1", is_fallback=True)
    )

    result = audit_message(draft)
    assert result.status == AuditStatus.APPROVED
    assert len(result.violations) == 0

def test_audit_message_blocked_forbidden_phrase():
    draft = MessageDraft(
        insured_id="INS001",
        insured_name="Ana Souza",
        channel="app",
        severity="orange",
        line_of_business="residential",
        body="Garantimos a indenização caso haja qualquer problema.",
        actions=["Nenhuma"],
        model_meta=ModelMeta(provider="template", model="offline-template-v1", is_fallback=True)
    )

    result = audit_message(draft)
    assert result.status == AuditStatus.BLOCKED
    assert "promessa_de_cobertura" in result.violations
