# Relatório Técnico — MeteoRisco (Desafio 5 — InsurMinds / I2A2)

> **Produto:** MeteoRisco — Sistema Multiagente de Comunicação Preventiva por Eventos Climáticos  
> **Data:** 20 de Agosto de 2026  
> **Status:** Concluído / Pronto para Submissão  
> **Versão:** 1.0 Final  

---

## 1. Resumo Executivo e Proposta de Valor

O **MeteoRisco** é um sistema multiagente de prevenção de sinistros (*loss prevention*) por eventos climáticos que transforma sinais meteorológicos externos em decisões de comunicação preventiva personalizadas orientadas a carteira de seguros (ramos Automóvel e Residencial).

* **Tagline:** *Do clima ao risco. Do risco à ação.*
* **Diferencial:** Transição de um modelo tradicional reativo (o segurado procura a seguradora após a tempestade) para um modelo proativo, auditável e altamente segmentado por perfil de exposição do bem segurado.
* **Escopo Demonstrado:** Piloto nacional parametrizado cobrindo 5 localidades-piloto representativas (Belém/PA, Recife/PE, Brasília/DF, São Paulo/SP, Porto Alegre/RS) e 20 segurados sintéticos.

---

## 2. Arquitetura de AI Engineering

O MeteoRisco foi construído seguindo os princípios modernos de AI Engineering:

### 2.1 Visão em Camadas
```
┌─────────────────────────────────────────────────────────────┐
│ INTERFACE (Product)                                         │
│ Streamlit · disparo de ciclo · visualização da trilha       │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│ HARNESS (AI Runtime / Control Plane)                        │
│ orquestração sequencial · contrato Pydantic · traces        │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│ AGENTS (Reasoning Plane)                                    │
│ Scout · Analista · Gestor de Exposição · Redator · Auditor  │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│ SKILLS / TOOLS (Capability Plane)                           │
│ fetch_weather · normalize · apply_matrix · audit · notify   │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│ DOMAIN (Business Plane)                                     │
│ portfolio.csv · risk_matrix.yaml · playbook.yaml · locations│
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Por que Cinco Agentes Especializados?
A decomposição do pipeline em 5 agentes garante responsabilidades semânticas isoladas:

1. **Scout Climático:** I/O externo. Obtém e normaliza previsões meteorológicas via API pública da Open-Meteo.
2. **Analista MeteoRisco:** Avaliação determinística do sinal climático segundo os thresholds securitários.
3. **Gestor de Exposição:** Cruzamento determinístico de underwriting entre a ameaça e a carteira de segurados, gerando a lista de elegíveis e registrando supressões justificadas (silêncio inteligente).
4. **Redator Preventivo:** Geração generativa de linguagem via LLM (Google Gemini / OpenAI) utilizando as diretrizes do `playbook.yaml`.
5. **Auditor de Decisão:** Governança independente. Valida cada rascunho de mensagem contra regras estritas (impedindo promessas indevidas de indenização, alarmismo ou superlatividade).

### 2.3 Abordagem Híbrida (Determinístico + LLM)
- **Elegibilidade e Underwriting são 100% Determinísticos:** Nenhuma decisão de quem deve ser avisado é delegada a prompts de LLM, eliminando riscos de alucinação ou inconsistência regulatória.
- **LLM para Linguagem:** O LLM é aplicado onde oferece o maior valor: personalização, tom de voz empático e geração contextualizada por ramo e canal.

---

## 3. Data Feasibility Study e Decisão Epistemológica de Granizo

Um estudo comparativo empírico avaliou três fontes de dados meteorológicos:

| Critério | Open-Meteo (Escolha Final) | OpenWeather 2.5 Free | INMET |
| :--- | :--- | :--- | :--- |
| **Acesso** | Público, sem chave (Zero atrito) | API Key obrigatória | Token governamental |
| **Previsão Futura** | Até 16 dias (horária) | Até 5 dias (3 em 3h) | Somente observação histórica |
| **Variáveis Convectivas** | Confirmado (CAPE, Lifted Index) | Ausente | Ausente |
| **Códigos WMO** | Confirmado (95, 96, 99) | Códigos 200–232 | Ausente |
| **Estabilidade** | 99.9%+ Uptime | Alta | Baixa (Erros 500/DNS) |

### Decisão Epistemológica sobre Granizo
Sensores de superfície e APIs meteorológicas globais **não observam granizo no solo em tempo real**; elas fornecem classificações meteorológicas **modeladas (NWP)** indicando potencial convectivo.
O MeteoRisco trata `weather_code = 96/99` e `CAPE elevado` como *sinais de convecção potencialmente produtores de granizo*, aplicando obrigatoriamente linguagem de ressalva no playbook ("previsão de granizo estimada por modelos meteorológicos").

---

## 4. Matriz RACI e Governança do Projeto

| Atividade | S1 (PO) | S2 (Underwriting) | S3 (CX/Comunicação) | T1 (AI/Harness) | T2 (Eng. Dados/UI) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Aprovação de Escopo e Freeze | **A/R** | C | C | C | C |
| Matriz de Risco (`risk_matrix.yaml`) | C | **A/R** | C | I | I |
| Playbook (`playbook.yaml`) | C | C | **A/R** | I | I |
| Contratos Pydantic & Harness | I | I | I | **A/R** | C |
| Skills Determinísticas & API | I | I | I | C | **A/R** |
| Suíte de Evals (Golden Cases) | C | C | C | **A/R** | **R** |
| Interface Streamlit | C | C | C | C | **A/R** |

---

## 5. Resultados da Suíte de Evals (100% de Sucesso)

O sistema foi submetido à suíte automatizada contendo 13 cenários de teste (`evals/golden_cases.yaml`), cobrindo regras de negócio, conformidade do auditor, resiliência de fallback e especificidades geográficas regionais:

```
=== Resultados dos Evals ===
[EV1] Granizo em São Paulo (Auto na rua vs Garagem) ... ✅ PASSED
[EV2] Chuva forte em Belém (Residencial térreo) ........ ✅ PASSED
[EV3] Vento forte em Porto Alegre (Telhados) ......... ✅ PASSED
[EV4] Evento abaixo do limiar em Brasília .............. ✅ PASSED
[EV5] Conformidade: Bloqueio de frase proibida ....... ✅ PASSED
[EV6] Personalização: Auto vs Residencial ............... ✅ PASSED
[EV7] Resiliência: Fallback offline em falha API ....... ✅ PASSED
[EV8] HITL: Respeito ao veto manual do operador ........ ✅ PASSED
[EV-GEO-1] Belém/PA (Norte - Equatorial) ............... ✅ PASSED
[EV-GEO-2] Recife/PE (Nordeste - Tropical litorâneo) ... ✅ PASSED
[EV-GEO-3] Brasília/DF (Centro-Oeste - Altitude) ....... ✅ PASSED
[EV-GEO-4] São Paulo/SP (Sudeste - Convectivo) .......... ✅ PASSED
[EV-GEO-5] Porto Alegre/RS (Sul - Frente fria) ......... ✅ PASSED

