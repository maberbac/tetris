"""
PieceI - Pièce ligne droite du Tetris

PieceI représente la pièce en ligne droite (4 blocs alignés).
- Forme : ████ (horizontal) ou  █ (vertical)
                                █
                                █  
                                █
- 2 orientations possibles
- Rotation alterne entre horizontal et vertical
- Position spawn : centre horizontal du plateau
"""

from typing import List
from ..piece import Piece, TypePiece
from ..position import Position


class PieceI(Piece):
    """
    Pièce I - Ligne droite de 4 blocs.
    
    Caractéristiques :
    - 4 blocs alignés
    - 2 orientations : horizontal ↔ vertical
    - Pivot : centre de la ligne
    """
    
    @property
    def type_piece(self) -> TypePiece:
        """Retourne le type I."""
        return TypePiece.I
    
    @classmethod
    def creer(cls, x_spawn: int, y_spawn: int) -> 'PieceI':
        """
        Factory method pour créer une PieceI.
        
        Args:
            x_spawn: Position X de spawn (centre de la pièce)
            y_spawn: Position Y de spawn
            
        Returns:
            Nouvelle instance PieceI en position horizontale
        """
        instance = cls.__new__(cls)
        positions_initiales = instance.obtenir_positions_initiales(x_spawn, y_spawn)
        
        # Pivot au centre de la ligne (position 1 sur 4)
        position_pivot = positions_initiales[1]
        
        instance.positions = positions_initiales
        instance.position_pivot = position_pivot
        
        return instance
    
    def obtenir_positions_initiales(self, x_spawn: int, y_spawn: int) -> List[Position]:
        """
        Crée les positions initiales pour PieceI (ligne horizontale).
        
        Format : ████ avec x_spawn au centre
        
        Args:
            x_spawn: Position X de spawn (centre)
            y_spawn: Position Y de spawn
            
        Returns:
            4 positions en ligne horizontale
        """
        return [
            Position(x_spawn - 2, y_spawn),  # Gauche
            Position(x_spawn - 1, y_spawn),  # Centre-gauche (pivot)  
            Position(x_spawn, y_spawn),      # Centre-droite
            Position(x_spawn + 1, y_spawn)   # Droite
        ]
    
    def tourner(self) -> None:
        """
        Rotation PieceI : alterne entre horizontal et vertical.
        
        Horizontal → Vertical : Positions autour du pivot
        Vertical → Horizontal : Retour à la position horizontale
        
        Logique :
        - Détecte orientation actuelle
        - Calcule nouvelles positions autour du pivot
        - Met à jour les positions (Entity behavior)
        """
        if self._est_horizontal():
            self._devenir_vertical()
        else:
            self._devenir_horizontal()
    
    def _est_horizontal(self) -> bool:
        """
        Détermine si la pièce est en orientation horizontale.
        
        Returns:
            True si horizontal (même y pour toutes positions)
        """
        y_premier = self.positions[0].y
        return all(pos.y == y_premier for pos in self.positions)
    
    def _devenir_vertical(self) -> None:
        """
        Transforme la pièce en orientation verticale.
        
        Calcule 4 positions en colonne autour du pivot :
        - pivot.y - 1
        - pivot.y     (pivot lui-même)
        - pivot.y + 1
        - pivot.y + 2
        """
        x_pivot = self.position_pivot.x
        y_pivot = self.position_pivot.y
        
        self.positions = [
            Position(x_pivot, y_pivot - 1),  # Haut
            Position(x_pivot, y_pivot),      # Pivot
            Position(x_pivot, y_pivot + 1),  # Bas
            Position(x_pivot, y_pivot + 2)   # Bas +1
        ]
    
    def _devenir_horizontal(self) -> None:
        """
        Transforme la pièce en orientation horizontale.
        
        Calcule 4 positions en ligne autour du pivot :
        - pivot.x - 1
        - pivot.x     (pivot lui-même)  
        - pivot.x + 1
        - pivot.x + 2
        """
        x_pivot = self.position_pivot.x
        y_pivot = self.position_pivot.y
        
        self.positions = [
            Position(x_pivot - 1, y_pivot),  # Gauche
            Position(x_pivot, y_pivot),      # Pivot
            Position(x_pivot + 1, y_pivot),  # Droite
            Position(x_pivot + 2, y_pivot)   # Droite +1
        ]
