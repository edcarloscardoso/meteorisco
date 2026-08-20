"""
MeteoRisco — Skill: draft_message

Interface plugável para geração de mensagens preventivas personalizadas via LLM.
Suporta integração nativa com Gemini (Google GenAI API) e OpenAI via HTTP/SDK,
com fallback transparente para o gerador de templates offline.

ARQUITETURA:
- O provider LLM é configurado via settings.llm_provider e settings.llm_api_key (.env).
- Se a chamada ao LLM falhar ou a chave for ausente -> usa _draft_with_template com is_fallback=True.
- Separação estrita: a LLM gera LINGUAGEM e COMUNICAÇÃO; não decide elegibilidade.
"""
import logging
import json
from datetime import datetime, timezone

import httpx

from src.contracts.audience import AudienceItem
from src.contracts.risk import RiskAssessment
from src.contracts.message import MessageDraft, ModelMeta
from src.skills.load_domain import load_playbook
from src.config import settings

logger = logging.getLogger(__name__)

_SEVERITY_LABELS = {
    "yellow": "atenção",
    "orange": "alerta preventivo",
    "red": "ALERTA URGENTE",
}

_HAZARD_LABELS = {
    "rain_heavy": "chuva intensa",
    "hail": "possibilidade de granizo (previsão modelada)",
    "wind_strong": "ventos fortes",
    "storm": "tempestade severa",
}


def draft_message(
    audience_item: AudienceItem,
    risk: RiskAssessment,
) -> MessageDraft:
    """
    Gera uma mensagem preventiva personalizada para um segurado elegível.

    Fluxo:
    1. Tenta gerar via LLM se configurado (Gemini / OpenAI).
    2. Em caso de falha ou ausência de chave -> usa _draft_with_template (stub offline).
    """
    playbook = load_playbook()

    if settings.has_llm:
        try:
            return _draft_with_llm(audience_item, risk, playbook)
        except Exception as exc:
            logger.warning(
                f"[draft_message] Falha ao chamar LLM ({settings.llm_provider}): {exc}. "
                f"Utilizando fallback por template offline."
            )
            return _draft_with_template(audience_item, risk, playbook, is_fallback_reason=str(exc))
    else:
        logger.debug("[draft_message] LLM não configurado. Utilizando template offline.")
        return _draft_with_template(audience_item, risk, playbook)


def _draft_with_llm(
    item: AudienceItem,
    risk: RiskAssessment,
    playbook: dict,
) -> MessageDraft:
    """
    Gera mensagem via LLM configurado (Gemini ou OpenAI API).
    """
    provider = (settings.llm_provider or "").lower()
    api_key = settings.llm_api_key

    hazard_label = _HAZARD_LABELS.get(risk.hazard_type.value, risk.hazard_type.value)
    severity_label = _SEVERITY_LABELS.get(risk.severity.value if risk.severity else "yellow", "atenção")
    actions_list = _build_actions(item.line_of_business, item.exposure_profile, risk, playbook)

    # Construção do Prompt do Sistema e Usuário
    system_prompt = f"""Você é o Redator Preventivo do sistema MeteoRisco.
Sua missão é gerar uma mensagem de comunicação preventiva em Português para um segurado.

DIRETRIZES DO PLAYBOOK DA SEGURADORA:
- Tom de Voz: {playbook.get('tone', {}).get(risk.severity.value if risk.severity else 'yellow', {}).get('description', '')}
- Canal de Envio: {item.channel.upper()}
- Ramo do Seguro: {item.line_of_business.upper()}
- Nome do Segurado: {item.insured_name}
- Localidade: {item.location_id}
- Ameaça Climática: {hazard_label} (Severidade: {severity_label.upper()})

REGRAS DE CONTEÚDO OBRIGATÓRIAS:
1. Respeite a estrutura: Contexto da previsão -> Risco para o bem segurado -> Ações recomendadas -> Fechamento cordial.
2. IMPORTANTE PARA GRANIZO: Mencione granizo SEMPRE como "previsão de granizo" ou "possibilidade prevista por modelos meteorológicos". Nunca afirme com certeza absoluta que vai granizar.
3. PROIBIÇÃO ABSOLUTA: NUNCA garanta indenização, NUNCA use frases como "garantimos sua indenização" ou "sua apólice cobre". NUNCA seja alarmista.
4. Inclua de 2 a 4 destas ações práticas recomendadas: {json.dumps(actions_list, ensure_ascii=False)}

FORMATO DA RESPOSTA (Retorne estritamente um JSON válido):
{{
  "subject": "Assunto da mensagem (somente se e-mail, senão null)",
  "body": "Texto completo do corpo da mensagem",
  "actions": ["ação 1", "ação 2"]
}}
"""

    user_prompt = f"Gere a mensagem preventiva para {item.insured_name} (Perfil: {item.exposure_profile})."

    if provider == "gemini":
        result_json = _call_gemini_api(api_key, settings.llm_model or "gemini-2.0-flash", system_prompt, user_prompt)
    elif provider == "openai":
        result_json = _call_openai_api(api_key, settings.llm_model or "gpt-4o-mini", system_prompt, user_prompt)
    else:
        raise ValueError(f"Provider LLM desconhecido: {provider}")

    return MessageDraft(
        insured_id=item.insured_id,
        insured_name=item.insured_name,
        channel=item.channel,
        severity=risk.severity.value if risk.severity else "yellow",
        line_of_business=item.line_of_business,
        subject=result_json.get("subject"),
        body=result_json.get("body", ""),
        actions=result_json.get("actions", actions_list),
        model_meta=ModelMeta(
            provider=provider,
            model=settings.llm_model or ("gemini-2.0-flash" if provider == "gemini" else "gpt-4o-mini"),
            is_fallback=False,
        ),
        playbook_version=playbook.get("version", "1.0"),
    )


