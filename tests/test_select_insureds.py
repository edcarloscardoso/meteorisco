import pytest
from src.contracts.risk import RiskAssessment, HazardType, SeverityLevel
from src.skills.select_insureds import select_insureds
from src.contracts.audience import AudienceSelection

def test_select_insureds_no_hazard():
    risk = RiskAssessment(
        hazard_type=HazardType.NO_HAZARD,
        severity=None,
        impacted_lines=[],
        rationale="Sem eventos"
    )

    selection = select_insureds(risk, "sao_paulo")
    assert isinstance(selection, AudienceSelection)
    assert selection.total_eligible == 0
    assert selection.total_suppressed > 0
    assert all(s.suppression_reason == "no_hazard" for s in selection.suppressed)

def test_select_insureds_with_hazard_line_not_impacted():
    risk = RiskAssessment(
        hazard_type=HazardType.RAIN_HEAVY,
        severity=SeverityLevel.ORANGE,
        impacted_lines=["residential"], # apenas residencial
        rationale="Chuva forte apenas em residencial"
    )

    selection = select_insureds(risk, "sao_paulo")
    
    # Auto deve ser suprimido pois o ramo impactado é apenas residential
    for item in selection.items:
        assert item.line_of_business == "residential"
    
    for s in selection.suppressed:
        if "INS002" in s.insured_id or "INS016" in s.insured_id: # Segurados auto de SP
            assert s.suppression_reason == "line_not_impacted"
