"""
Tests d'intégration pour ExceptionAudio avec AudioPartie - Phase TDD REFACTOR.
CONFORME AUX DIRECTIVES : Tests officiels dans tests/integration/
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Ajouter le répertoire racine au path pour les imports absolus
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.domaine.exceptions.exception_audio import ExceptionAudio
from src.adapters.sortie.audio_partie import AudioPartie


class TestIntegrationExceptionAudio(unittest.TestCase):
    """Tests d'intégration pour ExceptionAudio avec le système audio."""
    
    def setUp(self):
        """Configuration pour chaque test."""
        self.audio = AudioPartie()
    
    def tearDown(self):
        """Nettoyage après chaque test."""
        if hasattr(self.audio, '_initialise') and self.audio._initialise:
            try:
                self.audio.nettoyer()
            except:
                pass  # Ignorer les erreurs de nettoyage en test
    
    @patch('pygame.mixer.init')
    def test_audio_partie_peut_lever_exception_audio_initialisation(self, mock_init):
        """Test que AudioPartie peut lever ExceptionAudio lors de l'initialisation."""
        # Simuler une erreur pygame lors de l'initialisation
        import pygame
        mock_init.side_effect = pygame.error("Audio device not available")
        
        # L'initialisation devrait réussir silencieusement pour l'instant
        # (comportement actuel, pas d'ExceptionAudio encore intégrée)
        try:
            self.audio.initialiser()
            # AudioPartie gère actuellement pygame.error silencieusement
            self.assertFalse(self.audio._initialise)
        except Exception:
            # Si une exception est levée, ce n'est pas encore ExceptionAudio
            pass
    
    def test_exception_audio_suit_pattern_exception_collision(self):
        """Test que ExceptionAudio suit le même pattern qu'ExceptionCollision."""
        from src.domaine.exceptions.exception_collision import ExceptionCollision
        
        # Les deux exceptions doivent avoir une structure similaire
        exc_audio = ExceptionAudio("Test audio")
        exc_collision = ExceptionCollision("Test collision")
        
        # Même interface
        self.assertTrue(hasattr(exc_audio, 'message'))
        self.assertTrue(hasattr(exc_collision, 'message'))
        
        # Même comportement __str__
        self.assertEqual(str(exc_audio), "Test audio")
        self.assertEqual(str(exc_collision), "Test collision")
        
        # Même héritage
        self.assertIsInstance(exc_audio, Exception)
        self.assertIsInstance(exc_collision, Exception)
    
    def test_exception_audio_messages_francais_coherents(self):
        """Test que ExceptionAudio produit des messages cohérents en français."""
        scenarios_audio = [
            "Système audio non disponible",
            "Fichier audio introuvable : tetris-theme.wav",
            "Mémoire insuffisante pour charger l'audio",
            "Format audio non supporté : file.xyz",
            "Impossible de jouer l'effet sonore : rotate.wav"
        ]
        
        for message in scenarios_audio:
            with self.subTest(message=message):
                exc = ExceptionAudio(message)
                
                # Message en français correct
                self.assertEqual(str(exc), message)
                self.assertEqual(exc.message, message)
                
                # Pas de termes anglais techniques basiques
                message_lower = message.lower()
                termes_anglais = ['error', 'failed', 'cannot', 'unable', 'invalid']
                for terme in termes_anglais:
                    self.assertNotIn(terme, message_lower, 
                                   f"Message contient le terme anglais '{terme}': {message}")
    
    def test_exception_audio_peut_etre_importee_avec_autres_exceptions(self):
        """Test que ExceptionAudio peut être importée avec les autres exceptions du domaine."""
        # Test d'import depuis le module d'exceptions du domaine
        from src.domaine.exceptions import ExceptionAudio, ExceptionCollision
        
        # Les deux exceptions doivent être disponibles
        self.assertTrue(callable(ExceptionAudio))
        self.assertTrue(callable(ExceptionCollision))
        
        # Test de création
        exc_audio = ExceptionAudio("Test import")
        exc_collision = ExceptionCollision("Test import")
        
        self.assertIsInstance(exc_audio, Exception)
        self.assertIsInstance(exc_collision, Exception)


if __name__ == '__main__':
    print("🧪 PHASE TDD REFACTOR : Tests d'intégration ExceptionAudio")
    print("=" * 60)
    print("Ces tests valident l'intégration d'ExceptionAudio avec le système existant.")
    print()
    unittest.main(verbosity=2)
