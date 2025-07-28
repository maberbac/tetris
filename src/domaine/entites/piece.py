"""
Piece - Classe abstraite pour les pièces du jeu Tetris

Piece définit l'interface commune pour toutes les pièces :
- Déplacement
- Rotation  
- Vérification des limites
- État des positions

Les classes concrètes (PieceI, PieceO, etc.) implémentent les comportements spécifiques.

Architecture : Template Method + Factory Method patterns
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List

from .position import Position


class TypePiece(Enum):
    """
    Types de pièces dans Tetris.
    
    Chaque type a une forme caractéristique :
    - I : Ligne droite (4 blocs)
    - O : Carré (4 blocs)
    - T : Forme T (4 blocs)
    - S : Forme S (4 blocs)
    - Z : Forme Z (4 blocs)
    - J : Forme J (4 blocs)
    - L : Forme L (4 blocs)
    """
    I = "I"
    O = "O"
    T = "T"
    S = "S"
    Z = "Z"
    J = "J"
    L = "L"


@dataclass
class Piece(ABC):
    """
    Classe abstraite représentant une pièce de Tetris.
    
    Attributs:
        positions: Liste des positions occupées par la pièce
        position_pivot: Position utilisée pour les rotations
    
    Règles métier :
    - Entity : Peut changer d'état (déplacement, rotation)
    - Contient 4 positions (sauf cas spéciaux)
    - Position pivot détermine le centre de rotation
    - Chaque type de pièce a ses propres règles de rotation
    """
    positions: List[Position]
    position_pivot: Position
    
    @property
    @abstractmethod
    def type_piece(self) -> TypePiece:
        """Retourne le type de cette pièce."""
        pass
    
    @abstractmethod
    def obtenir_positions_initiales(self, x_spawn: int, y_spawn: int) -> List[Position]:
        """
        Crée les positions initiales pour ce type de pièce.
        
        Args:
            x_spawn: Position X de spawn
            y_spawn: Position Y de spawn
            
        Returns:
            Liste des positions initiales pour cette pièce
        """
        pass
    
    def deplacer(self, delta_x: int, delta_y: int) -> None:
        """
        Déplace la pièce (mutation de l'Entity).
        
        Contrairement aux Value Objects, les Entities mutent leur état.
        
        Args:
            delta_x: Déplacement horizontal
            delta_y: Déplacement vertical
        """
        nouvelles_positions = []
        for position in self.positions:
            nouvelle_position = position.deplacer(delta_x, delta_y)
            nouvelles_positions.append(nouvelle_position)
        
        self.positions = nouvelles_positions
        self.position_pivot = self.position_pivot.deplacer(delta_x, delta_y)
    
    @abstractmethod 
    def tourner(self) -> None:
        """
        Effectue une rotation de la pièce.
        
        Chaque type de pièce implémente sa propre logique :
        - O : Ne fait rien (carré)
        - I : Horizontal ↔ Vertical
        - T, S, Z, J, L : Rotation autour du pivot
        """
        pass
    
    def dans_limites(self, largeur_max: int, hauteur_max: int) -> bool:
        """
        Vérifie si toutes les positions de la pièce sont dans les limites.
        
        Args:
            largeur_max: Largeur maximale (exclusive)
            hauteur_max: Hauteur maximale (exclusive)
            
        Returns:
            True si toute la pièce est dans les limites
        """
        return all(
            position.dans_limites(largeur_max, hauteur_max) 
            for position in self.positions
        )
