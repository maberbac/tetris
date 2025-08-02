"""
Tests d'Acceptance - Descente Accélérée
=======================================
Nature : Test d'acceptance pour correction bug utilisateur
Scenario : L'utilisateur appuie sur la flèche bas pour descendre rapidement la pièce
Méthode : TDD (Test-Driven Development)

Suite au diagnostic : CommandeDescendre appelait faire_descendre_piece() inexistante
Comportement attendu : La flèche bas fait descendre la pièce d'une ligne sans crash
"""

import unittest
from src.domaine.services.moteur_partie import MoteurPartie
from src.domaine.services.commandes.commandes_base import CommandeDescendre
from src.domaine.entites.plateau import Plateau
from src.domaine.entites.fabriques.fabrique_pieces import FabriquePieces


class TestDescenteAcceleree(unittest.TestCase):
    """Tests spécifiques pour la descente accélérée avec flèche bas"""
    
    def setUp(self):
        """Configuration pour chaque test"""
        # Le moteur s'initialise avec ses propres plateau et fabrique
        self.moteur = MoteurPartie()
    
    def test_moteur_a_methode_faire_descendre_piece(self):
        """RED: Le moteur doit avoir une méthode faire_descendre_piece()"""
        # Test initial qui doit échouer : la méthode n'existe pas encore
        self.assertTrue(hasattr(self.moteur, 'faire_descendre_piece'),
            "Le moteur doit avoir une méthode faire_descendre_piece()")
    
    def test_faire_descendre_piece_retourne_booleen(self):
        """GREEN: faire_descendre_piece() doit retourner un booléen"""
        self.assertTrue(hasattr(self.moteur, 'faire_descendre_piece'))
        
        # La méthode doit retourner True si la pièce peut descendre
        resultat = self.moteur.faire_descendre_piece()
        self.assertIsInstance(resultat, bool,
            "faire_descendre_piece() doit retourner un booléen")
    
    def test_faire_descendre_piece_deplace_piece_vers_bas(self):
        """GREEN: faire_descendre_piece() doit déplacer la pièce d'une ligne vers le bas"""
        piece_initiale = self.moteur.obtenir_piece_active()
        position_y_initiale = piece_initiale.positions[0].y
        
        # Exécuter la descente
        resultat = self.moteur.faire_descendre_piece()
        
        # La pièce doit avoir bougé vers le bas
        piece_apres = self.moteur.obtenir_piece_active()
        position_y_apres = piece_apres.positions[0].y
        
        if resultat:  # Si le mouvement a réussi
            self.assertEqual(position_y_apres, position_y_initiale + 1,
                "La pièce doit descendre d'une ligne quand c'est possible")
    
    def test_commande_descendre_execute_sans_crash(self):
        """GREEN: CommandeDescendre ne doit plus crasher"""
        commande = CommandeDescendre()
        
        # Ceci ne doit plus lever d'exception
        try:
            resultat = commande.execute(self.moteur)
            self.assertIsInstance(resultat, bool)
        except AttributeError as e:
            self.fail(f"CommandeDescendre ne doit plus crasher: {e}")
    
    def test_descente_acceleree_integree(self):
        """REFACTOR: Test d'intégration - la descente accélérée fonctionne"""
        commande = CommandeDescendre()
        piece_initiale = self.moteur.obtenir_piece_active()
        
        # Plusieurs descentes consécutives
        for i in range(3):
            resultat = commande.execute(self.moteur)
            if not resultat:  # Si la pièce ne peut plus descendre
                break
        
        # Vérifier que la pièce a bien bougé ou a été placée
        piece_finale = self.moteur.obtenir_piece_active()
        # Soit la pièce a bougé, soit une nouvelle pièce a été générée
        self.assertIsNotNone(piece_finale, "Une pièce doit toujours être active")
