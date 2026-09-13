# 🎓 CoursIA

<p align="center">
  assets/logo.png
</p>

<p align="center">
    <b>Enregistrer • Transcrire • Réviser</b>
</p>

---

## 📖 Présentation

CoursIA est une application de bureau développée en Python et Qt permettant de transformer un cours enregistré en :

- retranscription intégrale ;
- résumé structuré ;
- fiche de révision ;
- support de mémorisation.

L'application utilise :

- Mistral AI
- Voxtral
- PySide6
- Python

afin de fournir une chaîne complète :

```text
Cours
↓
Enregistrement audio
↓
Retranscription IA
↓
Résumé pédagogique
↓
Fiche de révision
```

---

# ✨ Fonctionnalités

## 🎤 Enregistrement audio

- enregistrement direct depuis le microphone ;
- pause et reprise ;
- renommage automatique ;
- classement par matière ;
- import de fichiers audio externes.

Formats supportés :

- WAV
- MP3
- M4A
- FLAC
- OGG
- OPUS

---

## 📝 Retranscription IA

CoursIA utilise :

```text
voxtral-mini-latest
```

pour effectuer les retranscriptions.

Fonctionnalités :

- transcription longue durée ;
- conservation des contenus pédagogiques ;
- génération de fichiers TXT ;
- protection contre l'écrasement des fichiers existants.

---

## 📚 Résumé pédagogique

Production automatique d'un document DOCX structuré comprenant :

1. Objet du cours
2. Plan suivi
3. Synthèse développée
4. Exemples pédagogiques
5. Conclusion

---

## 📋 Fiche de révision

Production d'une fiche de révision comprenant :

- définitions ;
- concepts ;
- mécanismes ;
- auteurs ;
- dates ;
- erreurs fréquentes ;
- questions-réponses ;
- mini quiz ;
- checklist finale.

---

## 🔐 Sécurité

Avant tout écrasement :

- audio ;
- retranscription ;
- document Word ;

l'utilisateur doit confirmer l'opération.

---

## 🖼 Interface graphique

Interface moderne :

- thème sombre ;
- logo intégré ;
- gestionnaire de fichiers ;
- navigation par catégories.

---

# 📂 Arborescence

```text
CoursIA/
├── main.py
├── requirements.txt
├── run.sh
│
├── assets/
│   ├── logo.png
│   ├── logo.svg
│   ├── logo.ico
│   ├── logo_icon.ico
│   └── ...
│
├── Documents/
├── Enregistrements/
├── Metadonnees/
└── Transcriptions/
```

---

# 🤖 Modèles IA

Par défaut :

### Transcription

```text
voxtral-mini-latest
```

### Résumé

```text
mistral-small-latest
```

Ces modèles peuvent être modifiés depuis :

```text
Paramètres → Modèles Mistral
```

---

# 🚀 Installation rapide (CachyOS / Arch Linux)

Télécharger le paquet :

```bash
coursia-0.5-1-x86_64.pkg.tar.zst
```

Installation :

```bash
sudo pacman -U coursia-0.5-1-x86_64.pkg.tar.zst
```

Lancement :

```bash
coursia
```

ou via :

```text
Menu Applications
→ Education
→ CoursIA
```

---

# 🐍 Installation depuis les sources

## Dépendances système

```bash
sudo pacman -S \
    python \
    python-pip \
    portaudio
```

## Clonage

```bash
git clone https://github.com/Dofyx/CoursAI
cd CoursAI
```

## Installation Python

```bash
python -m venv .venv

source .venv/bin/activate

pip install -U pip

pip install -r requirements.txt
```

## Lancement

```bash
python main.py
```

---

# 📦 Création du paquet Arch Linux

Créer :

```text
coursia-pkg/
├── PKGBUILD
├── coursia.desktop
├── coursia.sh
└── source/
```

Copie du projet :

```bash
cp -r CoursAI/* source/
```

Compilation :

```bash
makepkg -f
```

Résultat :

```text
coursia-0.5-1-x86_64.pkg.tar.zst
```

Installation :

```bash
sudo pacman -U coursia-0.5-1-x86_64.pkg.tar.zst
```

---

# 🔧 Construction d'un binaire portable

Avec PyInstaller :

```bash
pip install pyinstaller
```

```bash
pyinstaller \
  --onefile \
  --windowed \
  --name CoursIA \
  --icon assets/logo_icon.ico \
  --add-data "assets:assets" \
  main.py
```

Résultat :

```text
dist/CoursIA
```

---

# 📄 Licence

Projet distribué sous licence :

```text
CC BY-NC-SA 4.0
```

Creative Commons Attribution - Pas d’Utilisation Commerciale - Partage dans les Mêmes Conditions.

---

# 👨‍💻 Auteur

**Dofyx AI Corp**

GitHub :

https://github.com/Dofyx/CoursAI

---

# ⭐ Soutenir le projet

Si CoursIA vous est utile :

- ⭐ laissez une étoile sur GitHub ;
- 🐛 ouvrez une issue pour signaler un bug ;
- 💡 proposez vos améliorations.

---

# ⚠️ Avertissement

L'utilisateur reste responsable de l'utilisation :

- des modèles IA ;
- des contenus générés ;
- du respect des droits d'auteur ;
- du respect de la confidentialité des enregistrements audio.
