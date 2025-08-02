"""
Tests pour PieceI - Pièce ligne droite du Tetris.

PieceI est la pièce en forme de ligne droite (4 blocs alignés).
Comportements spécifiques :
- 2 orientations : horizontal et vertical
- Rotation : alterne entre les 2 orientations
- Position spawn : centre du plateau
"""

import unittest
from src.domaine.entites.pieces.piece_i import PieceI
from src.domaine.entites.piece import TypePiece
from src.domaine.entites.position import Position


class TestPieceI(unittest.TestCase):
    """Tests TDD pour la pièce I (ligne droite)."""
    
    def test_piece_i_peut_etre_creee(self):
        """
        Test RED : Créer une PieceI avec positions initiales.
        
        PieceI doit :
        - Être de type I
        - Avoir 4 positions en ligne horizontale
        - Avoir un pivot au centre
        """
        # Act : Créer une PieceI
        piece = PieceI.creer(x_pivot=5, y_pivot=0)
        
        # Assert : Vérifier les propriétés
        self.assertEqual(piece.type_piece, TypePiece.I)
        self.assertEqual(len(piece.positions), 4)
        
        # Positions attendues : ligne horizontale centrée sur x=5 (zone invisible y=-1)
        positions_attendues = [
            Position(3, -1), Position(4, -1), 
            Position(5, -1), Position(6, -1)
        ]
        self.assertEqual(piece.positions, positions_attendues)
        
        # Pivot au centre de la ligne
        self.assertEqual(piece.position_pivot, Position(4, -1))
    
    def test_piece_i_peut_se_deplacer(self):
        """
        Test : PieceI peut se déplacer (Entity behavior).
        
        Contrairement aux Value Objects qui créent de nouvelles instances,
        les Entities mutent leur état.
        """
        # Arrange : Créer une PieceI
        piece = PieceI.creer(x_pivot=5, y_pivot=0)
        positions_initiales = piece.positions.copy()
        
        # Act : Déplacer la pièce vers la droite et vers le bas
        piece.deplacer(1, 2)
        
        # Assert : Vérifier que l'Entity a muté (même objet, nouvelles positions)
        positions_attendues = [
            Position(4, 1), Position(5, 1),
            Position(6, 1), Position(7, 1)
        ]
        self.assertEqual(piece.positions, positions_attendues)
        self.assertEqual(piece.position_pivot, Position(5, 1))
        
        # Vérifier que les positions ont bien changé (Entity behavior)
        self.assertNotEqual(piece.positions, positions_initiales)
    
    def test_piece_i_peut_tourner_horizontal_vers_vertical(self):
        """
        Test RED : PieceI peut tourner de horizontal vers vertical.
        
        PieceI a 2 orientations :
        - Horizontal : ████ (4 blocs en ligne)
        - Vertical :   █    (4 blocs en colonne)
                       █
                       █
                       █
        """
        # Arrange : PieceI horizontal (position initiale avec zone invisible)
        piece = PieceI.creer(x_pivot=5, y_pivot=1)
        positions_horizontales = [
            Position(3, 0), Position(4, 0),
            Position(5, 0), Position(6, 0)
        ]
        self.assertEqual(piece.positions, positions_horizontales)
        
        # Act : Rotation vers vertical
        piece.tourner()
        
        # Assert : Maintenant en vertical autour du pivot (4, 0)
        positions_verticales = [
            Position(4, -1), Position(4, 0),
            Position(4, 1), Position(4, 2)
        ]
        self.assertEqual(piece.positions, positions_verticales)
        self.assertEqual(piece.position_pivot, Position(4, 0))  # Pivot inchangé
    
    def test_piece_i_peut_tourner_vertical_vers_horizontal(self):
        """
        Test : PieceI peut tourner de vertical vers horizontal.
        
        Rotation inverse : vertical → horizontal
        """
        # Arrange : PieceI en position verticale
        piece = PieceI.creer(x_pivot=5, y_pivot=1)
        piece.tourner()  # Passer en vertical d'abord
        
        positions_verticales = piece.positions.copy()
        
        # Act : Rotation retour vers horizontal  
        piece.tourner()
        
        # Assert : Retour à l'horizontal (zone invisible)
        positions_horizontales = [
            Position(3, 0), Position(4, 0),
            Position(5, 0), Position(6, 0)
        ]
        self.assertEqual(piece.positions, positions_horizontales)
        self.assertNotEqual(piece.positions, positions_verticales)
    
    def test_piece_i_pivot_reste_fixe_pendant_rotation(self):
        """
        Test : Le pivot de PieceI reste à la même position pendant rotation.
        
        Le pivot est le centre de rotation et ne doit jamais bouger,
        seules les autres positions tournent autour.
        """
        # Arrange : PieceI avec pivot connu (zone invisible)
        piece = PieceI.creer(x_pivot=7, y_pivot=3)
        pivot_initial = piece.position_pivot
        self.assertEqual(pivot_initial, Position(6, 2))  # pivot = positions[1] avec zone invisible
        
        # Act & Assert : Plusieurs rotations, pivot inchangé
        for _ in range(4):  # 4 rotations = cycle complet
            piece.tourner()
            self.assertEqual(piece.position_pivot, pivot_initial)
            
            # Vérifier que le pivot est toujours présent dans les positions
            self.assertIn(pivot_initial, piece.positions)


if __name__ == '__main__':
    unittest.main()
