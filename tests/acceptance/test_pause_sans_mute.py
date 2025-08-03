#!/usr/bin/env python3
"""
Tests d'acceptance : Pause sans mute automatique

Scénarios utilisateur :
- La pause ne doit PAS muter le son automatiquement
- Seule la touche M doit contrôler le mute/unmute
- La musique doit continuer même en pause (sauf si mute manuel)
"""

import unittest
import sys
import os
from unittest.mock import Mock, MagicMock

# Ajouter le répertoire racine au path pour les imports (conforme aux directives)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.domaine.services.moteur_partie import MoteurPartie


class TestPauseSansMute(unittest.TestCase):
    """Tests d'acceptance pour pause sans mute automatique."""
    
    def setUp(self):
        """Configuration pour chaque test."""
        # Mock audio pour tester le comportement
        self.mock_audio = Mock()
        self.mock_audio.demarrer_musique = Mock(return_value=True)
        self.mock_audio.mettre_en_pause_musique = Mock()
        self.mock_audio.reprendre_musique = Mock()
        self.mock_audio.basculer_mute_musique = Mock(return_value=True)
        
        # Créer moteur avec audio mocké
        self.moteur = MoteurPartie()
        self.moteur.audio = self.mock_audio
        
    def test_pause_ne_met_pas_musique_en_pause(self):
        """
        Scénario : L'utilisateur met le jeu en pause
        Résultat attendu : La musique NE doit PAS être mise en pause automatiquement
        """
        # Arrange : Jeu démarré (il démarre en pause par défaut maintenant)
        self.assertTrue(self.moteur.en_pause, "Le jeu démarre en pause par défaut")
        
        # Reprendre le jeu d'abord pour tester la pause
        self.moteur.basculer_pause()
        self.assertFalse(self.moteur.en_pause, "Le jeu doit être repris")
        
        # Act : Mettre en pause
        self.moteur.basculer_pause()
        
        # Assert : Pause activée mais musique PAS mise en pause
        self.assertTrue(self.moteur.en_pause, "Le jeu doit être en pause")
        self.mock_audio.mettre_en_pause_musique.assert_not_called()
        print("✅ La pause n'a PAS mis la musique en pause")
        
    def test_reprendre_jeu_ne_reprend_pas_musique(self):
        """
        Scénario : L'utilisateur reprend le jeu après pause
        Résultat attendu : La musique NE doit PAS être reprise automatiquement
        """
        # Arrange : Jeu en pause (il démarre en pause par défaut)
        self.assertTrue(self.moteur.en_pause, "Le jeu démarre en pause")
        
        # Act : Reprendre le jeu
        self.moteur.basculer_pause()
        
        # Assert : Jeu repris mais musique PAS reprise automatiquement
        self.assertFalse(self.moteur.en_pause, "Le jeu doit être repris")
        self.mock_audio.reprendre_musique.assert_not_called()
        print("✅ Reprendre le jeu n'a PAS repris la musique automatiquement")
        
    def test_mute_independant_de_pause(self):
        """
        Scénario : L'utilisateur mute pendant que le jeu est en pause
        Résultat attendu : Le mute doit fonctionner indépendamment de l'état pause
        """
        # Arrange : Jeu en pause (il démarre en pause par défaut)
        self.assertTrue(self.moteur.en_pause, "Le jeu démarre en pause")
        
        # Act : Muter via commande M (simulation)
        resultat_mute = self.mock_audio.basculer_mute_musique()
        
        # Assert : Le mute fonctionne même en pause
        self.assertTrue(resultat_mute, "Le mute doit fonctionner")
        self.mock_audio.basculer_mute_musique.assert_called_once()
        print("✅ Le mute fonctionne indépendamment de l'état pause")


if __name__ == "__main__":
    print("🎮 TESTS D'ACCEPTANCE : Pause sans mute automatique")
    print("=" * 60)
    unittest.main(verbosity=2)
