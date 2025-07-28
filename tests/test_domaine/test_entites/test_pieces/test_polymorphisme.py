"""
Tests de polymorphisme entre les différents types de pièces.

Ces tests démontrent que toutes les pièces implémentent la même interface
mais avec des comportements différents (principe du polymorphisme).
"""

import unittest
from src.domaine.entites.pieces.piece_i import PieceI
from src.domaine.entites.pieces.piece_o import PieceO
from src.domaine.entites.piece import Piece
from src.domaine.entites.position import Position


class TestPolymorphismePieces(unittest.TestCase):
    """Tests du polymorphisme entre les types de pièces."""
    
    def test_polymorphisme_rotation_comportements_differents(self):
        """
        Test : Polymorphisme - même interface, comportements différents.
        
        PieceI.tourner() → change positions
        PieceO.tourner() → no-op (positions inchangées)
        """
        # Arrange : Une PieceI et une PieceO
        pieces: list[Piece] = [
            PieceI.creer(x_spawn=5, y_spawn=2),
            PieceO.creer(x_spawn=5, y_spawn=2)
        ]
        
        # Sauvegarder positions initiales
        positions_initiales = [piece.positions.copy() for piece in pieces]
        
        # Act : Appeler tourner() sur chaque pièce (même interface)
        for piece in pieces:
            piece.tourner()  # Polymorphisme : comportement dépend du type réel
        
        # Assert : Comportements différents selon le type
        piece_i, piece_o = pieces
        
        # PieceI : positions ont changé (rotation effective)
        self.assertNotEqual(piece_i.positions, positions_initiales[0])
        
        # PieceO : positions identiques (rotation no-op)
        self.assertEqual(piece_o.positions, positions_initiales[1])
    
    def test_polymorphisme_deplacer_comportement_commun(self):
        """
        Test : Polymorphisme - comportement commun hérité.
        
        Toutes les pièces héritent du même déplacement.
        """
        # Arrange : Différents types de pièces
        pieces: list[Piece] = [
            PieceI.creer(x_spawn=3, y_spawn=1),
            PieceO.creer(x_spawn=3, y_spawn=1)
        ]
        
        # Sauvegarder positions avant déplacement
        positions_avant = [piece.positions.copy() for piece in pieces]
        
        # Act : Déplacer toutes les pièces avec même delta
        for piece in pieces:
            piece.deplacer(2, 1)  # Même interface, même comportement
        
        # Assert : Toutes déplacées de la même façon
        for i, piece in enumerate(pieces):
            # Vérifier que chaque position a été déplacée de (2, 1)
            for j, position_apres in enumerate(piece.positions):
                position_avant = positions_avant[i][j]
                attendu_x = position_avant.x + 2
                attendu_y = position_avant.y + 1
                
                self.assertEqual(position_apres.x, attendu_x)
                self.assertEqual(position_apres.y, attendu_y)


if __name__ == '__main__':
    unittest.main()
