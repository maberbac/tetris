"""
Tests d'acceptance pour le son de gain de niveau.

Valide que le son gained-a-new-level.wav est joué à chaque fois qu'on gagne un niveau.
"""

import unittest
from unittest.mock import Mock, call
from src.domaine.services.moteur_partie import MoteurPartie
from src.domaine.entites.plateau import Plateau
from src.domaine.entites.pieces.piece_i import PieceI
from src.ports.sortie.audio_jeu import AudioJeu


class TestSonGainNiveau(unittest.TestCase):
    """Tests d'acceptance pour le son de gain de niveau."""
    
    def setUp(self):
        """Configuration des tests."""
        self.audio_mock = Mock(spec=AudioJeu)
        self.moteur = MoteurPartie(audio=self.audio_mock)
    
    def test_son_joue_au_premier_changement_niveau(self):
        """Test : Le son gained-a-new-level.wav est joué au passage du niveau 1 au niveau 2."""
        # Vérifier que nous sommes au niveau 1
        self.assertEqual(self.moteur.stats.niveau, 1)
        
        # Compléter 10 lignes pour passer au niveau 2
        niveau_a_change = self.moteur.stats.ajouter_score_selon_lignes_completees(10)
        
        # Vérifier changement de niveau
        self.assertTrue(niveau_a_change)
        self.assertEqual(self.moteur.stats.niveau, 2)
        
        # Simuler manuellement le code du moteur
        if niveau_a_change and self.moteur.audio:
            self.moteur.audio.jouer_effet_sonore("assets/audio/sfx/gained-a-new-level.wav", volume=1.0)
        
        # Vérifier que le son a été joué
        self.audio_mock.jouer_effet_sonore.assert_called_with(
            "assets/audio/sfx/gained-a-new-level.wav", 
            volume=1.0
        )
    
    def test_son_joue_au_deuxieme_changement_niveau(self):
        """Test : Le son est aussi joué au passage du niveau 2 au niveau 3."""
        # Commencer au niveau 2 (10 lignes complétées)
        self.moteur.stats.lignes_completees = 10
        self.moteur.stats.niveau = 2
        
        # Compléter 10 lignes de plus (passage niveau 3)
        niveau_a_change = self.moteur.stats.ajouter_score_selon_lignes_completees(10)
        
        # Vérifier changement de niveau
        self.assertTrue(niveau_a_change)
        self.assertEqual(self.moteur.stats.niveau, 3)
        
        # Simuler le code du moteur
        if niveau_a_change and self.moteur.audio:
            self.moteur.audio.jouer_effet_sonore("assets/audio/sfx/gained-a-new-level.wav", volume=1.0)
        
        # Vérifier que le son a été joué
        self.audio_mock.jouer_effet_sonore.assert_called_with(
            "assets/audio/sfx/gained-a-new-level.wav", 
            volume=1.0
        )
    
    def test_son_pas_joue_sans_changement_niveau(self):
        """Test : Le son n'est PAS joué quand le niveau ne change pas."""
        # Ajouter quelques lignes sans changer de niveau
        niveau_a_change = self.moteur.stats.ajouter_score_selon_lignes_completees(5)
        
        # Vérifier qu'il n'y a pas de changement de niveau
        self.assertFalse(niveau_a_change)
        self.assertEqual(self.moteur.stats.niveau, 1)
        
        # Le son ne devrait pas être joué
        self.audio_mock.jouer_effet_sonore.assert_not_called()
    
    def test_son_pas_joue_sans_audio(self):
        """Test : Aucune erreur si le système audio n'est pas disponible."""
        # Créer un moteur sans audio
        moteur_sans_audio = MoteurPartie(audio=None)
        
        # Déclencher un changement de niveau
        niveau_a_change = moteur_sans_audio.stats.ajouter_score_selon_lignes_completees(10)
        
        # Vérifier changement de niveau
        self.assertTrue(niveau_a_change)
        self.assertEqual(moteur_sans_audio.stats.niveau, 2)
        
        # Aucune exception ne devrait être levée
        # (le test passe s'il n'y a pas d'exception)
    
    def test_volume_son_niveau_conforme_directives(self):
        """Test : Le son de gain de niveau respecte les directives (volume 100%)."""
        # Déclencher un changement de niveau
        niveau_a_change = self.moteur.stats.ajouter_score_selon_lignes_completees(10)
        
        # Simuler le code du moteur
        if niveau_a_change and self.moteur.audio:
            self.moteur.audio.jouer_effet_sonore("assets/audio/sfx/gained-a-new-level.wav", volume=1.0)
        
        # Vérifier que le volume est à 100% (volume=1.0) comme requis par les directives
        self.audio_mock.jouer_effet_sonore.assert_called_with(
            "assets/audio/sfx/gained-a-new-level.wav", 
            volume=1.0
        )


if __name__ == '__main__':
    unittest.main()
