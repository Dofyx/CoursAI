from pathlib import Path
from typing import Dict, Any

# Dossier des prompts
PROMPTS_DIR = Path(__file__).parent / 'prompts'


def load_prompt(kind: str, language: str = 'fr') -> str:
    """Charge un prompt depuis un fichier."""
    prompt_file = PROMPTS_DIR / f"{kind}.{language}.md"
    if not prompt_file.exists():
        # Retourner un prompt par défaut si le fichier n'existe pas
        return _get_default_prompt(kind, language)
    return prompt_file.read_text(encoding='utf-8')


def render_prompt(prompt: str, **kwargs) -> str:
    """Remplace les placeholders dans le prompt."""
    return prompt.format(**kwargs)


def _get_default_prompt(kind: str, language: str = 'fr') -> str:
    """Retourne un prompt par défaut."""
    prompts = {
        'resume': {
            'fr': """Matière : {matiere}
Titre : {titre}
Date : {date_heure}

Produis un résumé universitaire rédigé et cohérent. Structure imposée :
1. Objet et problématique
2. Plan suivi
3. Synthèse développée des idées et raisonnements
4. Exemples pédagogiques utiles
5. Conclusion et points essentiels

Rédige en paragraphes complets, conserve les nuances et n'invente rien. N'ajoute ni quiz ni cartes mémoire.

TRANSCRIPTION :
{text}""",
            'en': """Subject: {matiere}
Title: {titre}
Date: {date_heure}

Produce a well-written and coherent academic summary. Required structure:
1. Object and problem statement
2. Followed plan
3. Developed synthesis of ideas and reasoning
4. Useful pedagogical examples
5. Conclusion and key points

Write in complete paragraphs, preserve nuances and do not invent anything. Do not add quizzes or flashcards.

TRANSCRIPTION:
{text}"""
        },
        'fiche': {
            'fr': """Matière : {matiere}
Titre : {titre}
Date : {date_heure}

Crée une fiche de révision opérationnelle, concise et mémorisable, non narrative. Structure imposée :
1. Objectifs à maîtriser
2. Définitions essentielles
3. Concepts et mécanismes en listes
4. Repères, auteurs, dates ou formules présents
5. Exemples à retenir
6. Erreurs à éviter
7. Questions-réponses
8. Mini-quiz corrigé
9. Checklist « Je sais… »

N'invente rien.

TRANSCRIPTION :
{text}""",
            'en': """Subject: {matiere}
Title: {titre}
Date: {date_heure}

Create an operational, concise and memorable revision sheet, not narrative. Required structure:
1. Objectives to master
2. Essential definitions
3. Concepts and mechanisms in lists
4. Landmarks, authors, dates or formulas present
5. Examples to remember
6. Errors to avoid
7. Questions and answers
8. Mini-quiz with corrections
9. Checklist "I know..."

Do not invent anything.

TRANSCRIPTION:
{text}"""
        }
    }
    
    if kind in prompts and language in prompts[kind]:
        return prompts[kind][language]
    elif kind in prompts:
        return prompts[kind]['fr']  # Fallback to French
    else:
        return "{text}"  # Fallback minimal
