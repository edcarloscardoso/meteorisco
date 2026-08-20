# MeteoRisco — Sistema Multiagente de Prevenção de Sinistros Climáticos

> **Projeto Acadêmico - InsurMinds / I2A2 (Desafio 5)**  
> *Do clima ao risco. Do risco à ação.*

O **MeteoRisco** é uma solução inteligente e proativa de *loss prevention* orientada a carteiras de seguros (Automóvel e Residencial). Ele monitora previsões meteorológicas, aplica regras de elegibilidade determinísticas sobre a carteira e gera orientações preventivas personalizadas antes da ocorrência do sinistro.

---

## 🏗️ Arquitetura do Sistema

O sistema é composto por cinco agentes especializados com responsabilidades semanticamente isoladas, operando em um pipeline controlado sequencial (*harness*):

```
+--------------------+      +----------------------+      +----------------------+
|   Scout Climático  | ---> |  Analista MeteoRisco | ---> | Gestor de Exposição  |
| (API Open-Meteo)   |      | (Thresholds de Risco)|      | (Elegibilidade/CSV)  |
+--------------------+      +----------------------+      +----------------------+
                                                                      |
+--------------------+      +----------------------+                  |
| Notification Sim.  | <--- |  Auditor de Decisão  | <----------------+
| (Envio simulado)   |      |  (Conformidade/CX)   |
+--------------------+      +----------------------+
```

1. **Scout Climático:** Consulta a API Forecast pública do **Open-Meteo** (sem API Key) para coletar dados meteorológicos (chuva, vento, códigos WMO e convecção/CAPE). Possui suporte a fallback offline via fixtures estáticas.
2. **Analista MeteoRisco:** Avalia os dados meteorológicos e os thresholds da `risk_matrix.yaml` de forma **determinística** (sem depender de LLM) para classificar o risco (Amarelo, Laranja ou Vermelho).
3. **Gestor de Exposição:** Aplica regras de underwriting e supressão da carteira de segurados (`portfolio.csv`). Garante que apenas pessoas afetadas de fato (ex: carro na rua durante granizo) recebam alertas, implementando o "silêncio inteligente" contra spam.
4. **Redator Preventivo:** Utiliza LLM (Gateway plugável) com diretrizes do `playbook.yaml` para redigir a mensagem de forma contextualizada. (Usa template offline como fallback de segurança).
5. **Auditor de Decisão:** Valida cada mensagem de forma independente contra o playbook de seguros, checando por termos proibidos (como prometer cobertura ou alarmismo) e garantindo conformidade.
6. **Notification Simulator:** Registra o envio simulado (SMS, App ou E-mail) das comunicações aprovadas, salvando a trilha de decisão auditável.

---

## 🛠️ Stack Tecnológica

- **Linguagem:** Python 3.11+
- **Validação:** Pydantic v2 (Contracts)
- **Configurações:** Pydantic-Settings & `.env`
- **Interface:** Streamlit (Visualizações de clima e fluxo de aprovação)
- **Testes:** pytest, pytest-httpx, respx

---

## 🚀 Como Executar o Projeto

### 1. Clonar e Acessar o Repositório
```bash
git clone https://github.com/seu-usuario/meteorisco.git
cd meteorisco
```

### 2. Configurar o Ambiente Virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Executar Testes Unitários
```bash
PYTHONPATH=. pytest tests/ -v
```

### 4. Executar os Evals de Negócio (Golden Cases)
```bash
PYTHONPATH=. python3 evals/eval_runner.py
```

### 5. Executar a Interface de Demonstração
```bash
streamlit run app/streamlit_app.py
```

---

## 📂 Organização do Repositório

```
meteorisco/
├── app/
│   └── streamlit_app.py      # Interface visual do operador (Streamlit)
├── domain/
│   ├── locations.yaml        # Coordenadas das 5 cidades-piloto
│   ├── risk_matrix.yaml      # Regras de elegibilidade (S2 Template)
│   ├── playbook.yaml         # Regras de comunicação (S3 Template)
│   └── portfolio.csv         # Carteira sintética de segurados
├── evals/
│   ├── golden_cases.yaml     # Cenários de negócio esperados
│   └── eval_runner.py        # Validador de evals
├── fixtures/
│   └── open_meteo_*.json     # Fixtures de dados climáticos reais/extremos
├── scripts/
│   └── capture_fixtures.py   # Utilitário para popular as fixtures
├── src/
│   ├── agents/               # Código dos 5 agentes
│   ├── config/               # Pydantic Settings
│   ├── contracts/            # Schemas Pydantic v2 (Contratos)
│   ├── harness/              # Runner sequencial do ciclo
│   └── skills/               # Funções determinísticas reutilizáveis
└── tests/                    # Testes de cobertura unitária (pytest)
```

---

## ⚖️ Licença

Este projeto é disponibilizado sob a **Licença MIT**. Veja o arquivo LICENSE para detalhes.
