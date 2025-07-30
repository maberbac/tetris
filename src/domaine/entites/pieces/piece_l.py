"""
PieceL - Pièce en forme de L

La PieceL forme un "L" et a 4 orientations possibles :
- Nord : L classique (  █  avec ███ en bas)
                      ███
- Est : L vers la droite (██ en haut, █ vertical à droite)
                           █          █   
                           █          █ 
- Sud : L inversé (███ en haut avec █ extension bas-gauche)
                   █
- Ouest : L vers la gauche (█ vertical avec ██ extension bas-droite)
                            █
                            ██

Auto-enregistrement : @piece_tetris(TypePiece.L)
"""

from typing import List
from ..position import Position  
from ..piece import Piece, TypePiece
from ..fabriques.registre_pieces import piece_tetris


@piece_tetris(TypePiece.L)
class PieceL(Piece):
    """
    Implémentation de la pièce L avec rotation sur 4 orientations.
    
    Pattern utilisé :
    - Template Method (héritage de Piece)
    - Factory Method (méthode creer)
    - Registry Pattern (auto-enregistrement)
    """
    
    def __init__(self):
        """Constructeur appelé par le factory method."""
        self._orientation = 0  # 0=Nord, 1=Est, 2=Sud, 3=Ouest

    @classmethod
    def creer(cls, x_pivot: int, y_pivot: int) -> 'PieceL':
        """
        Factory method pour créer une PieceL.
        
        Args:
            x_pivot: Position X du pivot
            y_pivot: Position Y de pivot
            
        Returns:
            Nouvelle instance PieceL en orientation Nord
        """
        instance = cls.__new__(cls)
        instance._orientation = 0
        positions_initiales = instance.obtenir_positions_initiales(x_pivot, y_pivot)
        
        # Pivot au coude de la pièce L (position 1 - coude-droite)
        position_pivot = positions_initiales[1]
        
        instance.positions = positions_initiales
        instance.position_pivot = position_pivot
        
        return instance

    def obtenir_positions_initiales(self, x_pivot: int, y_pivot: int) -> List[Position]:
        """
        Obtenir les positions initiales pour PieceL (orientation Nord).
        
        Configuration Nord - L classique avec coude à droite :
          █  ← position [x_pivot+1, y_pivot]
        ███  ← positions [x_pivot-1, y_pivot+1], [x_pivot, y_pivot+1], [x_pivot+1, y_pivot+1]
        
        Args:
            x_pivot: Position X du pivot
            y_pivot: Position Y du pivot
            
        Returns:
            Positions pour L en orientation Nord avec pivot au coude
        """
        return [
            Position(x_pivot + 1, y_pivot),      # Haut-droite
            Position(x_pivot + 1, y_pivot + 1),  # Coude-droite (pivot)
            Position(x_pivot, y_pivot + 1),      # Coude-centre
            Position(x_pivot - 1, y_pivot + 1)   # Coude-gauche
        ]

    @property  
    def type_piece(self) -> TypePiece:
        """Retourne le type de cette pièce."""
        return TypePiece.L

    def tourner(self) -> None:
        """
        Rotation de la pièce L (4 orientations).
        
        Nord → Est → Sud → Ouest → Nord
        Chaque rotation se fait autour du pivot fixe.
        """
        self._orientation = (self._orientation + 1) % 4
        
        if self._orientation == 0:
            self._devenir_nord()
        elif self._orientation == 1:
            self._devenir_est()
        elif self._orientation == 2:
            self._devenir_sud()
        else:  # self._orientation == 3
            self._devenir_ouest()

    def _devenir_nord(self) -> None:
        """
        Passage en orientation Nord (L classique).
        
        Configuration Nord autour du pivot fixe :
          █  ← [pivot.x, pivot.y-1]
        ███  ← [pivot.x-2, pivot.y], [pivot.x-1, pivot.y] et [pivot.x, pivot.y] (le pivot de la pièce)
        """
        self.positions = [
            Position(self.position_pivot.x, self.position_pivot.y - 1),      # Haut-droite
            Position(self.position_pivot.x, self.position_pivot.y),          # Coude-droite (pivot)
            Position(self.position_pivot.x - 1, self.position_pivot.y),      # Coude-centre
            Position(self.position_pivot.x - 2, self.position_pivot.y)       # Coude-gauche
        ]

    def _devenir_est(self) -> None:
        """
        Passage en orientation Est (L vers la droite).
        
        Configuration Est autour du pivot fixe (symétrie de PieceJ) :
        ██   ← [pivot.x-1, pivot.y-1] et [pivot.x, pivot.y-1]
         █   ← [pivot.x, pivot.y] (le pivot de la pièce)
         █   ← [pivot.x, pivot.y+1]
        """
        self.positions = [
            Position(self.position_pivot.x - 1, self.position_pivot.y - 1),  # Haut-gauche
            Position(self.position_pivot.x, self.position_pivot.y),          # Coude-droite (pivot)
            Position(self.position_pivot.x, self.position_pivot.y - 1),      # Haut-droite
            Position(self.position_pivot.x, self.position_pivot.y + 1)       # Bas-droite
        ]

    def _devenir_sud(self) -> None:
        """
        Passage en orientation Sud (L inversé).
        
        Configuration Sud autour du pivot fixe :
        ███  ← [pivot.x, pivot.y] (le pivot de la pièce), [pivot.x+1, pivot.y]  et [pivot.x+2, pivot.y]
        █    ← [pivot.x+1, pivot.y+1]
        """
        self.positions = [
            Position(self.position_pivot.x + 2, self.position_pivot.y),      # Coude-gauche
            Position(self.position_pivot.x, self.position_pivot.y),          # Coude-droite (pivot)
            Position(self.position_pivot.x + 1, self.position_pivot.y),      # Coude-centre
            Position(self.position_pivot.x, self.position_pivot.y + 1)       # Bas-droite
        ]

    def _devenir_ouest(self) -> None:
        """
        Passage en orientation Ouest (L vers la gauche).
        
        Configuration Ouest autour du pivot fixe :
        █    ← [pivot.x, pivot.y-1]
        █    ← [pivot.x, pivot.y] (le pivot de la pièce)
        ██   ← [pivot.x, pivot.y+1] et [pivot.x+1, pivot.y+1]
        """
        self.positions = [
            Position(self.position_pivot.x, self.position_pivot.y - 1),      # Haut-droite
            Position(self.position_pivot.x, self.position_pivot.y),          # Coude-droite (pivot)
            Position(self.position_pivot.x, self.position_pivot.y + 1),      # Bas-droite
            Position(self.position_pivot.x + 1, self.position_pivot.y + 1)   # Bas-centre
        ]
