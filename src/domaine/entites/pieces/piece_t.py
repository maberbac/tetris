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
    def creer(cls, x_pivot: int, y_pivot: int) -> 'PieceT':
        """
        Factory method pour créer une PieceT.
        
        Args:
            x_pivot: Position X du pivot
            y_pivot: Position Y du pivot
            
        Returns:
            Nouvelle instance PieceT en orientation Nord
        """
        instance = cls.__new__(cls)
        instance._orientation = 0
        # Sauvegarder les coordonnées absolues du pivot pour éviter la dérive
        instance._x_pivot_absolu = x_pivot
        instance._y_pivot_absolu = y_pivot - 1  # Le pivot réel est à y_pivot - 1 dans l'orientation 0
        positions_initiales = instance.obtenir_positions_initiales(x_pivot, y_pivot)
        
        # Pivot au centre de la pièce (position 1 sur 4)
        position_pivot = positions_initiales[1]
        
        instance.positions = positions_initiales
        instance.position_pivot = position_pivot
        
        return instance
    
    def obtenir_positions_initiales(self, x_pivot: int, y_pivot: int) -> List[Position]:
        """Obtenir les positions initiales pour l'orientation Nord."""
        return self._obtenir_positions_pour_orientation(0, x_pivot, y_pivot)
    
    
    def tourner(self) -> None:
        """Tourner la pièce dans le sens horaire."""
        self._orientation = (self._orientation + 1) % 4
        # Utiliser les coordonnées absolues du pivot pour éviter la dérive
        nouvelles_positions = self._obtenir_positions_pour_orientation(
            self._orientation, 
            self._x_pivot_absolu, 
            self._y_pivot_absolu + 1  # Convertir de coordonnée absolue à paramètre d'entrée
        )
        self.positions = nouvelles_positions
        # Mettre à jour le pivot pour pointer vers la bonne position dans la nouvelle liste
        self.position_pivot = nouvelles_positions[1]  # Le pivot est toujours à l'index 1

    def deplacer(self, delta_x: int, delta_y: int) -> None:
        """Déplace la pièce et met à jour les coordonnées absolues du pivot."""
        # Appeler la méthode parent pour déplacer les positions
        super().deplacer(delta_x, delta_y)
        # Mettre à jour les coordonnées absolues du pivot
        self._x_pivot_absolu += delta_x
        self._y_pivot_absolu += delta_y
    
    def _obtenir_positions_pour_orientation(self, orientation: int, x_pivot: int, y_pivot: int) -> List[Position]:
        """Obtenir les positions pour une orientation donnée.
        
        Args:
            orientation: 0=Nord, 1=Est, 2=Sud, 3=Ouest
            x_pivot: Position X du pivot
            y_pivot: Position Y du pivot
            
        Returns:
            Liste des positions absolues pour cette orientation
        """
        if orientation == 0:  # Nord - T inversé (branche vers le bas)
            return [
                Position(x_pivot - 1, y_pivot - 1),  # [pivot.x-1, pivot.y]
                Position(x_pivot, y_pivot - 1),      # [pivot.x, pivot.y] (le pivot de la pièce)
                Position(x_pivot + 1, y_pivot - 1),  # [pivot.x+1, pivot.y]
                Position(x_pivot, y_pivot)   # [pivot.x, pivot.y+1]
            ]
        elif orientation == 1:  # Est - T vers la droite (branche vers la gauche)
            return [
                Position(x_pivot, y_pivot - 2),  # [pivot.x, pivot.y-1]
                Position(x_pivot, y_pivot - 1),  # [pivot.x, pivot.y] (le pivot de la pièce)
                Position(x_pivot, y_pivot),      # [pivot.x, pivot.y+1]
                Position(x_pivot - 1, y_pivot - 1)  # [pivot.x-1, pivot.y]
            ]
        elif orientation == 2:  # Sud - T normal (branche vers le haut)
            return [
                Position(x_pivot - 1, y_pivot - 1),  # [pivot.x-1, pivot.y]
                Position(x_pivot, y_pivot - 1),      # [pivot.x, pivot.y] (le pivot de la pièce)
                Position(x_pivot + 1, y_pivot - 1),  # [pivot.x+1, pivot.y]
                Position(x_pivot, y_pivot - 2)       # [pivot.x, pivot.y-1]
            ]
        else:  # orientation == 3, Ouest - T vers la gauche (branche vers la droite)
            return [
                Position(x_pivot, y_pivot - 2),  # [pivot.x, pivot.y-1]
                Position(x_pivot, y_pivot - 1),  # [pivot.x, pivot.y] (le pivot de la pièce)
                Position(x_pivot, y_pivot),      # [pivot.x, pivot.y+1]
                Position(x_pivot + 1, y_pivot - 1)  # [pivot.x+1, pivot.y]
            ]
