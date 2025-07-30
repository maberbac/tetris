"""
Tests pour PieceJ - Pièce en forme de J (L inversé).

Tests TDD pour vérifier que PieceJ :
- Se crée avec la bonne forme J (4 orientations possibles)
- Peut tourner dans les 4 directions (Nord, Est, Sud, Ouest)  
- Hérite correctement des comportements de base (mouvement)
- S'auto-enregistre via le Registry Pattern
"""

import unittest
from src.domaine.entites.position import Position
from src.domaine.entites.piece import TypePiece
from src.domaine.entites.pieces.piece_j import PieceJ


class TestPieceJ(unittest.TestCase):
    """Tests pour la pièce J - forme L inversé avec 4 orientations."""
    
    def test_piece_j_peut_etre_creee(self):
        """Test RED : Créer une PieceJ avec positions initiales J Nord."""
        # Arrange & Act
        piece = PieceJ.creer(x_pivot=5, y_pivot=0)
        
        # Assert : Forme J Nord (L inversé) avec pivot à Position(x_pivot, y_pivot)
        positions_attendues = [
            Position(4, -1),  # Haut-gauche 
            Position(4, 0),   # Coude-gauche
            Position(5, 0),   # Coude-centre (pivot)
            Position(6, 0)    # Coude-droite
        ]
        
        self.assertEqual(piece.positions, positions_attendues)
        self.assertEqual(piece.position_pivot, Position(5, 0))  # Pivot à (x_pivot, y_pivot)
        self.assertEqual(len(piece.positions), 4)
        
    def test_piece_j_peut_se_deplacer(self):
        """Test : PieceJ peut se déplacer (héritage du comportement commun)."""
        # Arrange
        piece = PieceJ.creer(x_pivot=5, y_pivot=0)
        position_pivot_initiale = piece.position_pivot
        
        # Act
        piece.deplacer(2, 3)
        
        # Assert : Toutes les positions et le pivot ont bougé
        self.assertEqual(piece.position_pivot, Position(7, 3))  # 5+2, 0+3
        self.assertNotEqual(piece.position_pivot, position_pivot_initiale)
        
    def test_piece_j_peut_tourner_nord_vers_est(self):
        """Test RED : PieceJ peut tourner de Nord vers Est (J vers la droite)."""
        # Arrange
        piece = PieceJ.creer(x_pivot=5, y_pivot=0)
        
        # Act : Tourner vers Est
        piece.tourner()
        
        # Assert : Forme J Est avec pivot fixe à Position(x_pivot, y_pivot)
        positions_attendues = [
            Position(6, -1),  # Haut-centre
            Position(5, 0),   # Coude-centre (pivot) 
            Position(6, 0),   # Coude-droite
            Position(6, 1)    # Bas-centre
        ]
        
        self.assertEqual(piece.positions, positions_attendues)
        self.assertEqual(piece.position_pivot, Position(5, 0))  # Pivot fixe
        
    def test_piece_j_peut_tourner_est_vers_sud(self):
        """Test : PieceJ peut tourner de Est vers Sud (J vers le bas)."""
        # Arrange
        piece = PieceJ.creer(x_pivot=5, y_pivot=0)
        piece.tourner()  # Nord → Est
        
        # Act : Tourner vers Sud
        piece.tourner()
        
        # Assert : Forme J Sud avec pivot fixe à Position(x_pivot, y_pivot)
        positions_attendues = [
            Position(4, 0),  # Coude-gauche
            Position(5, 0),  # Coude-centre (pivot)
            Position(6, 0),  # Coude-droite
            Position(6, 1)   # Bas-droite
        ]
        
        self.assertEqual(piece.positions, positions_attendues)
        self.assertEqual(piece.position_pivot, Position(5, 0))  # Pivot fixe
        
    def test_piece_j_peut_tourner_sud_vers_ouest(self):
        """Test : PieceJ peut tourner de Sud vers Ouest (J vers la gauche)."""
        # Arrange
        piece = PieceJ.creer(x_pivot=5, y_pivot=0)
        piece.tourner()  # Nord → Est
        piece.tourner()  # Est → Sud
        
        # Act : Tourner vers Ouest
        piece.tourner()
        
        # Assert : Forme J Ouest avec pivot fixe à Position(x_pivot, y_pivot)
        positions_attendues = [
            Position(5, -1),  # Haut-centre
            Position(5, 0),   # Coude-centre (pivot)
            Position(6, 0),   # Coude-droite
            Position(5, 1)    # Bas-centre
        ]
        
        self.assertEqual(piece.positions, positions_attendues)
        self.assertEqual(piece.position_pivot, Position(5, 0))  # Pivot fixe
        
    def test_piece_j_rotation_complete_revient_a_origine(self):
        """Test : PieceJ après 4 rotations revient à l'orientation d'origine."""
        # Arrange
        piece = PieceJ.creer(x_pivot=5, y_pivot=0)
        positions_initiales = piece.positions[:]
        
        # Act : 4 rotations complètes
        for _ in range(4):
            piece.tourner()
        
        # Assert : Retour à l'état initial
        self.assertEqual(piece.positions, positions_initiales)
        self.assertEqual(piece.position_pivot, Position(5, 0))  # Pivot fixe à (x_pivot, y_pivot)
        
    def test_piece_j_a_type_correct(self):
        """Test : PieceJ retourne le bon type."""
        # Arrange & Act
        piece = PieceJ.creer(x_pivot=5, y_pivot=0)
        
        # Assert
        self.assertEqual(piece.type_piece, TypePiece.J)
        
    def test_piece_j_differ_de_piece_l(self):
        """Test : PieceJ a une forme différente de PieceL (symétrie)."""
        # Arrange
        piece_j = PieceJ.creer(x_pivot=5, y_pivot=0)
        
        # Act : Vérifier la forme J Nord spécifique
        positions_j = piece_j.positions
        
        # Assert : Forme J Nord distincte (extension vers la gauche en haut)
        self.assertIn(Position(4, -1), positions_j)  # Extension gauche-haut caractéristique du J
        self.assertIn(Position(4, 0), positions_j)   # Coude gauche
        self.assertIn(Position(5, 0), positions_j)   # Coude centre (pivot)  
        self.assertIn(Position(6, 0), positions_j)   # Coude droite
        
        # Note : PieceL aurait l'extension vers la droite en haut


if __name__ == '__main__':
    unittest.main()