TAXA DE APROVAÇÃO FINAL: 13/13 PASSERAM (100.0%)
```

---

## 6. Estratégia de Fallback e Resiliência

Contingência é uma *feature* de engenharia no MeteoRisco:
1. **API Clima indisponível:** O `ScoutClimático` aciona o fallback automático para fixtures offline previamente armazenadas (`fixtures/open_meteo_*.json`).
2. **LLM indisponível / sem crédito:** O `RedatorPreventivo` utiliza gerador por template offline de alta qualidade, marcando `is_fallback=True` na trilha de auditoria.
3. **Erros no pipeline:** Validação fail-fast via schemas Pydantic v2 interrompe a propagação de dados corrompidos.

---

## 7. Instruções de Execução e Demonstração

### Rodar a Suíte de Testes e Evals
```bash
# Testes Unitários (13/13 PASSED)
PYTHONPATH=. .venv/bin/pytest tests/ -v

# Suíte de Evals (13/13 PASSED)
PYTHONPATH=. .venv/bin/python3 evals/eval_runner.py
```

### Iniciar a Interface Streamlit
```bash
.venv/bin/streamlit run app/streamlit_app.py
```

---

## 8. Conclusão

O **MeteoRisco** atende integralmente aos requisitos do Desafio 5, entregando um sistema funcional, profissional, auditável e pronto para evolução no Projeto Final ou uso em portfólio.
