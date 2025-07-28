"""
Tests pour la classe Position - Value Object

Position représente des coordonnées (x, y) dans le jeu Tetris.
C'est un Value Object : immutable, égalité par valeur.
"""

import unittest
import sys
import os

# Ajouter src au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

class TestPosition(unittest.TestCase):
    """Tests pour le Value Object Position."""
    
    def test_position_peut_etre_creee(self):
        """
        Test RED : Créer une position avec x et y.
        Ce test va échouer car Position n'existe pas encore.
        """
        from domaine.entites.position import Position
        
        position = Position(5, 10)
        
        self.assertEqual(position.x, 5)
        self.assertEqual(position.y, 10)
    
    def test_position_est_immutable(self):
        """
        Test : Les positions sont immutables (Value Object).
        """
        from domaine.entites.position import Position
        
        position = Position(3, 7)
        
        # Tenter de modifier devrait lever une exception
        with self.assertRaises(AttributeError):
            position.x = 10
    
    def test_egalite_positions(self):
        """
        Test : Deux positions avec mêmes coordonnées sont égales.
        """
        from domaine.entites.position import Position
        
        position1 = Position(2, 5)
        position2 = Position(2, 5)
        position3 = Position(3, 5)
        
        self.assertEqual(position1, position2)
        self.assertNotEqual(position1, position3)
    
    def test_position_peut_se_deplacer(self):
        """
        Test : Une position peut créer une nouvelle position déplacée.
        (Immutable - retourne une nouvelle instance)
        """
        from domaine.entites.position import Position
        
        position_originale = Position(5, 5)
        position_deplacee = position_originale.deplacer(2, -1)
        
        # Position originale inchangée
        self.assertEqual(position_originale.x, 5)
        self.assertEqual(position_originale.y, 5)
        
        # Nouvelle position créée
        self.assertEqual(position_deplacee.x, 7)
        self.assertEqual(position_deplacee.y, 4)
    
    def test_position_dans_limites(self):
        """
        Test : Vérifier si une position est dans des limites données.
        """
        from domaine.entites.position import Position
        
        position = Position(5, 8)
        
        self.assertTrue(position.dans_limites(10, 20))  # Dans les limites
        self.assertFalse(position.dans_limites(4, 20))  # x trop grand
        self.assertFalse(position.dans_limites(10, 7))  # y trop grand

if __name__ == '__main__':
    unittest.main()