def _call_gemini_api(api_key: str, model_name: str, system_prompt: str, user_prompt: str) -> dict:
    """Chamada HTTP direta à API do Google Gemini (REST Endpoint)."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"{system_prompt}\n\n{user_prompt}"}]
            }
        ],
        "generationConfig": {
            "response_mime_type": "application/json",
            "temperature": 0.2
        }
    }

    with httpx.Client(timeout=15.0) as client:
        resp = client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()

    candidates = data.get("candidates", [])
    if not candidates:
        raise ValueError("Resposta da API Gemini vazia")

    text_resp = candidates[0]["content"]["parts"][0]["text"]
    return json.loads(text_resp)


def _call_openai_api(api_key: str, model_name: str, system_prompt: str, user_prompt: str) -> dict:
    """Chamada HTTP à API da OpenAI."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2
    }

    with httpx.Client(timeout=15.0) as client:
        resp = client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()

    text_resp = data["choices"][0]["message"]["content"]
    return json.loads(text_resp)


def _draft_with_template(
    item: AudienceItem,
    risk: RiskAssessment,
    playbook: dict,
    is_fallback_reason: str | None = None,
) -> MessageDraft:
    """
    Gera mensagem via template offline (fallback determinístico sem LLM).
    """
    hazard_label = _HAZARD_LABELS.get(risk.hazard_type.value, risk.hazard_type.value)
    severity_label = _SEVERITY_LABELS.get(
        risk.severity.value if risk.severity else "yellow", "atenção"
    )
    lob = item.line_of_business
    exposure = item.exposure_profile

    actions = _build_actions(lob, exposure, risk, playbook)

    if item.channel == "sms":
        body = (
            f"MeteoRisco | {severity_label.upper()} | "
            f"{hazard_label} prevista para {item.location_id.replace('_', ' ').title()}. "
            f"Ações: {'; '.join(actions[:2])}. "
            f"Fique atento."
        )
        subject = None
    else:
        lob_label = "residencial" if lob == "residential" else "automóvel"
        body = (
            f"Olá, {item.insured_name}!\n\n"
            f"Identificamos uma previsão de {hazard_label} para a sua região "
            f"({item.location_id.replace('_', ' ').title()}) nas próximas horas. "
            f"Esta é uma comunicação preventiva referente ao seu seguro {lob_label}.\n\n"
            f"O nível de {severity_label} foi identificado com base em dados meteorológicos "
            f"de modelos numéricos de previsão de tempo.\n\n"
            f"Recomendações:\n"
            + "\n".join(f"• {a}" for a in actions)
            + "\n\n"
            f"Estamos à disposição. Em caso de emergências graves, entre em contato com os órgãos locais.\n\n"
            f"MeteoRisco — Sistema de Prevenção de Sinistros"
        )
        subject = (
            f"[MeteoRisco] {severity_label.upper()} — "
            f"{hazard_label.capitalize()} prevista para sua região"
        )

    return MessageDraft(
        insured_id=item.insured_id,
        insured_name=item.insured_name,
        channel=item.channel,
        severity=risk.severity.value if risk.severity else "yellow",
        line_of_business=lob,
        subject=subject,
        body=body,
        actions=actions,
        model_meta=ModelMeta(
            provider="template",
            model="offline-template-v1",
            is_fallback=True,
        ),
        playbook_version=playbook.get("version", "1.0"),
    )


def _build_actions(lob: str, exposure: str, risk: RiskAssessment, playbook: dict) -> list[str]:
    """
    Constrói lista de ações práticas utilizando o mapeamento de guidance_keys do playbook.yaml.
    """
    guidance = playbook.get("guidance_keys", {})

    action_keys_map = {
        ("rain_heavy", "residential", "imovel_terreo"): [
            "recolher_bens_de_valor", "verificar_calhas", "verificar_sistema_de_drenagem"
        ],
        ("rain_heavy", "residential", "area_sujeita_alagamento"): [
            "recolher_bens_de_valor", "identificar_rota_de_evacuacao", "acao_imediata_recolher_bens"
        ],
        ("rain_heavy", "auto", "veiculo_na_rua"): [
            "buscar_abrigo_coberto", "evitar_cruzar_vias_alagadas", "mover_veiculo_imediatamente"
        ],
        ("hail", "auto", "veiculo_na_rua"): [
            "buscar_abrigo_coberto_imediato", "nao_estacionar_sob_arvores", "acao_imediata_abrigo_coberto"
        ],
        ("hail", "residential", "casa_com_telhado"): [
            "recolher_objetos_externos", "verificar_telhado_apos_evento"
        ],
        ("wind_strong", "residential", "casa_com_telhado"): [
            "recolher_objetos_externos", "verificar_fixacao_de_estruturas", "nao_sair_durante_rajadas"
        ],
        ("wind_strong", "residential", "objetos_externos"): [
            "recolher_objetos_externos", "nao_sair_durante_rajadas"
        ],
    }

    key = (risk.hazard_type.value, lob, exposure)
    keys = action_keys_map.get(key, ["recolher_objetos_externos", "contato_previo_com_prestadores"])

    actions = [guidance.get(k, k.replace("_", " ").capitalize()) for k in keys]
    return actions
