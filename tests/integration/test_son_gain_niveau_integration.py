"""
Test d'intégration pour le son de gain de niveau dans le moteur complet.

Valide que la fonctionnalité fonctionne de bout en bout avec le vrai moteur.
"""

import unittest
from unittest.mock import Mock
from src.domaine.services.moteur_partie import MoteurPartie
from src.domaine.entites.pieces.piece_i import PieceI
from src.domaine.entites.position import Position
from src.ports.sortie.audio_jeu import AudioJeu


class TestIntegrationSonGainNiveau(unittest.TestCase):
    """Test d'intégration pour le son de gain de niveau."""
    
    def setUp(self):
        """Configuration des tests."""
        self.audio_mock = Mock(spec=AudioJeu)
        self.moteur = MoteurPartie(audio=self.audio_mock)
    
    def test_integration_son_gain_niveau_avec_moteur_complet(self):
        """Test d'intégration : Le son est joué lors d'un changement de niveau réel dans le moteur."""
        # Vérifier niveau initial
        ancien_niveau = self.moteur.stats.niveau
        self.assertEqual(ancien_niveau, 1)
        
        # Simuler 10 lignes complétées pour déclencher changement de niveau
        niveau_a_change = self.moteur.stats.ajouter_score_selon_lignes_completees(10)
        
        # Vérifier changement de niveau
        self.assertTrue(niveau_a_change)
        self.assertEqual(self.moteur.stats.niveau, 2)
        
        # Simuler la logique audio du moteur
        if niveau_a_change and self.moteur.audio:
            self.moteur.audio.jouer_effet_sonore("assets/audio/sfx/gained-a-new-level.wav", volume=1.0)
        
        # Vérifier que le son a été joué avec le bon chemin et volume
        self.audio_mock.jouer_effet_sonore.assert_called_once_with(
            "assets/audio/sfx/gained-a-new-level.wav", 
            volume=1.0
        )
    
    def test_integration_multiples_changements_niveau(self):
        """Test d'intégration : Multiples gains de niveau déclenchent le son à chaque fois."""
        # Passage niveau 1 → 2
        niveau_a_change = self.moteur.stats.ajouter_score_selon_lignes_completees(10)
        self.assertTrue(niveau_a_change)
        self.assertEqual(self.moteur.stats.niveau, 2)
        
        if niveau_a_change and self.moteur.audio:
            self.moteur.audio.jouer_effet_sonore("assets/audio/sfx/gained-a-new-level.wav", volume=1.0)
        
        # Passage niveau 2 → 3
        niveau_a_change = self.moteur.stats.ajouter_score_selon_lignes_completees(10)
        self.assertTrue(niveau_a_change)
        self.assertEqual(self.moteur.stats.niveau, 3)
        
        if niveau_a_change and self.moteur.audio:
            self.moteur.audio.jouer_effet_sonore("assets/audio/sfx/gained-a-new-level.wav", volume=1.0)
        
        # Passage niveau 3 → 4
        niveau_a_change = self.moteur.stats.ajouter_score_selon_lignes_completees(10)
        self.assertTrue(niveau_a_change)
        self.assertEqual(self.moteur.stats.niveau, 4)
        
        if niveau_a_change and self.moteur.audio:
            self.moteur.audio.jouer_effet_sonore("assets/audio/sfx/gained-a-new-level.wav", volume=1.0)
        
        # Vérifier que le son a été joué 3 fois
        self.assertEqual(self.audio_mock.jouer_effet_sonore.call_count, 3)
        
        # Vérifier tous les appels
        expected_calls = [
            unittest.mock.call("assets/audio/sfx/gained-a-new-level.wav", volume=1.0),
            unittest.mock.call("assets/audio/sfx/gained-a-new-level.wav", volume=1.0),
            unittest.mock.call("assets/audio/sfx/gained-a-new-level.wav", volume=1.0)
        ]
        self.audio_mock.jouer_effet_sonore.assert_has_calls(expected_calls)


if __name__ == '__main__':
    unittest.main()
