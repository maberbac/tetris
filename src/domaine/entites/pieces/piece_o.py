"""
PieceO - Pièce carré du Tetris

PieceO représente la pièce en forme de carré (4 blocs en 2x2).
- Forme : ██ (carré 2x2)
         ██
- 1 seule orientation (carré reste carré)
- Rotation = no-op (ne fait rien)
- Position spawn : centre horizontal du plateau
"""

from typing import List
from ..piece import Piece, TypePiece
from ..position import Position
from ..fabriques.registre_pieces import piece_tetris


@piece_tetris(TypePiece.O)
class PieceO(Piece):
    """
    Pièce O - Carré de 4 blocs.
    
    Caractéristiques :
    - 4 blocs en carré 2x2
    - 1 seule orientation (rotation inutile)
    - Pivot : coin supérieur gauche du carré
    - Démontre polymorphisme avec rotation no-op
    """
    
    @property
    def type_piece(self) -> TypePiece:
        """Retourne le type O."""
        return TypePiece.O
    
    @classmethod
    def creer(cls, x_pivot: int, y_pivot: int) -> 'PieceO':
        """
        Factory method pour créer une PieceO.
        
        Args:
            x_pivot: Position X du pivot
            y_pivot: Position Y du pivot
            
        Returns:
            Nouvelle instance PieceO en carré 2x2
        """
        instance = cls.__new__(cls)
        positions_initiales = instance.obtenir_positions_initiales(x_pivot, y_pivot)
        
        # Pivot = coin supérieur gauche (position 0)
        position_pivot = positions_initiales[0]
        
        instance.positions = positions_initiales
        instance.position_pivot = position_pivot
        
        return instance
    
    def obtenir_positions_initiales(self, x_pivot: int, y_pivot: int) -> List[Position]:
        """
        Crée les positions initiales pour PieceO (carré 2x2).
        
        Format : ██ avec pivot = coin supérieur gauche
                ██
        
        Args:
            x_pivot: Position X du pivot
            y_pivot: Position Y du pivot
            
        Returns:
            4 positions en carré 2x2
        """
        return [
            Position(x_pivot, y_pivot - 1),         # [pivot.x, pivot.y] (le pivot de la pièce)
            Position(x_pivot + 1, y_pivot - 1),     # [pivot.x+1, pivot.y]
            Position(x_pivot, y_pivot),     # [pivot.x, pivot.y+1]
            Position(x_pivot + 1, y_pivot)  # [pivot.x+1, pivot.y+1]
        ]
    
    def tourner(self) -> None:
        """
        Rotation PieceO : ne fait rien (carré reste carré).
        
        Démontre polymorphisme : même interface que PieceI.tourner()
        mais comportement différent.
        
        Un carré est identique après rotation → no-op optimisé.
        """
        # Carré reste carré ! Pas besoin de recalculer les positions
        pass
