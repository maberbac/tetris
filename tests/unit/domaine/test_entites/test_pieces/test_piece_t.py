"""
Tests pour la PieceT - Pièce en forme de T.

La PieceT est une pièce qui a la forme d'un T et peut tourner dans 4 orientations.
Elle a toujours un axe central avec 3 blocks horizontaux et 1 block qui descend du centre.
"""

import unittest
from src.domaine.entites.position import Position
from src.domaine.entites.pieces.piece_t import PieceT
from src.domaine.entites.piece import TypePiece


class TestPieceT(unittest.TestCase):
    """Tests pour la PieceT - Pièce en T avec 4 orientations."""
    
    def setUp(self):
        """Préparer les données de test."""
        self.piece_t = PieceT.creer(x_pivot=5, y_pivot=0)
    
    def test_piece_t_a_type_correct(self):
        """Test : PieceT retourne le bon type."""
        self.assertEqual(self.piece_t.type_piece, TypePiece.T)
    
    def test_piece_t_positions_initiales_orientation_nord(self):
        """Test : PieceT a les bonnes positions initiales (orientation Nord - T inversé)."""
        positions = self.piece_t.positions
        positions_attendues = [
            Position(4, 0),  # Gauche du centre
            Position(5, 0),  # Centre
            Position(6, 0),  # Droite du centre  
            Position(5, 1)   # En bas du centre
        ]
        self.assertEqual(positions, positions_attendues)
    
    
    def test_piece_t_peut_tourner_vers_est(self):
        """Test : PieceT peut tourner vers l'Est (T vers la droite)."""
        self.piece_t.tourner()
        positions = self.piece_t.positions
        positions_attendues = [
            Position(5, -1), # En haut du centre
            Position(5, 0),  # Centre
            Position(5, 1),  # En bas du centre
            Position(4, 0)   # À gauche du centre
        ]
        self.assertEqual(positions, positions_attendues)
    
    def test_piece_t_peut_tourner_vers_sud(self):
        """Test : PieceT peut tourner vers le Sud (T normal)."""
        self.piece_t.tourner()  # Nord -> Est
        self.piece_t.tourner()  # Est -> Sud
        positions = self.piece_t.positions
        positions_attendues = [
            Position(4, 0),  # Gauche du centre
            Position(5, 0),  # Centre
            Position(6, 0),  # Droite du centre
            Position(5, -1)  # En haut du centre
        ]
        self.assertEqual(positions, positions_attendues)
    
    def test_piece_t_peut_tourner_vers_ouest(self):
        """Test : PieceT peut tourner vers l'Ouest (T vers la gauche)."""
        self.piece_t.tourner()  # Nord -> Est
        self.piece_t.tourner()  # Est -> Sud  
        self.piece_t.tourner()  # Sud -> Ouest
        positions = self.piece_t.positions
        positions_attendues = [
            Position(5, -1), # En haut du centre
            Position(5, 0),  # Centre
            Position(5, 1),  # En bas du centre
            Position(6, 0)   # À droite du centre
        ]
        self.assertEqual(positions, positions_attendues)
    
    def test_piece_t_rotation_complete_revient_a_origine(self):
        """Test : PieceT après 4 rotations revient à l'orientation d'origine."""
        positions_initiales = self.piece_t.positions[:]
        
        # 4 rotations complètes
        for _ in range(4):
            self.piece_t.tourner()
        
        positions_finales = self.piece_t.positions
        self.assertEqual(positions_initiales, positions_finales)


if __name__ == '__main__':
    unittest.main()
