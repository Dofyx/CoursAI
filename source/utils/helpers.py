import os
import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime


def open_file(path: Path) -> None:
    """Ouvre un fichier avec l'application par défaut (cross-platform)."""
    path = Path(path).absolute()
    if sys.platform == "win32":
        os.startfile(str(path))
    else:
        subprocess.Popen(["xdg-open", str(path)])


def clean(s: str) -> str:
    """Nettoie une chaîne de caractères pour être utilisée comme nom de fichier."""
    return re.sub(r'[\\/:*?"<>|]+', '_', s.strip()).strip(' .') or 'Sans titre'


def stem(subject: str, title: str, dt: datetime = None) -> str:
    """Génère un nom de fichier basé sur la matière, le titre et la date."""
    return f'{clean(subject)} - {clean(title)} - {(dt or datetime.now()).strftime("%Y-%m-%d_%H-%M")}'
