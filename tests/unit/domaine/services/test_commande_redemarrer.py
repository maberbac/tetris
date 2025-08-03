"""
Tests unitaires pour CommandeRedemarrer - Fonctionnalité restart avec touche R
Architecture : Command Pattern + TDD strict
"""

import unittest
from unittest.mock import Mock, MagicMock

from src.domaine.services.commandes.commande_redemarrer import CommandeRedemarrer
from src.domaine.services.moteur_partie import MoteurPartie


class TestCommandeRedemarrer(unittest.TestCase):
    """Tests unitaires pour CommandeRedemarrer selon directives TDD"""

    def setUp(self):
        """Configuration des tests selon directives TDD"""
        self.commande = CommandeRedemarrer()
        self.moteur_mock = Mock()  # Mock générique plutôt que spec

    def test_commande_redemarrer_peut_etre_creee(self):
        """RED: CommandeRedemarrer doit pouvoir être créée"""
        # Given : Rien de spécial
        # When : Création de la commande
        commande = CommandeRedemarrer()
        # Then : La commande existe
        self.assertIsNotNone(commande)

    def test_redemarrer_si_game_over_reinitialise_moteur(self):
        """RED: Si game over, R doit redémarrer le moteur"""
        # Given : Moteur en état game over
        self.moteur_mock.est_game_over.return_value = True
        self.moteur_mock.redemarrer_partie = Mock()
        
        # When : Exécution commande restart
        resultat = self.commande.execute(self.moteur_mock)
        
        # Then : Moteur redémarré
        self.moteur_mock.redemarrer_partie.assert_called_once()
        self.assertTrue(resultat)  # Succès

    def test_redemarrer_si_pas_game_over_ne_fait_rien(self):
        """RED: Si pas game over, R ne doit rien faire"""
        # Given : Moteur PAS en game over
        self.moteur_mock.est_game_over.return_value = False
        self.moteur_mock.redemarrer_partie = Mock()
        
        # When : Exécution commande restart
        resultat = self.commande.execute(self.moteur_mock)
        
        # Then : Rien ne se passe
        self.moteur_mock.redemarrer_partie.assert_not_called()
        self.assertFalse(resultat)  # Ignoré

    def test_redemarrer_reinitialise_score_niveau_plateau(self):
        """RED: Redémarrer doit réinitialiser score, niveau, plateau"""
        # Given : Moteur en game over avec redemarrer_partie mockée
        self.moteur_mock.est_game_over.return_value = True
        self.moteur_mock.redemarrer_partie = Mock()
        
        # When : Redémarrage
        self.commande.execute(self.moteur_mock)
        
        # Then : redemarrer_partie appelé (détails testés dans moteur)
        self.moteur_mock.redemarrer_partie.assert_called_once()

    def test_moteur_a_methode_redemarrer_partie(self):
        """RED: MoteurPartie doit avoir une méthode redemarrer_partie()"""
        # Given : Un vrai moteur de partie
        from src.domaine.services.moteur_partie import MoteurPartie
        
        moteur = MoteurPartie()
        
        # When/Then : La méthode doit exister
        self.assertTrue(hasattr(moteur, 'redemarrer_partie'))
        self.assertTrue(callable(getattr(moteur, 'redemarrer_partie')))
        self.assertTrue(hasattr(moteur, 'est_game_over'))
        self.assertTrue(callable(getattr(moteur, 'est_game_over')))


if __name__ == '__main__':
    unittest.main()
