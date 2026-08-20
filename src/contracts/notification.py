"""
MeteoRisco — Contrato: NotificationLog

Saída do Notification Simulator. Registro de simulação de envio após
aprovação pelo operador (human-in-the-loop).

IMPORTANTE: Nenhuma mensagem real é enviada. Status sempre "simulated".
Fora de escopo do MVP: SMS, e-mail, WhatsApp, push reais.
"""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class NotificationStatus(str, Enum):
    SIMULATED = "simulated"    # Envio simulado com sucesso (único status válido no MVP)


from enum import Enum


class NotificationLog(BaseModel):
    """
    Contrato de saída do Notification Simulator.
    Registro auditável da simulação de envio de uma mensagem aprovada.
    """
    insured_id: str = Field(description="ID do segurado destinatário")
    insured_name: str = Field(description="Nome do segurado")
    channel: str = Field(description="Canal simulado: 'app' | 'email' | 'sms'")
    status: NotificationStatus = Field(
        default=NotificationStatus.SIMULATED,
        description="Status do envio (sempre 'simulated' no MVP)",
    )
    payload_ref: str = Field(
        description="Referência ao conteúdo enviado (ex: ID da mensagem ou hash)"
    )
    timestamp: datetime = Field(
        description="Timestamp da simulação de envio"
    )

    # Rastreabilidade
    message_subject: Optional[str] = Field(
        default=None, description="Assunto da mensagem (se e-mail)"
    )
    message_body_preview: str = Field(
        description="Primeiros 200 chars do corpo da mensagem"
    )
    approved_by: str = Field(
        default="operador",
        description="Quem aprovou o envio (human-in-the-loop)",
    )
    justification: Optional[str] = Field(
        default=None,
        description="Justificativa do envio simulado",
    )
