import json
from pathlib import Path
from datetime import datetime
from .helpers import clean, stem

META = None  # Will be set in paths.py


def meta_path(stem_name: str) -> Path:
    """Retourne le chemin du fichier de métadonnées pour un cours."""
    global META
    if META is None:
        from config.paths import META as META_PATH
        META = META_PATH
    return META / (stem_name + '.json')


def write_meta(stem_name: str, subject: str, title: str, source: str) -> None:
    """Écrit les métadonnées d'un cours dans un fichier JSON."""
    meta_path(stem_name).write_text(
        json.dumps({
            'matiere': subject,
            'titre': title,
            'date_heure': datetime.now().isoformat(timespec='minutes'),
            'source': source
        }, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )


def read_meta(stem_name: str) -> dict:
    """Lit les métadonnées d'un cours depuis un fichier JSON."""
    try:
        return json.loads(meta_path(stem_name).read_text(encoding='utf-8'))
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            'matiere': 'Non renseignée',
            'titre': stem_name,
            'date_heure': 'Non renseignée',
            'source': 'inconnu'
        }
