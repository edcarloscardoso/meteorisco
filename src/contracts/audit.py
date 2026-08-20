"""
MeteoRisco — Contrato: AuditResult

Saída do Auditor de Decisão. Resultado da verificação de conformidade
de cada MessageDraft contra o playbook.

PRINCÍPIO: Quem redige não pode ser quem audita. O Auditor é independente
do Redator — garantia de governança de conteúdo.
"""
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class AuditStatus(str, Enum):
    APPROVED = "approved"    # Mensagem aprovada para simulação de envio
    BLOCKED = "blocked"      # Mensagem bloqueada por violação grave
    REVISED = "revised"      # Mensagem aprovada com ressalvas / sugestões de revisão


class AuditResult(BaseModel):
    """
    Contrato de saída do Auditor de Decisão.
    Resultado da auditoria de conformidade de uma mensagem ao playbook.
    """
    message_id: str = Field(
        description="ID da mensagem auditada (insured_id + timestamp)"
    )
    insured_id: str = Field(description="ID do segurado destinatário")
    insured_name: str = Field(description="Nome do segurado")
    status: AuditStatus = Field(description="Resultado da auditoria")

    # Violações encontradas (se houver)
    violations: list[str] = Field(
        default_factory=list,
        description=(
            "Lista de violações ao playbook detectadas. "
            "Ex: ['promessa_de_cobertura', 'alarmismo_excessivo', 'frases_proibidas']"
        ),
    )
    violation_details: list[str] = Field(
        default_factory=list,
        description="Trechos específicos que violam o playbook (para trilha de decisão)",
    )

    # Notas da auditoria
    notes: Optional[str] = Field(
        default=None,
        description="Observações gerais do auditor sobre a mensagem",
    )

    # Decisão de não comunicação (silêncio justificado)
    silence_reason: Optional[str] = Field(
        default=None,
        description="Se status==blocked, motivo principal do bloqueio",
    )

    # Referência à mensagem auditada
    original_body_preview: Optional[str] = Field(
        default=None,
        description="Primeiros 200 chars da mensagem auditada (para rastreabilidade)",
    )
