# MeteoRisco — Relatório Técnico & de Engenharia

**Projeto:** Desafio 05 — Ferramenta Inteligente para Comunicação Proativa com o Segurado  
**Equipe:** Seguros Connect  
**Data:** 12 de Setembro de 2026  
**Status do Projeto:** MVP Concluído & Homologado — 26/26 Testes Aprovados (100% Pass)  
**Classificação:** Documentação Técnica e Arquitetura de Inteligência Artificial (I2A2)  

### Integrantes:
- **Edcarlos Cardôso de Farias** — edcarlos.cfarias@gmail.com | (82) 99935-1714
- **Eric Pimentel** — casajogos242@gmail.com | (91) 98624-8987
- **Kleber Dias da Silva** — kdias.contabilista@gmail.com | (11) 99174-9480
- **Luiz Guilherme Rodrigues Silva** — guilhersilv@hotmail.com | (61) 98313-3519
- **Suellen Munford Merat** — suellenmunford@gmail.com | (21) 97475-2272

### Acesso Público e Demonstração:
- **Repositório Oficial no GitHub:** [https://github.com/edcarloscardoso/meteorisco](https://github.com/edcarloscardoso/meteorisco)
- **Repositório Fork (Deploy Streamlit):** [https://github.com/enps2015/meteorisco](https://github.com/enps2015/meteorisco)
- **Aplicação em Nuvem (Streamlit Cloud):** [https://meteorisco-fypi76f3ra7umxw8v9hbgt.streamlit.app](https://meteorisco-fypi76f3ra7umxw8v9hbgt.streamlit.app)

---

## 1. RESUMO EXECUTIVO & PROPOSTA DE VALOR

O **MeteoRisco** é uma solução de inteligência preventiva (*loss prevention*) orientada a carteiras de seguros nos ramos **Automóvel** e **Residencial**. Seu propósito central é transformar a dinâmica histórica do mercado segurador: em vez de manter uma postura passiva — onde o segurado procura a seguradora somente após a tragédia consumada para pedir indenização —, a plataforma monitora ativamente previsões meteorológicas em tempo real, avalia os riscos com base em regras de subscrição (*underwriting*) determinísticas e emite orientações práticas e personalizadas **antes da ocorrência do sinistro**.

```
       MODELO TRADICIONAL (REATIVO)              MODELO METEORISCO (PROATIVO)
┌────────────────────────────────────────┐ ┌────────────────────────────────────────┐
│  Tempestade atinge o bem segurado      │ │  1. Monitoramento contínuo do clima    │
│                 ▼                      │ │                 ▼                      │
│  Dano consumado (alagamento / quebra)  │ │  2. Avaliação atuarial de risco        │
│                 ▼                      │ │                 ▼                      │
│  Abertura de sinistro e desgaste       │ │  3. Orientação preventiva direcionada  │
│                 ▼                      │ │                 ▼                      │
│  Indenização financeira (Custo Alto)   │ │  4. Dano mitigado / Sinistro evitado   │
└────────────────────────────────────────┘ └────────────────────────────────────────┘
```

A solução foi construída sob uma arquitetura multiagente desacoplada, orientada por contratos tipados e ancorada em um princípio inegociável de engenharia: **a elegibilidade de quem recebe o alerta e a matriz de riscos são 100% determinísticas**. Modelos de Linguagem (LLM) são empregados exclusivamente na camada de redação e personalização da linguagem humana, impedindo alucinações jurídicas ou falhas de subscrição. Além disso, a plataforma introduz o conceito atuarial do **Silêncio Inteligente**: quando as condições climáticas estão abaixo dos limiares de perigo, o sistema deliberadamente não dispara comunicações, poupando o segurado da fadiga de alertas desnecessários.

### Indicadores Principais do MVP:
- **Cobertura de Testes:** 26/26 testes automatizados aprovados (13 testes unitários com Pytest + 13 cenários de negócio nos Golden Evals), alcançando **100% de aprovação**.
- **Latência Operacional:** Ciclo determinístico completo executado em **~120 ms**, permitindo processamento em escala.
- **Abrangência Geográfica:** Modelagem calibrada para as **5 macrorregiões do Brasil** (Norte, Nordeste, Centro-Oeste, Sudeste e Sul), com suporte visual às malhas territoriais do IBGE.
- **Rastreabilidade e Governança:** Cada mensagem despachada recebe um identificador único, carimbo de tempo UTC e hash criptográfico **SHA-256**, com suporte a veto operacional (*Human-in-the-Loop*).

---

## 2. O PROBLEMA DE NEGÓCIO: A VIRADA DE CHAVE DO REATIVO AO PROATIVO

### 2.1 A Dor do Segurado e da Seguradora
Quem contrata um seguro residencial ou automotivo costuma ter contato com a seguradora em apenas dois momentos: no fechamento da apólice e na abertura do aviso de sinistro. Quando um evento climático severo ocorre — seja uma enxurrada em Belém, uma chuva de granizo em São Paulo ou um vendaval em Porto Alegre —, o segurado enfrenta transtornos materiais graves e a seguradora arca com despesas elevadas de regulação e indenização.

Muitos desses sinistros poderiam ser evitados com atitudes simples de prevenção tomadas 2 ou 3 horas antes:
- Guardar o carro em um estacionamento coberto antes da tempestade com granizo;
- Não tentar atravessar um cruzamento urbano com histórico de alagamento;
- Elevar eletrodomésticos e móveis em residências térreas em áreas rebaixadas;
- Desobstruir ralos, calhas e grelhas externas antes de pancadas torrenciais.

### 2.2 Por que Alertas Tradicionais Falham? (O Efeito Spam)
Os sistemas comuns de notificação por SMS (como alertas gerais da Defesa Civil) enviam a mesma mensagem genérica para milhões de pessoas simultaneamente. O resultado é a **fadiga de notificações**:
1. Quem mora no 10º andar de um prédio recebe alerta de inundação e conclui que o aviso é inútil.
2. Quem tem o carro guardado em garagem subterrânea recebe alerta de granizo sem necessidade.
3. Com o tempo, o usuário silencia as mensagens e, quando um perigo real se aproxima, ele é pego desprevenido.

### 2.3 A Resposta do MeteoRisco
O MeteoRisco resolve esse problema ao combinar **dados meteorológicos em tempo real**, **cadastro detalhado da apólice** e **regras atuariais de underwriting**:
- **Segmentação Semântica por Ramo:** Uma tempestade severa gera orientações totalmente distintas para uma apólice Auto (rotas, trânsito, estacionamento) e para uma apólice Residencial (ralos, calhas, energia elétrica).
- **Filtro de Vulnerabilidade Real:** Se o veículo do segurado já pernoita em garagem coberta, o sistema não o incomoda com avisos de granizo leve.
- **Auditoria Jurídica Automática:** Nenhuma mensagem gerada por inteligência artificial é enviada sem passar por um auditor independente que barra promessas indevidas de cobertura securitária.

---

## 3. OBJETIVOS DA SOLUÇÃO & MATRIZ DE REQUISITOS (I2A2)

Para atender integralmente aos requisitos do Desafio 05, o projeto foi planejado e executado conforme a matriz funcional abaixo:

| Requisito | Descrição | Status no MVP |
|---|---|:---:|
| **RF-01: Ingestão Climática Aberta** | Obtenção de previsões meteorológicas em tempo real sem dependência de chaves de API restritivas. | **[Concluído]** |
| **RF-02: Underwriting Determinístico** | Matriz de regras com limiares objetivos de chuva, vento, código WMO e convecção (CAPE). | **[Concluído]** |
| **RF-03: Segmentação Auto & Residencial** | Aplicação de regras específicas para cada ramo de seguro e característica do bem. | **[Concluído]** |
| **RF-04: Silêncio Inteligente** | Supressão de mensagens quando o clima não oferece risco ou o bem está protegido. | **[Concluído]** |
| **RF-05: Redação Preventiva Contextual** | Geração de texto empático, claro e acionável para múltiplos canais (SMS, WhatsApp/App, E-mail). | **[Concluído]** |
| **RF-06: Auditoria de Conformidade** | Bloqueio automático de promessas de indenização, alarmismo excessivo ou alucinações. | **[Concluído]** |
| **RF-07: Intervenção Humana (HITL)** | Interface para operador inspecionar a trilha de agentes e exercer direito de veto manual. | **[Concluído]** |
| **RNF-01: Resiliência e Fallback Offline** | Garantia de funcionamento ininterrupto mesmo em caso de falha de conexão ou ausência de cota de LLM. | **[Concluído]** |
| **RNF-02: Integridade Criptográfica** | Geração de hash SHA-256 e timestamps UTC para auditoria atuarial de cada comunicação. | **[Concluído]** |
| **RNF-03: Performance de Execução** | Ciclo completo executado em fração de segundo (~120ms), viabilizando lotes volumosos. | **[Concluído]** |

---

## 4. ARQUITETURA DA SOLUÇÃO (AI ENGINEERING)

A arquitetura do MeteoRisco foi desenhada seguindo o padrão de **Camadas Desacopladas com Agentes Especializados**, garantindo total separação de responsabilidades:

```
┌──────────────────────────────────────────────────────────────────────────┐
│ 1. CAMADA DE APRESENTAÇÃO (Interface Executiva — Streamlit)             │
│    • Mapa Interativo das 5 Macrorregiões do IBGE (Plotly Scatter 2D)     │
│    • Painel de Disparo de Cenários (Normal, Adverso, Extremo)            │
│    • Trilha de Auditoria dos Agentes com Latências e Status              │
│    • Módulo Human-in-the-Loop com Veto Operacional Manual                │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ Chamada Direta via In-Process Runner
┌────────────────────────────────────▼─────────────────────────────────────┐
│ 2. CAMADA DE CONTROLE E RUNTIME (Harness / Control Plane)                │
│    • Orquestrador Sequencial (runner.py)                                 │
│    • Validação Rígida de Contratos Tipados (Pydantic v2)                 │
│    • Rastreabilidade e Coleta de Traces por Agente                       │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ Invocação de Agentes
┌────────────────────────────────────▼─────────────────────────────────────┐
│ 3. CAMADA DE RACIOCÍNIO & AGENTES (Reasoning Plane)                     │
│    [Scout Climático]       ──► I/O Externo e Coleta Meteorológica       │
│    [Analista MeteoRisco]   ──► Avaliação Atuarial Determinística        │
│    [Gestor de Exposição]   ──► Cruzamento de Carteira e Silêncio Ativo   │
│    [Redator Preventivo]    ──► Geração de Linguagem Natural (Playbook)  │
│    [Auditor de Decisão]    ──► Validação Regulatória e Bloqueio Legal    │
│    [Simulador/Despachante] ──► Log Criptográfico SHA-256 e Envio         │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ Chamada de Funções Especializadas
┌────────────────────────────────────▼─────────────────────────────────────┐
│ 4. CAMADA DE HABILIDADES & SERVIÇOS (Capability Plane)                  │
│    • fetch_weather (Open-Meteo REST Client + Fallback de Fixtures)       │
│    • normalize_weather (Cálculo de pior cenário nas próximas 24h)        │
│    • apply_risk_matrix (Motor de inferência determinística)             │
│    • select_insureds (Filtro relacional sobre carteira de clientes)      │
│    • audit_message (Validador semântico e regex de conformidade)        │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ Leitura de Arquivos de Domínio
┌────────────────────────────────────▼─────────────────────────────────────┐
│ 5. CAMADA DE DOMÍNIO SECURITÁRIO (Business & Domain Plane)              │
│    • locations.yaml (Metadados das 5 cidades-piloto brasileiras)         │
│    • risk_matrix.yaml (Regras de underwriting e thresholds de risco)     │
│    • playbook.yaml (Diretrizes de tom de voz, canais e proibições)       │
│    • portfolio.csv (Carteira sintética com 20 segurados e exposições)    │
│    • regioes_ibge.geojson (Fronteiras geográficas oficiais do IBGE)      │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 5. DESCRIÇÃO DOS AGENTES DESENVOLVIDOS

Em vez de criar um agente genérico e torcer para que ele não cometa erros na interpretação das apólices, o MeteoRisco adota **seis agentes com funções estritas e especializadas**:

```
[Open-Meteo API]
       │
       ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│    Scout     │ ───► │   Analista   │ ───► │  Gestor de   │
│  Climático   │      │  MeteoRisco  │      │  Exposição   │
└──────────────┘      └──────────────┘      └──────────────┘
                                                   │
                      ┌──────────────┐             │ (Apenas Elegíveis)
                      │   Redator    │ ◄───────────┘
                      │  Preventivo  │
                      └──────────────┘
                             │
                             ▼
                      ┌──────────────┐
                      │  Auditor de  │
                      │   Decisão    │
                      └──────────────┘
                             │
                             ▼
┌──────────────┐      ┌──────────────┐
│   Operador   │ ───► │  Simulador   │ ───► [Trilha Auditável SHA-256]
│    (HITL)    │      │ (Dispatcher) │
└──────────────┘      └──────────────┘
```

### 5.1 Scout Climático (`scout.py`)
- **Papel:** É o sentinela meteorológico do sistema.
- **Responsabilidade:** Conecta-se à API pública do Open-Meteo informando latitude e longitude da localidade. Coleta previsões horárias para as próximas 24 horas abrangendo precipitação acumulada (`precipitation`), rajadas de vento (`wind_gusts_10m`), código de tempo meteorológico WMO (`weather_code`) e energia convectiva (`cape` e `lifted_index`).
- **Resiliência:** Se a conexão externa falhar ou estiver sem internet, o Scout aciona imediatamente fixtures offline armazenadas localmente em `fixtures/`, garantindo que a operação nunca seja paralisada.

### 5.2 Analista MeteoRisco (`analyst.py`)
- **Papel:** É o perito de subscrição atuarial (*Underwriting Analyst*).
- **Responsabilidade:** Recebe as variáveis climáticas normalizadas e cruza com a `risk_matrix.yaml` de forma estritamente determinística. Classifica o evento em um dos quatro níveis de severidade: **Normal (Sem Risco)**, **Amarelo (Informativo)**, **Laranja (Preventivo)** ou **Vermelho (Severo/Urgente)**.
- **Garantia:** Nenhuma inteligência generativa atua aqui. A classificação é 100% matemática baseada em limiares técnicos.

### 5.3 Gestor de Exposição (`exposure_manager.py`)
- **Papel:** É o gerente de carteira e defensor da experiência do cliente (*Customer Experience*).
- **Responsabilidade:** Cruza a severidade identificada com o cadastro dos clientes (`portfolio.csv`) localizados na região afetada. Avalia os atributos de vulnerabilidade do bem:
  - *Automóvel:* O veículo fica estacionado na rua ou em garagem coberta?
  - *Residencial:* É casa térrea ou apartamento em andar alto? O imóvel fica em área com histórico de alagamento? Possui telhado tradicional ou laje?
- **Aplicação do Silêncio Inteligente:** Se o risco não afetar o perfil do cliente (por exemplo, granizo para um carro guardado em garagem fechada), o agente suprime o envio e registra a justificativa atuarial em auditoria.

### 5.4 Redator Preventivo (`writer.py`)
- **Papel:** É o comunicador empático e especialista em relacionamento.
- **Responsabilidade:** Para cada segurado considerado elegível, redige uma comunicação preventiva aderente às diretrizes do `playbook.yaml`.
- **Modos de Operação:**
  - *Modo Generativo:* Conecta-se ao gateway de LLM (Google Gemini ou OpenAI) com prompt rigorosamente instruído a manter tom respeitoso, sem termos técnicos indecifráveis (como "CAPE de 3000 J/kg") e com recomendações práticas imediatas.
  - *Modo Fallback:* Caso a API de LLM esteja indisponível, aciona um motor de templates paramétricos de alta qualidade, garantindo que a mensagem seja gerada sem interrupções.

### 5.5 Auditor de Decisão (`auditor.py`)
- **Papel:** É o oficial de conformidade jurídica e regulatória (*Compliance & Legal Officer*).
- **Responsabilidade:** Atua como barreira independente entre o Redator e o cliente final. Inspeciona cada texto gerado à procura de violações contratuais graves:
  - Promessas antecipadas de cobertura ("garantimos sua indenização", "sua apólice cobre integralmente");
  - Linguagem de pânico ou alarmismo indevido ("risco iminente de morte");
  - Afirmações categóricas sobre previsões estocásticas ("com certeza vai granizar");
  - Violações às diretrizes da SUSEP e da LGPD.
- **Comportamento:** Se detectar qualquer irregularidade, a mensagem recebe status **BLOCKED** com indicação da cláusula violada e não segue para despacho.

### 5.6 Simulador de Notificações / Despachante (`notification_simulator.py`)
- **Papel:** É a central transacional de disparos auditáveis.
- **Responsabilidade:** Recebe as mensagens aprovadas pelo Auditor e aplica o filtro de intervenção humana (HITL). Se o operador tiver exercido veto sobre algum segurado, o envio é cancelado com registro formal. Para os demais, gera a notificação formatada para o canal de destino (SMS, WhatsApp/App, E-mail), carimbando o registro com identificador único, data/hora UTC e hash criptográfico **SHA-256**.

---

## 6. STACK TECNOLÓGICA & RACIONAL DE ENGENHARIA

| Tecnologia | Versão | Função no Sistema | Racional da Escolha |
|---|---|---|---|
| **Python** | 3.11+ | Linguagem e Runtime | Padrão da indústria para ciência de dados, tipagem estática moderna e suporte nativo a ferramentas de IA. |
| **Pydantic v2** | 2.8+ | Contratos de Dados & Schemas | Validação rigorosa de tipos e dados intermediários em tempo de execução com altíssima velocidade. |
| **Pydantic-Settings** | 2.4+ | Gestão de Configurações | Leitura tipada de variáveis de ambiente (`.env`) com valores padrão seguros. |
| **Streamlit** | 1.38+ | Interface do Usuário | Desenvolvimento ágil de aplicações reativas em Python, permitindo neurodesign limpo e controle de estado nativo. |
| **Plotly** | 5.24+ | Visualização Geoespacial | Renderização vetorial leve de polígonos GeoJSON (IBGE) e pontos cartesianos sem necessidade de tokens de terceiros. |
| **Open-Meteo API** | v1 REST | Fonte de Dados Climáticos | API aberta, gratuita, de alta confiabilidade, sem exigência de chave de acesso e com dados convectivos detalhados. |
| **Pytest & HTTPX** | 8.3+ | Suíte de Testes Automatizados | Execução de testes unitários rápidos e interceptação segura de requisições HTTP (`pytest-httpx`, `respx`). |

### Racional da Escolha da API Open-Meteo
Durante o estudo de viabilidade técnica, três provedores de dados climáticos foram analisados:

| Critério Avaliado | Open-Meteo (Vencedor) | OpenWeatherMap (Free) | INMET (Oficial) |
|---|---|---|---|
| **Autenticação** | Aberto (Sem API Key) | Exige Chave de API | Chave restrita institucional |
| **Horizonte Temporal** | Previsão horária até 16 dias | Previsão a cada 3 horas (5 dias) | Predominantemente histórico |
| **Energia Convectiva (CAPE)** | **Disponível (Variável `cape`)** | Indisponível no plano gratuito | Indisponível via API REST |
| **Índice de Instabilidade** | **Disponível (`lifted_index`)** | Indisponível | Indisponível |
| **Códigos de Tempo (WMO)** | Suporte nativo (95, 96, 99) | Códigos próprios proprietários | Dados tabulares brutos |
| **Estabilidade de Acesso** | Superior a 99.9% | Boa | Instabilidades frequentes |

A presença de dados de convecção profunda (`cape` e `lifted_index`) foi o diferencial decisivo: tempestades de granizo e rajadas severas de vento no Brasil ocorrem por convecção térmica severa, parâmetros que o Open-Meteo disponibiliza abertamente.

---

## 7. FLUXO DE PROCESSAMENTO DETALHADO (ENGINE FLOW)

Cada ciclo de execução do MeteoRisco segue rigorosamente 6 fases consecutivas:

```
[Início do Ciclo: Seleção de Cidade / Disparo]
                     │
                     ▼
[Fase 1: Coleta Meteorológica — Scout Climático]
  - Conecta na API Open-Meteo (ou Fixture)
  - Extrai séries temporais de 24h (Chuva, Vento, WMO, CAPE)
  - Identifica o ponto de pico (pior momento nas próximas horas)
                     │
                     ▼
[Fase 2: Classificação Atuarial — Analista MeteoRisco]
  - Cruza métricas com a risk_matrix.yaml
  - Determina o tipo de evento (Chuva, Granizo, Vendaval ou Normal)
  - Classifica a severidade: Verde, Amarelo, Laranja ou Vermelho
                     │
                     ▼
[Fase 3: Seleção de Carteira — Gestor de Exposição]
  - Filtra clientes da cidade no portfolio.csv
  - Avalia fatores de vulnerabilidade do bem segurado
  - Aplica o Silêncio Inteligente (Supressão para bens protegidos)
  - Gera lista de clientes elegíveis e lista de suprimidos
                     │
                     ▼
[Fase 4: Redação Preventiva — Redator Preventivo]
  - Se houver elegíveis: aciona LLM ou Templates conforme o playbook.yaml
  - Ajusta tom de voz (Informativo, Preventivo ou Urgente)
  - Formata para o canal correto (SMS, App/WhatsApp ou E-mail)
                     │
                     ▼
[Fase 5: Auditoria Regulatória — Auditor de Decisão]
  - Varre o texto gerado contra regras proibitivas
  - Bloqueia promessas de indenização ou alarmismo
  - Emite parecer: APPROVED ou BLOCKED
                     │
                     ▼
[Fase 6: Simulação de Envio — Notification Simulator]
  - Aplica eventuais vetos manuais do operador humano (HITL)
  - Gera timestamp UTC e calcula hash SHA-256
  - Grava a trilha completa de auditoria no CycleResult
                     │
                     ▼
[Fim: Renderização no Painel Streamlit e Atualização de Estado]
```

---

## 8. REGRAS DE NEGÓCIO, UNDERWRITING DETERMINÍSTICO E SILÊNCIO INTELIGENTE

### 8.1 A Separação Sagrada: Decisão Determinística vs. Redação com IA
Um dos maiores aprendizados em projetos reais de Inteligência Artificial aplicada ao setor financeiro e segurador é: **nunca delegue decisões jurídicas ou de subscrição a um modelo probabilístico de linguagem**.

Se um LLM decidisse quem recebe o aviso ou quem tem cobertura, ele poderia sofrer alucinações, interpretar erradamente uma cláusula contratual ou prometer indenizações em desacordo com a apólice. No MeteoRisco, o LLM atua estritamente como redator e articulador de empatia; as decisões de quem é alertado e quais regras de risco são acionadas residem em código determinístico e tabelas YAML versionadas.

### 8.2 Matriz de Riscos (`risk_matrix.yaml`)
A tabela abaixo exemplifica os limiares técnicos aplicados pelo Analista:

| Evento de Risco | Severidade | Limiares Técnicos | Condição de Vulnerabilidade |
|---|:---:|---|---|
| **Chuva Intensa** | **Amarelo** | Precipitação $\ge 5{,}0$ mm/h | Imóvel térreo; veículo estacionado na rua |
| **Chuva Forte / Alagamento** | **Laranja** | Precipitação $\ge 15{,}0$ mm/h | Casas em áreas baixas; veículos em vias de trânsito |
| **Tempestade Severa** | **Vermelho** | Precipitação $\ge 30{,}0$ mm/h ou WMO 95 | Toda a carteira exposta ao ar livre |
| **Vendaval / Rajadas** | **Laranja** | Rajadas $\ge 50$ km/h | Imóveis com coberturas leves ou árvores próximas |
| **Vendaval Extremo** | **Vermelho** | Rajadas $\ge 70$ km/h | Casas com telhados tradicionais; veículos sob árvores |
| **Previsão de Granizo** | **Laranja** | WMO 96 ou CAPE $\ge 1500$ J/kg | Veículos sem garagem; residências com telhas frágeis |
| **Granizo Severo** | **Vermelho** | WMO 99 ou CAPE $\ge 2500$ J/kg | Veículos na rua (prioridade máxima de abrigo) |

### 8.3 O Momento Uau: Diferenciação Semântica por Ramo
Um mesmo temporal atinge uma cidade. O que acontece com os segurados?
- **Para o Segurado Auto (ex: Fábio Lima — Belém):** O foco imediato é o deslocamento e a proteção mecânica: *"Evite circular por vias expressas sujeitas a inundações e procure estacionamento em local elevado."*
- **Para o Segurado Residencial (ex: Ana Souza — Belém):** O foco é o patrimônio predial: *"Verifique se calhas e ralos estão limpos, eleve aparelhos elétricos do piso térreo e certifique-se do bom fechamento de janelas e portas."*

Essa distinção eleva drasticamente a percepção de valor: o cliente sente que a seguradora realmente conhece o patrimônio que está segurando.

### 8.4 A Decisão Epistemológica sobre Granizo
Radares e satélites meteorológicos em órbita não "enxergam" pedras de granizo caindo no chão em tempo real; o que a meteorologia moderna produz são **modelos numéricos de previsão atmosférica (NWP)** que calculam a instabilidade e o potencial convectivo do ar.

Por esse motivo, o Playbook de Comunicação do MeteoRisco estabelece uma **regra epistemológica estrita**:
- É terminantemente proibido redigir *"Granizo confirmado em seu bairro"* ou *"Com certeza vai cair granizo"*.
- É obrigatório utilizar ressalvas transparentes: *"Previsão de granizo estimada por modelos meteorológicos"* ou *"Condições favoráveis à formação de granizo"*.
Isso protege a reputação da seguradora caso o granizo se dissipe na alta atmosfera antes de atingir o solo.

---

## 9. EXEMPLOS REAIS DAS MENSAGENS GERADAS

Abaixo estão transcritos exemplos autênticos de mensagens geradas pelo pipeline do MeteoRisco para diferentes canais e situações:

### Exemplo 1: Chuva Severa em Belém (Ramo Residencial — Canal App / WhatsApp)
> **Notificação Push / WhatsApp:**  
> *"Olá, Ana Souza! Identificamos previsão de chuva forte com potencial de alagamento para a sua região em Belém nas próximas horas. Como o seu imóvel é térreo, recomendamos algumas ações simples para proteger sua casa: eleve eletrodomésticos e móveis de áreas baixas, verifique se os ralos externos e calhas estão desobstruídos e feche bem portas e janelas. Se precisar de assistência 24h, estamos à disposição no app da sua seguradora."*

### Exemplo 2: Tempestade com Potencial de Granizo em São Paulo (Ramo Automóvel — Canal SMS)
> **SMS (Limite de 160 caracteres):**  
> *"Alerta MeteoRisco: condicoes favoraveis a granizo em SP nas proximas horas. Recomendamos abrigar seu veiculo em local coberto seguro. Info no seu app."*

### Exemplo 3: Vendaval em Porto Alegre (Ramo Residencial — Canal E-mail)
> **Assunto:** *MeteoRisco: Alerta preventivo de vento forte para a sua residência*  
> **Corpo da Mensagem:**  
> *"Prezado Carlos Eduardo,*  
> *Nossos modelos de monitoramento climático apontam rajadas de vento severas previstas para Porto Alegre no final da tarde de hoje, que podem ultrapassar 75 km/h. Como sua residência possui cobertura de telhado tradicional, recomendamos algumas medidas preventivas:*  
> *1. Recolha ou amarre objetos soltos em áreas externas, varandas e quintais;*  
> *2. Certifique-se de que janelas e portões estejam travados;*  
> *3. Mantenha distância de estruturas metálicas leves e árvores de grande porte.*  
> *Nosso canal de atendimento e assistência residencial permanece pronto para apoiar você."*

---

## 10. GOVERNANÇA, AUDITORIA DE CONFORMIDADE & TRILHA CRIPTOGRÁFICA

### 10.1 O Trabalho do Auditor de Decisão
O agente Auditor realiza verificações automatizadas por expressões regulares e análise semântica. O quadro abaixo demonstra exemplos práticos de interceptação:

| Frase / Conteúdo Detectado | Classificação | Ação do Auditor | Justificativa Regulatória |
|---|:---:|:---:|---|
| *"Garantimos que a seguradora vai indenizar qualquer prejuízo."* | **VIOLAÇÃO** | **BLOCKED** | Promessa antecipada de cobertura sem abertura ou regulação de sinistro. |
| *"Com certeza vai cair granizo pesado no seu bairro."* | **VIOLAÇÃO** | **BLOCKED** | Falsa certeza sobre modelo probabilístico de previsão meteorológica. |
| *"Você corre risco de morte se sair de casa agora!"* | **VIOLAÇÃO** | **BLOCKED** | Alarmismo excessivo incompatível com comunicação corporativa sóbria. |
| *"Evacue seu bairro imediatamente e procure abrigo público."* | **VIOLAÇÃO** | **BLOCKED** | Ordem de evacuação é prerrogativa institucional exclusiva da Defesa Civil. |
| *"Previsão de chuva forte. Recomendamos guardar o carro em local coberto."* | **CONFORME** | **APPROVED** | Mensagem preventiva, educativa, acionável e juridicamente segura. |

### 10.2 Trilha Criptográfica SHA-256 e LGPD
Cada notificação simulada produz um registro com o seguinte formato:
```json
{
  "notification_id": "notif_sao_paulo_20260912T222129_f91a2b3c",
  "cycle_id": "sao_paulo_20260912T222129_a1b2c3d4",
  "insured_id": "INS001",
  "channel": "sms",
  "status": "sent",
  "timestamp_utc": "2026-09-12T22:21:29.412Z",
  "approved_by": "operador_hitl",
  "content_hash_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```
Esse hash garante a não-repudiação: a seguradora pode comprovar perante auditorias internas e reguladores da SUSEP o conteúdo exato, o momento e as condições meteorológicas em que o alerta foi disparado, respeitando a privacidade dos dados cadastrais em conformidade com a LGPD.

---

## 11. INTERFACE EXECUTIVA & NEURODESIGN (STREAMLIT)

A interface do usuário foi projetada seguindo diretrizes modernas de **Neurodesign**:
1. **Dark Mode First:** Fundo escuro com paleta calibrada (`#0B0F19`, `#1E293B`, `#38BDF8`), reduzindo o cansaço visual de operadores de centros de comando e seguros.
2. **Hierarquia e Semáforo Atuarial:** Cores funcionais indicam instantaneamente a severidade do evento (Verde para normal, Amarelo para informativo, Laranja para preventivo e Vermelho para emergencial).
3. **Mapa Interativo das 5 Macrorregiões do Brasil:** Desenvolvido em Plotly Scatter 2D integrado a polígonos GeoJSON oficiais do IBGE, permitindo alternar entre as 5 cidades-piloto com renderização leve e sem dependência de chaves de mapas pagos.
4. **Painel Human-in-the-Loop Integrado:** O operador visualiza todas as mensagens geradas em tempo real e pode desmarcar/vetar qualquer envio antes de confirmar o lote.
5. **Aba de Trilha de Execução:** Exibe a linha do tempo de execução com latências de cada agente (em milissegundos), garantindo total transparência e facilidade de diagnóstico.

---

## 12. SUÍTE DE TESTES AUTOMATIZADOS & HOMOLOGAÇÃO (26/26 APROVADOS)

A integridade e a robustez da solução são asseguradas por duas camadas de testes automatizados, totalizando **26 verificações independentes com 100% de sucesso**.

### 12.1 Testes Unitários via Pytest (13/13 Aprovados)

| Arquivo de Teste | Componente Auditado | Qtd | Resultado |
|---|---|:---:|:---:|
| `test_apply_risk_matrix.py` | Motor de inferência determinística da Matriz de Riscos | 1 | **PASSED** |
| `test_audit_message.py` | Bloqueio de frases proibidas e validação de mensagens aprovadas | 2 | **PASSED** |
| `test_fetch_weather.py` | Coleta via API Open-Meteo, fixtures locais e fallback em erro | 3 | **PASSED** |
| `test_normalize_weather.py` | Agregação estatística e detecção do pior cenário em 24h | 1 | **PASSED** |
| `test_runner.py` | Orquestração do ciclo sequencial e rejeição de localidade inválida | 2 | **PASSED** |
| `test_select_insureds.py` | Seleção determinística de carteira e Silêncio Inteligente | 2 | **PASSED** |
| `test_simulate_notify.py` | Registro de auditoria, cálculo de SHA-256 e respeito a vetos | 2 | **PASSED** |
| **Total Unitários** | **Suíte de Testes Unitários de Componentes** | **13** | **100% PASS** |

### 12.2 Suíte de Golden Evals de Negócio (`evals/eval_runner.py` — 13/13 Aprovados)

| Identificador | Descrição do Cenário de Negócio | Localidade | Resultado |
|---|---|---|:---:|
| **EV1** | Granizo Severo: Alerta para carro na rua e residência com telhado | São Paulo (SP) | **PASSED** |
| **EV2** | Chuva Forte Laranja: Alagamento em residências térreas | Belém (PA) | **PASSED** |
| **EV3** | Vendaval Severo: Impacto em coberturas vulneráveis | Porto Alegre (RS) | **PASSED** |
| **EV4** | Evento Abaixo do Limiar: Acionamento do **Silêncio Inteligente** | Brasília (DF) | **PASSED** |
| **EV5** | Conformidade Regulatória: Bloqueio de promessa de indenização | São Paulo (SP) | **PASSED** |
| **EV6** | Segmentação Semântica: Diferenciação simultânea Auto vs. Residencial | São Paulo (SP) | **PASSED** |
| **EV7** | Resiliência Operacional: Acionamento de fallback em queda de API | Recife (PE) | **PASSED** |
| **EV8** | Governança Human-in-the-Loop: Respeito ao veto manual do operador | São Paulo (SP) | **PASSED** |
| **EV-GEO-1** | Validação Regional Norte: Convecção equatorial e chuvas torrenciais | Belém (PA) | **PASSED** |
| **EV-GEO-2** | Validação Regional Nordeste: Chuvas tropicais costeiras | Recife (PE) | **PASSED** |
| **EV-GEO-3** | Validação Regional Centro-Oeste: Instabilidade de verão | Brasília (DF) | **PASSED** |
| **EV-GEO-4** | Validação Regional Sudeste: Ilhas de calor e granizo urbano | São Paulo (SP) | **PASSED** |
| **EV-GEO-5** | Validação Regional Sul: Ciclogênese e vendavais frontais | Porto Alegre (RS) | **PASSED** |
| **Total Evals** | **Cenários Homologados de Ponta a Ponta** | **13** | **100% PASS** |

### Registro de Execução Consolidado:
```bash
======================== 13 passed, 1 warning in 0.26s =========================
INFO - === Iniciando Execução da Suíte Completa de Evals (13 cenários) ===
...
INFO - [EV1] Granizo vermelho em São Paulo para segurados expostos ... [OK] PASSED
INFO - [EV2] Chuva intensa Laranja em Belém ........................... [OK] PASSED
INFO - [EV3] Vento forte em Porto Alegre afetando residências ........ [OK] PASSED
INFO - [EV4] Evento abaixo do limiar (Silêncio Inteligente) .......... [OK] PASSED
INFO - [EV5] Conformidade: Bloqueio de promessa de indenização ....... [OK] PASSED
INFO - [EV6] Personalização: Ações distintas por ramo ................. [OK] PASSED
INFO - [EV7] Resiliência: Acionamento de fallback em falha de API .... [OK] PASSED
INFO - [EV8] Human-in-the-Loop: Respeito ao veto manual .............. [OK] PASSED
INFO - [EV-GEO-1 a 5] Cobertura das 5 macrorregiões do IBGE .......... [OK] PASSED
================================================================================
INFO -   RESULTADO FINAL DOS EVALS: 13/13 PASSERAM (100.0%)
================================================================================
```

---

## 13. LIMITAÇÕES CONHECIDAS DO MVP & ROADMAP FUTURO

Com total honestidade e transparência técnica, registram-se os pontos de fronteira do MVP atual e o caminho planejado para versões de produção:

1. **Carteira Sintética Inicial:** O MVP opera com 20 segurados simulados em `portfolio.csv` para viabilizar demonstração didática e rápida. Na versão de escala corporativa, a camada de dados será conectada via conector SQL a sistemas de apólices reais (como Guidewire ou SAP for Insurance).
2. **Disparo Simulado (Mock Dispatcher):** O envio das mensagens ocorre atualmente no `NotificationSimulator`, gerando logs com hash criptográfico SHA-256. A arquitetura está pronta para plugar adaptadores reais de mensageria (como Twilio para SMS/WhatsApp e Firebase Cloud Messaging para push notifications).
3. **Resolução de Microrregiões por CEP:** A versão atual calcula o risco no nível de coordenadas municipais centrais. A evolução natural envolverá interpolação espacial com base no CEP do segurado, prevendo alagamentos em ruas específicas.

---

## 14. INSTRUÇÕES DE EXECUÇÃO & GUIA PRÁTICO

### 14.1 Acesso Online Imediato (Sem Instalação)
A aplicação está implantada e disponível publicamente no Streamlit Cloud:  
Link de Acesso: **[https://meteorisco-fypi76f3ra7umxw8v9hbgt.streamlit.app](https://meteorisco-fypi76f3ra7umxw8v9hbgt.streamlit.app)**

### 14.2 Execução Local no Ambiente do Usuário
Caso deseje rodar a aplicação localmente:

```bash
# 1. Clonar o repositório
git clone https://github.com/edcarloscardoso/meteorisco.git
cd meteorisco

# 2. Criar e ativar o ambiente virtual (Linux/macOS)
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar os testes unitários
PYTHONPATH=. pytest tests/ -v

# 5. Executar os Golden Evals de negócio
PYTHONPATH=. python3 evals/eval_runner.py

# 6. Iniciar a interface gráfica (Streamlit)
streamlit run app/streamlit_app.py
```
Acesse no navegador: `http://localhost:8501`.

---

## 15. ESTRUTURA DO PROJETO

```
meteorisco/
├── app/
│   ├── regioes_ibge.geojson      # Malha territorial oficial das 5 macrorregiões (IBGE)
│   └── streamlit_app.py          # Dashboard executivo com neurodesign e mapa interativo
├── domain/
│   ├── locations.yaml            # Metadados geográficos e climáticos das 5 capitais-piloto
│   ├── playbook.yaml             # Diretrizes de tom de voz, canais e regras proibitivas
│   ├── portfolio.csv             # Base de segurados sintética com atributos de risco
│   └── risk_matrix.yaml          # Matriz de underwriting e thresholds determinísticos
├── evals/
│   ├── eval_runner.py            # Motor de execução dos 13 Golden Evals
│   └── golden_cases.yaml         # Definição declarativa dos cenários de teste
├── fixtures/
│   ├── open_meteo_*.json         # Telemetria meteorológica offline para resiliência
│   └── open_meteo_extreme_*.json # Cenários meteorológicos severos para homologação
├── imagens_capturadas/           # Registro visual da aplicação em funcionamento
├── src/
│   ├── agents/                   # Implementação dos 6 agentes especializados
│   │   ├── analyst.py            # Analista MeteoRisco (Underwriting)
│   │   ├── auditor.py            # Auditor de Decisão (Compliance)
│   │   ├── exposure_manager.py   # Gestor de Exposição (Silêncio Inteligente)
│   │   ├── notification_simulator.py # Despachante transacional com SHA-256
│   │   ├── scout.py              # Scout Climático (Open-Meteo)
│   │   └── writer.py             # Redator Preventivo (Playbook e LLM)
│   ├── config/
│   │   └── settings.py           # Gestão de variáveis de ambiente com Pydantic
│   ├── contracts/                # Schemas Pydantic v2 (CycleResult, WeatherSignal, etc.)
│   ├── harness/
│   │   └── runner.py             # Orquestrador do ciclo e controle de observabilidade
│   └── skills/                   # Funções de I/O, normalização e auditoria
├── tests/                        # 13 Testes unitários automatizados com Pytest
├── streamlit_app.py              # Entrypoint raiz para deploy no Streamlit Cloud
├── requirements.txt              # Declaração determinística de dependências Python
├── Relatorio_Tecnico_Final_desafio_5.md # Relatório Técnico Oficial do Projeto
└── README.md                     # Documentação executiva do repositório
```

---

## 16. CONCLUSÃO

O **MeteoRisco** cumpre com excelência todos os requisitos do **Desafio 05 (I2A2)**. O projeto demonstra que o verdadeiro valor da Inteligência Artificial aplicada ao setor securitário não está em substituir o julgamento humano ou automatizar decisões jurídicas de forma descuidada, mas sim em atuar de forma simbiótica: **regras determinísticas onde a precisão atuarial é sagrada** e **agentes de linguagem onde a empatia, a clareza e a personalização salvam patrimônios**.

Ao unir resiliência de engenharia, governança com intervenção humana, respeito aos dados do segurado e uma interface profissional orientada a neurodesign, a equipe **Seguros Connect** entrega uma solução madura, com 100% de aprovação em testes automatizados e pronta para transformar a relação entre seguradoras e seus segurados.

---

*Relatório técnico final elaborado e consolidado pela equipe Seguros Connect para a banca avaliadora do I2A2.*  
*Setembro de 2026 — Desafio 05: Ferramenta Inteligente para Comunicação Proativa com o Segurado.*
