"""
MeteoRisco — Skill: select_insureds

Seleciona segurados elegíveis para comunicação preventiva com base em:
  - RiskAssessment (tipo de evento, severidade, ramos impactados)
  - Carteira sintética (portfolio.csv)
  - Regras de elegibilidade da risk_matrix.yaml

Registra TODOS os segurados avaliados — tanto elegíveis quanto suprimidos.
A supressão justificada é parte do valor do produto (evitar ruído/spam).

Determinístico. Sem LLM. Testável unitariamente.
"""
import logging
from typing import Optional

from src.contracts.risk import RiskAssessment, HazardType
from src.contracts.audience import AudienceSelection, AudienceItem, SuppressedItem
from src.skills.load_domain import load_portfolio, load_risk_matrix, get_insureds_by_location

logger = logging.getLogger(__name__)


def select_insureds(
    risk: RiskAssessment,
    location_id: str,
) -> AudienceSelection:
    """
    Seleciona segurados elegíveis para comunicação preventiva.

    Regras aplicadas (em ordem):
    1. Se NO_HAZARD → suprimir todos (nenhum evento relevante)
    2. Filtrar por localidade
    3. Filtrar por ramo impactado (impacted_lines do RiskAssessment)
    4. Aplicar regras de exposição da risk_matrix (do_not_alert_if)
    5. Registrar motivo de supressão para cada excluído

    Args:
        risk: RiskAssessment produzido pelo Analista.
        location_id: ID da localidade do ciclo.

    Returns:
        AudienceSelection com segurados elegíveis e suprimidos justificados.
    """
    # Caso base: sem hazard, suprimir todos
    if not risk.has_hazard:
        all_insureds = get_insureds_by_location(location_id)
        suppressed = [
            SuppressedItem(
                insured_id=ins["id"],
                insured_name=ins["name"],
                suppression_reason="no_hazard",
                suppression_detail=(
                    f"Nenhum evento climático relevante identificado para "
                    f"{location_id}. Silêncio justificado."
                ),
            )
            for ins in all_insureds
        ]
        logger.info(
            f"[select_insureds] NO_HAZARD para {location_id} — "
            f"todos os {len(suppressed)} segurados suprimidos"
        )
        return AudienceSelection(items=[], suppressed=suppressed, applied_matrix_rules=[])

    # Carrega regras de supressão da matriz
    matrix = load_risk_matrix()
    rules = matrix.get("rules", [])

    # Regras relevantes para este hazard + severity
    relevant_rules = [
        r for r in rules
        if r.get("event") == risk.hazard_type.value
        and r.get("severity") == (risk.severity.value if risk.severity else None)
    ]
    applied_rule_ids = [r.get("id", "unknown") for r in relevant_rules]

    # Coleta todas as condições de supressão das regras relevantes
    suppression_conditions = set()
    for rule in relevant_rules:
        for cond in rule.get("do_not_alert_if", []):
            suppression_conditions.add(cond)

    # Segurados da localidade
    insureds = get_insureds_by_location(location_id)

    eligible: list[AudienceItem] = []
    suppressed: list[SuppressedItem] = []

    for ins in insureds:
        result = _evaluate_insured(ins, risk, suppression_conditions, relevant_rules)
        if result["eligible"]:
            eligible.append(
                AudienceItem(
                    insured_id=ins["id"],
                    insured_name=ins["name"],
                    channel=ins.get("channel", "app"),
                    line_of_business=ins["line_of_business"],
                    exposure_profile=ins.get("exposure_profile", "unknown"),
                    reason_codes=result["reason_codes"],
                    priority=result["priority"],
                    location_id=location_id,
                )
            )
        else:
            suppressed.append(
                SuppressedItem(
                    insured_id=ins["id"],
                    insured_name=ins["name"],
                    suppression_reason=result["suppression_reason"],
                    suppression_detail=result.get("suppression_detail"),
                )
            )

    logger.info(
        f"[select_insureds] {location_id} | "
        f"hazard={risk.hazard_type} | severity={risk.severity} | "
        f"elegíveis={len(eligible)} | suprimidos={len(suppressed)}"
    )

    return AudienceSelection(
        items=eligible,
        suppressed=suppressed,
        applied_matrix_rules=applied_rule_ids,
    )


def _evaluate_insured(
    ins: dict,
    risk: RiskAssessment,
    suppression_conditions: set,
    relevant_rules: list[dict],
) -> dict:
    """
    Avalia um segurado individualmente e retorna dict com resultado.
    """
    line_of_business = ins.get("line_of_business", "")
    exposure_profile = ins.get("exposure_profile", "")
    is_vip = ins.get("is_vip", False)
    is_high_risk = ins.get("is_high_risk", False)

    # 1. Verificar se ramo está impactado
    if risk.impacted_lines and line_of_business not in risk.impacted_lines:
        # Ramo não impactado pelo evento
        # Se não há impacted_lines definidos (thresholds não preenchidos), passa
        return {
            "eligible": False,
            "suppression_reason": "line_not_impacted",
            "suppression_detail": (
                f"Ramo '{line_of_business}' não está na lista de ramos impactados "
                f"pelo evento {risk.hazard_type}: {risk.impacted_lines}"
            ),
        }

    # 2. Verificar condições de supressão da risk_matrix
    for cond in suppression_conditions:
        if cond and exposure_profile == cond:
            return {
                "eligible": False,
                "suppression_reason": "exposure_mismatch",
                "suppression_detail": (
                    f"Perfil de exposição '{exposure_profile}' está na condição de supressão "
                    f"da risk_matrix para {risk.hazard_type}/{risk.severity}: '{cond}'"
                ),
            }

    # 3. Elegível — determinar prioridade
    reason_codes = [f"{risk.hazard_type.value}_{risk.severity.value if risk.severity else 'unknown'}"]
    if is_high_risk:
        reason_codes.append("high_risk_insured")
    if exposure_profile in ("imovel_terreo", "area_sujeita_alagamento", "veiculo_na_rua"):
        reason_codes.append("high_exposure_profile")

    # Prioridade: VIP ou alto risco → high; exposição alta → medium; default → low
    if is_vip or is_high_risk:
        priority = "high"
    elif exposure_profile in ("imovel_terreo", "area_sujeita_alagamento", "veiculo_na_rua"):
        priority = "medium"
    else:
        priority = "low"

    return {
        "eligible": True,
        "reason_codes": reason_codes,
        "priority": priority,
    }
