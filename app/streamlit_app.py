"""
MeteoRisco — Interface Executiva de Demonstração (Streamlit)
Arquitetura Multiagente de Prevenção de Sinistros Climáticos

Design: Dark-Mode First · Neurodesign · Seguros & Inteligência Artificial
"""
import sys
import os
import json
import html
from pathlib import Path

# Determina a raiz do projeto de forma resiliente
_current_dir = Path(__file__).resolve().parent
_root_dir = _current_dir if (_current_dir / "src").exists() else _current_dir.parent
if str(_root_dir) not in sys.path:
    sys.path.insert(0, str(_root_dir))

import streamlit as st
import pandas as pd
from datetime import datetime, timezone
import plotly.express as px
import plotly.graph_objects as go

from src.harness.runner import run_cycle
from src.skills.load_domain import load_locations, load_portfolio
from src.contracts.audit import AuditStatus
from src.config import settings

# ─── CONFIGURAÇÃO DA PÁGINA ──────────────────────────────────────────────────
st.set_page_config(
    page_title="MeteoRisco — Inteligência Preventiva de Sinistros",
    page_icon="⛈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── NEURODESIGN SYSTEM (DARK MODE FIRST) ────────────────────────────────────
# Paleta Temática: Seguros (Confiança/Proteção) + IA (Cyan/Índigo) + MeteoRisco (Severidade)
st.markdown("""
<style>
    /* Reset & Base Dark Mode */
    .stApp {
        background-color: #070B12;
        color: #F8FAFC;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    section[data-testid="stSidebar"] {
        background-color: #0B132B !important;
        border-right: 1px solid rgba(56, 189, 248, 0.15) !important;
    }

    /* Cabeçalho Principal Hero (Neurodesign & Modern Aesthetics) */
    .brand-hero {
        margin-bottom: 2.35rem;
    }
    .brand-title-wrap {
        display: flex;
        align-items: center;
        gap: 0.85rem;
        margin-bottom: 0.25rem;
    }
    .brand-icon {
        font-size: 2.75rem;
        line-height: 1;
        filter: drop-shadow(0 0 16px rgba(56, 189, 248, 0.5));
    }
    .brand-name {
        font-size: 2.75rem;
        font-weight: 900;
        letter-spacing: -0.035em;
        background: linear-gradient(135deg, #FFFFFF 20%, #7DD3FC 65%, #38BDF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
        margin: 0;
        padding: 0;
        filter: drop-shadow(0 2px 14px rgba(56, 189, 248, 0.3));
    }
    .brand-subtitle-line {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.75rem;
        font-size: 0.98rem;
        line-height: 1.4;
        margin-top: 0.25rem;
    }
    .brand-sub-main {
        color: #F8FAFC;
        font-weight: 600;
        letter-spacing: 0.01em;
    }
    .brand-sub-sep {
        color: #475569;
        font-weight: 400;
    }
    .brand-sub-tag {
        color: #38BDF8;
        font-weight: 600;
        letter-spacing: 0.02em;
        background: rgba(14, 165, 233, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.28);
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.82rem;
    }

    /* Elimina caixas, molduras e fundos delimitadores das colunas de topo */
    div[data-testid="column"] div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="column"] div[data-testid="stVerticalBlockBorderWrapper"] > div {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
        padding: 0 !important;
    }

    /* Elimina qualquer moldura, fundo retangular ou camada espúria gerada pelo Plotly Geo */
    div[data-testid="stPlotlyChart"] .layer.bg,
    div[data-testid="stPlotlyChart"] .layer.frame,
    div[data-testid="stPlotlyChart"] .layer.ocean,
    div[data-testid="stPlotlyChart"] .layer.land,
    div[data-testid="stPlotlyChart"] .layer.lakes,
    div[data-testid="stPlotlyChart"] .layer.rivers,
    div[data-testid="stPlotlyChart"] .layer.countries,
    div[data-testid="stPlotlyChart"] .layer.coastlines,
    div[data-testid="stPlotlyChart"] .layer.subunits,
    div[data-testid="stPlotlyChart"] g.geo > g.layer:not(.frontplot):not(.backplot),
    div[data-testid="stPlotlyChart"] svg rect.bg,
    div[data-testid="stPlotlyChart"] svg path.bg,
    div[data-testid="stPlotlyChart"] svg .bg,
    div[data-testid="stPlotlyChart"] .bgrect,
    .js-plotly-plot .plotly svg g.geo > g.layer:not(.frontplot):not(.backplot),
    .js-plotly-plot .plotly svg .layer.bg,
    .js-plotly-plot .plotly svg .layer.frame,
    .js-plotly-plot .plotly svg .layer.ocean {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        fill: transparent !important;
        fill-opacity: 0 !important;
        stroke: transparent !important;
        stroke-width: 0 !important;
    }

    /* Card Cidade-Piloto (Neurodesign Integrado) */
    .pilot-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.6) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 12px;
        padding: 0.95rem 1.1rem;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.5);
    }
    .pilot-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.35rem;
    }
    .pilot-badge-live {
        font-size: 0.7rem;
        font-weight: 800;
        color: #38BDF8;
        background: rgba(14, 165, 233, 0.16);
        border: 1px solid rgba(56, 189, 248, 0.35);
        padding: 0.15rem 0.55rem;
        border-radius: 20px;
        letter-spacing: 0.04em;
    }
    .pilot-city-name {
        font-size: 1.35rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.2;
    }
    .pilot-city-state {
        color: #38BDF8;
        font-size: 1.05rem;
        font-weight: 600;
    }
    .pilot-coords {
        font-size: 0.82rem;
        color: #94A3B8;
        margin-top: 0.25rem;
        line-height: 1.35;
    }
    .pilot-climate-pill {
        font-size: 0.78rem;
        color: #CBD5E1;
        background: rgba(15, 23, 42, 0.85);
        padding: 0.45rem 0.65rem;
        border-radius: 8px;
        border-left: 3px solid #38BDF8;
        margin-top: 0.65rem;
        line-height: 1.35;
    }

    /* Centro de Comando Executivo */
    .command-hub-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.6) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 12px;
        padding: 0.95rem 1.1rem;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.5);
        margin-bottom: 0.65rem;
    }
    .hub-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(148, 163, 184, 0.15);
        padding-bottom: 0.45rem;
        margin-bottom: 0.65rem;
    }
    .hub-title {
        font-size: 0.76rem;
        font-weight: 800;
        color: #38BDF8;
        letter-spacing: 0.08em;
    }
    .hub-status-badge {
        font-size: 0.7rem;
        font-weight: 700;
        color: #34D399;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(52, 211, 153, 0.35);
        padding: 0.15rem 0.5rem;
        border-radius: 20px;
    }
    .hub-param-row {
        margin-bottom: 0.5rem;
    }
    .hub-param-label {
        font-size: 0.68rem;
        font-weight: 700;
        color: #94A3B8;
        letter-spacing: 0.04em;
        margin-bottom: 0.1rem;
    }
    .hub-param-value {
        font-size: 0.86rem;
        color: #F8FAFC;
        font-weight: 600;
    }
    .hub-pipeline-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(15, 23, 42, 0.7);
        border-radius: 8px;
        padding: 0.35rem 0.6rem;
        border: 1px solid rgba(148, 163, 184, 0.12);
        margin-top: 0.35rem;
    }

    /* Botão Primário - Neurodesign Call-to-Action */
    div.stButton > button:first-child[kind="primary"] {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #38BDF8 !important;
        border-radius: 10px !important;
        font-size: 0.96rem !important;
        font-weight: 700 !important;
        padding: 0.65rem 1.0rem !important;
        box-shadow: 0 4px 16px rgba(2, 132, 199, 0.35) !important;
        transition: all 0.25s ease !important;
    }
    div.stButton > button:first-child[kind="primary"]:hover {
        background: linear-gradient(135deg, #0369A1 0%, #075985 100%) !important;
        border-color: #7DD3FC !important;
        box-shadow: 0 6px 22px rgba(56, 189, 248, 0.5) !important;
        transform: translateY(-2px) !important;
    }

    /* Cards de Alta Performance Cognitiva (Glassmorphism Escuro) */
    .neuro-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 14px;
        padding: 1.25rem;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.45);
        backdrop-filter: blur(12px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .neuro-card:hover {
        border-color: rgba(56, 189, 248, 0.35);
    }

    /* Cartões de Métricas com Destaque Semântico */
    .metric-container {
        background: rgba(15, 23, 42, 0.85);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        border: 1px solid rgba(148, 163, 184, 0.15);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .metric-container.accent-blue { border-top: 4px solid #38BDF8; }
    .metric-container.accent-red { border-top: 4px solid #EF4444; }
    .metric-container.accent-green { border-top: 4px solid #10B981; }
    .metric-container.accent-amber { border-top: 4px solid #F59E0B; }

    .metric-label {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94A3B8;
        margin-bottom: 0.35rem;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.65rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.02em;
    }

    /* Badges de Ramos e Status */
    .badge-auto {
        background: rgba(14, 165, 233, 0.16);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.35);
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
    }
    .badge-res {
        background: rgba(16, 185, 129, 0.16);
        color: #34D399;
        border: 1px solid rgba(52, 211, 153, 0.35);
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
    }
    .badge-silence {
        background: rgba(245, 158, 11, 0.14);
        color: #FBBF24;
        border: 1px solid rgba(251, 191, 36, 0.3);
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
    }
    .badge-approved {
        background: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid #10B981;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 700;
    }

    /* Container do Momento Uau */
    .wow-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 1.5rem;
    }

    /* Pipeline Step Tracker */
    .pipeline-step {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 10px;
        padding: 0.8rem 1rem;
        text-align: left;
    }
    .pipeline-step.active {
        border-color: #38BDF8;
        background: rgba(14, 165, 233, 0.08);
    }

    /* Mensagens Preventivas (Neurodesign - Alto Contraste & Legibilidade Cristalina) */
    .message-bubble {
        background: #0B132B !important;
        border: 1px solid rgba(148, 163, 184, 0.28) !important;
        border-radius: 10px !important;
        padding: 1.1rem 1.25rem !important;
        margin: 0.85rem 0 !important;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.5) !important;
    }
    .message-bubble.auto {
        border-left: 5px solid #38BDF8 !important;
    }
    .message-bubble.res {
        border-left: 5px solid #34D399 !important;
    }
    .message-meta {
        display: flex;
        justify-content: space-between;
        font-size: 0.82rem;
        color: #94A3B8;
        border-bottom: 1px solid rgba(148, 163, 184, 0.15);
        padding-bottom: 0.45rem;
        margin-bottom: 0.75rem;
    }
    .message-content {
        color: #FFFFFF !important;
        font-size: 1.0rem !important;
        font-weight: 400 !important;
        line-height: 1.7 !important;
        white-space: pre-wrap !important;
        font-family: inherit !important;
        letter-spacing: 0.01em !important;
    }

    /* Badges de Ações Recomendadas (Substituindo blocos mono/backticks) */
    .action-badge {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        border-radius: 8px !important;
        padding: 0.65rem 0.95rem !important;
        margin-bottom: 0.5rem !important;
        display: flex;
        align-items: center;
        gap: 0.7rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
    }
    .action-badge.res {
        border-color: rgba(52, 211, 153, 0.35) !important;
    }
    .action-icon {
        font-size: 1.2rem;
    }
    .action-text {
        color: #F8FAFC !important;
        font-size: 0.94rem !important;
        font-weight: 500 !important;
        line-height: 1.45 !important;
    }

    /* Override Global para TextAreas caso utilizadas */
    .stTextArea textarea:disabled, .stTextArea textarea {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        background-color: #0B132B !important;
        opacity: 1 !important;
        border: 1px solid rgba(148, 163, 184, 0.3) !important;
        font-size: 0.98rem !important;
        line-height: 1.6 !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR: CONTROLES & CONFIGURAÇÕES ───────────────────────────────────────
with st.sidebar:
    st.markdown("### ⛈️ MeteoRisco Control")
    st.caption("Sistema Multiagente de Loss Prevention")
    st.markdown("---")

    # 1. Localidade-Piloto
    locations = load_locations()
    location_options = {f"{loc['city']} ({loc['state']}) — {loc['region'].upper()}": loc["id"] for loc in locations}
    selected_label = st.selectbox("📍 Cidade-Piloto:", list(location_options.keys()))
    location_id = location_options[selected_label]
    loc_data = next(l for l in locations if l["id"] == location_id)

    # 2. Seletor de Cenário
    st.markdown("#### 🎯 Cenário Meteorológico:")
    scenario_choice = st.radio(
        "Selecione o modo de teste:",
        [
            "⛈️ Tempestade Severa (Simulação de Estresse)",
            "☀️ Clima Normal (Silêncio Inteligente)",
            "📡 Tempo Real ao Vivo (Open-Meteo Live API)"
        ],
        index=0,
        help=(
            "• Tempestade Severa: Dados de tempestade convectiva (WMO 99, CAPE > 2000 J/kg) para testar alertas e o Momento Uau.\n"
            "• Clima Normal: Dados históricos calmos para demonstrar o Silêncio Inteligente (Anti-Spam).\n"
            "• Tempo Real: Consulta a previsão ao vivo das próximas 48h."
        )
    )

    force_extreme = "Tempestade Severa" in scenario_choice
    force_fixture = "Clima Normal" in scenario_choice

    st.markdown("---")

    # 3. LLM Gateway
    st.markdown("#### 🤖 LLM Gateway:")
    llm_choice = st.selectbox(
        "Provedor do Redator:",
        ["Template Offline (Determinístico)", "Google Gemini", "OpenAI"],
        help="Escolha entre template offline seguro ou inteligência generativa via API."
    )

    if llm_choice == "Google Gemini":
        gemini_key = st.text_input("Gemini API Key:", type="password", help="Insira sua chave AI Studio")
        if gemini_key:
            settings.llm_provider = "gemini"
            settings.gemini_api_key = gemini_key
            settings.llm_model = "gemini-2.0-flash"
            st.success("🟢 Gemini 2.0 Flash Conectado", icon="✅")
        else:
            settings.llm_provider = None
            st.warning("Insira a chave ou use o Template Offline", icon="⚠️")
    elif llm_choice == "OpenAI":
        openai_key = st.text_input("OpenAI API Key:", type="password")
        if openai_key:
            settings.llm_provider = "openai"
            settings.openai_api_key = openai_key
            settings.llm_model = "gpt-4o-mini"
            st.success("🟢 OpenAI Conectado", icon="✅")
        else:
            settings.llm_provider = None
            st.warning("Insira a chave da OpenAI", icon="⚠️")
    else:
        settings.llm_provider = None
        st.info("🟡 Template Offline (100% Gratuito & Seguro)", icon="🛡️")

# ─── FUNÇÃO DO MAPA DO BRASIL (IBGE + PLOTLY) ───────────────────────────────
@st.cache_data(ttl=86400)
def load_ibge_regions():
    candidates = [
        _root_dir / "fixtures" / "ibge_regioes_brasil_expanded.geojson",
        Path("fixtures/ibge_regioes_brasil_expanded.geojson"),
    ]
    for p in candidates:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

    fallback_candidates = [
        _root_dir / "fixtures" / "ibge_regioes_brasil.geojson",
        Path("fixtures/ibge_regioes_brasil.geojson"),
    ]
    for p in fallback_candidates:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                new_features = []
                for feat in data.get("features", []):
                    geom = feat.get("geometry", {})
                    code = str(feat.get("properties", {}).get("codarea"))
                    if geom.get("type") == "MultiPolygon":
                        for poly_coords in geom.get("coordinates", []):
                            new_features.append({
                                "type": "Feature",
                                "properties": {"codarea": code},
                                "geometry": {"type": "Polygon", "coordinates": poly_coords}
                            })
                    else:
                        new_features.append(feat)
                return {"type": "FeatureCollection", "features": new_features}
        except Exception:
            pass
    return None

def build_brazil_map(selected_city_id: str):
    geojson = load_ibge_regions()
    city_to_code = {"belem": "1", "recife": "2", "sao_paulo": "3", "porto_alegre": "4", "brasilia": "5"}
    active_code = city_to_code.get(selected_city_id, "1")

    palette = {
        "1": {"name": "Região Norte", "line": "#38BDF8", "fill": "rgba(56, 189, 248, 0.14)", "desc": "7 Estados · Convecção Equatorial"},
        "2": {"name": "Região Nordeste", "line": "#60A5FA", "fill": "rgba(96, 165, 250, 0.14)", "desc": "9 Estados · Chuvas Costeiras"},
        "3": {"name": "Região Sudeste", "line": "#34D399", "fill": "rgba(52, 211, 153, 0.14)", "desc": "4 Estados · Densidade Auto & Residencial"},
        "4": {"name": "Região Sul", "line": "#FBBF24", "fill": "rgba(251, 191, 36, 0.14)", "desc": "3 Estados · Frentes Frias & Granizo"},
        "5": {"name": "Região Centro-Oeste", "line": "#C084FC", "fill": "rgba(192, 132, 252, 0.14)", "desc": "3 Estados + DF · Instabilidade de Verão"},
    }

    fig = go.Figure()

    if geojson:
        for code in ["1", "2", "3", "4", "5"]:
            polys = [f for f in geojson.get("features", []) if f.get("properties", {}).get("codarea") == code]
            if not polys:
                continue
            polys.sort(key=lambda x: len(x.get("geometry", {}).get("coordinates", [[]])[0]), reverse=True)
            main = polys[0]
            ring = main.get("geometry", {}).get("coordinates", [[]])[0]
            lons = [p[0] for p in ring]
            lats = [p[1] for p in ring]

            is_active = (code == active_code)
            meta = palette.get(code, {"name": f"Região {code}", "line": "#38BDF8", "fill": "rgba(56, 189, 248, 0.1)", "desc": ""})

            line_col = "#38BDF8" if is_active else meta["line"]
            line_w = 3.2 if is_active else 1.8
            fill_col = "rgba(56, 189, 248, 0.28)" if is_active else meta["fill"]

            fig.add_trace(go.Scatter(
                x=lons,
                y=lats,
                mode="lines",
                fill="toself",
                fillcolor=fill_col,
                line=dict(color=line_col, width=line_w),
                name=meta["name"],
                hoverinfo="text",
                text=f"<b>{meta['name']}</b>{' [ATIVA]' if is_active else ''}<br>{meta['desc']}"
            ))

    # Cidades-piloto
    cities = [
        {"id": "belem", "name": "Belém", "state": "PA", "lat": -1.4558, "lon": -48.4902},
        {"id": "recife", "name": "Recife", "state": "PE", "lat": -8.0476, "lon": -34.8770},
        {"id": "brasilia", "name": "Brasília", "state": "DF", "lat": -15.7975, "lon": -47.8919},
        {"id": "sao_paulo", "name": "São Paulo", "state": "SP", "lat": -23.5505, "lon": -46.6333},
        {"id": "porto_alegre", "name": "Porto Alegre", "state": "RS", "lat": -30.0346, "lon": -51.2177},
    ]

    others = [c for c in cities if c["id"] != selected_city_id]
    fig.add_trace(go.Scatter(
        x=[c["lon"] for c in others],
        y=[c["lat"] for c in others],
        text=[f"{c['name']} ({c['state']})" for c in others],
        mode="markers+text",
        textposition="bottom center",
        textfont=dict(size=9.5, color="#94A3B8", family="Inter, sans-serif"),
        marker=dict(size=7, color="#334155", line=dict(width=1.5, color="#94A3B8")),
        hoverinfo="text"
    ))

    sel = next((c for c in cities if c["id"] == selected_city_id), cities[0])
    fig.add_trace(go.Scatter(
        x=[sel["lon"]],
        y=[sel["lat"]],
        mode="markers",
        marker=dict(size=24, color="rgba(56, 189, 248, 0.35)", symbol="circle"),
        hoverinfo="none"
    ))
    fig.add_trace(go.Scatter(
        x=[sel["lon"]],
        y=[sel["lat"]],
        text=[f"<b>{sel['name']} ({sel['state']})</b>"],
        mode="markers+text",
        textposition="top center",
        textfont=dict(size=11.5, color="#38BDF8", family="Inter, sans-serif"),
        marker=dict(size=11, color="#38BDF8", line=dict(width=2.5, color="#FFFFFF")),
        hoverinfo="text"
    ))

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=340,
        xaxis=dict(range=[-74.0, -34.5], visible=False, showgrid=False, zeroline=False),
        yaxis=dict(range=[-34.0, 5.5], visible=False, showgrid=False, zeroline=False, scaleanchor="x", scaleratio=1),
        hovermode="closest"
    )
    return fig

# ─── HEADER HERO & LAYOUT HARMONIZADO ─────────────────────────────────────────
st.markdown("""
<div class="brand-hero">
    <div class="brand-title-wrap">
        <span class="brand-icon">⛈️</span>
        <span class="brand-name">MeteoRisco</span>
    </div>
    <div class="brand-subtitle-line">
        <span class="brand-sub-main">Do clima ao risco. Do risco à ação.</span>
        <span class="brand-sub-sep">—</span>
        <span class="brand-sub-tag">Inteligência Preventiva para Seguros Auto & Residencial</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Layout em 3 Colunas: Cards Laterais Perfeitamente Alinhados & Mapa Central Livre e Ampliado
top_col1, top_col2, top_col3 = st.columns([1.05, 1.65, 1.05], gap="large")

with top_col1:
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; justify-content: space-between; height: 340px; padding: 0.15rem 0;">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.55rem;">
                <span class="pilot-badge-live">● CIDADE-PILOTO ATIVA</span>
                <span class="hub-status-badge">● ONLINE</span>
            </div>
            <div style="font-size: 1.6rem; font-weight: 800; color: #FFFFFF; line-height: 1.2; margin-top: 0.35rem;">
                {loc_data['city']} <span style="color: #38BDF8; font-size: 1.2rem; font-weight: 600;">({loc_data['state']})</span>
            </div>
            <div style="font-size: 0.84rem; color: #94A3B8; margin-top: 0.35rem; line-height: 1.4;">
                <b style="color: #E2E8F0;">Região:</b> {loc_data['region'].upper()} · <b style="color: #E2E8F0;">Coord:</b> {loc_data['latitude']:.4f}, {loc_data['longitude']:.4f}
            </div>
            <div class="pilot-climate-pill" style="margin-top: 0.95rem;">
                🌿 {loc_data['climate_profile']}
            </div>
        </div>
        <div style="padding-top: 0.85rem; border-top: 1px solid rgba(148, 163, 184, 0.15); display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-size: 0.68rem; font-weight: 700; color: #94A3B8;">APÓLICES ATIVAS</div>
                <div style="font-size: 0.9rem; font-weight: 700; color: #F8FAFC;">4 Segurados na Base</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.68rem; font-weight: 700; color: #94A3B8;">MONITORAMENTO</div>
                <div style="font-size: 0.9rem; font-weight: 700; color: #34D399;">● Satélite Conectado</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with top_col2:
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 0.2rem;">
        <span style="font-size: 0.78rem; font-weight: 800; color: #38BDF8; letter-spacing: 0.06em; text-transform: uppercase;">🗺️ Malha Territorial · 5 Regiões IBGE</span>
        <span style="font-size: 0.72rem; color: #94A3B8; font-weight: 600; margin-left: 0.5rem;">Região Ativa: <b style="color: #38BDF8;">{loc_data['region'].upper()}</b></span>
    </div>
    """, unsafe_allow_html=True)
    map_fig = build_brazil_map(location_id)
    st.plotly_chart(map_fig, use_container_width=True, theme=None, config={"displayModeBar": False, "scrollZoom": False})

with top_col3:
    scenario_label = scenario_choice.split('(')[0].strip()
    scenario_icon = "🌩️" if "Tempestade" in scenario_choice else "☀️"
    gateway_badge = "🛡️ Template Offline (Determinístico)" if llm_choice == "Offline" else f"🤖 {llm_choice}"

    st.markdown(f"""
    <div style="display: flex; flex-direction: column; justify-content: space-between; height: 200px; padding: 0.15rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(148, 163, 184, 0.15); padding-bottom: 0.55rem;">
            <span style="font-size: 0.78rem; font-weight: 800; color: #38BDF8; letter-spacing: 0.08em;">⚡ CENTRO DE COMANDO</span>
            <span class="hub-status-badge">● PRONTO</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.35rem;">
            <span style="font-size: 0.72rem; font-weight: 700; color: #94A3B8; letter-spacing: 0.04em;">CENÁRIO:</span>
            <span style="font-size: 0.88rem; color: #F8FAFC; font-weight: 600;">{scenario_icon} {scenario_label}</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.35rem;">
            <span style="font-size: 0.72rem; font-weight: 700; color: #94A3B8; letter-spacing: 0.04em;">MOTOR:</span>
            <span style="font-size: 0.86rem; color: #F8FAFC; font-weight: 600;">{gateway_badge}</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.45rem; margin-bottom: 0.2rem;">
            <span style="font-size: 0.74rem; color: #94A3B8; font-weight: 600;">Pipeline Multiagente:</span>
            <span style="font-size: 0.76rem; color: #38BDF8; font-weight: 700;">● 5 Agentes Ativos</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    execute_btn = st.button("⚡ Executar Ciclo Multiagente", type="primary", use_container_width=True)

    st.markdown("""
    <div style="font-size: 0.7rem; color: #64748B; text-align: center; margin-top: 0.55rem;">
        🔒 Decisão determinística & conformidade LGPD
    </div>
    """, unsafe_allow_html=True)

if execute_btn:
    st.session_state["executed"] = True
    st.session_state["result"] = run_cycle(
        location_id,
        force_fixture=force_fixture,
        force_extreme=force_extreme,
    )
    st.session_state["operator_rejections"] = []

st.markdown("---")

# ─── RESULTADOS DO CICLO MULTIAGENTE ─────────────────────────────────────────
if st.session_state.get("executed"):
    result = st.session_state["result"]

    if not result.ok:
        st.error(f"Erro na execução do ciclo: {result.errors}")
    else:
        # Métricas de Alto Impacto Cognitivo (Neurodesign)
        k1, k2, k3, k4 = st.columns(4)

        with k1:
            st.markdown("""
            <div class="metric-container accent-blue">
                <div class="metric-label">Localidade Piloto</div>
                <div class="metric-value">""" + loc_data["city"] + """</div>
            </div>
            """, unsafe_allow_html=True)

        with k2:
            hazard = result.risk_assessment.hazard_type.value if result.risk_assessment else "no_hazard"
            sev = result.risk_assessment.severity.value.upper() if (result.risk_assessment and result.risk_assessment.severity) else "NORMAL"
            border_cls = "accent-red" if sev in ("RED", "ORANGE") else "accent-green"
            color_txt = "#EF4444" if sev == "RED" else ("#F97316" if sev == "ORANGE" else "#10B981")

            st.markdown(f"""
            <div class="metric-container {border_cls}">
                <div class="metric-label">Risco Identificado</div>
                <div class="metric-value" style="color: {color_txt};">{hazard.upper()} ({sev})</div>
            </div>
            """, unsafe_allow_html=True)

        with k3:
            eleg = result.audience_selection.total_eligible if result.audience_selection else 0
            st.markdown(f"""
            <div class="metric-container accent-blue">
                <div class="metric-label">Segurados Elegíveis</div>
                <div class="metric-value" style="color: #38BDF8;">{eleg} acionados</div>
            </div>
            """, unsafe_allow_html=True)

        with k4:
            sup = result.audience_selection.total_suppressed if result.audience_selection else 0
            st.markdown(f"""
            <div class="metric-container accent-amber">
                <div class="metric-label">Silêncio Inteligente</div>
                <div class="metric-value" style="color: #FBBF24;">{sup} suprimidos</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ─── JORNADA COMPLETA DO OPERADOR (TABS) ─────────────────────────────
        tab_wow, tab_weather, tab_risk, tab_audience, tab_drafts, tab_hitl, tab_trace = st.tabs([
            "✨ O Momento Uau (Diferenciação por Ramo)",
            "1. 📡 Clima & Indicadores",
            "2. 🧠 Análise de Risco (Matriz)",
            "3. 👥 Carteira & Silêncio Inteligente",
            "4. 📝 Mensagens Geradas",
            "5. 🤝 Aprovação Humana (HITL)",
            "6. 📊 Trilha Multiagente (Observabilidade)"
        ])

        # ─── TAB 1: MOMENTO UAU (CORE DE NEGÓCIOS DE SEGUROS) ───────────────
        with tab_wow:
            st.markdown("""
            <div class="wow-container">
                <h3 style="color: #38BDF8; margin-bottom: 0.4rem;">🌟 O Momento Uau: Inteligência Semântica por Ramo</h3>
                <p style="color: #CBD5E1; font-size: 0.95rem; margin-bottom: 0;">
                    Em seguros, a mesma tempestade afeta o patrimônio de maneiras totalmente distintas.
                    Veja como o MeteoRisco segmenta as orientações práticas para <b>Automóvel</b> vs <b>Residencial</b> de forma 100% determinística e auditável:
                </p>
            </div>
            """, unsafe_allow_html=True)

            if result.message_drafts:
                auto_drafts = [d for d in result.message_drafts if d.line_of_business == "auto"]
                res_drafts = [d for d in result.message_drafts if d.line_of_business == "residential"]

                col_auto, col_res = st.columns(2)

                with col_auto:
                    st.markdown("""
                    <div class="neuro-card" style="border-top: 3px solid #38BDF8;">
                        <h4 style="color: #38BDF8; display: flex; align-items: center; gap: 0.5rem; margin-top: 0;">
                            🚗 Ramo Automóvel
                        </h4>
                    """, unsafe_allow_html=True)

                    if auto_drafts:
                        st.markdown(f'<span class="badge-auto">🚗 Total Elegíveis: {len(auto_drafts)}</span>', unsafe_allow_html=True)
                        if len(auto_drafts) > 1:
                            auto_options = {f"{d.insured_name} ({d.channel.upper()})": idx for idx, d in enumerate(auto_drafts)}
                            sel_auto_label = st.selectbox("Inspecionar Segurado:", list(auto_options.keys()), key="sel_auto_client")
                            d = auto_drafts[auto_options[sel_auto_label]]
                        else:
                            d = auto_drafts[0]

                        st.markdown(f"""
                        <div class="message-bubble auto">
                            <div class="message-meta">
                                <span>Segurado: <b>{d.insured_name}</b> · Canal: <b style="color: #38BDF8;">{d.channel.upper()}</b></span>
                                <span>Severidade: <b style="color: #EF4444;">{d.severity.upper()}</b></span>
                            </div>
                            <div class="message-content">{html.escape(d.body)}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<p style='color: #94A3B8; font-weight: 600; font-size: 0.88rem; margin-top: 0.8rem; margin-bottom: 0.4rem;'>AÇÕES RECOMENDADAS PELO PLAYBOOK:</p>", unsafe_allow_html=True)
                        for act in d.actions:
                            st.markdown(f"""
                            <div class="action-badge auto">
                                <span class="action-icon">🚗</span>
                                <span class="action-text">{html.escape(act)}</span>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("ℹ️ Nenhum veículo elegível nesta localidade (veículos protegidos em garagem coberta acionaram o Silêncio Inteligente).")
                    st.markdown("</div>", unsafe_allow_html=True)

                with col_res:
                    st.markdown("""
                    <div class="neuro-card" style="border-top: 3px solid #34D399;">
                        <h4 style="color: #34D399; display: flex; align-items: center; gap: 0.5rem; margin-top: 0;">
                            🏠 Ramo Residencial
                        </h4>
                    """, unsafe_allow_html=True)

                    if res_drafts:
                        st.markdown(f'<span class="badge-res">🏠 Total Elegíveis: {len(res_drafts)}</span>', unsafe_allow_html=True)
                        if len(res_drafts) > 1:
                            res_options = {f"{d.insured_name} ({d.channel.upper()})": idx for idx, d in enumerate(res_drafts)}
                            sel_res_label = st.selectbox("Inspecionar Segurado:", list(res_options.keys()), key="sel_res_client")
                            d = res_drafts[res_options[sel_res_label]]
                        else:
                            d = res_drafts[0]

                        st.markdown(f"""
                        <div class="message-bubble res">
                            <div class="message-meta">
                                <span>Segurada: <b>{d.insured_name}</b> · Canal: <b style="color: #34D399;">{d.channel.upper()}</b></span>
                                <span>Severidade: <b style="color: #EF4444;">{d.severity.upper()}</b></span>
                            </div>
                            <div class="message-content">{html.escape(d.body)}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<p style='color: #94A3B8; font-weight: 600; font-size: 0.88rem; margin-top: 0.8rem; margin-bottom: 0.4rem;'>AÇÕES RECOMENDADAS PELO PLAYBOOK:</p>", unsafe_allow_html=True)
                        for act in d.actions:
                            st.markdown(f"""
                            <div class="action-badge res">
                                <span class="action-icon">🏠</span>
                                <span class="action-text">{html.escape(act)}</span>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("ℹ️ Nenhum imóvel elegível nesta localidade.")
                    st.markdown("</div>", unsafe_allow_html=True)

            else:
                st.markdown("""
                <div class="neuro-card" style="border-left: 4px solid #10B981;">
                    <h4 style="color: #10B981; margin-top:0;">🛡️ Proteção por Silêncio Inteligente Ativada</h4>
                    <p style="color: #E2E8F0;">
                        O sistema avaliou as métricas meteorológicas e concluiu que o clima está abaixo dos limiares de risco para sinistros.
                        <b>Nenhum segurado foi incomodado</b>, preservando o canal da seguradora contra a fadiga de alertas (anti-spam).
                    </p>
                    <p style="color: #94A3B8; font-size: 0.9rem;">
                        👉 <i>Para demonstrar a geração de alertas e o Momento Uau, selecione <b>'⛈️ Tempestade Severa'</b> na barra lateral e clique em Executar Ciclo Multiagente.</i>
                    </p>
                </div>
                """, unsafe_allow_html=True)

        # ─── TAB 2: METEOROLOGIA ─────────────────────────────────────────────
        with tab_weather:
            sig = result.weather_signal
            m = sig.metrics
            st.markdown(f"### 📡 Sinal Meteorológico Normalizado (`{sig.source}`)")
            st.caption(f"Validade da Previsão: {sig.forecast_valid_from.strftime('%d/%m/%Y %H:%M')} até {sig.forecast_valid_until.strftime('%d/%m/%Y %H:%M')}")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Chuva Prevista", f"{m.precipitation_mm_h or 0:.1f} mm/h", help="Volume de precipitação horária pico")
            c2.metric("Rajadas de Vento", f"{m.wind_gusts_10m_kmh or 0:.1f} km/h", help="Velocidade máxima de rajada a 10m de altitude")
            c3.metric("Código WMO", str(m.weather_code or 0), help="Código padrão da Organização Meteorológica Mundial (95=Tempestade, 96/99=Granizo)")
            c4.metric("Instabilidade (CAPE)", f"{m.cape_j_kg or 0:.0f} J/kg", help="Convective Available Potential Energy: energia para formação de granizo")

            # Gráfico Plotly Dark
            df_plot = pd.DataFrame({
                "Indicador": ["Chuva (mm/h)", "Vento (km/h)", "CAPE (J/kg ÷ 50)"],
                "Valor": [m.precipitation_mm_h or 0, m.wind_gusts_10m_kmh or 0, (m.cape_j_kg or 0)/50]
            })
            fig = px.bar(
                df_plot, x="Indicador", y="Valor", color="Indicador",
                color_discrete_sequence=["#38BDF8", "#F59E0B", "#EF4444"],
                title="Indicadores de Pico no Horizonte de Previsão"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#F8FAFC",
                showlegend=False,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            fig.update_yaxes(gridcolor="rgba(148, 163, 184, 0.1)")
            st.plotly_chart(fig, use_container_width=True)

        # ─── TAB 3: ANÁLISE DE RISCO ─────────────────────────────────────────
        with tab_risk:
            risk = result.risk_assessment
            st.markdown("### 🧠 Avaliação de Risco Determinística (Underwriting)")
            st.markdown("""
            A classificação securitária cruza os sinais climáticos com a matriz de regras (`risk_matrix.yaml`).
            <b>Nenhuma decisão de risco é delegada à LLM</b>, garantindo conformidade regulatória plena.
            """)

            col_r1, col_r2 = st.columns([2, 1])
            with col_r1:
                st.markdown(f"**Evento Classificado:** `{risk.hazard_type.value}`")
                st.markdown(f"**Severidade Atribuída:** `{risk.severity.value.upper() if risk.severity else 'NENHUMA'}`")
                st.markdown(f"**Ramos de Seguro Impactados:** `{', '.join(risk.impacted_lines) if risk.impacted_lines else 'Nenhum'}`")
                st.info(f"**Justificativa Atuarial (Rationale):** {risk.rationale}")
            with col_r2:
                st.markdown("**Métricas Ativadoras:**")
                st.json(risk.triggered_metrics)

        # ─── TAB 4: CARTEIRA & SILÊNCIO INTELIGENTE ──────────────────────────
        with tab_audience:
            st.markdown("### 👥 Cruzamento de Exposição da Carteira")
            st.caption(f"Avaliando 4 segurados sintéticos cadastrados para {loc_data['city']}")

            col_el, col_sup = st.columns(2)
            with col_el:
                st.markdown("#### ✅ Segurados Elegíveis (Comunicação Ativa)")
                if result.audience_selection.items:
                    data_el = [
                        {
                            "ID": i.insured_id,
                            "Segurado": i.insured_name,
                            "Ramo": i.line_of_business.upper(),
                            "Exposição": i.exposure_profile.replace("_", " "),
                            "Canal": i.channel.upper(),
                            "Prioridade": i.priority.upper()
                        }
                        for i in result.audience_selection.items
                    ]
                    st.dataframe(pd.DataFrame(data_el), use_container_width=True, hide_index=True)
                else:
                    st.info("Nenhum segurado elegível neste ciclo.")

            with col_sup:
                st.markdown("#### 🛡️ Segurados Suprimidos (Silêncio Inteligente)")
                if result.audience_selection.suppressed:
                    data_sup = [
                        {
                            "ID": s.insured_id,
                            "Segurado": s.insured_name,
                            "Motivo de Supressão": s.suppression_reason,
                            "Justificativa": s.suppression_detail
                        }
                        for s in result.audience_selection.suppressed
                    ]
                    st.dataframe(pd.DataFrame(data_sup), use_container_width=True, hide_index=True)

        # ─── TAB 5: MENSAGENS GERADAS & AUDITORIA ────────────────────────────
        with tab_drafts:
            st.markdown("### 📝 Mensagens Personalizadas & Auditoria Independente")
            st.caption("O Redator gera o texto com empatia. O Auditor valida conformidade contra frases proibidas.")

            if result.message_drafts:
                for d in result.message_drafts:
                    audit = next((r for r in result.audit_results if r.insured_id == d.insured_id), None)
                    st_status = audit.status.value.upper() if audit else "PENDENTE"
                    border_color = "#10B981" if st_status == "APPROVED" else "#EF4444"

                    with st.expander(f"👤 {d.insured_name} ({d.line_of_business.upper()}) — Status: {st_status}"):
                        st.markdown(f"**Canal:** `{d.channel.upper()}` · **Modelo:** `{d.model_meta.model if d.model_meta else 'template'}` (Fallback: `{d.model_meta.is_fallback if d.model_meta else True}`)")
                        if d.subject:
                            st.markdown(f"**Assunto:** {d.subject}")
                        st.markdown(f"""
                        <div class="message-bubble {'auto' if d.line_of_business == 'auto' else 'res'}">
                            <div class="message-meta">
                                <span>Destinatário: <b>{d.insured_name}</b> ({d.line_of_business.upper()})</span>
                                <span>Canal: <b>{d.channel.upper()}</b></span>
                            </div>
                            <div class="message-content">{html.escape(d.body)}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        if audit:
                            if audit.status == AuditStatus.APPROVED:
                                st.markdown('<span class="badge-approved">✅ Mensagem Aprovada pelo Auditor</span> (100% em conformidade securitária)', unsafe_allow_html=True)
                            elif audit.status == AuditStatus.REVISED:
                                st.markdown(f"""
                                <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 8px; padding: 0.6rem 0.9rem; margin-top: 0.5rem;">
                                    <b style="color: #FBBF24;">⚠️ Aprovada com Ressalva pelo Auditor:</b>
                                    <span style="color: #E2E8F0; font-size: 0.9rem;"> {', '.join(audit.violations)}</span>
                                    <div style="color: #94A3B8; font-size: 0.8rem; margin-top: 0.2rem;">
                                        ℹ️ <i>Mensagem liberada para envio. A ressalva é um alerta não-bloqueante de recomendação de canal.</i>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 8px; padding: 0.6rem 0.9rem; margin-top: 0.5rem;">
                                    <b style="color: #EF4444;">🚫 Mensagem BLOQUEADA pelo Auditor:</b>
                                    <span style="color: #E2E8F0; font-size: 0.9rem;"> {', '.join(audit.violations)}</span>
                                    <div style="color: #FCA5A5; font-size: 0.8rem; margin-top: 0.2rem;">
                                        ⚠️ <i>Envio impedido por violação de regras regulatórias (termos proibidos ou ausência de ressalva epistemológica).</i>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
            else:
                st.info("Nenhuma mensagem gerada neste ciclo devido à ausência de risco relevante.")

        # ─── TAB 6: HUMAN-IN-THE-LOOP (APROVAÇÃO) ────────────────────────────
        with tab_hitl:
            st.markdown("### 🤝 Human-in-the-Loop (Governança Operacional)")
            st.markdown("O operador humano tem autoridade final de veto antes do envio simulado.")

            if result.message_drafts:
                rejections = []
                for d in result.message_drafts:
                    audit = next((r for r in result.audit_results if r.insured_id == d.insured_id), None)
                    if audit and audit.status == AuditStatus.BLOCKED:
                        st.error(f"🚫 **{d.insured_name}** foi bloqueado pelo Auditor de Conformidade. Envio impedido.")
                    else:
                        appr = st.checkbox(
                            f"Aprovar envio preventivo para {d.insured_name} ({d.line_of_business.upper()} via {d.channel.upper()})",
                            value=True,
                            key=f"hitl_{d.insured_id}"
                        )
                        if not appr:
                            rejections.append(d.insured_id)

                if st.button("🚀 Confirmar & Simular Disparos Aprovados", type="primary"):
                    from src.agents.notification_simulator import NotificationSimulator
                    sim = NotificationSimulator()
                    logs, trace_sim = sim.run(
                        drafts=result.message_drafts,
                        audit_results=result.audit_results,
                        approved_by="operador_humano",
                        operator_rejections=rejections
                    )
                    st.success(f"✅ Sucesso! {len(logs)} disparos simulados com trilha de decisão auditável.")
                    if logs:
                        data_logs = [
                            {
                                "Segurado": l.insured_name,
                                "Canal": l.channel.upper(),
                                "Status": l.status.value.upper(),
                                "Hash SHA-256": l.payload_ref[:16] + "...",
                                "Horário (UTC)": l.timestamp.strftime('%H:%M:%S')
                            }
                            for l in logs
                        ]
                        st.dataframe(pd.DataFrame(data_logs), use_container_width=True, hide_index=True)
            else:
                st.info("Nenhuma mensagem elegível para aprovação neste ciclo.")

        # ─── TAB 7: OBSERVABILIDADE MULTIAGENTE ──────────────────────────────
        with tab_trace:
            st.markdown("### 📊 Trilha de Decisão por Agente (`CycleResult`)")
            st.caption(f"Cycle ID: `{result.cycle_id}` · Duração Total: `{result.cycle_duration_ms:.1f} ms`")

            for t in result.trace:
                badge_bg = "rgba(16, 185, 129, 0.2)" if t.status == "ok" else "rgba(148, 163, 184, 0.2)"
                st.markdown(f"""
                <div class="pipeline-step" style="margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <b style="color: #38BDF8; font-size: 1rem;">🤖 {t.agent_name}</b>
                        <span style="font-size: 0.8rem; color: #94A3B8;">{t.duration_ms:.1f} ms</span>
                    </div>
                    <div style="margin-top: 0.3rem; color: #E2E8F0; font-size: 0.9rem;">
                        {t.summary}
                    </div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="neuro-card" style="text-align: center; padding: 3rem 2rem;">
        <h3 style="color: #38BDF8; margin-bottom: 0.5rem;">Pronto para Simulação Operacional</h3>
        <p style="color: #94A3B8; max-width: 600px; margin: 0 auto 1.5rem auto;">
            Selecione a <b>Cidade-Piloto</b> e o <b>Cenário de Teste</b> na barra lateral à esquerda e clique em <b>Executar Ciclo Multiagente</b> para iniciar a jornada de prevenção de sinistros.
        </p>
    </div>
    """, unsafe_allow_html=True)
