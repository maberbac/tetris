"""
PieceT - Pièce en forme de T.

La PieceT a 4 orientations possibles :
- Nord : T inversé (branche vers le bas)
- Est : T vers la droite (branche vers la gauche)  
- Sud : T normal (branche vers le haut)
- Ouest : T vers la gauche (branche vers la droite)

🔧 REFACTORING : Architecture harmonisée avec PieceJ et PieceL
- Utilisation des méthodes _devenir_xxx() au lieu de _obtenir_positions_pour_orientation()
- Suppression des coordonnées absolues complexes (_x_pivot_absolu, _y_pivot_absolu)
- Architecture simple et cohérente avec les autres pièces
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
        positions_initiales = instance.obtenir_positions_initiales(x_pivot, y_pivot)
        
        # Pivot exactement aux coordonnées spécifiées (index 1 dans les positions)
        position_pivot = positions_initiales[1]
        
        instance.positions = positions_initiales
        instance.position_pivot = position_pivot
        instance._orientation = 0  # 0=Nord, 1=Est, 2=Sud, 3=Ouest
        
        return instance

    def obtenir_positions_initiales(self, x_pivot: int, y_pivot: int) -> List[Position]:
        """
        Crée les positions initiales pour PieceT (forme T normal Nord).
        
        Format T Nord avec pivot au centre :
          █   ← position [x_pivot, y_pivot-1] (branche vers le haut)
         ███   ← positions [x_pivot-1, y_pivot], [x_pivot, y_pivot] (pivot), [x_pivot+1, y_pivot]
        
        Args:
            x_pivot: Position X du pivot 
            y_pivot: Position Y du pivot
            
        Returns:
            4 positions en forme T Nord avec pivot à (x_pivot, y_pivot)
        """
        return [
            Position(x_pivot - 1, y_pivot),      # Gauche
            Position(x_pivot, y_pivot),          # Pivot (centre) - INDEX 1
            Position(x_pivot + 1, y_pivot),      # Droite
            Position(x_pivot, y_pivot - 1)       # Branche vers le haut
        ]
    
    def tourner(self) -> None:
        """
        Rotation de la pièce T (4 orientations) - SENS HORAIRE.
        
        Nord → Ouest → Sud → Est → Nord → ...
        """
        self._orientation = (self._orientation + 1) % 4
        
        if self._orientation == 0:
            self._devenir_nord()
        elif self._orientation == 1:
            self._devenir_ouest()  # HORAIRE : Nord → Ouest
        elif self._orientation == 2:
            self._devenir_sud()
        else:  # self._orientation == 3
            self._devenir_est()    # HORAIRE : Sud → Est

    def _devenir_nord(self) -> None:
        """
        Passage en orientation Nord (T normal).
        
        Configuration Nord autour du pivot :
          █   ← [pivot.x, pivot.y-1] (branche vers le haut)
         ███   ← [pivot.x-1, pivot.y], [pivot.x, pivot.y] (le pivot), [pivot.x+1, pivot.y]
        """
        self.positions = [
            Position(self.position_pivot.x - 1, self.position_pivot.y),      # Gauche
            Position(self.position_pivot.x, self.position_pivot.y),          # Pivot
            Position(self.position_pivot.x + 1, self.position_pivot.y),      # Droite
            Position(self.position_pivot.x, self.position_pivot.y - 1)       # Branche vers le haut
        ]

    def _devenir_est(self) -> None:
        """
        Passage en orientation Est (T vers la droite).
        
        Configuration Est autour du pivot :
         █    ← [pivot.x, pivot.y-1]
        ██    ← [pivot.x-1, pivot.y] et [pivot.x, pivot.y] (le pivot)
         █    ← [pivot.x, pivot.y+1]
        """
        self.positions = [
            Position(self.position_pivot.x, self.position_pivot.y - 1),      # Haut
            Position(self.position_pivot.x, self.position_pivot.y),          # Pivot
            Position(self.position_pivot.x, self.position_pivot.y + 1),      # Bas
            Position(self.position_pivot.x - 1, self.position_pivot.y)       # Branche vers la gauche
        ]

    def _devenir_sud(self) -> None:
        """
        Passage en orientation Sud (T inversé).
        
        Configuration Sud autour du pivot :
         ███   ← [pivot.x-1, pivot.y], [pivot.x, pivot.y] (le pivot), [pivot.x+1, pivot.y]
          █    ← [pivot.x, pivot.y+1] (branche vers le bas)
        """
        self.positions = [
            Position(self.position_pivot.x - 1, self.position_pivot.y),      # Gauche
            Position(self.position_pivot.x, self.position_pivot.y),          # Pivot
            Position(self.position_pivot.x + 1, self.position_pivot.y),      # Droite
            Position(self.position_pivot.x, self.position_pivot.y + 1)       # Branche vers le bas
        ]

    def _devenir_ouest(self) -> None:
        """
        Passage en orientation Ouest (T vers la gauche).
        
        Configuration Ouest autour du pivot :
        █     ← [pivot.x, pivot.y-1]
        ██    ← [pivot.x, pivot.y] (le pivot) et [pivot.x+1, pivot.y]
        █     ← [pivot.x, pivot.y+1]
        """
        self.positions = [
            Position(self.position_pivot.x, self.position_pivot.y - 1),      # Haut
            Position(self.position_pivot.x, self.position_pivot.y),          # Pivot
            Position(self.position_pivot.x, self.position_pivot.y + 1),      # Bas
            Position(self.position_pivot.x + 1, self.position_pivot.y)       # Branche vers la droite
        ]
