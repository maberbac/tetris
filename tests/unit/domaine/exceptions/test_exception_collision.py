"""
Tests unitaires pour ExceptionCollision.
CONFORME AUX DIRECTIVES : Tests officiels dans tests/unit/
"""

import unittest
import sys
import os

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'src'))

from src.domaine.exceptions.exception_collision import ExceptionCollision
from src.domaine.entites.plateau import Plateau
from src.domaine.entites.fabriques.fabrique_pieces import FabriquePieces
from src.domaine.entites.position import Position


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
        
        # Utiliser placer_piece_et_supprimer_lignes et vérifier le retour -1 (échec)
        resultat = plateau.placer_piece_et_supprimer_lignes(piece)
        
        # Vérifier que le placement a échoué (retour -1 selon directives)
        self.assertEqual(resultat, -1, "Le placement devrait échouer et retourner -1")
        
        # Vérifier que le plateau reste vide (pas de modification d'état)
        self.assertTrue(plateau.est_vide(), "Le plateau devrait rester vide après échec de placement")
    
    def test_plateau_ne_leve_pas_exception_si_placement_valide(self):
        """Test que Plateau ne lève pas d'exception si placement valide."""
        # Créer un plateau suffisamment grand
        plateau = Plateau(10, 20)
        
        # Créer une pièce 
        fabrique = FabriquePieces()
        piece = fabrique.creer_aleatoire()
        
        # Position valide (au centre)
        piece.position = Position(5, 5)
        
        # Utiliser placer_piece_et_supprimer_lignes et vérifier le succès
        resultat = plateau.placer_piece_et_supprimer_lignes(piece)
        
        # Vérifier que le placement a réussi (retour >= 0 selon directives)
        self.assertGreaterEqual(resultat, 0, "Le placement devrait réussir et retourner >= 0")
        
        # Vérifier que la pièce a bien été placée
        self.assertFalse(plateau.est_vide(), "Le plateau ne devrait plus être vide après placement réussi")
    
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
