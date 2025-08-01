"""
Tests pour PieceL - Pièce en forme de L.

Tests TDD pour vérifier que PieceL :
- Se crée avec la bonne forme L (4 orientations possibles)
- Peut tourner dans les 4 directions (Nord, Est, Sud, Ouest)  
- Hérite correctement des comportements de base (mouvement)
- S'auto-enregistre via le Registry Pattern
- Diffère de PieceJ (symétrie)
"""

import unittest
from src.domaine.entites.position import Position
from src.domaine.entites.piece import TypePiece
from src.domaine.entites.pieces.piece_l import PieceL


class TestPieceL(unittest.TestCase):
    """Tests pour la PieceL - Pièce en L avec 4 orientations."""

    def test_piece_l_peut_etre_creee(self):
        """Test RED : Créer une PieceL avec positions initiales L Nord."""
        # Arrange & Act
        piece = PieceL.creer(x_pivot=4, y_pivot=0)
        
        # Assert - Forme L Nord avec coude à droite :
        #   █   ← position (5, 0)
        # ███   ← positions (3, 1), (4, 1), (5, 1)
        positions_attendues = [
            Position(5, 0),  # Haut-droite
            Position(5, 1),  # Coude-droite (pivot)
            Position(4, 1),  # Coude-centre  
            Position(3, 1)   # Coude-gauche
        ]
        self.assertEqual(piece.positions, positions_attendues)
        self.assertEqual(piece.type_piece, TypePiece.L)
        
    def test_piece_l_peut_se_deplacer(self):
        """Test : PieceL peut se déplacer (héritage du comportement commun)."""
        # Arrange
        piece = PieceL.creer(x_pivot=4, y_pivot=0)
        positions_initiales = piece.positions.copy()
        
        # Act
        piece.deplacer(2, 3)
        
        # Assert - Toutes les positions décalées
        positions_attendues = [
            Position(7, 3),  # (5,0) + (2,3)
            Position(7, 4),  # (5,1) + (2,3)
            Position(6, 4),  # (4,1) + (2,3)
            Position(5, 4)   # (3,1) + (2,3)
        ]
        self.assertEqual(piece.positions, positions_attendues)
        self.assertNotEqual(piece.positions, positions_initiales)

    def test_piece_l_peut_tourner_nord_vers_est(self):
        """Test RED : PieceL peut tourner de Nord vers Est (L vers la droite)."""
        # Arrange
        piece = PieceL.creer(x_pivot=4, y_pivot=1)
        
        # Act
        piece.tourner()
        
        # Assert - L vers la droite autour du pivot fixe (5,2)
        positions_attendues = [
            Position(4, 1),  # Haut-gauche
            Position(5, 2),  # Coude-droite (pivot)
            Position(5, 1),  # Haut-droite
            Position(5, 3)   # Bas-droite
        ]
        self.assertEqual(piece.positions, positions_attendues)

    def test_piece_l_peut_tourner_est_vers_sud(self):
        """Test : PieceL peut tourner de Est vers Sud (L vers le bas)."""
        # Arrange  
        piece = PieceL.creer(x_pivot=4, y_pivot=1)
        piece.tourner()  # Nord -> Est
        
        # Act
        piece.tourner()  # Est -> Sud
        
        # Assert - L vers le bas autour du pivot fixe (5,2)
        positions_attendues = [
            Position(7, 2),  # Coude-gauche
            Position(5, 2),  # Coude-droite (pivot)
            Position(6, 2),  # Coude-centre
            Position(5, 3)   # Bas-droite (extension L)
        ]
        self.assertEqual(piece.positions, positions_attendues)

    def test_piece_l_peut_tourner_sud_vers_ouest(self):
        """Test : PieceL peut tourner de Sud vers Ouest (L vers la gauche)."""
        # Arrange
        piece = PieceL.creer(x_pivot=4, y_pivot=1)
        piece.tourner()  # Nord -> Est
        piece.tourner()  # Est -> Sud
        
        # Act
        piece.tourner()  # Sud -> Ouest
        
        # Assert - L vers la gauche autour du pivot fixe (5,2)
        positions_attendues = [
            Position(5, 1),  # Haut-droite
            Position(5, 2),  # Coude-droite (pivot)
            Position(5, 3),  # Bas-droite
            Position(6, 3)   # Bas-centre (extension L)
        ]
        self.assertEqual(piece.positions, positions_attendues)

    def test_piece_l_rotation_complete_revient_a_origine(self):
        """Test : PieceL après 4 rotations revient à l'orientation d'origine."""
        # Arrange
        piece = PieceL.creer(x_pivot=4, y_pivot=1)
        positions_initiales = piece.positions.copy()
        
        # Act - 4 rotations complètes
        for _ in range(4):
            piece.tourner()
            
        # Assert - Retour à la forme initiale
        self.assertEqual(piece.positions, positions_initiales)

    def test_piece_l_a_type_correct(self):
        """Test : PieceL retourne le bon type."""
        # Arrange & Act
        piece = PieceL.creer(x_pivot=4, y_pivot=0)
        
        # Assert
        self.assertEqual(piece.type_piece, TypePiece.L)

    def test_piece_l_differ_de_piece_j(self):
        """Test : PieceL a une forme différente de PieceJ (symétrie)."""
        # Arrange
        from src.domaine.entites.pieces.piece_j import PieceJ
        piece_l = PieceL.creer(x_pivot=4, y_pivot=1)
        piece_j = PieceJ.creer(x_pivot=4, y_pivot=1)
        
        # Act & Assert - Formes différentes même position de spawn
        self.assertNotEqual(piece_l.positions, piece_j.positions)
        self.assertNotEqual(piece_l.type_piece, piece_j.type_piece)
        
        # Vérification spécifique : L et J sont symétriques
        # L Nord :   █ avec extension en haut à droite
        #          ███
        # J Nord : █   avec extension en haut à gauche  
        #          ███
        self.assertIn(Position(5, 1), piece_l.positions)  # Extension L en haut à droite
        self.assertIn(Position(3, 1), piece_j.positions)  # Extension J en haut à gauche


if __name__ == '__main__':
    unittest.main()
