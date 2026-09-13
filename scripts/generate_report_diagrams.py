"""
Gera diagramas visuais modernos em alta resolução (300 DPI) para o Relatório Técnico ABNT do MeteoRisco.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

output_dir = Path("docs/diagramas")
output_dir.mkdir(parents=True, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Liberation Sans', 'Arial', 'sans-serif']
plt.rcParams['font.family'] = 'sans-serif'

def create_paradigm_diagram():
    fig, ax = plt.subplots(figsize=(10, 3.8), dpi=300)
    ax.set_facecolor("#FAFAFA")
    fig.patch.set_facecolor("#FFFFFF")
    
    # Coluna 1: Tradicional
    box1 = patches.FancyBboxPatch((0.5, 0.4), 4.0, 3.0, boxstyle="round,pad=0.2,rounding_size=0.15",
                                  linewidth=1.5, edgecolor="#DC2626", facecolor="#FEF2F2")
    ax.add_patch(box1)
    ax.text(2.5, 3.1, "MODELO TRADICIONAL (REATIVO)", fontsize=11, fontweight="bold", color="#991B1B", ha="center")
    
    steps_trad = [
        "1. Tempestade atinge o bem segurado",
        "2. Sinistro e dano material consumados",
        "3. Segurado aciona abertura de sinistro",
        "4. Indenização financeira e alto custo"
    ]
    for i, step in enumerate(steps_trad):
        ax.text(2.5, 2.5 - i * 0.55, step, fontsize=9.5, color="#7F1D1D", ha="center",
                bbox=dict(boxstyle="round,pad=0.3", fc="#FFFFFF", ec="#FCA5A5", lw=1))
        if i < len(steps_trad) - 1:
            ax.annotate("", xy=(2.5, 2.22 - i * 0.55), xytext=(2.5, 2.38 - i * 0.55),
                        arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=1.2))

    # Coluna 2: MeteoRisco
    box2 = patches.FancyBboxPatch((5.5, 0.4), 4.0, 3.0, boxstyle="round,pad=0.2,rounding_size=0.15",
                                  linewidth=1.5, edgecolor="#059669", facecolor="#ECFDF5")
    ax.add_patch(box2)
    ax.text(7.5, 3.1, "MODELO METEORISCO (PROATIVO)", fontsize=11, fontweight="bold", color="#065F46", ha="center")
    
    steps_pro = [
        "1. Monitoramento climático em tempo real",
        "2. Avaliação de risco e elegibilidade",
        "3. Orientação preventiva personalizada",
        "4. Dano evitado e sinistro mitigado"
    ]
    for i, step in enumerate(steps_pro):
        ax.text(7.5, 2.5 - i * 0.55, step, fontsize=9.5, color="#064E3B", ha="center",
                bbox=dict(boxstyle="round,pad=0.3", fc="#FFFFFF", ec="#6EE7B7", lw=1))
        if i < len(steps_pro) - 1:
            ax.annotate("", xy=(7.5, 2.22 - i * 0.55), xytext=(7.5, 2.38 - i * 0.55),
                        arrowprops=dict(arrowstyle="-|>", color="#059669", lw=1.2))
            
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.8)
    ax.axis("off")
    plt.tight_layout()
    out_path = output_dir / "diagrama_paradigma.png"
    plt.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Salvo: {out_path}")

def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 5.8), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    
    layers = [
        ("1. CAMADA DE APRESENTAÇÃO (Interface Executiva — Streamlit)", 
         "Dashboard com Neurodesign Dark Mode · Mapa 5 Regiões IBGE · Simulação e HITL", 
         "#0284C7", "#F0F9FF"),
        ("2. CAMADA DE RUNTIME & CONTROLE (Control Plane / Harness)", 
         "Orquestrador Sequencial (runner.py) · Contratos Tipados Pydantic v2 · Traces", 
         "#4F46E5", "#EEF2FF"),
        ("3. CAMADA DE RACIOCÍNIO & AGENTES (Reasoning Plane)", 
         "Scout Climático · Analista MeteoRisco · Gestor de Exposição · Redator · Auditor · Simulator", 
         "#0D9488", "#F0FDFA"),
        ("4. CAMADA DE CAPACIDADES & SERVIÇOS (Capability Plane)", 
         "fetch_weather (Open-Meteo) · normalize_weather · apply_risk_matrix · audit_message", 
         "#D97706", "#FFFBEB"),
        ("5. CAMADA DE DOMÍNIO & CONHECIMENTO SECURITÁRIO (Domain Plane)", 
         "risk_matrix.yaml · playbook.yaml · portfolio.csv · locations.yaml · regioes_ibge.geojson", 
         "#475569", "#F8FAFC")
    ]
    
    y_start = 4.8
    y_spacing = 1.05
    
    for i, (title, desc, border_col, bg_col) in enumerate(layers):
        y = y_start - i * y_spacing
        box = patches.FancyBboxPatch((0.5, y), 9.5, 0.82, boxstyle="round,pad=0.1,rounding_size=0.12",
                                      linewidth=1.4, edgecolor=border_col, facecolor=bg_col)
        ax.add_patch(box)
        ax.text(0.8, y + 0.52, title, fontsize=10.5, fontweight="bold", color=border_col)
        ax.text(0.8, y + 0.22, desc, fontsize=9.0, color="#1E293B")
        
        if i < len(layers) - 1:
            ax.annotate("", xy=(5.25, y - 0.04), xytext=(5.25, y + 0.02),
                        arrowprops=dict(arrowstyle="-|>", color="#64748B", lw=1.5))
            
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 5.8)
    ax.axis("off")
    plt.tight_layout()
    out_path = output_dir / "diagrama_arquitetura.png"
    plt.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Salvo: {out_path}")

def create_agents_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(10.8, 3.8), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    
    # Agentes sequenciais
    agents_top = [
        ("1. Scout\nClimático", "Coleta Open-Meteo\n& Fallback Offline", "#0284C7", "#E0F2FE"),
        ("2. Analista\nMeteoRisco", "Classificação Atuarial\n100% Determinística", "#4F46E5", "#EEF2FF"),
        ("3. Gestor de\nExposição", "Carteira & Regras de\nSilêncio Inteligente", "#0D9488", "#CCFBF1"),
        ("4. Redator\nPreventivo", "Linguagem Natural\nEmpática (Playbook)", "#D97706", "#FEF3C7"),
        ("5. Auditor de\nDecisão", "Conformidade Legal\nAnti-Promessa Sinistro", "#DC2626", "#FEE2E2"),
        ("6. Simulador\nTransacional", "Despacho & Trilha\nHash SHA-256", "#16A34A", "#DCFCE7")
    ]
    
    x_coords = [0.4, 2.15, 3.9, 5.65, 7.4, 9.15]
    w = 1.45
    h = 1.6
    y_top = 1.8
    
    for i, (title, desc, border_col, bg_col) in enumerate(agents_top):
        x = x_coords[i]
        box = patches.FancyBboxPatch((x, y_top), w, h, boxstyle="round,pad=0.1,rounding_size=0.1",
                                      linewidth=1.3, edgecolor=border_col, facecolor=bg_col)
        ax.add_patch(box)
        ax.text(x + w/2, y_top + 1.15, title, fontsize=9.0, fontweight="bold", color=border_col, ha="center")
        ax.text(x + w/2, y_top + 0.45, desc, fontsize=7.2, color="#1E293B", ha="center")
        
        # Seta para o próximo agente
        if i < len(agents_top) - 1:
            ax.annotate("", xy=(x_coords[i+1] - 0.05, y_top + h/2), xytext=(x + w + 0.05, y_top + h/2),
                        arrowprops=dict(arrowstyle="-|>", color="#64748B", lw=1.5))
            
    # Módulo Human-in-the-Loop embaixo
    hitl_box = patches.FancyBboxPatch((5.65, 0.3), 3.2, 0.95, boxstyle="round,pad=0.1,rounding_size=0.1",
                                     linewidth=1.3, edgecolor="#7C3AED", facecolor="#F5F3FF")
    ax.add_patch(hitl_box)
    ax.text(7.25, 0.85, "GOVERNANÇA HUMAN-IN-THE-LOOP (HITL)", fontsize=8.5, fontweight="bold", color="#6D28D9", ha="center")
    ax.text(7.25, 0.52, "Painel com Prerrogativa de Veto Operacional Manual", fontsize=7.5, color="#374151", ha="center")
    
    # Seta conectando HITL ao Simulador e Auditor
    ax.annotate("", xy=(9.8, y_top - 0.08), xytext=(8.85, 0.8),
                arrowprops=dict(arrowstyle="-|>", color="#7C3AED", lw=1.3, linestyle="dashed"))
    ax.annotate("", xy=(8.1, y_top - 0.08), xytext=(7.25, 1.25),
                arrowprops=dict(arrowstyle="<->", color="#7C3AED", lw=1.3, linestyle="dashed"))

    # Rótulo de fluxo
    ax.text(0.4, 0.6, "• Execução Sequencial Garantida via Contratos Pydantic v2\n• Latência do Ciclo Completo: ~120 ms\n• Zero Risco de Alucinação em Subscrição",
            fontsize=8.0, color="#475569", va="center")

    ax.set_xlim(0, 10.8)
    ax.set_ylim(0, 3.8)
    ax.axis("off")
    plt.tight_layout()
    out_path = output_dir / "diagrama_agentes.png"
    plt.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Salvo: {out_path}")

def create_engine_flow_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 4.2), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    
    steps = [
        ("Fase 1: Coleta Meteorológica", "Open-Meteo REST API\nSéries 24h & Pior Cenário", "#0284C7", "#F0F9FF"),
        ("Fase 2: Classificação Atuarial", "risk_matrix.yaml\nVerde/Amarelo/Laranja/Vermelho", "#4F46E5", "#EEF2FF"),
        ("Fase 3: Seleção de Carteira", "portfolio.csv\nAplicação do Silêncio Inteligente", "#0D9488", "#F0FDFA"),
        ("Fase 4: Redação Preventiva", "playbook.yaml\nTom empático e canais", "#D97706", "#FFFBEB"),
        ("Fase 5: Auditoria Regulatória", "Varredura SUSEP/LGPD\nBloqueio de Promessas", "#DC2626", "#FEF2F2"),
        ("Fase 6: Despacho Auditado", "Trilha Criptográfica\nHash SHA-256 e UTC", "#16A34A", "#F0FDF4")
    ]
    
    xs = [0.4, 3.8, 7.2]
    ys = [2.2, 0.5]
    
    # 3 colunas x 2 linhas
    for idx, (title, desc, border_col, bg_col) in enumerate(steps):
        col = idx % 3
        row = idx // 3
        x = xs[col]
        y = ys[row]
        w = 3.0
        h = 1.35
        
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.1",
                                      linewidth=1.3, edgecolor=border_col, facecolor=bg_col)
        ax.add_patch(box)
        ax.text(x + w/2, y + 0.92, title, fontsize=9.0, fontweight="bold", color=border_col, ha="center")
        ax.text(x + w/2, y + 0.42, desc, fontsize=8.0, color="#1E293B", ha="center")
        
        # Conexões
        if idx == 0 or idx == 1:
            ax.annotate("", xy=(x + w + 0.35, y + h/2), xytext=(x + w + 0.05, y + h/2),
                        arrowprops=dict(arrowstyle="-|>", color="#64748B", lw=1.4))
        elif idx == 2:
            # Desce para linha 2
            ax.annotate("", xy=(x + w/2, 1.88), xytext=(x + w/2, 2.18),
                        arrowprops=dict(arrowstyle="-|>", color="#64748B", lw=1.4))
        elif idx == 5:
            pass
        else: # 3 ou 4
            ax.annotate("", xy=(x + w + 0.35, y + h/2), xytext=(x + w + 0.05, y + h/2),
                        arrowprops=dict(arrowstyle="-|>", color="#64748B", lw=1.4))

    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 4.0)
    ax.axis("off")
    plt.tight_layout()
    out_path = output_dir / "diagrama_fluxo.png"
    plt.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Salvo: {out_path}")

if __name__ == "__main__":
    create_paradigm_diagram()
    create_architecture_diagram()
    create_agents_pipeline_diagram()
    create_engine_flow_diagram()
    print("Todos os diagramas modernos foram gerados com sucesso!")
