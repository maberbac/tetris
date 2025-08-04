"""
Test TDD pour CommandeChuteRapide avec ExceptionCollision
Validation de la conformité aux directives de développement
"""

import unittest
import sys
import os

# Ajouter le répertoire racine du projet au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from src.domaine.services.commandes.commandes_base import CommandeChuteRapide
from src.domaine.exceptions.exception_collision import ExceptionCollision
from src.domaine.entites.pieces.piece_i import PieceI
from src.domaine.entites.plateau import Plateau


class MockMoteurJeu:
    """Mock du moteur de jeu pour les tests."""
    
    def __init__(self, piece, plateau):
        self.piece = piece
        self.plateau = plateau
        self.piece_placee = False
        self.nouvelle_piece_generee = False
    
    def obtenir_piece_active(self):
        return self.piece
    
    def obtenir_plateau(self):
        return self.plateau
    
    def placer_piece_definitivement(self):
        self.piece_placee = True
    
    def generer_nouvelle_piece(self):
        self.nouvelle_piece_generee = True


class TestCommandeChuteRapideExceptionCollision(unittest.TestCase):
    """Tests TDD pour CommandeChuteRapide avec ExceptionCollision."""
    
    def setUp(self):
        """Initialisation pour chaque test."""
        self.commande = CommandeChuteRapide()
    
    def test_chute_rapide_piece_bloquee_leve_exception_collision(self):
        """Test TDD: CommandeChuteRapide lève ExceptionCollision si pièce complètement bloquée."""
        # Arrange - Créer une pièce qui ne peut absolument pas descendre
        piece = PieceI.creer(x_pivot=5, y_pivot=17)  # Position en y=16
        plateau = Plateau(largeur=10, hauteur=20)
        
        # Bloquer la ligne directement en dessous (y=17) pour empêcher la descente
        from src.domaine.entites.position import Position
        for x in range(10):
            plateau._positions_occupees.add(Position(x, 17))  # Bloquer la ligne où la pièce essaie d'aller
        
        moteur = MockMoteurJeu(piece, plateau)
        
        # Act & Assert - La commande doit lever ExceptionCollision
        with self.assertRaises(ExceptionCollision) as context:
            self.commande.execute(moteur)
        
        # Vérifier le message d'erreur
        self.assertIn("Impossible d'effectuer une chute rapide", str(context.exception))
        self.assertIn("pièce bloquée", str(context.exception))
    
    def test_chute_rapide_normale_ne_leve_pas_exception(self):
        """Test TDD: CommandeChuteRapide normale ne lève pas ExceptionCollision."""
        # Arrange - Créer une pièce qui peut descendre normalement
        piece = PieceI.creer(x_pivot=5, y_pivot=0)
        plateau = Plateau(largeur=10, hauteur=20)  # Plateau vide
        
        moteur = MockMoteurJeu(piece, plateau)
        
        # Act - Exécuter la commande
        try:
            resultat = self.commande.execute(moteur)
            # Assert - Doit réussir sans exception
            self.assertTrue(resultat)
            self.assertTrue(moteur.piece_placee)
            self.assertTrue(moteur.nouvelle_piece_generee)
        except ExceptionCollision:
            self.fail("CommandeChuteRapide ne devrait pas lever ExceptionCollision pour une chute normale")


if __name__ == '__main__':
    print("🧪 Tests TDD CommandeChuteRapide avec ExceptionCollision")
    print("=" * 60)
    unittest.main(verbosity=2)
