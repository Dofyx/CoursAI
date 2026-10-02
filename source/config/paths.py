from pathlib import Path

# Chemins de base pour l'application
APP = 'CoursIA'
BASE = Path.home() / 'Documents' / 'CoursIA'
REC = BASE / 'Enregistrements'
TR = BASE / 'Transcriptions'
DOC = BASE / 'Documents'
META = BASE / 'Metadonnees'
CFG = BASE / 'config.json'

# Créer les dossiers s'ils n'existent pas
for p in (REC, TR, DOC, META):
    p.mkdir(parents=True, exist_ok=True)
