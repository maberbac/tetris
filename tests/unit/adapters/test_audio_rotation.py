"""
Tests unitaires pour les effets sonores de rotation avec système mute/unmute.

Test du respect de l'interface AudioJeu et du comportement mute.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from src.adapters.sortie.audio_partie import AudioPartie


class TestAudioRotation(unittest.TestCase):
    """Tests pour les effets sonores de rotation."""
    
    def setUp(self):
        """Configuration pour chaque test."""
        self.audio = AudioPartie()
    
    def test_jouer_effet_sonore_avec_volume_correct(self):
        """Un effet sonore doit respecter le volume spécifié."""
        with patch('pygame.mixer.Sound') as mock_sound_class:
            mock_sound = Mock()
            mock_sound_class.return_value = mock_sound
            
            # Mock du système audio initialisé
            self.audio._initialise = True
            self.audio._est_mute = False
            
            # Jouer l'effet avec volume spécifique
            resultat = self.audio.jouer_effet_sonore("assets/audio/sfx/rotate.wav", volume=1.0)
            
            # Vérifications
            self.assertTrue(resultat)
            mock_sound.set_volume.assert_called_once_with(1.0)
            mock_sound.play.assert_called_once()
    
    def test_jouer_effet_sonore_respecte_mute(self):
        """Un effet sonore doit être muté si le système est en mode mute."""
        with patch('pygame.mixer.Sound') as mock_sound_class:
            mock_sound = Mock()
            mock_sound_class.return_value = mock_sound
            
            # Mock du système audio initialisé et muté
            self.audio._initialise = True
            self.audio._est_mute = True
            
            # Jouer l'effet
            resultat = self.audio.jouer_effet_sonore("assets/audio/sfx/rotate.wav", volume=1.0)
            
            # Vérifications : volume doit être 0.0 quand muté
            self.assertTrue(resultat)
            mock_sound.set_volume.assert_called_once_with(0.0)
            mock_sound.play.assert_called_once()
    
    def test_jouer_effet_sonore_respecte_unmute(self):
        """Un effet sonore doit utiliser le bon volume quand non-muté."""
        with patch('pygame.mixer.Sound') as mock_sound_class:
            mock_sound = Mock()
            mock_sound_class.return_value = mock_sound
            
            # Mock du système audio initialisé et non-muté
            self.audio._initialise = True
            self.audio._est_mute = False
            
            # Jouer l'effet
            resultat = self.audio.jouer_effet_sonore("assets/audio/sfx/rotate.wav", volume=1.0)
            
            # Vérifications : volume doit être respecté
            self.assertTrue(resultat)
            mock_sound.set_volume.assert_called_once_with(1.0)
            mock_sound.play.assert_called_once()
    
    def test_jouer_effet_sonore_gere_fichier_inexistant(self):
        """L'effet sonore doit gérer gracieusement les fichiers inexistants."""
        from src.domaine.exceptions.exception_audio import ExceptionAudio
        
        self.audio._initialise = True
        
        # Tenter de jouer un fichier inexistant doit lever ExceptionAudio
        with self.assertRaises(ExceptionAudio):
            self.audio.jouer_effet_sonore("fichier_inexistant.wav")
    
    def test_jouer_effet_sonore_initialise_automatiquement(self):
        """L'effet sonore doit initialiser automatiquement le système si nécessaire."""
        from src.domaine.exceptions.exception_audio import ExceptionAudio
        
        with patch.object(self.audio, 'initialiser') as mock_init:
            mock_init.return_value = None
            self.audio._initialise = False
            
            # Sans initialisation doit lever ExceptionAudio
            with self.assertRaises(ExceptionAudio):
                self.audio.jouer_effet_sonore("assets/audio/sfx/rotate.wav")


if __name__ == '__main__':
    unittest.main()
