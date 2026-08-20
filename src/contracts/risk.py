"""
MeteoRisco — Contrato: RiskAssessment

Saída do Analista MeteoRisco. Representa a avaliação de ameaça climática
no contexto de risco securitário, produzida de forma DETERMINÍSTICA
com base nos thresholds da risk_matrix.yaml.

DECISÃO TOMADA: Elegibilidade não depende de LLM. A LLM agrega valor
na comunicação (Redator), não na "legislação interna" da operação.
"""
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class SeverityLevel(str, Enum):
    """
    Níveis de severidade do MeteoRisco.
    Mapeados para ações de comunicação conforme playbook.
    """
    YELLOW = "yellow"    # Atenção / monitoramento → tom informativo
    ORANGE = "orange"    # Risco relevante → tom preventivo, claro
    RED = "red"          # Risco elevado / iminente → tom urgente, acionável, sóbrio


class HazardType(str, Enum):
    """Tipos de evento climático no MVP."""
    RAIN_HEAVY = "rain_heavy"        # Chuva intensa (P0)
    HAIL = "hail"                    # Granizo — classificação modelada NWP (P0)
    WIND_STRONG = "wind_strong"      # Vento forte (P0)
    STORM = "storm"                  # Tempestade / tempestade severa (P0)
    NO_HAZARD = "no_hazard"          # Nenhum evento relevante identificado


class RiskAssessment(BaseModel):
    """
    Contrato de saída do Analista MeteoRisco.
    Avaliação determinística de ameaça climática para uma localidade.
    """
    hazard_type: HazardType = Field(
        description="Tipo de evento climático identificado"
    )
    severity: Optional[SeverityLevel] = Field(
        default=None,
        description="Nível de severidade (None se hazard_type == NO_HAZARD)",
    )
    impacted_lines: list[str] = Field(
        default_factory=list,
        description="Ramos de seguro impactados (ex: ['residential', 'auto'])",
    )
    rationale: str = Field(
        description=(
            "Justificativa legível da classificação — "
            "quais métricas acionaram quais thresholds"
        )
    )
    confidence: Optional[str] = Field(
        default=None,
        description="Indicação de confiança na classificação (ex: 'high', 'medium', 'low')",
    )

    # Métricas que motivaram a classificação (rastreabilidade)
    triggered_metrics: dict = Field(
        default_factory=dict,
        description="Valores das métricas que acionaram os thresholds (para trilha de decisão)",
    )
    triggered_thresholds: dict = Field(
        default_factory=dict,
        description="Thresholds da risk_matrix que foram superados",
    )

    @property
    def has_hazard(self) -> bool:
        """Retorna True se há ameaça identificada."""
        return self.hazard_type != HazardType.NO_HAZARD
