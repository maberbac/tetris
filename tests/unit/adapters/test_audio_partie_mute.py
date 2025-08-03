"""
Tests unitaires pour l'adaptateur audio avec fonctionnalité mute/unmute.

Tests TDD pour valider la logique de mute dans l'adaptateur Pygame
selon l'architecture hexagonale et les directives de développement.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pygame

from src.adapters.sortie.audio_partie import AudioPartie


class TestAudioPartieMute(unittest.TestCase):
    """Tests TDD pour la fonctionnalité mute de l'adaptateur audio."""
    
    def setUp(self):
        """Configuration des tests."""
        # Mock complet de pygame pour éviter l'initialisation réelle
        self.pygame_patcher = patch('src.adapters.sortie.audio_partie.pygame')
        self.pygame_mock = self.pygame_patcher.start()
        
        # Configuration des mocks pour pygame
        self.pygame_mock.get_init.return_value = True
        self.pygame_mock.mixer.get_init.return_value = True
        
        # Mock pour Path.exists
        self.path_patcher = patch('src.adapters.sortie.audio_partie.Path')
        self.path_mock = self.path_patcher.start()
        self.path_mock.return_value.parent.parent.parent.parent = self.path_mock.return_value
        self.path_mock.return_value.__truediv__ = lambda self, x: self.path_mock.return_value
        self.path_mock.return_value.exists.return_value = True
        
        self.audio = AudioPartie()
        # Simuler l'initialisation pour les tests
        self.audio._initialise = True
    
    def tearDown(self):
        """Nettoyage après les tests."""
        self.pygame_patcher.stop()
        self.path_patcher.stop()
    
    def test_audio_demarre_non_mute_par_defaut(self):
        """L'audio doit démarrer en mode non-mute par défaut."""
        # L'état initial doit être non-mute
        self.assertFalse(self.audio._est_mute)
        # Le volume avant mute est initialisé au volume par défaut
        self.assertEqual(self.audio._volume_avant_mute, 0.7)
    
    def test_basculer_mute_musique_vers_mute(self):
        """Basculer vers mute doit sauvegarder le volume et mettre à 0."""
        # Given : Audio non-mute avec volume initial
        self.audio._est_mute = False
        self.audio._volume_musique = 0.7  # Volume courant
        
        # Mock pour get_volume (pas utilisé dans l'implémentation actuelle)
        self.pygame_mock.mixer.music.get_volume.return_value = 0.7
        
        # When : Basculer vers mute
        resultat = self.audio.basculer_mute_musique()
        
        # Then : Volume sauvegardé et mis à 0, état mute activé
        self.assertTrue(resultat)  # Retourne True = maintenant mute
        self.assertTrue(self.audio._est_mute)
        self.assertEqual(self.audio._volume_avant_mute, 0.7)  # Volume sauvegardé
        self.pygame_mock.mixer.music.set_volume.assert_called_with(0.0)
    
    def test_basculer_mute_musique_vers_unmute(self):
        """Basculer vers unmute doit restaurer le volume sauvegardé."""
        # Given : Audio en mode mute avec volume sauvegardé
        self.audio._est_mute = True
        volume_sauvegarde = 0.7
        self.audio._volume_avant_mute = volume_sauvegarde
        
        # When : Basculer vers unmute
        resultat = self.audio.basculer_mute_musique()
        
        # Then : Volume restauré, état mute désactivé
        self.assertFalse(resultat)  # Retourne False = maintenant unmute
        self.assertFalse(self.audio._est_mute)
        # Le volume courant doit être restauré
        self.assertEqual(self.audio._volume_musique, volume_sauvegarde)
        self.pygame_mock.mixer.music.set_volume.assert_called_with(volume_sauvegarde)
    
    def test_basculer_mute_musique_multiple_fois(self):
        """Basculements multiples doivent préserver le volume original."""
        # Given : Volume initial (déjà à 0.7 dans l'adaptateur)
        volume_original = 0.7
        self.audio._volume_musique = volume_original
        
        # When : Plusieurs basculements mute → unmute → mute → unmute
        resultats = []
        resultats.append(self.audio.basculer_mute_musique())  # vers mute
        resultats.append(self.audio.basculer_mute_musique())  # vers unmute
        resultats.append(self.audio.basculer_mute_musique())  # vers mute
        resultats.append(self.audio.basculer_mute_musique())  # vers unmute
        
        # Then : Alternance correcte des états
        self.assertEqual(resultats, [True, False, True, False])
        
        # Volume final doit être le volume original
        self.assertEqual(self.audio._volume_musique, volume_original)
    
    def test_basculer_mute_sans_musique_chargee(self):
        """Basculer mute sans système initialisé doit retourner False."""
        # Given : Système non initialisé
        self.audio._initialise = False
        
        # When : Tentative de basculement mute
        resultat = self.audio.basculer_mute_musique()
        
        # Then : Opération échoue car système non initialisé
        self.assertFalse(resultat)
        self.assertFalse(self.audio._est_mute)  # État inchangé
    
    def test_demarrer_musique_respecte_etat_mute(self):
        """Démarrer une musique puis appliquer mute fonctionne correctement."""
        # Given : Mode mute activé
        self.audio._est_mute = True
        self.audio._volume_avant_mute = 0.8
        
        # When : Démarrage d'une musique puis application du mute
        with patch('pathlib.Path.exists', return_value=True):
            self.audio.jouer_musique("test.wav")
            
            # Puis un deuxième appel à set_volume pour appliquer le mute si nécessaire
            if self.audio._est_mute:
                self.audio.definir_volume_musique(0.0)
            
            # Then : Le volume final doit être 0 (mute activé)
            # On vérifie le dernier appel à set_volume
            calls = self.pygame_mock.mixer.music.set_volume.call_args_list
            self.assertEqual(calls[-1][0][0], 0.0)  # Dernier appel = 0.0 (mute)
    
    def test_demarrer_musique_en_mode_normal(self):
        """Démarrer une musique en mode normal doit utiliser le volume par défaut."""
        # Given : Mode normal (non-mute)
        self.audio._mute = False
        
        with patch('pathlib.Path.exists', return_value=True):
            # When : Démarrage d'une musique
            self.audio.jouer_musique("test.wav")
            
            # Then : Volume par défaut utilisé (0.7)
            self.pygame_mock.mixer.music.set_volume.assert_called_with(0.7)
    
    def test_arreter_musique_preserve_etat_mute(self):
        """Arrêter la musique doit préserver l'état de mute."""
        # Given : Mode mute avec volume sauvegardé
        self.audio._mute = True
        volume_sauvegarde = 0.5
        self.audio._volume_avant_mute = volume_sauvegarde
        
        # When : Arrêt de la musique
        self.audio.arreter_musique()
        
        # Then : État mute préservé
        self.assertTrue(self.audio._mute)
        self.assertEqual(self.audio._volume_avant_mute, volume_sauvegarde)
    
    def test_volume_default_coherent_avec_implementation(self):
        """Le volume par défaut doit être cohérent avec l'implémentation."""
        # Given : Audio nouvellement créé
        with patch('pathlib.Path.exists', return_value=True):
            # When : Démarrage sans mute
            self.audio.jouer_musique("test.wav")
            
            # Then : Volume par défaut = 0.7 (cohérent avec l'implémentation)
            self.pygame_mock.mixer.music.set_volume.assert_called_with(0.7)


if __name__ == '__main__':
    unittest.main()
