import json
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import keyring
except ImportError:
    keyring = None

from .paths import CFG, APP

# Configuration par défaut
DEFAULT_CONFIG = {
    'subjects': ['Droit', 'Économie', 'Histoire', 'Informatique', 'Mathématiques'],
    'mistral_transcription_model': 'voxtral-mini-latest',
    'mistral_text_model': 'mistral-small-latest'
}


def load_config() -> Dict[str, Any]:
    """Charge la configuration depuis config.json."""
    try:
        return {**DEFAULT_CONFIG, **json.loads(CFG.read_text(encoding='utf-8'))}
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]) -> None:
    """Sauvegarde la configuration dans config.json."""
    CFG.write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )


def get_secret(name: str, config: Dict[str, Any]) -> str:
    """Récupère un secret depuis keyring ou config."""
    if keyring:
        try:
            return keyring.get_password(APP, name) or ''
        except Exception:
            pass
    return config.get(name, '')


def set_secret(name: str, value: str, config: Dict[str, Any]) -> None:
    """Stocke un secret dans keyring ou config."""
    if keyring:
        try:
            keyring.set_password(APP, name, value)
            config.pop(name, None)
            return
        except Exception:
            pass
    if value:
        config[name] = value
    else:
        config.pop(name, None)
