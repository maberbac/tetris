"""
Module contenant l'exception spécifique aux collisions.
CONFORME AUX DIRECTIVES : Exception française du domaine
"""

class ExceptionCollision(Exception):
    """
    Exception levée lors de collisions dans le jeu Tetris.
    
    Cette exception est utilisée quand :
    - Une pièce ne peut pas être placée à cause d'une collision
    - Une opération de déplacement/rotation est impossible
    - Une situation de collision inattendue se produit
    
    Exemples d'usage :
        >>> raise ExceptionCollision("Collision détectée lors du placement")
        >>> raise ExceptionCollision("Impossible de déplacer la pièce - collision avec le bord")
    """
    
    def __init__(self, message: str = "Collision détectée"):
        """
        Initialise l'exception avec un message descriptif.
        
        Args:
            message: Description de la collision (par défaut: "Collision détectée")
        """
        super().__init__(message)
        self.message = message
    
    def __str__(self) -> str:
        """Retourne le message d'erreur."""
        return self.message
