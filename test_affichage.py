"""
Tests pour l'affichage de base du jeu Tetris.
Premier test TDD : vérifier qu'on peut créer une fenêtre de jeu.
"""

import unittest
import pygame
import sys
import os

# Ajouter le répertoire parent au path pour importer nos modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAffichage(unittest.TestCase):
    """Tests pour le système d'affichage du jeu."""
    
    def setUp(self):
        """Configuration avant chaque test."""
        pygame.init()
    
    def tearDown(self):
        """Nettoyage après chaque test."""
        pygame.quit()
    
    def test_affichage_peut_etre_cree(self):
        """
        Test RED : Vérifier qu'on peut créer un objet Affichage.
        Ce test va échouer car la classe Affichage n'existe pas encore.
        """
        from affichage import Affichage
        
        affichage = Affichage()
        self.assertIsNotNone(affichage)
    
    def test_affichage_a_surface_ecran(self):
        """
        Test : Vérifier qu'Affichage crée une surface d'écran.
        """
        from affichage import Affichage
        
        affichage = Affichage()
        self.assertIsNotNone(affichage.ecran)
    
    def test_affichage_calcule_position_grille(self):
        """
        Test : Vérifier qu'Affichage calcule correctement la position de la grille.
        """
        from affichage import Affichage
        
        affichage = Affichage()
        
        # La grille doit être centrée
        # Grille : 300px × 600px (10×20 cellules de 30px)
        position_x_attendue = (affichage.largeur_ecran - 300) // 2
        position_y_attendue = (affichage.hauteur_ecran - 600) // 2
        
        self.assertEqual(affichage.position_grille_x, position_x_attendue)
        self.assertEqual(affichage.position_grille_y, position_y_attendue)

if __name__ == '__main__':
    unittest.main()
