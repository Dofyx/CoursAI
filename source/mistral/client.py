import requests
import mimetypes
from pathlib import Path
from typing import Optional, Dict, Any

from mistral.exceptions import MistralAPIError, MistralAuthError, MistralQuotaError, NetworkError


class MistralClient:
    """Client pour interagir avec l'API Mistral AI."""
    
    BASE_URL = "https://api.mistral.ai/v1"
    
    def __init__(self, api_key: str):
        """Initialise le client avec une clé API."""
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })

    def transcribe(
        self, 
        audio_path: Path, 
        model: str = "voxtral-mini-latest", 
        language: str = "fr"
    ) -> str:
        """Transcrit un fichier audio en texte."""
        mime = mimetypes.guess_type(audio_path.name)[0] or 'application/octet-stream'
        
        try:
            with open(audio_path, 'rb') as f:
                response = self.session.post(
                    f"{self.BASE_URL}/audio/transcriptions",
                    files={'file': (audio_path.name, f, mime)},
                    data={'model': model, 'language': language},
                    timeout=7200
                )
            self._handle_error(response)
            return response.json()['text']
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Problème de connexion réseau : {str(e)}")

    def chat(
        self, 
        prompt: str, 
        model: str = "mistral-small-latest", 
        temperature: float = 0.2
    ) -> str:
        """Génère du texte avec l'API Mistral Chat."""
        try:
            response = self.session.post(
                f"{self.BASE_URL}/chat/completions",
                json={
                    'model': model,
                    'messages': [{'role': 'user', 'content': prompt}],
                    'temperature': temperature
                },
                timeout=1800
            )
            self._handle_error(response)
            return response.json()['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Problème de connexion réseau : {str(e)}")

    def _handle_error(self, response: requests.Response) -> None:
        """Gère les erreurs de l'API Mistral."""
        if not response.ok:
            if response.status_code == 401:
                raise MistralAuthError(
                    "Clé API Mistral invalide ou expirée.", 
                    response.status_code
                )
            elif response.status_code == 429:
                raise MistralQuotaError(
                    "Quota Mistral épuisé. Veuillez vérifier votre abonnement.",
                    response.status_code
                )
            elif response.status_code >= 500:
                raise MistralAPIError(
                    f"Erreur serveur Mistral ({response.status_code}). Réessayez plus tard.",
                    response.status_code
                )
            else:
                try:
                    detail = response.json().get('message') or \
                           response.json().get('error', {}).get('message') or \
                           response.text
                except Exception:
                    detail = response.text
                raise MistralAPIError(
                    f"Erreur Mistral {response.status_code} : {detail}",
                    response.status_code
                )
