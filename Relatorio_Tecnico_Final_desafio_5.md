# METEORISCO — RELATÓRIO TÉCNICO & DE ENGENHARIA

**Programa de Especialização em Inteligência Artificial Aplicada (I2A2)**  
**Desafio 05:** Ferramenta Inteligente para Comunicação Proativa com o Segurado  
**Equipe:** Seguros Connect  
**Data:** 12 de Setembro de 2026  
**Status da Solução:** MVP Concluído & Homologado — 26/26 Testes Aprovados (100% Pass)  

### Equipe de Desenvolvimento:
- **Edcarlos Cardôso de Farias** — edcarlos.cfarias@gmail.com | (82) 99935-1714
- **Eric Pimentel** — casajogos242@gmail.com | (91) 98624-8987
- **Kleber Dias da Silva** — kdias.contabilista@gmail.com | (11) 99174-9480
- **Luiz Guilherme Rodrigues Silva** — guilhersilv@hotmail.com | (61) 98313-3519
- **Suellen Munford Merat** — suellenmunford@gmail.com | (21) 97475-2272

### Acesso Público e Demonstração Operacional:
- **Repositório Oficial no GitHub:** [https://github.com/edcarloscardoso/meteorisco](https://github.com/edcarloscardoso/meteorisco)
- **Repositório Fork (Deploy Streamlit):** [https://github.com/enps2015/meteorisco](https://github.com/enps2015/meteorisco)
- **Aplicação em Nuvem (Streamlit Cloud):** [https://meteorisco-fypi76f3ra7umxw8v9hbgt.streamlit.app](https://meteorisco-fypi76f3ra7umxw8v9hbgt.streamlit.app)


# 1. RESUMO EXECUTIVO & PROPOSTA DE VALOR

O MeteoRisco é uma solução de inteligência preventiva (*loss prevention*) voltada para carteiras de seguros nos ramos Automóvel e Residencial. Seu propósito fundamental é transformar a dinâmica histórica do mercado segurador: em vez de manter uma postura puramente reativa — na qual o segurado procura a companhia apenas após o desastre consumado para solicitar indenização —, a plataforma monitora continuamente previsões meteorológicas em tempo real, avalia o potencial de dano com regras de subscrição (*underwriting*) determinísticas e emite orientações práticas e personalizadas antes da ocorrência do sinistro.

![Comparativo entre o Modelo Tradicional Reativo e o Modelo MeteoRisco Proativo](docs/diagramas/diagrama_paradigma.png){width=95%}

*Fonte: Autores (2026).*

A solução foi concebida sob uma arquitetura multiagente desacoplada, orientada por contratos de dados rigorosamente tipados e alicerçada em uma premissa inegociável de engenharia: a elegibilidade de quem recebe o alerta e a matriz de riscos são 100% determinísticas. Modelos de Linguagem (LLM) são empregados exclusivamente na camada de redação e personalização da linguagem humana, impedindo qualquer alucinação jurídica ou distorção de coberturas securitárias. Além disso, a plataforma introduz o conceito do Silêncio Inteligente: quando as condições climáticas estão dentro dos padrões normais ou o segurado possui proteção natural, o sistema deliberadamente não dispara mensagens, protegendo o cliente da fadiga de alertas desnecessários.

Os principais indicadores do projeto atestam a maturidade da entrega:
1. Cobertura de Testes Automatizados: 26 testes aprovados em 2 baterias independentes (13 testes unitários com Pytest e 13 cenários de negócio nos Golden Evals), alcançando 100% de sucesso.
2. Latência Operacional: Ciclo determinístico completo executado em aproximadamente 120 milissegundos, garantindo viabilidade para processamento massivo de carteiras.
3. Abrangência Territorial: Calibração atuarial para as cinco macrorregiões geográficas do Brasil (Norte, Nordeste, Centro-Oeste, Sudeste e Sul), com suporte visual às malhas territoriais do IBGE.
4. Rastreabilidade Criptográfica: Cada notificação despachada recebe um identificador universal, carimbo de tempo UTC e hash criptográfico SHA-256 para fins de auditoria interna e conformidade regulatória.


# 2. O PROBLEMA DE NEGÓCIO: A VIRADA DE CHAVE DO REATIVO AO PROATIVO

## 2.1 A Realidade do Mercado Segurador
Quem contrata uma apólice de seguro residencial ou automotivo costuma ter contato com a seguradora em apenas duas ocasiões: no momento da assinatura do contrato e na hora do sinistro. Quando um evento climático extremo se manifesta — seja uma chuva torrencial em Belém, uma tempestade de granizo em São Paulo ou um vendaval em Porto Alegre —, o segurado enfrenta perdas patrimoniais dolorosas e a seguradora arca com elevados custos de regulação, reboque, reparos e indenizações financeiras.

Muitos desses sinistros poderiam ser completamente evitados ou drasticamente atenuados com ações preventivas simples, executadas duas ou três horas antes da tempestade:
- Estacionar o veículo em local coberto antes da ocorrência de granizo severo;
- Evitar o tráfego por vias rebaixadas com histórico de alagamento rápido;
- Elevar eletrodomésticos do chão em imóveis térreos localizados em áreas de baixada;
- Desobstruir ralos, calhas e grelhas pluviais antes de chuvas de forte intensidade.

## 2.2 O Fenômeno da Fadiga de Notificações
Os sistemas convencionais de alerta em massa (como mensagens genéricas via SMS da Defesa Civil) disparam o mesmo texto idêntico para milhões de pessoas indiscriminadamente. Essa abordagem gera o problema crônico da fadiga de notificações:
1. Quem reside no décimo andar de um edifício recebe alerta de enchente e percebe o aviso como irrelevante;
2. Quem guarda o automóvel em garagem subterrânea fechada recebe alerta de granizo sem necessidade;
3. Com o tempo, o usuário passa a ignorar ou silenciar todas as mensagens da seguradora, ficando desprotegido quando um perigo real se aproxima.

## 2.3 A Abordagem Proativa do MeteoRisco
O MeteoRisco resolve esse dilema combinando dados meteorológicos em tempo real, características cadastrais detalhadas do bem e regras atuarialmente validadas:
- Segmentação Semântica por Ramo: Uma mesma tempestade severa gera orientações completamente distintas para uma apólice Automóvel (rotas alternativas, estacionamento elevado) e para uma apólice Residencial (ralos, calhas, desligamento de eletrônicos);
- Filtro de Vulnerabilidade Efetiva: Se a residência ou veículo já estiver protegido contra aquela ameaça específica, o sistema não incomoda o segurado;
- Auditoria Jurídica Prévia: Nenhuma mensagem produzida por inteligência artificial é enviada ao cliente sem passar por um auditor automatizado que barra promessas indevidas de cobertura securitária.


# 3. OBJETIVOS DA SOLUÇÃO & MATRIZ DE REQUISITOS (I2A2)

Para cumprir integralmente o escopo pedagógico e técnico do Desafio 05, o sistema foi concebido e implementado de acordo com a matriz de requisitos abaixo:

| Requisito | Descrição Funcional / Não-Funcional | Status no MVP |
|:----------------|:---------------------------------------------------------|:-------------:|
| RF-01: Ingestão Climática Aberta | Obtenção de previsões meteorológicas em tempo real sem dependência de chaves de API restritivas. | Aprovado |
| RF-02: Underwriting Determinístico | Matriz de regras com limiares objetivos de chuva, vento, código WMO e convecção (CAPE). | Aprovado |
| RF-03: Segmentação Auto & Residencial | Aplicação de regras específicas para cada ramo de seguro e característica do bem. | Aprovado |
| RF-04: Silêncio Inteligente | Supressão de mensagens quando o clima não oferece risco ou o bem está protegido. | Aprovado |
| RF-05: Redação Preventiva Contextual | Geração de texto empático, claro e acionável para múltiplos canais (SMS, WhatsApp/App, E-mail). | Aprovado |
| RF-06: Auditoria de Conformidade | Bloqueio automático de promessas de indenização, alarmismo excessivo ou alucinações. | Aprovado |
| RF-07: Intervenção Humana (HITL) | Interface para operador inspecionar a trilha de agentes e exercer direito de veto manual. | Aprovado |
| RNF-01: Resiliência e Fallback Offline | Garantia de funcionamento ininterrupto mesmo em caso de falha de conexão ou ausência de cota de LLM. | Aprovado |
| RNF-02: Integridade Criptográfica | Geração de hash SHA-256 e timestamps UTC para auditoria atuarial de cada comunicação. | Aprovado |
| RNF-03: Performance de Execução | Ciclo completo executado em fração de segundo (~120ms), viabilizando lotes volumosos. | Aprovado |


# 4. ARQUITETURA DA SOLUÇÃO (AI ENGINEERING)

A arquitetura do MeteoRisco segue o padrão moderno de Engenharia de Inteligência Artificial em cinco camadas desacopladas, assegurando isolamento estrutural e alta testabilidade:

![Visão Arquitetural em Cinco Camadas Desacopladas do MeteoRisco](docs/diagramas/diagrama_arquitetura.png){width=95%}

*Fonte: Autores (2026).*

As cinco camadas operam com responsabilidades bem delimitadas:
1. Camada de Apresentação (Interface Executiva — Streamlit): Provê o painel operacional com neurodesign em modo escuro, renderização geográfica vetorial das cinco regiões do IBGE, disparo de simulações e painel de governança Human-in-the-Loop;
2. Camada de Runtime & Controle (Control Plane / Harness): Implementada pelo módulo `runner.py`, orquestra a cadeia de execução de ponta a ponta, valida rigidamente os contratos tipados via Pydantic v2 e captura as métricas de latência e traces de cada agente;
3. Camada de Raciocínio & Agentes (Reasoning Plane): Abriga os agentes cognitivos e especializados, isolando o papel de cada inteligência na esteira;
4. Camada de Capacidades & Serviços (Capability Plane): Conjunto de funções determinísticas puras de I/O, cálculo estatístico de pior cenário em 24 horas, aplicação de matriz de risco e varredura léxico-semântica de conformidade;
5. Camada de Domínio & Regras Securitárias (Domain Plane): Concentra as definições de negócio em arquivos declarativos (YAML e CSV), facilitando a calibração por especialistas em seguros sem necessidade de alterações no código-fonte.


# 5. DESCRIÇÃO DOS AGENTES DESENVOLVIDOS

Em vez de concentrar toda a lógica em um único modelo de linguagem monolítico — abordagem propensa a alucinações e erros de subscrição —, o MeteoRisco adota seis agentes especializados com atribuições estritas e complementares, operando em cadeia sequencial sob supervisão humana.

![Pipeline Sequencial dos Agentes Especializados e Governança Human-in-the-Loop](docs/diagramas/diagrama_agentes.png){width=98%}

*Fonte: Autores (2026).*

## 5.1 Scout Climático (`scout.py`)
O Scout Climático atua como o sentinela meteorológico do sistema. Ele é responsável por conectar-se à API pública do Open-Meteo passando as coordenadas geográficas da localidade monitorada. O agente extrai séries temporais para as próximas 24 horas contemplando precipitação acumulada (`precipitation`), velocidade das rajadas de vento a 10 metros (`wind_gusts_10m`), código de tempo meteorológico WMO (`weather_code`), energia potencial convectiva disponível (`cape`) e índice de levantamento atmosférico (`lifted_index`). Se a conectividade externa falhar, o Scout aciona automaticamente fixtures locais em `fixtures/`, mantendo a estabilidade operacional.

## 5.2 Analista MeteoRisco (`analyst.py`)
O Analista MeteoRisco personifica o especialista de subscrição atuarial (*Underwriting Analyst*). Ele recebe a telemetria normalizada do Scout e cruza os dados com a matriz de regras determinística (`risk_matrix.yaml`). O agente classifica o evento em um dos quatro níveis de severidade padronizados: Verde (Normal/Sem Risco), Amarelo (Informativo), Laranja (Preventivo) ou Vermelho (Severo/Urgente). Nenhuma inteligência generativa atua nesta etapa: a classificação é 100% matemática e baseada em limiares pré-fixados.

## 5.3 Gestor de Exposição (`exposure_manager.py`)
O Gestor de Exposição atua como o curador da carteira de clientes e guardião do relacionamento (*Customer Experience*). Ele cruza a severidade identificada com a base de segurados (`portfolio.csv`) da região afetada. O agente examina detalhadamente os fatores de vulnerabilidade física do bem:
- Para Automóveis: o veículo pernoita na rua ou em garagem coberta?
- Para Residências: trata-se de casa térrea ou apartamento em andar alto? O imóvel localiza-se em área sujeita a alagamento? A cobertura é de telhado tradicional ou laje impermeabilizada?
Se o risco previsto não atingir o perfil daquele segurado (por exemplo, granizo para um automóvel abrigado em garagem fechada), o agente aplica o Silêncio Inteligente e registra formalmente a justificativa da supressão.

## 5.4 Redator Preventivo (`writer.py`)
O Redator Preventivo é o comunicador empático da plataforma. Para os clientes considerados elegíveis pelo Gestor de Exposição, ele redige mensagens preventivas personalizadas seguindo as diretrizes do `playbook.yaml`. O agente ajusta dinamicamente a urgência e o tom de voz conforme a severidade, adaptando o formato para o canal de contato específico (SMS com até 160 caracteres, WhatsApp/Push Notification para aplicativo ou E-mail com orientações detalhadas). Conta com suporte nativo a modelos de linguagem (Google Gemini / OpenAI) e fallback automático para gerador paramétrico de alta fidelidade.

## 5.5 Auditor de Decisão (`auditor.py`)
O Auditor de Decisão é o oficial independente de conformidade jurídica e regulatória (*Compliance Officer*). Ele atua como uma barreira de proteção entre a redação e o cliente final, inspecionando cada rascunho em busca de violações regulatórias:
- Promessas indevidas de indenização ("garantimos o ressarcimento financeiro");
- Afirmações precipitadas sobre cobertura contratual antes da regulação de sinistro;
- Expressões de alarmismo extremo ("risco iminente de morte");
- Certezas descabidas sobre previsões probabilísticas ("com certeza vai cair granizo").
Caso qualquer inconsistência seja detectada, a mensagem é imediatamente bloqueada (status BLOCKED) com indicação da regra violada.

## 5.6 Simulador de Notificações / Despachante (`notification_simulator.py`)
O Simulador de Notificações representa a central transacional de disparos. Ele recebe as mensagens validadas pelo Auditor e aplica o filtro de governança Human-in-the-Loop. Havendo veto manual do operador, o envio é cancelado com registro de justificativa. Para as mensagens autorizadas, o agente gera um registro auditável com identificador universal, carimbo de tempo UTC e hash criptográfico SHA-256 do conteúdo despachado.


# 6. STACK TECNOLÓGICA & RACIONAL DE ENGENHARIA

A seleção tecnológica do projeto priorizou solidez, simplicidade de implantação e aderência aos padrões de mercado:

| Tecnologia | Versão | Função na Solução | Justificativa Técnica |
|:--------------------|:-------:|:----------------------------|:-----------------------------------------------------|
| Python | 3.11+ | Linguagem e Runtime | Padrão dominante em ciência de dados e tipagem estática moderna. |
| Pydantic v2 | 2.8+ | Contratos de Dados | Validação estrita de schemas em tempo de execução com altíssima performance. |
| Pydantic-Settings | 2.4+ | Gestão de Configuração | Leitura tipada de variáveis de ambiente com suporte a arquivos `.env`. |
| Streamlit | 1.38+ | Interface do Usuário | Construção rápida de dashboards reativos em Python com suporte a neurodesign. |
| Plotly | 5.24+ | Visualização Cartográfica | Renderização vetorial leve de malhas GeoJSON oficiais do IBGE sem chaves pagas. |
| Open-Meteo API | v1 REST | Provedor Meteorológico | Dados abertos em tempo real, sem necessidade de token e com variáveis convectivas. |
| Pytest & HTTPX | 8.3+ | Suíte de Testes | Execução veloz de testes unitários com simulação controlada de I/O (`respx`). |

## 6.1 Racional da Escolha da API Open-Meteo
Durante o estudo de viabilidade, foram comparadas três alternativas de dados meteorológicos:
1. OpenWeatherMap (Plano Gratuito): Exige cadastro e chave de API pessoal; não disponibiliza variáveis de convecção profunda e possui limite restrito de requisições;
2. INMET (Instituto Nacional de Meteorologia): Apresenta histórico consolidado no Brasil, mas sua interface REST carece de previsões horárias futuras consistentes e enfrenta frequentes instabilidades de infraestrutura;
3. Open-Meteo (Escolha Adotada): Totalmente aberta, sem necessidade de chave de autenticação, alta disponibilidade comprovada (>99,9%) e fornecimento nativo de energia potencial convectiva (`cape` em J/kg) e índice de instabilidade (`lifted_index`). Esses parâmetros são cruciais para a previsão assertiva de tempestades de granizo no território brasileiro.


# 7. FLUXO DE PROCESSAMENTO DETALHADO (ENGINE FLOW)

A execução do pipeline do MeteoRisco segue uma sequência de seis etapas integradas, representadas no fluxo a seguir:

![Fluxo de Processamento Ponta a Ponta (Engine Flow)](docs/diagramas/diagrama_fluxo.png){width=95%}

*Fonte: Autores (2026).*

O detalhamento operacional de cada etapa compreende:
1. Fase 1 (Coleta Meteorológica): O Scout Climático conecta-se à API do Open-Meteo, recupera as séries horárias das próximas 24 horas e calcula os valores extremos (pico de precipitação, rajada máxima e instabilidade convectiva);
2. Fase 2 (Classificação Atuarial): O Analista MeteoRisco confronta os picos climáticos com a `risk_matrix.yaml`, determinando a categoria do evento e sua gravidade (Verde, Amarelo, Laranja ou Vermelho);
3. Fase 3 (Seleção de Carteira): O Gestor de Exposição avalia cada segurado da praça geográfica no `portfolio.csv`, aplicando as regras de vulnerabilidade física e ativando o Silêncio Inteligente para segurados sem risco;
4. Fase 4 (Redação Preventiva): Para os clientes elegíveis, o Redator Preventivo formula a orientação com base no `playbook.yaml`, calibrando tom de voz e call-to-action de acordo com o canal;
5. Fase 5 (Auditoria Regulatória): O Auditor de Decisão realiza varredura automática sobre o texto, bloqueando afirmações indevidas antes do envio;
6. Fase 6 (Despacho Auditado): O Simulador de Notificações aplica as decisões do operador humano, gera o carimbo UTC e calcula o hash SHA-256 de auditoria.


# 8. REGRAS DE NEGÓCIO, UNDERWRITING DETERMINÍSTICO E SILÊNCIO INTELIGENTE

## 8.1 A Separação Sagrada: Decisão Determinística vs. Redação com IA
Um dos pilares conceituais do MeteoRisco é a estrita separação entre a tomada de decisão atuarial e a redação de mensagens:
- A decisão de subscrição (quem é afetado, qual o nível de severidade e quais clientes devem ser avisados) é 100% determinística, governada por algoritmos de código aberto e matrizes declarativas YAML auditáveis;
- A geração de linguagem natural (como explicar o evento de forma calorosa, clara e acionável) é delegada aos agentes de redação, operando sob restrições rígidas de vocabulário e estilo.
Essa distinção elimina de forma definitiva o risco de alucinações em critérios de seguro.

## 8.2 Matriz de Riscos (`risk_matrix.yaml`)
A Matriz de Riscos do sistema adota limiares técnicos calibrados para a realidade climática brasileira:

| Evento de Risco | Severidade | Limiares Técnicos de Acionamento | Condição de Vulnerabilidade Específica |
|:-------------------|:----------:|:----------------------------------|:---------------------------------------|
| Chuva Moderada | Amarelo | Precipitação $\ge 5{,}0$ mm/h | Imóvel térreo; veículo estacionado na rua |
| Chuva Forte / Alagamento | Laranja | Precipitação $\ge 15{,}0$ mm/h | Residências em baixadas; tráfego urbano |
| Tempestade Severa | Vermelho | Precipitação $\ge 30{,}0$ mm/h ou WMO 95 | Toda a carteira exposta ao ar livre |
| Vendaval Moderado | Laranja | Rajadas de vento $\ge 50$ km/h | Imóveis com coberturas leves ou árvores |
| Vendaval Severo | Vermelho | Rajadas de vento $\ge 70$ km/h | Residências com telhados tradicionais |
| Previsão de Granizo | Laranja | Código WMO 96 ou CAPE $\ge 1500$ J/kg | Veículos sem garagem coberta |
| Granizo Severo | Vermelho | Código WMO 99 ou CAPE $\ge 2500$ J/kg | Veículos na rua (prioridade máxima de abrigo) |

## 8.3 A Diferenciação Semântica por Ramo
A mesma tempestade climática impõe ameaças distintas conforme a natureza do bem:
- Para o Ramo Automóvel: O risco preponderante é o dano mecânico por calço hidráulico (tentativa de atravessar poças profundas), amassamento de lataria e quebra de vidros por granizo ou queda de galhos. A comunicação orienta: *"Procure abrigo em estacionamento coberto e evite circular por vias alagadas."*
- Para o Ramo Residencial: O risco concentra-se no refluxo de água por bueiros, transbordamento de calhas entupidas e queima de circuitos por descargas elétricas. A comunicação orienta: *"Limpe ralos e calhas, eleve eletrodomésticos do solo e retire aparelhos da tomada."*

## 8.4 A Decisão Epistemológica sobre Modelos de Granizo
Sensores de superfície e radares meteorológicos não registram pedras de granizo caindo ao solo em tempo real; a ciência meteorológica produz modelos numéricos de previsão atmosférica (NWP) que estimam a probabilidade convectiva.

Por essa razão, o Playbook de Comunicação do MeteoRisco impõe uma diretriz epistemológica transparente:
- É proibido afirmar categoricamente *"Granizo confirmado em seu bairro"*;
- É obrigatório utilizar fórmulas de ressalva como *"Previsão de granizo estimada por modelos meteorológicos"* ou *"Condições atmosféricas favoráveis à ocorrência de granizo"*.
Isso salvaguarda a credibilidade institucional da seguradora caso o granizo se funda na atmosfera antes de atingir a superfície.


# 9. EXEMPLOS REAIS DAS MENSAGENS GERADAS

Abaixo estão transcritos exemplos literais de comunicações produzidas pelo MeteoRisco durante os testes de homologação:

### 9.1 Chuva Severa em Belém (Ramo Residencial — Canal App / WhatsApp)
> "Olá, Ana Souza! Identificamos previsão de chuva forte com potencial de alagamento para a sua região em Belém nas próximas horas. Como o seu imóvel é térreo, recomendamos algumas ações simples para proteger sua casa: eleve eletrodomésticos e móveis de áreas baixas, verifique se os ralos externos e calhas estão desobstruídos e feche bem portas e janelas. Se precisar de assistência 24h, estamos à disposição no app da sua seguradora."

### 9.2 Tempestade com Risco de Granizo em São Paulo (Ramo Automóvel — Canal SMS)
> "Alerta MeteoRisco: condicoes favoraveis a granizo em SP nas proximas horas. Recomendamos abrigar seu veiculo em local coberto seguro. Info no seu app."

### 9.3 Vendaval Severo em Porto Alegre (Ramo Residencial — Canal E-mail)
> **Assunto:** MeteoRisco: Alerta preventivo de vento forte para a sua residência  
> **Mensagem:**  
> "Prezado Carlos Eduardo,  
> Nossos modelos de monitoramento climático apontam rajadas de vento severas previstas para Porto Alegre no final da tarde de hoje, podendo ultrapassar 75 km/h. Como sua residência possui cobertura de telhado tradicional, recomendamos algumas medidas preventivas:  
> 1. Recolha ou amarre objetos soltos em varandas, sacadas e jardins;  
> 2. Certifique-se do travamento seguro de portões e janelas;  
> 3. Mantenha distância de estruturas metálicas provisórias e árvores de grande porte.  
> Nossa central de assistência residencial está pronta para apoiar você em caso de necessidade."


# 10. GOVERNANÇA, CONFORMIDADE & TRILHA CRIPTOGRÁFICA

## 10.1 Inspeção Regulatória do Auditor de Decisão
O agente Auditor aplica filtros automáticos por correspondência de padrões e análise semântica. O quadro abaixo demonstra casos reais de fiscalização:

| Conteúdo Inspecionado no Rascunho | Classificação | Parecer do Auditor | Fundamentação Regulatória |
|:-----------------------------------------------------|:-------------:|:------------------:|:---------------------------------------------------|
| "Garantimos a indenização integral de qualquer dano." | Violação | BLOQUEADO | Promessa antecipada de cobertura sem regulação de sinistro. |
| "Com certeza vai cair granizo pesado no seu bairro." | Violação | BLOQUEADO | Afirmação categórica sobre modelo probabilístico de clima. |
| "Você corre risco de morte se permanecer no local!" | Violação | BLOQUEADO | Tom alarmista e sensacionalista incompatível com seguros. |
| "Evacue o bairro imediatamente e busque abrigo." | Violação | BLOQUEADO | Prerrogativa institucional privativa da Defesa Civil. |
| "Previsão de chuva forte. Recomendamos guardar o veículo." | Conforme | APROVADO | Orientação educativa, preventiva e juridicamente correta. |

## 10.2 Trilha de Auditoria com Hash SHA-256
Cada notificação homologada gera uma estrutura de log padronizada em conformidade com as diretrizes da LGPD:
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
O hash SHA-256 garante a não-repudiação da comunicação perante instâncias de fiscalização (como a SUSEP e auditorias de solvência), provando o exato teor da mensagem enviada e o contexto meteorológico que a motivou.


# 11. INTERFACE EXECUTIVA & NEURODESIGN (STREAMLIT)

O painel de controle do MeteoRisco foi desenvolvido sob os preceitos do Neurodesign Aplicado a Ambientes Operacionais:
1. Paleta Dark Mode First: Emprego de tons escuros calibrados (`#0B0F19`, `#1E293B`, `#38BDF8`), diminuindo a fadiga ocular de operadores de centrais de monitoramento durante turnos prolongados;
2. Semáforo Visual Atuarial: Uso rigoroso de cores semafóricas universais (Verde para situação normal, Amarelo para atenção preventiva, Laranja para alerta tático e Vermelho para emergência severa);
3. Mapa Vetorial das 5 Macrorregiões do IBGE: Construído em Plotly com polígonos GeoJSON oficiais, garantindo navegação geográfica fluida sem depender de serviços externos de mapa sujeitos a cobrança;
4. Governança Human-in-the-Loop Integrada: O operador visualiza a lista completa de comunicações aprovadas pelo Auditor e possui o poder de desmarcar ou vetar qualquer destinatário com um único clique antes da autorização do lote;
5. Linha do Tempo e Trilha de Agentes: Aba dedicada com registro cronológico e medição de latência individual de cada agente em milissegundos, oferecendo total transparência diagnóstica.


# 12. SUÍTE DE TESTES AUTOMATIZADOS & HOMOLOGAÇÃO (26/26 APROVADOS)

A robustez da solução é atestada por duas suítes automatizadas complementares, somando 26 testes rigorosamente aprovados.

## 12.1 Testes Unitários de Componentes via Pytest (13/13 Aprovados)

| Arquivo de Teste | Camada / Componente Auditado | Qtd. Testes | Resultado |
|:---------------------------------------|:-----------------------------------------------------|:-----------:|:---------:|
| test_apply_risk_matrix.py | Motor determinístico da Matriz de Riscos | 1 | APROVADO |
| test_audit_message.py | Bloqueio de frases proibidas e mensagens conformes | 2 | APROVADO |
| test_fetch_weather.py | Coleta via API Open-Meteo, fixtures e resiliência | 3 | APROVADO |
| test_normalize_weather.py | Normalização estatística e pior cenário em 24h | 1 | APROVADO |
| test_runner.py | Orquestração do ciclo e tratamento de exceções | 2 | APROVADO |
| test_select_insureds.py | Seleção de carteira e Silêncio Inteligente | 2 | APROVADO |
| test_simulate_notify.py | Trilha criptográfica SHA-256 e respeito a vetos | 2 | APROVADO |
| **TOTAL UNITÁRIOS** | **Suíte de Testes Unitários de Componentes** | **13** | **100% PASS** |

## 12.2 Suíte de Golden Evals de Negócio (`eval_runner.py` — 13/13 Aprovados)

| Caso de Teste | Descrição do Cenário de Negócio | Localidade / Região | Resultado |
|:--------------|:-----------------------------------------------------|:--------------------|:---------:|
| EV1 | Granizo Severo: Alerta para carro na rua e telhado | São Paulo (SP) | APROVADO |
| EV2 | Chuva Forte Laranja: Alagamento em casas térreas | Belém (PA) | APROVADO |
| EV3 | Vendaval Severo: Impacto em coberturas vulneráveis | Porto Alegre (RS) | APROVADO |
| EV4 | Evento Abaixo do Limiar: Silêncio Inteligente | Brasília (DF) | APROVADO |
| EV5 | Conformidade: Bloqueio de promessa de indenização | São Paulo (SP) | APROVADO |
| EV6 | Segmentação Semântica: Diferenciação Auto vs Residencial | São Paulo (SP) | APROVADO |
| EV7 | Resiliência: Acionamento de fallback em falha de API | Recife (PE) | APROVADO |
| EV8 | Human-in-the-Loop: Respeito ao veto manual do operador | São Paulo (SP) | APROVADO |
| EV-GEO-1 | Validação Regional Norte: Convecção equatorial | Belém (PA) | APROVADO |
| EV-GEO-2 | Validação Regional Nordeste: Chuvas tropicais costeiras | Recife (PE) | APROVADO |
| EV-GEO-3 | Validação Regional Centro-Oeste: Instabilidade de verão | Brasília (DF) | APROVADO |
| EV-GEO-4 | Validação Regional Sudeste: Ilhas de calor e granizo | São Paulo (SP) | APROVADO |
| EV-GEO-5 | Validação Regional Sul: Ciclogênese e vendavais | Porto Alegre (RS) | APROVADO |
| **TOTAL EVALS** | **Cenários Homologados de Ponta a Ponta** | **5 Regiões do Brasil** | **100% PASS** |

### Registro de Execução da Suíte de Evals:
```
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


# 13. LIMITAÇÕES CONHECIDAS DO MVP & ROADMAP FUTURO

Com rigor ético e transparência de engenharia, destacam-se os pontos de fronteira do MVP atual e o planejamento para escala industrial:
1. Base Sintética de Demonstração: O MVP opera com 20 apólices sintéticas para manter a execução didática e veloz. O próximo passo de integração conectará a camada de domínio a bancos relacionais corporativos (PostgreSQL/Oracle) ou plataformas de apólices como Guidewire e SAP for Insurance;
2. Adaptadores de Mensageria em Produção: O envio das mensagens ocorre de forma simulada no módulo `NotificationSimulator`, gerando os logs criptográficos com hash SHA-256. A arquitetura está desacoplada e pronta para receber conectores reais via webhook (Twilio para WhatsApp e SMS, SendGrid para E-mail e Firebase Cloud Messaging para Push Notifications);
3. Resolução Espacial Hiperlocalizada por CEP: Atualmente, a consulta climática utiliza as coordenadas centrais das cidades-piloto. A evolução do produto incorporará geocodificação direta pelo CEP do risco segurado, permitindo identificar áreas inundadas em nível de microbacia e quarteirão.


# 14. INSTRUÇÕES DE EXECUÇÃO & GUIA PRÁTICO

## 14.1 Acesso Online Imediato (Sem Instalação)
A plataforma está hospedada e operacional publicamente no Streamlit Community Cloud:  
Link de Acesso: **[https://meteorisco-fypi76f3ra7umxw8v9hbgt.streamlit.app](https://meteorisco-fypi76f3ra7umxw8v9hbgt.streamlit.app)**

## 14.2 Execução Local no Ambiente de Desenvolvimento
Para executar a solução localmente a partir do código-fonte:

```bash
# 1. Clonar o repositório
git clone https://github.com/edcarloscardoso/meteorisco.git
cd meteorisco

# 2. Criar e ativar o ambiente virtual (Linux / macOS)
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar a suíte de testes unitários
PYTHONPATH=. pytest tests/ -v

# 5. Executar a suíte de Golden Evals de negócio
PYTHONPATH=. python3 evals/eval_runner.py

# 6. Iniciar a interface gráfica (Streamlit)
streamlit run app/streamlit_app.py
```
O painel estará acessível no navegador pelo endereço `http://localhost:8501`.


# 15. ESTRUTURA DO PROJETO

```
meteorisco/
├── app/
│   ├── regioes_ibge.geojson      # Malha territorial oficial das 5 macrorregiões (IBGE)
│   └── streamlit_app.py          # Dashboard executivo com neurodesign e mapa interativo
├── docs/
│   ├── abnt_header.tex           # Configurações tipográficas e normativas ABNT
│   ├── diagramas/                # Diagramas visuais modernos em alta resolução (300 DPI)
│   │   ├── diagrama_agentes.png
│   │   ├── diagrama_arquitetura.png
│   │   ├── diagrama_fluxo.png
│   │   └── diagrama_paradigma.png
│   ├── relatorio_tecnico_meteorisco.md # Relatório técnico espelhado
│   └── Relatorio_Tecnico_Final_desafio_5.pdf # Relatório oficial em PDF
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
├── scripts/
│   └── generate_report_diagrams.py # Gerador automatizado de diagramas em alta resolução
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
├── Relatorio_Tecnico_Final_desafio_5.pdf # Relatório Oficial ABNT em PDF
└── README.md                     # Documentação executiva do repositório
```


# 16. CONCLUSÃO

O MeteoRisco cumpre integralmente os objetivos propostos pelo Desafio 05 do I2A2. A solução demonstra que a Inteligência Artificial aplicada ao setor segurador atinge sua máxima eficácia quando estruturada em arquitetura simbiótica: regras estritamente determinísticas onde a precisão financeira e a conformidade atuarial são inegociáveis, combinadas com agentes de linguagem onde a empatia, a agilidade e a clareza salvam vidas e patrimônios.

Ao aliar robustez de engenharia, prevenção ativa de sinistros, governança com controle humano e uma interface desenhada sob os princípios do neurodesign, a equipe Seguros Connect entrega um produto maduro, validado por 100% de aprovação em testes automatizados e preparado para liderar a transformação digital das seguradoras brasileiras.

*Relatório técnico final elaborado pela equipe Seguros Connect para avaliação oficial da banca do I2A2.*  
*São Paulo, Setembro de 2026.*
