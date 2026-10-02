"""Exceptions personnalisées pour l'API Mistral."""


class MistralAPIError(Exception):
    """Erreur générique de l'API Mistral."""
    
    def __init__(self, message: str, status_code: int):
        self.status_code = status_code
        super().__init__(message)


class MistralAuthError(MistralAPIError):
    """Erreur d'authentification (clé API invalide ou expirée)."""
    pass


class MistralQuotaError(MistralAPIError):
    """Quota Mistral épuisé."""
    pass


class NetworkError(Exception):
    """Problème de connexion réseau."""
    pass
