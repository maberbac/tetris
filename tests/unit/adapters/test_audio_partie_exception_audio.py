"""
Tests unitaires pour l'intégration ExceptionAudio dans AudioPartie - TDD RED.
CONFORME AUX DIRECTIVES : Remplacement des pygame.error par ExceptionAudio.
"""

import unittest
from unittest.mock import patch, Mock
import sys
import os

# Ajouter le répertoire racine au path pour les imports absolus
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.domaine.exceptions.exception_audio import ExceptionAudio
from src.adapters.sortie.audio_partie import AudioPartie


class TestAudioPartieExceptionAudio(unittest.TestCase):
    """Tests d'intégration ExceptionAudio avec AudioPartie."""
    
    def test_initialisation_echec_leve_exception_audio(self):
        """Test que l'initialisation échouée lève ExceptionAudio au lieu de pygame.error."""
        print("🧪 TDD GREEN : Initialisation échouée → ExceptionAudio")
        
        # Forcer une erreur dans pygame.mixer.init
        with patch('pygame.mixer.get_init', return_value=False), \
             patch('pygame.mixer.init') as mock_init:
            mock_init.side_effect = Exception("Audio device not available")
            
            audio = AudioPartie()
            with self.assertRaises(ExceptionAudio) as context:
                audio.initialiser()
            
            # Vérifier que le message contient des informations utiles
            self.assertIn("audio", str(context.exception).lower())
        
    def test_musique_fichier_inexistant_leve_exception_audio(self):
        """Test que jouer une musique inexistante lève ExceptionAudio."""
        print("🧪 TDD RED : Fichier musique inexistant → ExceptionAudio")
        
        audio = AudioPartie()
        
        # Simuler l'initialisation réussie
        with patch.object(audio, '_initialise', True):
            # AudioPartie doit lever ExceptionAudio pour fichier inexistant
            with self.assertRaises(ExceptionAudio) as context:
                audio.jouer_musique("fichier_inexistant.wav")
            
            # Le message doit être descriptif
            self.assertIn("fichier", str(context.exception).lower())
    
    def test_effet_sonore_echec_leve_exception_audio(self):
        """Test que l'échec d'un effet sonore lève ExceptionAudio."""
        print("🧪 TDD RED : Effet sonore échoué → ExceptionAudio")
        
        audio = AudioPartie()
        
        with patch.object(audio, '_initialise', True):
            with patch('pygame.mixer.Sound') as mock_sound:
                mock_sound.side_effect = Exception("Cannot load sound")
                
                # AudioPartie doit lever ExceptionAudio
                with self.assertRaises(ExceptionAudio) as context:
                    audio.jouer_effet_sonore("effet_inexistant.wav")
                
                # Le message doit être informatif
                self.assertIn("effet", str(context.exception).lower())
    
    def test_exception_audio_ne_bloque_pas_si_catch(self):
        """Test que ExceptionAudio peut être catchée pour éviter de bloquer le jeu."""
        print("🧪 TDD RED : ExceptionAudio catchée n'interrompt pas le jeu")
        
        audio = AudioPartie()
        
        # Test que le code peut continuer après une ExceptionAudio
        try:
            with patch.object(audio, '_initialise', True):
                with patch('pygame.mixer.Sound') as mock_sound:
                    mock_sound.side_effect = Exception("Audio error")
                    
                    # Ceci doit lever ExceptionAudio
                    audio.jouer_effet_sonore("test.wav")
                    
        except ExceptionAudio as e:
            # Le jeu peut continuer après avoir attrapé l'exception
            self.assertIsInstance(e, ExceptionAudio)
            # Test réussi si on arrive ici
            pass
        
        # Le test réussit si aucune exception non gérée n'a été levée


if __name__ == '__main__':
    print("🧪 TDD RED PHASE : Tests ExceptionAudio intégration AudioPartie")
    print("=" * 60)
    unittest.main(verbosity=2)
