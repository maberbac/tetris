"""
Test d'intégration pour la fonctionnalité restart (touche R)
Valide l'intégration complète entre commande, gestionnaire et moteur
"""

import unittest
from src.domaine.services.moteur_partie import MoteurPartie
from src.domaine.services.gestionnaire_evenements import GestionnaireEvenements, TypeEvenement


class TestIntegrationRestart(unittest.TestCase):
    """Test d'intégration pour la fonctionnalité restart"""

    def setUp(self):
        """Configuration des tests d'intégration"""
        self.moteur = MoteurPartie()
        self.gestionnaire = GestionnaireEvenements()

    def test_integration_complete_restart_apres_game_over(self):
        """
        Test d'intégration complet : touche R redémarre le jeu après game over
        """
        # Given : Moteur en game over avec statistiques modifiées
        self.moteur.jeu_termine = True
        self.moteur.stats.score = 1000
        self.moteur.stats.niveau = 3
        self.moteur.stats.lignes_completees = 25
        
        # Vérifier l'état initial
        self.assertTrue(self.moteur.est_game_over())
        
        # When : Traiter événement touche R
        succes = self.gestionnaire.traiter_evenement_clavier(
            "r", TypeEvenement.CLAVIER_APPUI, self.moteur
        )
        
        # Then : Jeu redémarré complètement
        self.assertTrue(succes)
        self.assertFalse(self.moteur.est_game_over())
        self.assertEqual(self.moteur.stats.score, 0)
        self.assertEqual(self.moteur.stats.niveau, 1)
        self.assertEqual(self.moteur.stats.lignes_completees, 0)
        self.assertTrue(self.moteur.en_pause)  # Redémarre en pause selon directives

    def test_integration_restart_ignore_si_pas_game_over(self):
        """
        Test d'intégration : touche R ignorée si pas en game over
        """
        # Given : Moteur PAS en game over
        self.moteur.jeu_termine = False
        self.moteur.en_pause = False
        score_initial = self.moteur.stats.score
        
        # When : Traiter événement touche R
        succes = self.gestionnaire.traiter_evenement_clavier(
            "r", TypeEvenement.CLAVIER_APPUI, self.moteur
        )
        
        # Then : Rien ne change
        self.assertFalse(succes)
        self.assertFalse(self.moteur.est_game_over())
        self.assertEqual(self.moteur.stats.score, score_initial)
        self.assertFalse(self.moteur.en_pause)

    def test_restart_initialise_pieces_correctement(self):
        """
        Test d'intégration : restart génère correctement les pièces
        """
        # Given : Moteur en game over
        self.moteur.jeu_termine = True
        
        # When : Restart
        self.gestionnaire.traiter_evenement_clavier(
            "r", TypeEvenement.CLAVIER_APPUI, self.moteur
        )
        
        # Then : Pièces initialisées
        self.assertIsNotNone(self.moteur.piece_active)
        self.assertIsNotNone(self.moteur.piece_suivante)


if __name__ == '__main__':
    unittest.main()
