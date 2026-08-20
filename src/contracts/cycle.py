"""
MeteoRisco — Contrato: CycleResult

Estado final do ciclo completo. Agrega todos os contratos intermediários
e a trilha de decisão por agente. Consumido pela UI e pelos evals.
"""
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field

from .weather import WeatherSignal
from .risk import RiskAssessment
from .audience import AudienceSelection
from .message import MessageDraft
from .audit import AuditResult
from .notification import NotificationLog


class AgentTrace(BaseModel):
    """Span de execução de um agente — unidade de observabilidade."""
    agent_name: str = Field(description="Nome do agente (ex: 'ScoutClimático')")
    t_start: datetime = Field(description="Timestamp de início da execução")
    t_end: datetime = Field(description="Timestamp de fim da execução")
    duration_ms: float = Field(description="Duração em milissegundos")
    status: str = Field(description="'ok' | 'error' | 'skipped'")
    summary: str = Field(description="Resumo legível do que o agente fez")
    error: Optional[str] = Field(default=None, description="Mensagem de erro, se houver")
    is_fallback: bool = Field(
        default=False,
        description="True se o agente usou modo fallback (fixture, template offline, etc.)",
    )


class CycleResult(BaseModel):
    """
    Contrato de saída do Harness (run_cycle).
    Estado final completo do ciclo MeteoRisco para uma localidade.
    Inclui todos os artefatos intermediários e a trilha de decisão.
    """
    # Identificação do ciclo
    cycle_id: str = Field(description="ID único do ciclo (ex: 'sao_paulo_20260818T194521')")
    location_id: str = Field(description="ID da localidade-piloto")
    run_at: datetime = Field(description="Timestamp de início do ciclo")

    # Status geral
    ok: bool = Field(description="True se o ciclo completou sem erros críticos")
    errors: list[str] = Field(default_factory=list, description="Erros críticos do ciclo")

    # Artefatos por etapa (ordem canônica do pipeline)
    weather_signal: Optional[WeatherSignal] = None
    risk_assessment: Optional[RiskAssessment] = None
    audience_selection: Optional[AudienceSelection] = None
    message_drafts: list[MessageDraft] = Field(default_factory=list)
    audit_results: list[AuditResult] = Field(default_factory=list)
    notification_logs: list[NotificationLog] = Field(default_factory=list)

    # Trilha de decisão (observabilidade)
    trace: list[AgentTrace] = Field(
        default_factory=list,
        description="Trace por etapa — cada agente registra seu span",
    )

    # Modo de operação (transparência)
    used_fixture: bool = Field(
        default=False,
        description="True se qualquer etapa do ciclo usou dados de fixture",
    )

    @property
    def total_notified(self) -> int:
        """Total de segurados com envio simulado."""
        return len(self.notification_logs)

    @property
    def total_blocked(self) -> int:
        """Total de mensagens bloqueadas pelo auditor."""
        from .audit import AuditStatus
        return sum(1 for a in self.audit_results if a.status == AuditStatus.BLOCKED)

    @property
    def cycle_duration_ms(self) -> float:
        """Duração total do ciclo em ms."""
        if not self.trace:
            return 0.0
        return sum(t.duration_ms for t in self.trace)
