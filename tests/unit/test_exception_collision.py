"""
Tests unitaires pour ExceptionCollision.
CONFORME AUX DIRECTIVES : Tests officiels dans tests/unit/
"""

import unittest
import sys
import os

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from domaine.exceptions.exception_collision import ExceptionCollision
from domaine.entites.plateau import Plateau
from domaine.entites.fabriques.fabrique_pieces import FabriquePieces
from domaine.entites.position import Position


class TestExceptionCollision(unittest.TestCase):
    """Tests unitaires pour la classe ExceptionCollision."""
    
    def test_creation_exception_avec_message_defaut(self):
        """Test que ExceptionCollision peut être créée avec message par défaut."""
        exc = ExceptionCollision()
        self.assertEqual(str(exc), "Collision détectée")
        self.assertEqual(exc.message, "Collision détectée")
    
    def test_creation_exception_avec_message_personnalise(self):
        """Test que ExceptionCollision peut être créée avec message personnalisé."""
        message = "Collision spécifique détectée"
        exc = ExceptionCollision(message)
        self.assertEqual(str(exc), message)
        self.assertEqual(exc.message, message)
    
    def test_exception_herite_de_exception(self):
        """Test que ExceptionCollision hérite bien de Exception."""
        exc = ExceptionCollision()
        self.assertIsInstance(exc, Exception)
    
    def test_plateau_leve_exception_collision(self):
        """Test que Plateau lève ExceptionCollision lors de collisions."""
        # Créer un petit plateau
        plateau = Plateau(3, 3)
        
        # Créer une pièce valide  
        fabrique = FabriquePieces()
        piece = fabrique.creer_aleatoire()
        
        # Forcer collision en plaçant à une position impossible
        piece.position = Position(10, 10)  # Hors limites
        
        # Vérifier que ExceptionCollision est levée
        with self.assertRaises(ExceptionCollision) as context:
            plateau.placer_piece(piece)
        
        # Vérifier le message d'erreur
        self.assertEqual(str(context.exception), "Impossible de placer la pièce à cette position")
    
    def test_plateau_ne_leve_pas_exception_si_placement_valide(self):
        """Test que Plateau ne lève pas d'exception si placement valide."""
        # Créer un plateau suffisamment grand
        plateau = Plateau(10, 20)
        
        # Créer une pièce 
        fabrique = FabriquePieces()
        piece = fabrique.creer_aleatoire()
        
        # Position valide (au centre)
        piece.position = Position(5, 5)
        
        # Ne doit pas lever d'exception
        try:
            plateau.placer_piece(piece)
        except ExceptionCollision:
            self.fail("ExceptionCollision levée pour un placement valide")
    
    def test_message_exception_francais(self):
        """Test que les messages d'exception sont en français."""
        exc = ExceptionCollision("Collision détectée lors du placement")
        message = str(exc)
        
        # Vérifier que le message contient des mots français
        self.assertIn("détectée", message)
        self.assertIn("placement", message)
        # Le mot "collision" est acceptable en français
        self.assertIn("collision", message.lower())
        # Vérifier qu'il n'y a pas de mots anglais courants
        self.assertNotIn("detected", message.lower())
        self.assertNotIn("error", message.lower())


if __name__ == '__main__':
    unittest.main()
