import pytest
from src.harness.runner import run_cycle
from src.contracts.cycle import CycleResult

def test_run_cycle_success_with_fixture():
    # Executa o runner sequencial completo usando fixture offline
    result = run_cycle("sao_paulo", force_fixture=True)
    
    assert isinstance(result, CycleResult)
    assert result.ok is True
    assert result.location_id == "sao_paulo"
    assert result.used_fixture is True
    assert len(result.trace) > 0
    assert result.trace[0].agent_name == "ScoutClimático"

def test_run_cycle_invalid_location():
    result = run_cycle("invalid_city")
    assert result.ok is False
    assert len(result.errors) > 0
    assert "não encontrada" in result.errors[0].lower()
