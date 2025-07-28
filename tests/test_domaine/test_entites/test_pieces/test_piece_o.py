"""
Tests pour PieceO - Pièce carré du Tetris.

PieceO est la pièce en forme de carré (4 blocs en 2x2).
Comportements spécifiques :
- 1 seule orientation : carré 2x2
- Rotation : no-op (carré reste identique)
- Position spawn : centre du plateau
- Démontre polymorphisme avec PieceI
"""

import unittest
from src.domaine.entites.pieces.piece_o import PieceO
from src.domaine.entites.piece import TypePiece
from src.domaine.entites.position import Position


class TestPieceO(unittest.TestCase):
    """Tests TDD pour la pièce O (carré)."""
    
    def test_piece_o_peut_etre_creee(self):
        """
        Test RED : Créer une PieceO avec positions carré 2x2.
        
        PieceO doit :
        - Être de type O
        - Avoir 4 positions en carré 2x2
        - Avoir un pivot au centre du carré
        """
        # Act : Créer une PieceO
        piece = PieceO.creer(x_spawn=5, y_spawn=1)
        
        # Assert : Vérifier les propriétés
        self.assertEqual(piece.type_piece, TypePiece.O)
        self.assertEqual(len(piece.positions), 4)
        
        # Positions attendues : carré 2x2 centré sur x=5, y=1
        # ██
        # ██
        positions_attendues = [
            Position(5, 1), Position(6, 1),    # Ligne du haut
            Position(5, 2), Position(6, 2)     # Ligne du bas
        ]
        self.assertEqual(piece.positions, positions_attendues)
        
        # Pivot au centre du carré (entre les 4 blocs)
        # Pour un carré 2x2, le pivot logique est (5.5, 1.5)
        # Mais comme on utilise des entiers, on choisit un coin
        self.assertEqual(piece.position_pivot, Position(5, 1))
    
    def test_piece_o_rotation_ne_fait_rien(self):
        """
        Test : PieceO rotation est un no-op (carré reste identique).
        
        Démontre polymorphisme : même interface que PieceI.tourner()
        mais comportement différent.
        """
        # Arrange : PieceO avec positions initiales
        piece = PieceO.creer(x_spawn=7, y_spawn=2)
        positions_initiales = piece.positions.copy()
        pivot_initial = piece.position_pivot
        
        # Act : Plusieurs rotations (devrait ne rien faire)
        for _ in range(4):  # 4 rotations
            piece.tourner()
            
            # Assert : Positions inchangées à chaque rotation
            self.assertEqual(piece.positions, positions_initiales)
            self.assertEqual(piece.position_pivot, pivot_initial)
    
    def test_piece_o_peut_se_deplacer(self):
        """
        Test : PieceO peut se déplacer (héritage du comportement commun).
        
        Vérifie que le déplacement fonctionne comme PieceI.
        """
        # Arrange : PieceO
        piece = PieceO.creer(x_spawn=5, y_spawn=1)
        
        # Act : Déplacer vers la droite et vers le bas
        piece.deplacer(2, 3)
        
        # Assert : Toutes positions déplacées de (2, 3)
        positions_attendues = [
            Position(7, 4), Position(8, 4),    # Ligne du haut
            Position(7, 5), Position(8, 5)     # Ligne du bas
        ]
        self.assertEqual(piece.positions, positions_attendues)
        self.assertEqual(piece.position_pivot, Position(7, 4))


if __name__ == '__main__':
    unittest.main()
