"""
Tests pour le RegistrePieces - Registry Pattern.

Vérifie que l'auto-enregistrement des pièces fonctionne correctement.
"""

import unittest
from src.domaine.entites.piece import TypePiece
from src.domaine.entites.fabriques.registre_pieces import RegistrePieces
from src.domaine.entites.pieces.piece_i import PieceI
from src.domaine.entites.pieces.piece_o import PieceO
from src.domaine.entites.pieces.piece_t import PieceT
from src.domaine.entites.pieces.piece_s import PieceS
from src.domaine.entites.pieces.piece_z import PieceZ
from src.domaine.entites.pieces.piece_j import PieceJ
from src.domaine.entites.pieces.piece_l import PieceL


class TestRegistrePieces(unittest.TestCase):
    """Tests pour le Registry Pattern d'auto-enregistrement."""
    
    def test_pieces_sont_auto_enregistrees(self):
        """Test : Les pièces s'auto-enregistrent via le décorateur."""
        types_supportes = RegistrePieces.obtenir_types_supportes()
        
        # Vérifier que nos 7 pièces sont enregistrées
        self.assertIn(TypePiece.I, types_supportes)
        self.assertIn(TypePiece.O, types_supportes)
        self.assertIn(TypePiece.T, types_supportes)
        self.assertIn(TypePiece.S, types_supportes)
        self.assertIn(TypePiece.Z, types_supportes)
        self.assertIn(TypePiece.J, types_supportes)
        self.assertIn(TypePiece.L, types_supportes)
        
        # Exactement 7 pièces maintenant
        self.assertEqual(len(types_supportes), 7)
    
    def test_registre_peut_obtenir_classes_pieces(self):
        """Test : Le registre peut retourner les bonnes classes."""
        classe_i = RegistrePieces.obtenir_classe_piece(TypePiece.I)
        classe_o = RegistrePieces.obtenir_classe_piece(TypePiece.O)
        classe_t = RegistrePieces.obtenir_classe_piece(TypePiece.T)
        classe_s = RegistrePieces.obtenir_classe_piece(TypePiece.S)
        classe_z = RegistrePieces.obtenir_classe_piece(TypePiece.Z)
        classe_j = RegistrePieces.obtenir_classe_piece(TypePiece.J)
        classe_l = RegistrePieces.obtenir_classe_piece(TypePiece.L)
        
        self.assertEqual(classe_i, PieceI)
        self.assertEqual(classe_o, PieceO)
        self.assertEqual(classe_t, PieceT)
        self.assertEqual(classe_s, PieceS)
        self.assertEqual(classe_z, PieceZ)
        self.assertEqual(classe_j, PieceJ)
        self.assertEqual(classe_l, PieceL)
    
    def test_registre_refuse_type_non_supporte(self):
        """Test : Le registre refuse les types non supportés."""
        from enum import Enum
        
        # Simule un type inexistant
        class FakeType(Enum):
            INCONNU = "inconnu"
        
        with self.assertRaises(ValueError) as context:
            RegistrePieces.obtenir_classe_piece(FakeType.INCONNU)  # Type vraiment inexistant
        
        self.assertIn("Type de pièce non supporté", str(context.exception))
    
    def test_statistiques_registre(self):
        """Test : Le registre peut donner des statistiques."""
        stats = RegistrePieces.statistiques()
        
        self.assertIn("Registre", stats)
        self.assertIn("pièces enregistrées", stats)
        self.assertIn("I", stats)
        self.assertIn("O", stats)
        self.assertIn("T", stats)
        self.assertIn("S", stats)
        self.assertIn("Z", stats)
        self.assertIn("J", stats)
        self.assertIn("L", stats)


if __name__ == '__main__':
    unittest.main()
