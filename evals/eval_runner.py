"""
MeteoRisco — Evals Runner Completo (EV1–EV8 + EV-GEO-1..5)

Executa a suíte de avaliação de negócio, segurança, resiliência e multi-localidade
definida em golden_cases.yaml usando as regras v1.0 da risk_matrix.yaml.
"""
import yaml
import logging
from pathlib import Path
from datetime import datetime, timezone

from src.contracts.weather import WeatherSignal, WeatherMetrics, LocationRef
from src.contracts.message import MessageDraft, ModelMeta
from src.contracts.audit import AuditStatus
from src.skills.load_domain import get_location_by_id
from src.skills.apply_risk_matrix import apply_risk_matrix
from src.skills.select_insureds import select_insureds
from src.skills.audit_message import audit_message
from src.agents.notification_simulator import NotificationSimulator

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger("eval_runner")


def run_evals():
    evals_dir = Path(__file__).parent
    cases_file = evals_dir / "golden_cases.yaml"

    if not cases_file.exists():
        logger.error(f"Arquivo de golden cases não encontrado: {cases_file}")
        return

    with cases_file.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    cases = config.get("cases", [])
    logger.info(f"=== Iniciando Execução da Suíte Completa de Evals ({len(cases)} cenários) ===")

    passed_count = 0
    results = []

    for idx, case in enumerate(cases):
        case_id = case.get("id", f"case_{idx}")
        name = case.get("name", "Cenário")
        loc_id = case.get("location_id")
        test_type = case.get("test_type", "business_rules")
        metrics_dict = case.get("metrics", {})
        expected = case.get("expected", {})

        logger.info(f"\n[{case_id}] {name} ({loc_id})...")

        try:
            # 1. Caso de Teste Especial: Audit Compliance (EV5)
            if test_type == "audit_compliance":
                forbidden_body = case.get("forbidden_body", "")
                draft = MessageDraft(
                    insured_id="TEST_001",
                    insured_name="Segurado Teste",
                    channel="app",
                    severity="red",
                    line_of_business="auto",
                    body=forbidden_body,
                    actions=["Verificar veículo"],
                    model_meta=ModelMeta(provider="test", model="test-model", is_fallback=True)
                )
                audit_res = audit_message(draft)
                exp_status = expected.get("audit_status")
                exp_violation = expected.get("violation")

                passed = audit_res.status.value == exp_status and exp_violation in audit_res.violations
                if passed:
                    passed_count += 1
                    logger.info(f"✅ {case_id} PASSED (Auditor bloqueou corretamente a frase proibida)")
                    results.append({"id": case_id, "status": "PASSED"})
                else:
                    failures = [f"Status auditado: {audit_res.status.value}, Violações: {audit_res.violations}"]
                    logger.error(f"❌ {case_id} FAILED: {failures}")
                    results.append({"id": case_id, "status": "FAILED", "errors": failures})
                continue

            # 2. Caso de Teste Especial: Resiliência / Fallback (EV7)
            if case.get("force_fallback"):
                from src.harness.runner import run_cycle
                res = run_cycle(loc_id, force_fixture=True)
                if res.used_fixture:
                    passed_count += 1
                    logger.info(f"✅ {case_id} PASSED (Fallback ativado com sucesso)")
                    results.append({"id": case_id, "status": "PASSED"})
                else:
                    logger.error(f"❌ {case_id} FAILED: Fallback não ativado")
                    results.append({"id": case_id, "status": "FAILED"})
                continue

            # 3. Caso de Teste Especial: Human-in-the-Loop (EV8)
            if case.get("operator_rejection_id"):
                from src.harness.runner import run_cycle
                rej_id = case.get("operator_rejection_id")
                res = run_cycle(loc_id, force_fixture=True, operator_rejections=[rej_id])
                # Verifica se a notificação para o ID rejeitado foi suprimida
                envios_simulados = [n for n in res.notification_logs if n.insured_id == rej_id]
                if len(envios_simulados) == expected.get("simulated_envios_count", 0):
                    passed_count += 1
                    logger.info(f"✅ {case_id} PASSED (Operador rejeitou {rej_id} com sucesso)")
                    results.append({"id": case_id, "status": "PASSED"})
                else:
                    logger.error(f"❌ {case_id} FAILED: Segurado rejeitado recebeu envio simulado")
                    results.append({"id": case_id, "status": "FAILED"})
                continue

            # 4. Caso Padrão: Regras de Negócio e Multi-Localidade
            loc = get_location_by_id(loc_id)
            location_ref = LocationRef(
                id=loc["id"], city=loc["city"], state=loc["state"],
                region=loc["region"], latitude=loc["latitude"],
                longitude=loc["longitude"], timezone=loc["timezone"]
            )

            weather_metrics = WeatherMetrics(
                precipitation_mm_h=metrics_dict.get("precipitation_mm_h"),
                precipitation_probability_pct=metrics_dict.get("precipitation_probability_pct"),
                wind_gusts_10m_kmh=metrics_dict.get("wind_gusts_10m_kmh"),
                weather_code=metrics_dict.get("weather_code"),
                cape_j_kg=metrics_dict.get("cape_j_kg"),
                lifted_index=metrics_dict.get("lifted_index")
            )
            signal = WeatherSignal(
                location=location_ref,
                forecast_generated_at=datetime.now(timezone.utc),
                forecast_valid_from=datetime.now(timezone.utc),
                forecast_valid_until=datetime.now(timezone.utc),
                metrics=weather_metrics,
                is_fixture=True
            )

            # Executa a matriz e a seleção sem monkey patching
            risk = apply_risk_matrix(signal)
            selection = select_insureds(risk, loc_id)

            case_passed = True
            failures = []

            # Valida hazard_type
            expected_hazard = expected.get("hazard_type")
            if expected_hazard and risk.hazard_type.value != expected_hazard:
                case_passed = False
                failures.append(f"Hazard: esperado={expected_hazard}, obtido={risk.hazard_type.value}")

            # Valida severity
            expected_severity = expected.get("severity")
            if expected_severity and (not risk.severity or risk.severity.value != expected_severity):
                case_passed = False
                failures.append(f"Severidade: esperada={expected_severity}, obtida={risk.severity.value if risk.severity else None}")

            # Valida elegíveis (se especificado)
            if "eligible_insured_ids" in expected:
                expected_eligible = set(expected.get("eligible_insured_ids", []))
                actual_eligible = set(item.insured_id for item in selection.items)
                if expected_eligible != actual_eligible:
                    case_passed = False
                    failures.append(f"Elegíveis: esperado={expected_eligible}, obtido={actual_eligible}")

            # Valida suprimidos (se especificado)
            if "suppressed_insured_ids" in expected:
                expected_suppressed = set(expected.get("suppressed_insured_ids", []))
                actual_suppressed = set(s.insured_id for s in selection.suppressed)
                if expected_suppressed and not expected_suppressed.issubset(actual_suppressed):
                    case_passed = False
                    failures.append(f"Suprimidos: esperado subconjunto de={expected_suppressed}, obtido={actual_suppressed}")

            if case_passed:
                passed_count += 1
                logger.info(f"✅ {case_id} PASSED (hazard={risk.hazard_type.value}, severity={risk.severity.value if risk.severity else None})")
                results.append({"id": case_id, "status": "PASSED"})
            else:
                logger.error(f"❌ {case_id} FAILED: {'; '.join(failures)}")
                results.append({"id": case_id, "status": "FAILED", "errors": failures})

        except Exception as exc:
            logger.error(f"💥 {case_id} CRASHED: {exc}", exc_info=True)
            results.append({"id": case_id, "status": "CRASHED", "error": str(exc)})

    pct = (passed_count / len(cases)) * 100
    logger.info(f"\n==================================================")
    logger.info(f"  RESULTADO FINAL DOS EVALS: {passed_count}/{len(cases)} PASSERAM ({pct:.1f}%)")
    logger.info(f"==================================================")


if __name__ == "__main__":
    run_evals()
