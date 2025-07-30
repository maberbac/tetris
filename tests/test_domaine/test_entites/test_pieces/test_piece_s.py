"""
Tests pour PieceS - Forme S (Snake)

La PieceS a la forme d'un S et peut tourner entre 2 orientations :
- Horizontal : positions formant un S horizontal
- Vertical : positions formant un S vertical

Architecture testée : Registry Pattern avec @piece_tetris(TypePiece.S)
"""

import unittest
from src.domaine.entites.position import Position
from src.domaine.entites.piece import TypePiece
from src.domaine.entites.pieces.piece_s import PieceS


class TestPieceS(unittest.TestCase):
    """Tests pour la pièce S avec pattern Registry"""

    def test_piece_s_peut_etre_creee(self):
        """Test RED : Créer une PieceS avec positions initiales S horizontal."""
        # Arrange & Act
        piece = PieceS.creer(x_pivot=5, y_pivot=0)
        
        # Assert - Form S horizontal (orientation par défaut)
        #  ██  ← positions (5,0) et (6,0)
        # ██   ← positions (4,1) et (5,1)
        positions_attendues = [
            Position(5, 0),  # Centre-haut
            Position(6, 0),  # Droite-haut  
            Position(4, 1),  # Gauche-bas
            Position(5, 1)   # Centre-bas (pivot)
        ]
        self.assertEqual(piece.positions, positions_attendues)
        self.assertEqual(piece.type_piece, TypePiece.S)

    def test_piece_s_peut_se_deplacer(self):
        """Test : PieceS peut se déplacer (héritage du comportement commun)."""
        # Arrange
        piece = PieceS.creer(x_pivot=5, y_pivot=0)
        positions_initiales = piece.positions.copy()
        
        # Act
        piece.deplacer(2, 3)
        
        # Assert - Toutes les positions décalées
        positions_attendues = [
            Position(7, 3),  # (5,0) + (2,3)
            Position(8, 3),  # (6,0) + (2,3)
            Position(6, 4),  # (4,1) + (2,3)  
            Position(7, 4)   # (5,1) + (2,3)
        ]
        self.assertEqual(piece.positions, positions_attendues)
        self.assertNotEqual(piece.positions, positions_initiales)

    def test_piece_s_peut_tourner_horizontal_vers_vertical(self):
        """Test RED : PieceS peut tourner de horizontal vers vertical."""
        # Arrange
        piece = PieceS.creer(x_pivot=5, y_pivot=1)
        
        # Act
        piece.tourner()
        
        # Assert - Form S vertical autour du pivot (5,2)
        # █    ← position (5,1)
        # ██   ← positions (5,2) et (6,2)  
        #  █   ← position (6,3)
        positions_attendues = [
            Position(5, 1),  # Haut
            Position(5, 2),  # Centre (pivot)
            Position(6, 2),  # Centre-droite
            Position(6, 3)   # Bas-droite
        ]
        self.assertEqual(piece.positions, positions_attendues)

    def test_piece_s_peut_tourner_vertical_vers_horizontal(self):
        """Test : PieceS peut tourner de vertical vers horizontal."""
        # Arrange
        piece = PieceS.creer(x_pivot=5, y_pivot=1)
        piece.tourner()  # Passage en vertical
        
        # Act
        piece.tourner()  # Retour en horizontal
        
        # Assert - Retour à la forme horizontale
        positions_attendues = [
            Position(5, 1),  # Centre-haut  
            Position(6, 1),  # Droite-haut
            Position(4, 2),  # Gauche-bas
            Position(5, 2)   # Centre-bas (pivot)
        ]
        self.assertEqual(piece.positions, positions_attendues)

    def test_piece_s_rotation_complete_revient_a_origine(self):
        """Test : PieceS après 2 rotations revient à l'orientation d'origine."""
        # Arrange
        piece = PieceS.creer(x_pivot=5, y_pivot=1)
        positions_initiales = piece.positions.copy()
        
        # Act - 2 rotations pour S (seulement 2 orientations)
        piece.tourner()
        piece.tourner()
        
        # Assert
        self.assertEqual(piece.positions, positions_initiales)

    def test_piece_s_a_type_correct(self):
        """Test : PieceS retourne le bon type."""
        # Arrange & Act
        piece = PieceS.creer(x_pivot=0, y_pivot=0)
        
        # Assert
        self.assertEqual(piece.type_piece, TypePiece.S)


if __name__ == '__main__':
    unittest.main()
