"""
PieceT - Pièce en forme de T.

La PieceT a 4 orientations possibles :
- Nord : T inversé (branche vers le bas)
- Est : T vers la droite (branche vers la gauche)  
- Sud : T normal (branche vers le haut)
- Ouest : T vers la gauche (branche vers la droite)
"""

from typing import List
from ..piece import Piece, TypePiece
from ..position import Position
from ..fabriques.registre_pieces import piece_tetris


@piece_tetris(TypePiece.T)
class PieceT(Piece):
    """Pièce en T avec 4 orientations possibles."""
    
    def __init__(self):
        """Constructeur privé - utiliser PieceT.creer() à la place."""
        self._orientation = 0  # 0=Nord, 1=Est, 2=Sud, 3=Ouest
    
    @property
    def type_piece(self) -> TypePiece:
        """Retourner le type de cette pièce."""
        return TypePiece.T
    
    @classmethod
    def creer(cls, x_spawn: int, y_spawn: int) -> 'PieceT':
        """
        Factory method pour créer une PieceT.
        
        Args:
            x_spawn: Position X de spawn (centre de la pièce)
            y_spawn: Position Y de spawn
            
        Returns:
            Nouvelle instance PieceT en orientation Nord
        """
        instance = cls.__new__(cls)
        instance._orientation = 0
        positions_initiales = instance.obtenir_positions_initiales(x_spawn, y_spawn)
        
        # Pivot au centre de la pièce (position 1 sur 4)
        position_pivot = positions_initiales[1]
        
        instance.positions = positions_initiales
        instance.position_pivot = position_pivot
        
        return instance
    
    def obtenir_positions_initiales(self, x_spawn: int, y_spawn: int) -> List[Position]:
        """Obtenir les positions initiales pour l'orientation Nord."""
        return self._obtenir_positions_pour_orientation(0, x_spawn, y_spawn)
    
    
    def tourner(self) -> None:
        """Tourner la pièce dans le sens horaire."""
        self._orientation = (self._orientation + 1) % 4
        nouvelles_positions = self._obtenir_positions_pour_orientation(
            self._orientation, 
            self.position_pivot.x, 
            self.position_pivot.y
        )
        self.positions = nouvelles_positions
    
    def _obtenir_positions_pour_orientation(self, orientation: int, x_centre: int, y_centre: int) -> List[Position]:
        """Obtenir les positions pour une orientation donnée.
        
        Args:
            orientation: 0=Nord, 1=Est, 2=Sud, 3=Ouest
            x_centre: Position X du centre
            y_centre: Position Y du centre
            
        Returns:
            Liste des positions absolues pour cette orientation
        """
        if orientation == 0:  # Nord - T inversé (branche vers le bas)
            return [
                Position(x_centre - 1, y_centre),  # Gauche du centre
                Position(x_centre, y_centre),      # Centre
                Position(x_centre + 1, y_centre),  # Droite du centre
                Position(x_centre, y_centre + 1)   # En bas du centre
            ]
        elif orientation == 1:  # Est - T vers la droite (branche vers la gauche)
            return [
                Position(x_centre, y_centre - 1),  # En haut du centre
                Position(x_centre, y_centre),      # Centre
                Position(x_centre, y_centre + 1),  # En bas du centre
                Position(x_centre - 1, y_centre)   # À gauche du centre
            ]
        elif orientation == 2:  # Sud - T normal (branche vers le haut)
            return [
                Position(x_centre - 1, y_centre),  # Gauche du centre
                Position(x_centre, y_centre),      # Centre
                Position(x_centre + 1, y_centre),  # Droite du centre
                Position(x_centre, y_centre - 1)   # En haut du centre
            ]
        else:  # orientation == 3, Ouest - T vers la gauche (branche vers la droite)
            return [
                Position(x_centre, y_centre - 1),  # En haut du centre
                Position(x_centre, y_centre),      # Centre
                Position(x_centre, y_centre + 1),  # En bas du centre
                Position(x_centre + 1, y_centre)   # À droite du centre
            ]
