"""
MeteoRisco — Skill: load_domain

Utilitários para carregar e parsear os arquivos de domínio:
  - locations.yaml
  - risk_matrix.yaml
  - playbook.yaml
  - portfolio.csv

Determinístico. Sem LLM. Testável unitariamente.
"""
import csv
import logging
from pathlib import Path
from typing import Any

import yaml

from src.config import settings

logger = logging.getLogger(__name__)


def _load_yaml(path: Path) -> dict:
    """Carrega um arquivo YAML e retorna como dict. Raises FileNotFoundError se ausente."""
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de domínio não encontrado: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_locations() -> list[dict]:
    """
    Carrega as localidades-piloto do domain/locations.yaml.
    Retorna lista de dicts com campos: id, city, state, region, latitude, longitude, timezone.
    """
    data = _load_yaml(settings.domain_dir / "locations.yaml")
    locations = data.get("locations", [])
    logger.debug(f"Localidades carregadas: {[loc['id'] for loc in locations]}")
    return locations


def get_location_by_id(location_id: str) -> dict:
    """Retorna dados de uma localidade pelo ID. Raises ValueError se não encontrada."""
    locations = load_locations()
    for loc in locations:
        if loc["id"] == location_id:
            return loc
    valid_ids = [loc["id"] for loc in locations]
    raise ValueError(
        f"Localidade '{location_id}' não encontrada. "
        f"IDs válidos: {valid_ids}"
    )


def load_risk_matrix() -> dict:
    """
    Carrega a matriz de risco do domain/risk_matrix.yaml.
    Retorna o dict completo com 'rules', 'cooldown' e metadados.
    """
    data = _load_yaml(settings.domain_dir / "risk_matrix.yaml")
    rules = data.get("rules", [])
    logger.debug(f"Regras da risk_matrix carregadas: {len(rules)} regras")
    return data


def load_playbook() -> dict:
    """
    Carrega o playbook de comunicação do domain/playbook.yaml.
    Retorna o dict completo com tone, prohibitions, guidance_keys, etc.
    """
    data = _load_yaml(settings.domain_dir / "playbook.yaml")
    logger.debug("Playbook carregado")
    return data


def load_portfolio() -> list[dict]:
    """
    Carrega a carteira sintética do domain/portfolio.csv.
    Retorna lista de dicts com os atributos de cada segurado.
    """
    path = settings.domain_dir / "portfolio.csv"
    if not path.exists():
        raise FileNotFoundError(f"Carteira não encontrada: {path}")

    portfolio = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Normalizar booleans
            row["is_high_risk"] = row.get("is_high_risk", "").lower() == "true"
            row["is_vip"] = row.get("is_vip", "").lower() == "true"
            portfolio.append(dict(row))

    logger.debug(f"Carteira carregada: {len(portfolio)} segurados")
    return portfolio


def get_insureds_by_location(location_id: str) -> list[dict]:
    """Filtra segurados de uma localidade específica."""
    portfolio = load_portfolio()
    return [ins for ins in portfolio if ins["location_id"] == location_id]
