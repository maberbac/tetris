"""
Position - Value Object pour les coordonnées

Position représente une coordonnée (x, y) dans le jeu Tetris.
C'est un Value Object : immutable, égalité par valeur, pas d'identité.

Exemple d'usage :
    position = Position(5, 10)
    nouvelle_position = position.deplacer(1, -2)  # Position(6, 8)
"""

from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True)  # frozen=True rend la classe immutable
class Position:
    """
    Value Object représentant une position (x, y) dans le jeu.
    
    Attributs:
        x: Coordonnée horizontale (colonne)
        y: Coordonnée verticale (ligne)
    
    Règles métier :
    - Immutable : Une fois créée, une position ne peut pas changer
    - Égalité par valeur : Deux positions avec mêmes x,y sont égales
    - Pas d'identité : Pas d'ID unique, juste des valeurs
    """
    x: int
    y: int
    
    def deplacer(self, delta_x: int, delta_y: int) -> Self:
        """
        Crée une nouvelle position déplacée.
        
        Args:
            delta_x: Déplacement horizontal
            delta_y: Déplacement vertical
            
        Returns:
            Nouvelle instance Position avec les nouvelles coordonnées
            
        Exemple:
            >>> pos = Position(5, 5)
            >>> nouvelle_pos = pos.deplacer(2, -1)
            >>> print(nouvelle_pos)  # Position(x=7, y=4)
        """
        return Position(self.x + delta_x, self.y + delta_y)
    
    def dans_limites(self, largeur_max: int, hauteur_max: int) -> bool:
        """
        Vérifie si cette position est dans les limites données.
        
        Args:
            largeur_max: Largeur maximale (exclusive)
            hauteur_max: Hauteur maximale (exclusive)
            
        Returns:
            True si la position est dans les limites, False sinon
            
        Exemple:
            >>> pos = Position(5, 8)
            >>> pos.dans_limites(10, 20)  # True
            >>> pos.dans_limites(4, 20)   # False (x >= largeur_max)
        """
        return 0 <= self.x < largeur_max and 0 <= self.y < hauteur_max
