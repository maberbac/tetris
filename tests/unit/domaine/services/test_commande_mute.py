"""
Tests pour la commande de basculement mute/unmute.

Tests TDD pour valider le bon fonctionnement de la nouvelle commande
de contrôle audio avec la touche M.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Ajouter le répertoire racine du projet au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from src.domaine.services.commandes.commandes_base import CommandeBasculerMute


class TestCommandeBasculerMute(unittest.TestCase):
    """Tests TDD pour la commande de basculement mute/unmute."""
    
    def setUp(self):
        """Configuration des tests."""
        self.moteur_mock = Mock()
        self.audio_mock = Mock()
        self.moteur_mock.obtenir_audio.return_value = self.audio_mock
        
        self.commande = CommandeBasculerMute()
    
    def test_commande_peut_etre_creee(self):
        """Une commande de basculement mute peut être créée."""
        commande = CommandeBasculerMute()
        self.assertIsNotNone(commande)
        self.assertIsInstance(commande, CommandeBasculerMute)
    
    def test_executer_appelle_basculer_mute_musique(self):
        """L'exécution de la commande doit appeler basculer_mute_musique sur l'audio."""
        # Arrange - Préparer le test
        # (setUp déjà fait)
        
        # Act - Exécuter l'action
        resultat = self.commande.execute(self.moteur_mock)
        
        # Assert - Vérifier le résultat
        self.assertTrue(resultat)
        self.moteur_mock.obtenir_audio.assert_called_once()
        self.audio_mock.basculer_mute_musique.assert_called_once()
    
    @patch('src.domaine.services.commandes.commandes_base.logger_tetris')
    def test_executer_affiche_message_mute(self, mock_logger):
        """L'exécution doit afficher un message de feedback utilisateur."""
        # Simuler que l'audio confirme le basculement vers mute
        self.audio_mock.basculer_mute_musique.return_value = True
        
        resultat = self.commande.execute(self.moteur_mock)
        
        self.assertTrue(resultat)
        # Vérifier que le logger a été appelé avec le bon message mute
        mock_logger.info.assert_called_with("🔇 Musique désactivée")
    
    @patch('src.domaine.services.commandes.commandes_base.logger_tetris')
    def test_executer_affiche_message_unmute(self, mock_logger):
        """L'exécution doit afficher un message de feedback pour unmute."""
        # Simuler que l'audio confirme le basculement vers unmute
        self.audio_mock.basculer_mute_musique.return_value = False
        
        resultat = self.commande.execute(self.moteur_mock)
        
        self.assertTrue(resultat)
        # Vérifier que le logger a été appelé avec le bon message unmute
        mock_logger.info.assert_called_with("🔊 Musique réactivée")
    
    @patch('src.domaine.services.commandes.commandes_base.logger_tetris')
    def test_executer_gere_echec_audio(self, mock_logger):
        """La commande doit gérer l'échec du système audio."""
        # Simuler un problème avec le système audio
        self.moteur_mock.obtenir_audio.side_effect = Exception("Audio indisponible")
        
        resultat = self.commande.execute(self.moteur_mock)
        
        # La commande doit retourner False en cas d'échec
        self.assertFalse(resultat)
        # Vérifier que le logger error a été appelé
        mock_logger.error.assert_called_with("❌ Erreur audio: Audio indisponible")
    
    def test_executer_gere_audio_none(self):
        """La commande doit gérer le cas où l'audio n'est pas disponible."""
        # Simuler l'absence de système audio
        self.moteur_mock.obtenir_audio.return_value = None
        
        resultat = self.commande.execute(self.moteur_mock)
        
        # La commande doit retourner False si pas d'audio
        self.assertFalse(resultat)
    
    @patch('src.domaine.services.commandes.commandes_base.logger_tetris')
    def test_executer_sans_audio_affiche_message_erreur(self, mock_logger):
        """Sans audio, un message d'information doit être affiché."""
        self.moteur_mock.obtenir_audio.return_value = None
        
        resultat = self.commande.execute(self.moteur_mock)
        
        self.assertFalse(resultat)
        # Vérifier que le logger a été appelé avec le bon message d'erreur
        mock_logger.warning.assert_called_with("❌ Audio non disponible")


if __name__ == '__main__':
    unittest.main()
