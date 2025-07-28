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


class TestRegistrePieces(unittest.TestCase):
    """Tests pour le Registry Pattern d'auto-enregistrement."""
    
    def test_pieces_sont_auto_enregistrees(self):
        """Test : Les pièces s'auto-enregistrent via le décorateur."""
        types_supportes = RegistrePieces.obtenir_types_supportes()
        
        # Vérifier que nos 4 pièces sont enregistrées
        self.assertIn(TypePiece.I, types_supportes)
        self.assertIn(TypePiece.O, types_supportes)
        self.assertIn(TypePiece.T, types_supportes)
        self.assertIn(TypePiece.S, types_supportes)  # ← Nouvelle pièce S
        
        # Au minimum 4 pièces maintenant
        self.assertGreaterEqual(len(types_supportes), 4)
    
    def test_registre_peut_obtenir_classes_pieces(self):
        """Test : Le registre peut retourner les bonnes classes."""
        classe_i = RegistrePieces.obtenir_classe_piece(TypePiece.I)
        classe_o = RegistrePieces.obtenir_classe_piece(TypePiece.O)
        classe_t = RegistrePieces.obtenir_classe_piece(TypePiece.T)
        classe_s = RegistrePieces.obtenir_classe_piece(TypePiece.S)
        
        self.assertEqual(classe_i, PieceI)
        self.assertEqual(classe_o, PieceO)
        self.assertEqual(classe_t, PieceT)
        self.assertEqual(classe_s, PieceS)
    
    def test_registre_refuse_type_non_supporte(self):
        """Test : Le registre refuse les types non supportés."""
        with self.assertRaises(ValueError) as context:
            RegistrePieces.obtenir_classe_piece(TypePiece.Z)  # Pas encore implémentée
        
        self.assertIn("Type de pièce non supporté", str(context.exception))
        self.assertIn("Z", str(context.exception))
    
    def test_statistiques_registre(self):
        """Test : Le registre peut donner des statistiques."""
        stats = RegistrePieces.statistiques()
        
        self.assertIn("Registre", stats)
        self.assertIn("pièces enregistrées", stats)
        self.assertIn("I", stats)
        self.assertIn("O", stats)
        self.assertIn("T", stats)


if __name__ == '__main__':
    unittest.main()
