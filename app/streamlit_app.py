"""
MeteoRisco — Interface de Demonstração (Streamlit)

Apresenta a jornada completa do operador conforme a seção 23 do Master Plan v1.1,
destacando o 'Momento Uau': Mesmo evento climático -> destinatários e mensagens
completamente distintos por ramo (Auto vs Residencial), com justificativa auditável.
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timezone
import plotly.express as px
import plotly.graph_objects as go

from src.harness.runner import run_cycle
from src.skills.load_domain import load_locations, load_portfolio
from src.contracts.audit import AuditStatus

# Configuração da Página
st.set_page_config(
    page_title="MeteoRisco — Operação Preventiva Multiagente",
    page_icon="⛈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada para um design moderno e elegante
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0F172A 0%, #2563EB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 1.8rem;
    }
    .wow-box {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border: 2px solid #0284C7;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #FFFFFF;
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: center;
        border-top: 4px solid #2563EB;
    }
    .tag-auto {
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .tag-residential {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_dict=True)

# --- SIDEBAR ---
st.sidebar.image("https://img.icons8.com/color/96/storm.png", width=70)
st.sidebar.title("MeteoRisco Control Plane")
st.sidebar.markdown("---")

locations = load_locations()
location_options = {f"{loc['city']} ({loc['state']})": loc["id"] for loc in locations}
selected_label = st.sidebar.selectbox("Localidade-Piloto:", list(location_options.keys()))
location_id = location_options[selected_label]

weather_mode = st.sidebar.radio(
    "Fonte Meteorológica:",
    ["Extremo (Fixture Offline)", "Live (API Open-Meteo)"],
    index=0
)
force_fixture = "Extremo" in weather_mode

st.sidebar.markdown("---")
st.sidebar.markdown("### LLM Gateway")
llm_choice = st.sidebar.selectbox("Provedor LLM:", ["Template Offline (Default)", "Google Gemini", "OpenAI"])

if llm_choice == "Google Gemini":
    gemini_key = st.sidebar.text_input("Gemini API Key:", type="password")
    if gemini_key:
        from src.config import settings
        settings.llm_provider = "gemini"
        settings.gemini_api_key = gemini_key
        settings.llm_model = "gemini-2.0-flash"
elif llm_choice == "OpenAI":
    openai_key = st.sidebar.text_input("OpenAI API Key:", type="password")
    if openai_key:
        from src.config import settings
        settings.llm_provider = "openai"
        settings.openai_api_key = openai_key
        settings.llm_model = "gpt-4o-mini"
else:
    from src.config import settings
    settings.llm_provider = None

# --- HEADER PRINCIPAL ---
st.markdown('<div class="main-header">MeteoRisco</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Do clima ao risco. Do risco à ação. (Desafio 5 — InsurMinds / I2A2)</div>', unsafe_allow_html=True)

loc_data = next(l for l in locations if l["id"] == location_id)

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"📍 **{loc_data['city']} / {loc_data['state']}** ({loc_data['region'].upper()}) — *{loc_data['climate_profile']}*")
with col2:
    if st.button("⚡ Executar Ciclo Multiagente", type="primary", use_container_width=True):
        st.session_state["executed"] = True
        st.session_state["result"] = run_cycle(location_id, force_fixture=force_fixture)
        st.session_state["operator_rejections"] = []

st.markdown("---")

if st.session_state.get("executed"):
    result = st.session_state["result"]

    if not result.ok:
        st.error(f"Erro na execução: {result.errors}")
    else:
        # KPI Cards
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f'<div class="metric-card"><h4>Localidade</h4><h3>{loc_data["city"]}</h3></div>', unsafe_allow_html=True)
        with k2:
            hazard_txt = result.risk_assessment.hazard_type.value.upper() if result.risk_assessment else "NONE"
            sev_txt = result.risk_assessment.severity.value.upper() if (result.risk_assessment and result.risk_assessment.severity) else "OK"
            st.markdown(f'<div class="metric-card"><h4>Risco Classificado</h4><h3 style="color:#DC2626;">{hazard_txt} ({sev_txt})</h3></div>', unsafe_allow_html=True)
        with k3:
            eleg = result.audience_selection.total_eligible if result.audience_selection else 0
            st.markdown(f'<div class="metric-card"><h4>Segurados Elegíveis</h4><h3 style="color:#2563EB;">{eleg}</h3></div>', unsafe_allow_html=True)
        with k4:
            sup = result.audience_selection.total_suppressed if result.audience_selection else 0
            st.markdown(f'<div class="metric-card"><h4>Silêncio Inteligente</h4><h3 style="color:#D97706;">{sup} suprimidos</h3></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Tabs da Jornada do Operador
        tab_wow, tab_weather, tab_risk, tab_audience, tab_drafts, tab_hitl, tab_trace = st.tabs([
            "✨ Momento Uau (Diferenciação por Ramo)",
            "1. Sinal Meteorológico",
            "2. Avaliação de Risco",
            "3. Elegibilidade & Supressão",
            "4. Rascunhos de Mensagem",
            "5. Aprovação Human-in-the-Loop",
            "6. Observabilidade & Trace"
        ])

        # --- TAB MOMENTO UAU ---
        with tab_wow:
            st.markdown("""
            <div class="wow-box">
                <h3>🌟 O Momento Uau do MeteoRisco</h3>
                <p>O mesmo evento climático afeta carteiras de forma distinta. Veja como a arquitetura híbrida diferencia a comunicação e as orientações para o <b>Ramo Automóvel</b> vs <b>Ramo Residencial</b> de forma totalmente auditável.</p>
            </div>
            """, unsafe_allow_html=True)

            if result.message_drafts:
                auto_drafts = [d for d in result.message_drafts if d.line_of_business == "auto"]
                res_drafts = [d for d in result.message_drafts if d.line_of_business == "residential"]

                col_auto, col_res = st.columns(2)

                with col_auto:
                    st.markdown("#### 🚗 Ramo Automóvel")
                    if auto_drafts:
                        d = auto_drafts[0]
                        st.markdown(f'<span class="tag-auto">Destinatário: {d.insured_name}</span>', unsafe_allow_html=True)
                        st.write(f"**Canal:** {d.channel.upper()}")
                        st.text_area("Mensagem Gerada (Auto):", d.body, height=180, key="wow_auto", disabled=True)
                        st.write("**Ações Recomendadas (Auto):**")
                        for act in d.actions:
                            st.write(f"- 🚗 {act}")
                    else:
                        st.info("Nenhum segurado do Ramo Automóvel elegível ou suprimido por garagem coberta.")

                with col_res:
                    st.markdown("#### 🏠 Ramo Residencial")
                    if res_drafts:
                        d = res_drafts[0]
                        st.markdown(f'<span class="tag-residential">Destinatário: {d.insured_name}</span>', unsafe_allow_html=True)
                        st.write(f"**Canal:** {d.channel.upper()}")
                        st.text_area("Mensagem Gerada (Residencial):", d.body, height=180, key="wow_res", disabled=True)
                        st.write("**Ações Recomendadas (Residencial):**")
                        for act in d.actions:
                            st.write(f"- 🏠 {act}")
                    else:
                        st.info("Nenhum segurado do Ramo Residencial elegível nesta localidade.")
            else:
                st.info("Nenhuma ameaça acionada para demonstrar mensagens. Alterne a fonte para 'Extremo (Fixture Offline)'.")

        # --- TAB METEOROLOGIA ---
        with tab_weather:
            st.markdown("### 📡 Sinal Meteorológico Normalizado (Open-Meteo)")
            sig = result.weather_signal
            st.write(f"**Fonte:** {sig.source} | **Forecast Objeto em:** {sig.forecast_generated_at} (Validade: {sig.forecast_valid_from.strftime('%H:%M')} a {sig.forecast_valid_until.strftime('%H:%M')})")
            
            m = sig.metrics
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Precipitação Prevista", f"{m.precipitation_mm_h or 0} mm/h")
            c2.metric("Rajadas de Vento", f"{m.wind_gusts_10m_kmh or 0} km/h")
            c3.metric("Código WMO", str(m.weather_code or 0))
            c4.metric("Instabilidade (CAPE)", f"{m.cape_j_kg or 0} J/kg")

            # Gráfico Plotly
            df_plot = pd.DataFrame({
                "Indicador": ["Precipitação (mm/h)", "Rajadas Vento (km/h)", "CAPE (J/kg / 50)"],
                "Valor": [m.precipitation_mm_h or 0, m.wind_gusts_10m_kmh or 0, (m.cape_j_kg or 0)/50]
            })
            fig = px.bar(df_plot, x="Indicador", y="Valor", color="Indicador", title="Valores de Pico Previstos")
            st.plotly_chart(fig, use_container_width=True)

        # --- TAB RISCO ---
        with tab_risk:
            st.markdown("### 🧠 Classificação Determinística do Analista")
            risk = result.risk_assessment
            st.write(f"**Hazard Identificado:** `{risk.hazard_type.value}`")
            st.write(f"**Severidade:** `{risk.severity.value if risk.severity else 'Nenhuma'}`")
            st.info(f"**Justificativa (Rationale):** {risk.rationale}")
            st.json(risk.triggered_metrics)

        # --- TAB CARTEIRA E SUPRESSÃO ---
        with tab_audience:
            st.markdown("### 👥 Seleção de Carteira e Silêncio Inteligente")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("#### ✅ Segurados Elegíveis")
                if result.audience_selection.items:
                    st.table(pd.DataFrame([
                        {"ID": i.insured_id, "Nome": i.insured_name, "Ramo": i.line_of_business, "Exposição": i.exposure_profile, "Prioridade": i.priority}
                        for i in result.audience_selection.items
                    ]))
                else:
                    st.write("Nenhum segurado elegível.")
            with col_b:
                st.markdown("#### 🛡️ Segurados Suprimidos (Silêncio)")
                if result.audience_selection.suppressed:
                    st.table(pd.DataFrame([
                        {"ID": s.insured_id, "Nome": s.insured_name, "Motivo": s.suppression_reason, "Detalhes": s.suppression_detail}
                        for s in result.audience_selection.suppressed
                    ]))

        # --- TAB DRAFTS ---
        with tab_drafts:
            st.markdown("### 📝 Mensagens Geradas e Auditoria")
            for d in result.message_drafts:
                audit = next((r for r in result.audit_results if r.insured_id == d.insured_id), None)
                st_txt = audit.status.value.upper() if audit else "PENDENTE"
                with st.expander(f"{d.insured_name} ({d.line_of_business.upper()}) - Status Auditoria: {st_txt}"):
                    st.write(f"**Assunto:** {d.subject or 'N/A'}")
                    st.write(f"**Corpo:**\n{d.body}")
                    st.write(f"**Modelo Meta:** Provider={d.model_meta.provider if d.model_meta else 'template'} | Fallback={d.model_meta.is_fallback if d.model_meta else True}")

        # --- TAB HITL ---
        with tab_hitl:
            st.markdown("### 🤝 Human-in-the-Loop (Aprovação do Operador)")
            st.write("Aprovação manual antes da simulação de envio:")
            
            rejections = []
            for d in result.message_drafts:
                audit = next((r for r in result.audit_results if r.insured_id == d.insured_id), None)
                if audit and audit.status == AuditStatus.BLOCKED:
                    st.error(f"🚫 {d.insured_name} ({d.insured_id}) BLOQUEADO pelo Auditor de Conformidade. Envio impedido.")
                else:
                    appr = st.checkbox(f"Aprovar Envio Simulado para {d.insured_name} ({d.channel.upper()})", value=True, key=f"appr_{d.insured_id}")
                    if not appr:
                        rejections.append(d.insured_id)

            if st.button("Confirmar Operação", type="primary"):
                from src.agents.notification_simulator import NotificationSimulator
                sim = NotificationSimulator()
                logs, trace_sim = sim.run(
                    drafts=result.message_drafts,
                    audit_results=result.audit_results,
                    approved_by="operador_humano",
                    operator_rejections=rejections
                )
                st.success(f"Simulação concluída! {len(logs)} notificações confirmadas.")
                if logs:
                    st.table(pd.DataFrame([
                        {"Segurado": l.insured_name, "Canal": l.channel, "Ref Hash": l.payload_ref[:12], "Horário": l.timestamp}
                        for l in logs
                    ]))

        # --- TAB TRACE ---
        with tab_trace:
            st.markdown("### 📊 Observabilidade e Trilha por Agente (CycleResult)")
            st.write(f"Cycle ID: `{result.cycle_id}` | Duração: `{result.cycle_duration_ms:.2f} ms`")
            for t in result.trace:
                st.markdown(f"- **{t.agent_name}** (`{t.status.upper()}`) - {t.duration_ms:.1f}ms: *{t.summary}*")
else:
    st.info("💡 Selecione a localidade desejada na barra lateral e clique em **Executar Ciclo Multiagente** para visualizar a demonstração.")
