"""
PieceJ - Pièce en forme de J (L inversé)

La PieceJ forme un "J" et a 4 orientations possibles :
- Nord : Configuration J classique (L inversé)
- Est : J tourné à 90° (vers la droite)
- Sud : J tourné à 180° (L normal)
- Ouest : J tourné à 270° (vers la gauche)

Forme Nord initiale :
█     ← bloc haut-gauche
███   ← bloc coude (pivot au centre)

Auto-enregistrement : @piece_tetris(TypePiece.J)
"""

from typing import List
from ..position import Position  
from ..piece import Piece, TypePiece
from ..fabriques.registre_pieces import piece_tetris


@piece_tetris(TypePiece.J)
class PieceJ(Piece):
    """
    Implémentation de la pièce J avec rotation sur 4 orientations.
    
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
    def creer(cls, x_pivot: int, y_pivot: int) -> 'PieceJ':
        """
        Factory method pour créer une PieceJ.
        
        Args:
            x_pivot: Position X du pivot
            y_pivot: Position Y du pivot
            
        Returns:
            Nouvelle instance de PieceJ
        """
        instance = cls.__new__(cls)
        positions_initiales = instance.obtenir_positions_initiales(x_pivot, y_pivot)
        
        # Position pivot : toujours Position(x_pivot, y_pivot) - ici position 2 sur 4
        position_pivot = positions_initiales[2]
        
        instance.positions = positions_initiales
        instance.position_pivot = position_pivot
        instance._orientation = 0  # 0=Nord, 1=Est, 2=Sud, 3=Ouest
        
        return instance

    def obtenir_positions_initiales(self, x_pivot: int, y_pivot: int) -> List[Position]:
        """
        Crée les positions initiales pour PieceJ (forme J Nord).
        
        Format J Nord avec pivot au centre du coude :
        █     ← position [x_pivot-1, y_pivot-1] 
        ███   ← positions [x_pivot-1, y_pivot], [x_pivot, y_pivot] (pivot), [x_pivot+1, y_pivot]
        
        Args:
            x_pivot: Position X du pivot 
            y_pivot: Position Y du pivot
            
        Returns:
            4 positions en forme J Nord avec pivot à (x_pivot, y_pivot)
        """
        return [
            Position(x_pivot - 1, y_pivot - 1),  # Haut-gauche
            Position(x_pivot - 1, y_pivot),      # Coude-gauche
            Position(x_pivot, y_pivot),          # Coude-centre (pivot)
            Position(x_pivot + 1, y_pivot)       # Coude-droite
        ]

    @property  
    def type_piece(self) -> TypePiece:
        """Retourne le type de cette pièce."""
        return TypePiece.J

    def tourner(self) -> None:
        """
        Rotation de la pièce J (4 orientations).
        
        Nord → Est → Sud → Ouest → Nord → ...
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
        Passage en orientation Nord (J classique).
        
        Configuration Nord autour du pivot (doit correspondre aux positions initiales) :
        █     ← [pivot.x-1, pivot.y-1]
        ███   ← [pivot.x-1, pivot.y], [pivot.x, pivot.y] (le pivot de la pièce), [pivot.x+1, pivot.y]
        """
        self.positions = [
            Position(self.position_pivot.x - 1, self.position_pivot.y - 1),  # Haut-gauche
            Position(self.position_pivot.x - 1, self.position_pivot.y),      # Coude-gauche
            Position(self.position_pivot.x, self.position_pivot.y),          # Coude-centre (pivot)
            Position(self.position_pivot.x + 1, self.position_pivot.y)       # Coude-droite
        ]

    def _devenir_est(self) -> None:
        """
        Passage en orientation Est (J vers la droite).
        
        Configuration Est autour du pivot :
        █     ← [pivot.x+1, pivot.y-1]
        █     ← [pivot.x, pivot.y] (le pivot de la pièce)
        ██    ← [pivot.x+1, pivot.y], [pivot.x+1, pivot.y+1]
        """
        self.positions = [
            Position(self.position_pivot.x + 1, self.position_pivot.y - 1),  # Haut-centre
            Position(self.position_pivot.x, self.position_pivot.y),          # Coude-gauche (pivot)
            Position(self.position_pivot.x + 1, self.position_pivot.y),      # Coude-centre
            Position(self.position_pivot.x + 1, self.position_pivot.y + 1)   # Bas-centre
        ]

    def _devenir_sud(self) -> None:
        """
        Passage en orientation Sud (J inversé / L normal).
        
        Configuration Sud autour du pivot :
        ███   ← [pivot.x-1, pivot.y], [pivot.x, pivot.y] (le pivot de la pièce), [pivot.x+1, pivot.y]
          █   ← [pivot.x+1, pivot.y+1]
        """
        self.positions = [
            Position(self.position_pivot.x - 1, self.position_pivot.y),      # Coude-gauche
            Position(self.position_pivot.x, self.position_pivot.y),          # Coude-centre (pivot)
            Position(self.position_pivot.x + 1, self.position_pivot.y),      # Coude-droite
            Position(self.position_pivot.x + 1, self.position_pivot.y + 1)   # Bas-droite
        ]

    def _devenir_ouest(self) -> None:
        """
        Passage en orientation Ouest (J vers la gauche).
        
        Configuration Ouest autour du pivot :
         █     ← [pivot.x, pivot.y-1]
         █     ← [pivot.x, pivot.y] (le pivot de la pièce)
        ██     ← [pivot.x+1, pivot.y], [pivot.x, pivot.y+1]
        """
        self.positions = [
            Position(self.position_pivot.x, self.position_pivot.y - 1),      # Haut-centre
            Position(self.position_pivot.x, self.position_pivot.y),          # Coude-centre (pivot)
            Position(self.position_pivot.x + 1, self.position_pivot.y),      # Coude-droite
            Position(self.position_pivot.x, self.position_pivot.y + 1)       # Bas-centre
        ]
