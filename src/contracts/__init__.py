"""
MeteoRisco — Contratos de Dados
Exporta todos os schemas Pydantic do pipeline.
"""
from .weather import WeatherSignal, WeatherMetrics, LocationRef
from .risk import RiskAssessment, SeverityLevel, HazardType
from .audience import AudienceSelection, AudienceItem, SuppressedItem
from .message import MessageDraft, ModelMeta
from .audit import AuditResult, AuditStatus
from .notification import NotificationLog, NotificationStatus
from .cycle import CycleResult, AgentTrace

__all__ = [
    # Weather
    "WeatherSignal",
    "WeatherMetrics",
    "LocationRef",
    # Risk
    "RiskAssessment",
    "SeverityLevel",
    "HazardType",
    # Audience
    "AudienceSelection",
    "AudienceItem",
    "SuppressedItem",
    # Message
    "MessageDraft",
    "ModelMeta",
    # Audit
    "AuditResult",
    "AuditStatus",
    # Notification
    "NotificationLog",
    "NotificationStatus",
    # Cycle
    "CycleResult",
    "AgentTrace",
]
