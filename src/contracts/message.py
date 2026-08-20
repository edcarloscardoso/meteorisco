"""
MeteoRisco — Contrato: MessageDraft

Saída do Redator Preventivo. Mensagem personalizada gerada por LLM
com base no playbook e no perfil do segurado.

IMPORTANTE: A LLM gera COMUNICAÇÃO. Não decide elegibilidade.
"""
from typing import Optional, Any
from pydantic import BaseModel, Field


class ModelMeta(BaseModel):
    """Metadados sobre a chamada ao LLM (rastreabilidade e custo)."""
    provider: str = Field(description="Provedor LLM (ex: 'gemini', 'openai', 'anthropic')")
    model: str = Field(description="Modelo usado (ex: 'gemini-2.0-flash')")
    prompt_tokens: Optional[int] = Field(default=None)
    completion_tokens: Optional[int] = Field(default=None)
    is_fallback: bool = Field(
        default=False,
        description="True se a mensagem foi gerada por template offline (sem LLM)",
    )


class MessageDraft(BaseModel):
    """
    Contrato de saída do Redator Preventivo.
    Mensagem preventiva personalizada por segurado.
    """
    insured_id: str = Field(description="ID do segurado destinatário")
    insured_name: str = Field(description="Nome do segurado")
    channel: str = Field(description="Canal de envio simulado: 'app' | 'email' | 'sms'")
    severity: str = Field(description="Severidade que motivou a mensagem")
    line_of_business: str = Field(description="Ramo do seguro do destinatário")

    # Conteúdo da mensagem
    subject: Optional[str] = Field(
        default=None,
        description="Assunto (para e-mail). None para SMS/app.",
    )
    body: str = Field(
        description=(
            "Corpo principal da mensagem preventiva. "
            "Deve seguir: contexto → risco → ações → fechamento (playbook)."
        )
    )
    actions: list[str] = Field(
        default_factory=list,
        description="Ações práticas recomendadas ao segurado",
    )

    # Rastreabilidade
    model_meta: Optional[ModelMeta] = Field(
        default=None,
        description="Metadados do LLM que gerou a mensagem",
    )
    playbook_version: Optional[str] = Field(
        default=None,
        description="Versão do playbook.yaml usado para gerar esta mensagem",
    )
