"""
Tests pour PieceZ - Forme Z (Snake inversé)

La PieceZ a la forme d'un Z et peut tourner entre 2 orientations :
- Horizontal : positions formant un Z horizontal  
- Vertical : positions formant un Z vertical

Architecture testée : Registry Pattern avec @piece_tetris(TypePiece.Z)
"""

import unittest
from src.domaine.entites.position import Position
from src.domaine.entites.piece import TypePiece
from src.domaine.entites.pieces.piece_z import PieceZ


class TestPieceZ(unittest.TestCase):
    """Tests pour la pièce Z avec pattern Registry"""

    def test_piece_z_peut_etre_creee(self):
        """Test RED : Créer une PieceZ avec positions initiales Z horizontal."""
        # Arrange & Act
        piece = PieceZ.creer(x_pivot=5, y_pivot=-1)  # Zone invisible : spawn à y=-1
        
        # Assert - Form Z horizontal (orientation par défaut)
        # ██   ← positions (4,-2) et (5,-2)
        #  ██  ← positions (5,-1) et (6,-1)
        positions_attendues = [
            Position(4, -2),  # Gauche-haut
            Position(5, -2),  # Centre-haut (pivot réel)
            Position(5, -1),  # Centre-bas
            Position(6, -1)   # Droite-bas
        ]
        self.assertEqual(piece.positions, positions_attendues)
        self.assertEqual(piece.type_piece, TypePiece.Z)

    def test_piece_z_peut_se_deplacer(self):
        """Test : PieceZ peut se déplacer (héritage du comportement commun)."""
        # Arrange
        piece = PieceZ.creer(x_pivot=5, y_pivot=-1)  # Zone invisible
        positions_initiales = piece.positions.copy()
        
        # Act
        piece.deplacer(2, 3)
        
        # Assert - Toutes les positions décalées
        positions_attendues = [
            Position(6, 1),  # (4,-2) + (2,3)
            Position(7, 1),  # (5,-2) + (2,3)
            Position(7, 2),  # (5,-1) + (2,3)  
            Position(8, 2)   # (6,-1) + (2,3)
        ]
        self.assertEqual(piece.positions, positions_attendues)
        self.assertNotEqual(piece.positions, positions_initiales)

    def test_piece_z_peut_tourner_horizontal_vers_vertical(self):
        """Test RED : PieceZ peut tourner de horizontal vers vertical."""
        # Arrange
        piece = PieceZ.creer(x_pivot=5, y_pivot=-1)  # Zone invisible, pivot sera à (5,-2)
        
        # Act
        piece.tourner()
        
        # Assert - Form Z vertical autour du pivot (5,-2)
        #  █   ← position (6,-3)
        # ██   ← positions (5,-2) et (6,-2)  
        # █    ← position (5,-1)
        positions_attendues = [
            Position(6, -3),  # Haut-droite
            Position(5, -2),  # Centre (pivot)
            Position(6, -2),  # Centre-droite
            Position(5, -1)   # Bas-gauche
        ]
        self.assertEqual(piece.positions, positions_attendues)

    def test_piece_z_peut_tourner_vertical_vers_horizontal(self):
        """Test : PieceZ peut tourner de vertical vers horizontal."""
        # Arrange
        piece = PieceZ.creer(x_pivot=5, y_pivot=-1)  # Zone invisible, pivot sera à (5,-2)
        piece.tourner()  # Passage en vertical
        
        # Act
        piece.tourner()  # Retour en horizontal
        
        # Assert - Retour à la forme horizontale autour du pivot (5,-2)
        positions_attendues = [
            Position(4, -2),  # Gauche-haut
            Position(5, -2),  # Centre-haut (pivot)
            Position(5, -1),  # Centre-bas
            Position(6, -1)   # Droite-bas
        ]
        self.assertEqual(piece.positions, positions_attendues)

    def test_piece_z_rotation_complete_revient_a_origine(self):
        """Test : PieceZ après 2 rotations revient à l'orientation d'origine."""
        # Arrange
        piece = PieceZ.creer(x_pivot=5, y_pivot=-1)  # Zone invisible
        positions_initiales = piece.positions.copy()
        
        # Act - 2 rotations pour Z (seulement 2 orientations)
        piece.tourner()
        piece.tourner()
        
        # Assert
        self.assertEqual(piece.positions, positions_initiales)

    def test_piece_z_a_type_correct(self):
        """Test : PieceZ retourne le bon type."""
        # Arrange & Act
        piece = PieceZ.creer(x_pivot=0, y_pivot=0)
        
        # Assert
        self.assertEqual(piece.type_piece, TypePiece.Z)

    def test_piece_z_differ_de_piece_s(self):
        """Test : PieceZ a une forme différente de PieceS."""
        # Arrange
        piece_z = PieceZ.creer(x_pivot=5, y_pivot=0)
        
        # Import ici pour éviter les dépendances circulaires dans les tests
        from src.domaine.entites.pieces.piece_s import PieceS
        piece_s = PieceS.creer(x_pivot=5, y_pivot=0)
        
        # Act & Assert - Les formes sont différentes
        self.assertNotEqual(piece_z.positions, piece_s.positions)
        self.assertEqual(piece_z.type_piece, TypePiece.Z)
        self.assertEqual(piece_s.type_piece, TypePiece.S)


if __name__ == '__main__':
    unittest.main()
