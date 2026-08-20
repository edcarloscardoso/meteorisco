"""
MeteoRisco — Skill: apply_risk_matrix

Aplica a risk_matrix.yaml sobre um WeatherSignal para produzir um RiskAssessment.
Lógica 100% DETERMINÍSTICA — sem LLM.

DECISÃO TOMADA: Decisões de elegibilidade auditáveis não devem depender de
alucinação de modelo. A LLM não decide quem é elegível.
"""
import logging

from src.contracts.weather import WeatherSignal
from src.contracts.risk import RiskAssessment, SeverityLevel, HazardType
from src.skills.load_domain import load_risk_matrix

logger = logging.getLogger(__name__)

_SEVERITY_MAP = {
    "yellow": SeverityLevel.YELLOW,
    "orange": SeverityLevel.ORANGE,
    "red": SeverityLevel.RED,
}

_HAZARD_MAP = {
    "rain_heavy": HazardType.RAIN_HEAVY,
    "hail": HazardType.HAIL,
    "wind_strong": HazardType.WIND_STRONG,
    "storm": HazardType.STORM,
}

# Ordem de severidade para desempate
_SEVERITY_ORDER = {SeverityLevel.RED: 3, SeverityLevel.ORANGE: 2, SeverityLevel.YELLOW: 1}

# Prioridade intrínseca de hazard em caso de mesma severidade (granizo/tempestade > chuva/vento)
_HAZARD_PRIORITY = {HazardType.HAIL: 4, HazardType.STORM: 3, HazardType.WIND_STRONG: 2, HazardType.RAIN_HEAVY: 1}


def apply_risk_matrix(signal: WeatherSignal) -> RiskAssessment:
    """
    Cruza o WeatherSignal com as regras da risk_matrix e retorna o pior risco identificado.
    """
    matrix = load_risk_matrix()
    rules = matrix.get("rules", [])
    metrics = signal.metrics

    activated_rules = []

    for rule in rules:
        thresholds = rule.get("thresholds", {})
        if _rule_is_triggered(thresholds, metrics):
            severity = _SEVERITY_MAP.get(rule.get("severity"), SeverityLevel.YELLOW)
            hazard = _HAZARD_MAP.get(rule.get("event"), HazardType.NO_HAZARD)
            activated_rules.append({
                "rule_id": rule.get("id", "unknown"),
                "hazard": hazard,
                "severity": severity,
                "line_of_business": rule.get("line_of_business"),
                "rationale": rule.get("rationale", "").strip(),
                "thresholds_checked": thresholds,
            })
            logger.debug(f"[apply_risk_matrix] Regra ativada: {rule.get('id')} → {severity}")

    if not activated_rules:
        logger.info(f"[apply_risk_matrix] Nenhum evento relevante para {signal.location.id}")
        return RiskAssessment(
            hazard_type=HazardType.NO_HAZARD,
            severity=None,
            impacted_lines=[],
            rationale=(
                f"Nenhuma regra da risk_matrix foi ativada para as métricas observadas "
                f"em {signal.location.city}/{signal.location.state}. "
                f"Chuva: {metrics.precipitation_mm_h}mm/h | "
                f"Rajadas: {metrics.wind_gusts_10m_kmh}km/h | "
                f"WMO: {metrics.weather_code} | "
                f"CAPE: {metrics.cape_j_kg}J/kg"
            ),
            triggered_metrics=_metrics_snapshot(metrics),
        )

    # Ordena primeiro por severidade (maior primeiro), depois por prioridade intrínseca do hazard
    activated_rules.sort(
        key=lambda r: (_SEVERITY_ORDER.get(r["severity"], 0), _HAZARD_PRIORITY.get(r["hazard"], 0)),
        reverse=True
    )

    # Pega o pior caso
    worst = activated_rules[0]

    # Coleta todos os ramos impactados por regras ativadas
    impacted_lines = list({
        r["line_of_business"] for r in activated_rules if r["line_of_business"]
    })

    triggered_metrics = _metrics_snapshot(metrics)
    triggered_thresholds = {r["rule_id"]: r["thresholds_checked"] for r in activated_rules}

    assessment = RiskAssessment(
        hazard_type=worst["hazard"],
        severity=worst["severity"],
        impacted_lines=impacted_lines,
        rationale=(
            f"{worst['rationale']} "
            f"[Regras ativadas: {', '.join(r['rule_id'] for r in activated_rules)}]"
        ).strip(),
        triggered_metrics=triggered_metrics,
        triggered_thresholds=triggered_thresholds,
    )

    logger.info(
        f"[apply_risk_matrix] {signal.location.id} | "
        f"hazard={assessment.hazard_type} | "
        f"severity={assessment.severity} | "
        f"ramos={assessment.impacted_lines}"
    )

    return assessment


def _rule_is_triggered(thresholds: dict, metrics) -> bool:
    """
    Verifica se um conjunto de thresholds é ativado pelas métricas.
    Retorna True apenas se TODOS os thresholds não-None forem satisfeitos.
    """
    checks = {
        "precipitation_mm_h": (metrics.precipitation_mm_h, ">="),
        "wind_gusts_kmh": (metrics.wind_gusts_10m_kmh, ">="),
        "cape_jkg": (metrics.cape_j_kg, ">="),
        "lifted_index_max": (metrics.lifted_index, "<="),  # Mais negativo = pior
        "weather_code_min": (metrics.weather_code, ">="),
    }

    for threshold_key, (metric_value, operator) in checks.items():
        threshold_value = thresholds.get(threshold_key)
        if threshold_value is None:
            continue
        if metric_value is None:
            return False
        if operator == ">=" and metric_value < threshold_value:
            return False
        elif operator == "<=" and metric_value > threshold_value:
            return False

    has_any_threshold = any(v is not None for v in thresholds.values())
    return has_any_threshold


def _metrics_snapshot(metrics) -> dict:
    """Retorna snapshot das métricas relevantes para a trilha de decisão."""
    return {
        "precipitation_mm_h": metrics.precipitation_mm_h,
        "wind_gusts_10m_kmh": metrics.wind_gusts_10m_kmh,
        "weather_code": metrics.weather_code,
        "cape_j_kg": metrics.cape_j_kg,
        "lifted_index": metrics.lifted_index,
    }
