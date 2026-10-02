#!/usr/bin/env python3
"""
Lanceur multiplateforme pour CoursIA.
Crée automatiquement un environnement virtuel Python et installe les dépendances.
"""

import os
import sys
import subprocess
from pathlib import Path


def get_venv_path() -> Path:
    """Retourne le chemin du venv en fonction de l'OS."""
    if sys.platform == "win32":
        # Windows: %LOCALAPPDATA%\coursia\.venv
        local_app_data = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return local_app_data / "coursia" / ".venv"
    else:
        # Linux/macOS: ~/.local/share/coursia/.venv
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


def create_venv(venv_path: Path) -> None:
    """Crée un environnement virtuel Python."""
    print(f"Création de l'environnement virtuel dans {venv_path}...")
    subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)


def install_dependencies(venv_path: Path, requirements_path: Path) -> None:
    """Installe les dépendances Python dans le venv."""
    pip_path = get_pip_path(venv_path)
    print(f"Installation des dépendances avec {pip_path}...")
    
    # Mise à jour de pip
    subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
    
    # Installation des dépendances
    subprocess.run([str(pip_path), "install", "-r", str(requirements_path)], check=True)


def main():
    """Point d'entrée principal."""
    # Chemins
    app_dir = Path(__file__).parent.resolve()
    source_dir = app_dir / "source"
    requirements_path = source_dir / "requirements.txt"
    main_py_path = source_dir / "main.py"
    
    # Vérifier que les fichiers existent
    if not requirements_path.exists():
        print(f"ERREUR: Fichier introuvable: {requirements_path}")
        sys.exit(1)
    if not main_py_path.exists():
        print(f"ERREUR: Fichier introuvable: {main_py_path}")
        sys.exit(1)
    
    # Chemin du venv
    venv_path = get_venv_path()
    python_path = get_python_path(venv_path)
    
    # Créer le venv s'il n'existe pas
    if not venv_path.exists():
        create_venv(venv_path)
        install_dependencies(venv_path, requirements_path)
    
    # Changer de répertoire
    os.chdir(source_dir)
    
    # Lancer l'application
    print("Lancement de CoursIA...")
    subprocess.run([str(python_path), str(main_py_path)])


if __name__ == "__main__":
    main()
