"""
MeteoRisco — Contrato: AudienceSelection

Saída do Gestor de Exposição. Lista de segurados elegíveis para comunicação
preventiva, com justificativa por segurado. Decisão 100% determinística —
nunca delegada a LLM.
"""
from typing import Optional
from pydantic import BaseModel, Field


class AudienceItem(BaseModel):
    """Um segurado elegível para receber comunicação preventiva."""
    insured_id: str = Field(description="ID único do segurado na carteira sintética")
    insured_name: str = Field(description="Nome do segurado (para mensagem personalizada)")
    channel: str = Field(description="Canal preferencial: 'app' | 'email' | 'sms'")
    line_of_business: str = Field(description="Ramo do seguro: 'residential' | 'auto' | 'commercial'")
    exposure_profile: str = Field(description="Perfil de exposição (ex: 'imovel_terreo', 'veiculo_na_rua')")
    reason_codes: list[str] = Field(
        default_factory=list,
        description="Códigos de motivo de elegibilidade (da risk_matrix)",
    )
    priority: str = Field(
        default="medium",
        description="Prioridade de envio: 'high' | 'medium' | 'low'",
    )
    location_id: str = Field(description="ID da localidade do segurado")


class SuppressedItem(BaseModel):
    """Um segurado que NÃO receberá comunicação, com motivo registrado."""
    insured_id: str = Field(description="ID único do segurado")
    insured_name: str = Field(description="Nome do segurado")
    suppression_reason: str = Field(
        description="Motivo de supressão (ex: 'exposure_mismatch', 'below_threshold', 'cooldown')"
    )
    suppression_detail: Optional[str] = Field(
        default=None,
        description="Detalhamento adicional (ex: 'veículo em garagem coberta')",
    )


class AudienceSelection(BaseModel):
    """
    Contrato de saída do Gestor de Exposição.
    Resultado da aplicação das regras de carteira sobre o RiskAssessment.
    """
    items: list[AudienceItem] = Field(
        default_factory=list,
        description="Segurados elegíveis para comunicação preventiva",
    )
    suppressed: list[SuppressedItem] = Field(
        default_factory=list,
        description="Segurados avaliados e suprimidos (silêncio justificado)",
    )
    applied_matrix_rules: list[str] = Field(
        default_factory=list,
        description="IDs das regras da risk_matrix aplicadas nesta seleção",
    )

    @property
    def total_eligible(self) -> int:
        return len(self.items)

    @property
    def total_suppressed(self) -> int:
        return len(self.suppressed)
