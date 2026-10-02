#!/usr/bin/env python3
"""
Lanceur pour CoursIA (version source).
Crée automatiquement un environnement virtuel Python et installe les dépendances.
"""

import os
import sys
import subprocess
from pathlib import Path


def get_venv_path() -> Path:
    """Retourne le chemin du venv en fonction de l'OS."""
    if sys.platform == "win32":
        local_app_data = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return local_app_data / "coursia" / ".venv"
    else:
        return Path.home() / ".local" / "share" / "coursia" / ".venv"


def get_python_path(venv_path: Path) -> Path:
    """Retourne le chemin de l'exécutable Python dans le venv."""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"


def get_pip_path(venv_path: Path) -> Path:
    """Retourne le chemin de l'exécutable pip dans le venv."""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "pip"
    else:
        return venv_path / "bin" / "pip"


def main():
    """Point d'entrée principal."""
    app_dir = Path(__file__).parent.resolve()
    requirements_path = app_dir / "requirements.txt"
    main_py_path = app_dir / "main.py"
    
    if not requirements_path.exists():
        print(f"ERREUR: Fichier introuvable: {requirements_path}")
        sys.exit(1)
    if not main_py_path.exists():
        print(f"ERREUR: Fichier introuvable: {main_py_path}")
        sys.exit(1)
    
    venv_path = get_venv_path()
    python_path = get_python_path(venv_path)
    
    if not venv_path.exists():
        print(f"Création de l'environnement virtuel dans {venv_path}...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        
        pip_path = get_pip_path(venv_path)
        print(f"Installation des dépendances avec {pip_path}...")
        subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
        subprocess.run([str(pip_path), "install", "-r", str(requirements_path)], check=True)
    
    os.chdir(app_dir)
    print("Lancement de CoursIA...")
    subprocess.run([str(python_path), str(main_py_path)])


if __name__ == "__main__":
    main()
