"""
PieceS - Pièce en forme de S

La PieceS forme un "S" et a 2 orientations possibles :
- Horizontal : Configuration S classique
- Vertical : S tourné à 90°

Forme horizontale initiale :
 ██   ← bloc droit et centre-haut
██    ← bloc gauche et centre-bas (pivot)

Auto-enregistrement : @piece_tetris(TypePiece.S)
"""

from typing import List
from ..position import Position  
from ..piece import Piece, TypePiece
from ..fabriques.registre_pieces import piece_tetris


@piece_tetris(TypePiece.S)
class PieceS(Piece):
    """
    Implémentation de la pièce S avec rotation sur 2 orientations.
    
    Pattern utilisé :
    - Template Method (héritage de Piece)
    - Factory Method (méthode creer)
    - Registry Pattern (auto-enregistrement)
    """
    
    def __init__(self):
        """Constructeur appelé par le factory method."""
        # Sera initialisé par la méthode creer
        pass
    
    @classmethod
    def creer(cls, x_pivot: int, y_pivot: int) -> 'PieceS':
        """
        Factory method pour créer une PieceS.
        
        Args:
            x_pivot: Position X du pivot
            y_pivot: Position Y du pivot
            
        Returns:
            Nouvelle instance de PieceS
        """
        instance = cls.__new__(cls)
        positions_initiales = instance.obtenir_positions_initiales(x_pivot, y_pivot)
        
        # Position pivot : centre-bas de la forme S (position 3 sur 4)
        position_pivot = positions_initiales[3]
        
        instance.positions = positions_initiales
        instance.position_pivot = position_pivot
        instance._est_vertical = False
        
        return instance

    def obtenir_positions_initiales(self, x_pivot: int, y_pivot: int) -> List[Position]:
        """
        Crée les positions initiales pour PieceS (forme S horizontale).
        
        Format S horizontal avec pivot au centre-bas :
         ██   ← positions [pivot.x, pivot.y] (pivot) et [pivot.x+1, pivot.y]
        ██    ← positions [pivot.x-1, pivot.y+1] et [pivot.x, pivot.y+1]
        
        Args:
            x_pivot: Position X du pivot
            y_pivot: Position Y du pivot
            
        Returns:
            4 positions en forme S horizontal
        """
        return [
            Position(x_pivot, y_pivot - 1),          # [pivot.x, pivot.y] (le pivot de la pièce)
            Position(x_pivot + 1, y_pivot - 1),      # [pivot.x+1, pivot.y]
            Position(x_pivot - 1, y_pivot),          # [pivot.x-1, pivot.y+1]  
            Position(x_pivot, y_pivot)               # [pivot.x, pivot.y+1] 
        ]

    @property  
    def type_piece(self) -> TypePiece:
        """Retourne le type de cette pièce."""
        return TypePiece.S

    def tourner(self) -> None:
        """
        Rotation de la pièce S (2 orientations).
        
        Horizontal → Vertical → Horizontal → ...
        """
        if self._est_vertical:
            self._devenir_horizontal()
        else:
            self._devenir_vertical()
        
        self._est_vertical = not self._est_vertical

    def _devenir_vertical(self) -> None:
        """
        Passage en orientation verticale.
        
        Configuration verticale autour du pivot :
        █     ← [pivot.x, pivot.y-1]
        ██    ← [pivot.x, pivot.y] (le pivot de la pièce) et [pivot.x+1, pivot.y]
         █    ← [pivot.x+1, pivot.y+1]
        """
        self.positions = [
            Position(self.position_pivot.x, self.position_pivot.y - 1),      # [pivot.x, pivot.y-1]
            Position(self.position_pivot.x, self.position_pivot.y),          # [pivot.x, pivot.y] (le pivot de la pièce)
            Position(self.position_pivot.x + 1, self.position_pivot.y),      # [pivot.x+1, pivot.y]
            Position(self.position_pivot.x + 1, self.position_pivot.y + 1)   # [pivot.x+1, pivot.y+1]
        ]

    def _devenir_horizontal(self) -> None:
        """
        Passage en orientation horizontale.
        
        Configuration horizontale autour du pivot :
         ██   ← [pivot.x, pivot.y-1] et [pivot.x+1, pivot.y-1]
        ██    ← [pivot.x-1, pivot.y] et [pivot.x, pivot.y] (le pivot de la pièce)
        """
        self.positions = [
            Position(self.position_pivot.x, self.position_pivot.y - 1),      # [pivot.x, pivot.y-1]
            Position(self.position_pivot.x + 1, self.position_pivot.y - 1),  # [pivot.x+1, pivot.y-1]  
            Position(self.position_pivot.x - 1, self.position_pivot.y),      # [pivot.x-1, pivot.y]
            Position(self.position_pivot.x, self.position_pivot.y)           # [pivot.x, pivot.y] (le pivot de la pièce)
        ]
