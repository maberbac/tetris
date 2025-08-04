"""
Exception Audio - Exception personnalisée du domaine pour les erreurs audio.

Cette exception suit le pattern établi avec ExceptionCollision et respecte
l'architecture hexagonale en tant qu'exception spécifique au domaine.
CONFORME AUX DIRECTIVES : Exception française du domaine
"""


class ExceptionAudio(Exception):
    """
    Exception levée lors d'erreurs audio dans le jeu Tetris.
    
    Cette exception est utilisée quand :
    - Le système audio ne peut pas s'initialiser
    - Un fichier audio est corrompu ou introuvable
    - La lecture audio échoue pour des raisons techniques
    - Les ressources audio sont insuffisantes (mémoire)
    
    Exemples d'usage :
        >>> raise ExceptionAudio("Système audio non disponible")
        >>> raise ExceptionAudio("Fichier audio corrompu : tetris-theme.wav")
        >>> raise ExceptionAudio("Mémoire insuffisante pour charger l'audio")
    """
    
    def __init__(self, message: str = "Erreur audio"):
        """
        Initialise l'exception avec un message descriptif.
        
        Args:
            message: Description de l'erreur audio (par défaut: "Erreur audio")
        """
        super().__init__(message)
        self.message = message
    
    def __str__(self) -> str:
        """Retourne le message d'erreur."""
        return self.message
