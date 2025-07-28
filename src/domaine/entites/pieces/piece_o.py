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
    def creer(cls, x_spawn: int, y_spawn: int) -> 'PieceO':
        """
        Factory method pour créer une PieceO.
        
        Args:
            x_spawn: Position X de spawn (coin gauche du carré)
            y_spawn: Position Y de spawn (ligne du haut)
            
        Returns:
            Nouvelle instance PieceO en carré 2x2
        """
        instance = cls.__new__(cls)
        positions_initiales = instance.obtenir_positions_initiales(x_spawn, y_spawn)
        
        # Pivot = coin supérieur gauche (position 0)
        position_pivot = positions_initiales[0]
        
        instance.positions = positions_initiales
        instance.position_pivot = position_pivot
        
        return instance
    
    def obtenir_positions_initiales(self, x_spawn: int, y_spawn: int) -> List[Position]:
        """
        Crée les positions initiales pour PieceO (carré 2x2).
        
        Format : ██ avec x_spawn, y_spawn = coin supérieur gauche
                ██
        
        Args:
            x_spawn: Position X de spawn (gauche)
            y_spawn: Position Y de spawn (haut)
            
        Returns:
            4 positions en carré 2x2
        """
        return [
            Position(x_spawn, y_spawn),         # Haut-gauche (pivot)
            Position(x_spawn + 1, y_spawn),     # Haut-droite
            Position(x_spawn, y_spawn + 1),     # Bas-gauche
            Position(x_spawn + 1, y_spawn + 1)  # Bas-droite
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
