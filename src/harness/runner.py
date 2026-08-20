"""
MeteoRisco — Control Plane / Harness

Orquestra e controla o ciclo de execução multiagente de forma sequencial.
Aplica validação rígida de contratos e captura traces por etapa.
"""
import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from src.contracts.cycle import CycleResult, AgentTrace
from src.agents.scout import ScoutClimatico
from src.agents.analyst import AnalistaMeteoRisco
from src.agents.exposure_manager import GestorDeExposicao
from src.agents.writer import RedatorPreventivo
from src.agents.auditor import AuditordDeDecisao
from src.agents.notification_simulator import NotificationSimulator
from src.skills.load_domain import get_location_by_id

logger = logging.getLogger(__name__)

def run_cycle(
    location_id: str,
    force_fixture: bool = False,
    operator_rejections: Optional[list[str]] = None,
    approved_by: str = "operador",
) -> CycleResult:
    """
    Executa o ciclo sequencial completo do pipeline MeteoRisco.

    Fluxo:
    1. Valida a localidade informada.
    2. Inicializa o estado com cycle_id e timestamp.
    3. Executa em ordem canônica:
       Scout → Analista → Gestor de Exposição → Redator → Auditor → Simulator.
    4. Valida contratos de saída em cada etapa.
    5. Registra traces de observabilidade.
    6. Retorna o CycleResult completo.
    """
    run_at = datetime.now(timezone.utc)
    cycle_id = f"{location_id}_{run_at.strftime('%Y%m%dT%H%M%S')}_{str(uuid.uuid4())[:8]}"
    trace: list[AgentTrace] = []
    
    # 1. Validar localidade
    try:
        location = get_location_by_id(location_id)
    except ValueError as exc:
        logger.error(f"[Harness] Localidade inválida: {location_id}")
        return CycleResult(
            cycle_id=cycle_id,
            location_id=location_id,
            run_at=run_at,
            ok=False,
            errors=[str(exc)],
            trace=[]
        )

    # Inicializar agentes
    scout = ScoutClimatico()
    analyst = AnalistaMeteoRisco()
    exposure_manager = GestorDeExposicao()
    writer = RedatorPreventivo()
    auditor = AuditordDeDecisao()
    simulator = NotificationSimulator()

    # Estado intermediário
    weather_signal = None
    risk_assessment = None
    audience_selection = None
    message_drafts = []
    audit_results = []
    notification_logs = []
    used_fixture = force_fixture

    # --- 1. Scout Climático ---
    try:
        weather_signal, scout_trace = scout.run(location_id, force_fixture=force_fixture)
        trace.append(scout_trace)
        if weather_signal.is_fixture:
            used_fixture = True
    except Exception as exc:
        logger.error(f"[Harness] Falha no Scout: {exc}")
        return CycleResult(
            cycle_id=cycle_id, location_id=location_id, run_at=run_at,
            ok=False, errors=[f"Erro no Scout: {str(exc)}"], trace=trace,
            used_fixture=used_fixture
        )

    # --- 2. Analista MeteoRisco ---
    try:
        risk_assessment, analyst_trace = analyst.run(weather_signal)
        trace.append(analyst_trace)
    except Exception as exc:
        logger.error(f"[Harness] Falha no Analista: {exc}")
        return CycleResult(
            cycle_id=cycle_id, location_id=location_id, run_at=run_at,
            ok=False, errors=[f"Erro no Analista: {str(exc)}"], trace=trace,
            weather_signal=weather_signal, used_fixture=used_fixture
        )

    # --- 3. Gestor de Exposição ---
    try:
        audience_selection, manager_trace = exposure_manager.run(risk_assessment, location_id)
        trace.append(manager_trace)
    except Exception as exc:
        logger.error(f"[Harness] Falha no Gestor de Exposição: {exc}")
        return CycleResult(
            cycle_id=cycle_id, location_id=location_id, run_at=run_at,
            ok=False, errors=[f"Erro no Gestor de Exposição: {str(exc)}"], trace=trace,
            weather_signal=weather_signal, risk_assessment=risk_assessment,
            used_fixture=used_fixture
        )

    # --- 4. Redator Preventivo ---
    # Só gera mensagens se houver segurados elegíveis
    if audience_selection.items:
        try:
            message_drafts, writer_trace = writer.run(audience_selection, risk_assessment)
            trace.append(writer_trace)
            if any(d.model_meta and d.model_meta.is_fallback for d in message_drafts):
                used_fixture = True
        except Exception as exc:
            logger.error(f"[Harness] Falha no Redator: {exc}")
            return CycleResult(
                cycle_id=cycle_id, location_id=location_id, run_at=run_at,
                ok=False, errors=[f"Erro no Redator: {str(exc)}"], trace=trace,
                weather_signal=weather_signal, risk_assessment=risk_assessment,
                audience_selection=audience_selection, used_fixture=used_fixture
            )
    else:
        trace.append(
            AgentTrace(
                agent_name=writer.NAME,
                t_start=datetime.now(timezone.utc),
                t_end=datetime.now(timezone.utc),
                duration_ms=0.0,
                status="skipped",
                summary="Nenhum segurado elegível. Geração de mensagens ignorada."
            )
        )

    # --- 5. Auditor de Decisão ---
    if message_drafts:
        try:
            audit_results, auditor_trace = auditor.run(message_drafts)
            trace.append(auditor_trace)
        except Exception as exc:
            logger.error(f"[Harness] Falha no Auditor: {exc}")
            return CycleResult(
                cycle_id=cycle_id, location_id=location_id, run_at=run_at,
                ok=False, errors=[f"Erro no Auditor: {str(exc)}"], trace=trace,
                weather_signal=weather_signal, risk_assessment=risk_assessment,
                audience_selection=audience_selection, message_drafts=message_drafts,
                used_fixture=used_fixture
            )
    else:
        trace.append(
            AgentTrace(
                agent_name=auditor.NAME,
                t_start=datetime.now(timezone.utc),
                t_end=datetime.now(timezone.utc),
                duration_ms=0.0,
                status="skipped",
                summary="Nenhuma mensagem gerada. Auditoria ignorada."
            )
        )

    # --- 6. Notification Simulator ---
    if message_drafts and audit_results:
        try:
            notification_logs, simulator_trace = simulator.run(
                drafts=message_drafts,
                audit_results=audit_results,
                approved_by=approved_by,
                operator_rejections=operator_rejections
            )
            trace.append(simulator_trace)
        except Exception as exc:
            logger.error(f"[Harness] Falha no Notification Simulator: {exc}")
            return CycleResult(
                cycle_id=cycle_id, location_id=location_id, run_at=run_at,
                ok=False, errors=[f"Erro no Simulator: {str(exc)}"], trace=trace,
                weather_signal=weather_signal, risk_assessment=risk_assessment,
                audience_selection=audience_selection, message_drafts=message_drafts,
                audit_results=audit_results, used_fixture=used_fixture
            )
    else:
        trace.append(
            AgentTrace(
                agent_name=simulator.NAME,
                t_start=datetime.now(timezone.utc),
                t_end=datetime.now(timezone.utc),
                duration_ms=0.0,
                status="skipped",
                summary="Nenhuma simulação de envio executada."
            )
        )

    # Ciclo concluído com sucesso
    return CycleResult(
        cycle_id=cycle_id,
        location_id=location_id,
        run_at=run_at,
        ok=True,
        weather_signal=weather_signal,
        risk_assessment=risk_assessment,
        audience_selection=audience_selection,
        message_drafts=message_drafts,
        audit_results=audit_results,
        notification_logs=notification_logs,
        trace=trace,
        used_fixture=used_fixture
    )
