"""
Tests pour FabriquePieces - Factory Pattern pour créer les pièces Tetris.

FabriquePieces centralise la création de toutes les pièces avec :
- Création par type spécifique
- Création aléatoire pour le jeu
- Interface cohérente
- Position de spawn configurable
"""

import unittest
from src.domaine.entites.fabriques.fabrique_pieces import FabriquePieces
from src.domaine.entites.piece import TypePiece
from src.domaine.entites.pieces.piece_i import PieceI
from src.domaine.entites.pieces.piece_o import PieceO
from src.domaine.entites.position import Position


class TestFabriquePieces(unittest.TestCase):
    """Tests TDD pour la fabrique de pièces."""
    
    def setUp(self):
        """Configuration commune pour tous les tests."""
        self.fabrique = FabriquePieces()
    
    def test_fabrique_peut_creer_piece_par_type(self):
        """
        Test RED : La fabrique peut créer une pièce par son type.
        
        La fabrique doit :
        - Accepter un TypePiece en paramètre
        - Retourner la bonne classe concrète
        - Utiliser les positions de spawn par défaut
        """
        # Act : Créer des pièces par type
        piece_i = self.fabrique.creer(TypePiece.I)
        piece_o = self.fabrique.creer(TypePiece.O)
        
        # Assert : Types et classes correctes
        self.assertIsInstance(piece_i, PieceI)
        self.assertEqual(piece_i.type_piece, TypePiece.I)
        
        self.assertIsInstance(piece_o, PieceO)
        self.assertEqual(piece_o.type_piece, TypePiece.O)
    
    def test_fabrique_peut_creer_piece_avec_position_spawn(self):
        """
        Test : La fabrique peut créer une pièce à une position spécifique.
        
        Utile pour positionner les pièces dans le jeu.
        """
        # Act : Créer une pièce à une position spécifique
        piece = self.fabrique.creer(TypePiece.I, x_pivot=7, y_pivot=3)
        
        # Assert : Position de spawn correcte
        # Pour PieceI, le pivot devrait être à (6, 3) avec spawn (7, 3)
        self.assertEqual(piece.position_pivot, Position(6, 3))
        
        # Vérifier qu'au moins une position contient le spawn
        positions_x = [pos.x for pos in piece.positions]
        self.assertIn(7, positions_x)
    
    def test_fabrique_peut_creer_piece_aleatoire(self):
        """
        Test : La fabrique peut créer une pièce aléatoire.
        
        Essentiel pour le gameplay Tetris.
        """
        # Act : Créer plusieurs pièces aléatoires
        pieces = [self.fabrique.creer_aleatoire() for _ in range(10)]
        
        # Assert : Toutes sont des instances valides
        for piece in pieces:
            self.assertIn(piece.type_piece, [TypePiece.I, TypePiece.O, TypePiece.T, TypePiece.S, TypePiece.Z, TypePiece.J, TypePiece.L])
            self.assertEqual(len(piece.positions), 4)
            self.assertIsNotNone(piece.position_pivot)
        
        # Assert : On devrait avoir de la variété (probabiliste)
        # Note : Test probabiliste, peut échouer 1 fois sur des millions
        types_obtenus = {piece.type_piece for piece in pieces}
        self.assertGreater(len(types_obtenus), 1, 
                          "Devrait avoir au moins 2 types différents en 10 essais")
    
    def test_fabrique_utilise_position_spawn_par_defaut(self):
        """
        Test : La fabrique utilise une position de spawn par défaut sensée.
        
        Pour Tetris, la position par défaut devrait être au centre-haut.
        """
        # Act : Créer sans spécifier position
        piece = self.fabrique.creer(TypePiece.I)
        
        # Assert : Position par défaut (centre du plateau Tetris)
        # Tetris standard : largeur 10, spawn au centre = x=5
        self.assertEqual(piece.position_pivot, Position(4, 0))  # PieceI pivot


if __name__ == '__main__':
    unittest.main()
