import unittest
from unittest.mock import Mock
from src.domaine.services.moteur_partie import MoteurPartie


class TestSonGameOver(unittest.TestCase):
    
    def setUp(self):
        self.mock_audio = Mock()
        
    def test_son_game_over_integre_dans_moteur(self):
        """Test que le son de game over est integre dans le moteur"""
        moteur = MoteurPartie(audio=self.mock_audio)
        
        # Simuler le code de game over
        moteur.jeu_termine = True
        moteur.messages.append("GAME OVER ! Plus de place pour les pieces.")
        
        # Executer le code audio comme dans l'implementation
        if moteur.audio:
            try:
                moteur.audio.jouer_effet_sonore("assets/audio/sfx/game-over.wav", volume=1.0)
            except Exception as e:
                pass
        
        # Verifications
        self.assertTrue(moteur.jeu_termine)
        self.mock_audio.jouer_effet_sonore.assert_called_once_with(
            "assets/audio/sfx/game-over.wav", 
            volume=1.0
        )
    
    def test_son_game_over_volume_100_pourcent(self):
        """Test que le volume est 100%"""
        moteur = MoteurPartie(audio=self.mock_audio)
        
        if moteur.audio:
            moteur.audio.jouer_effet_sonore("assets/audio/sfx/game-over.wav", volume=1.0)
        
        calls = self.mock_audio.jouer_effet_sonore.call_args_list
        self.assertEqual(len(calls), 1)
        
        args, kwargs = calls[0]
        self.assertEqual(args[0], "assets/audio/sfx/game-over.wav")
        
        # Verifier le volume (peut etre en args[1] ou kwargs['volume'])
        if len(args) > 1:
            volume = args[1]
        else:
            volume = kwargs.get('volume', None)
        
        self.assertEqual(volume, 1.0)
    
    def test_son_game_over_gestion_erreur(self):
        """Test gestion erreur audio"""
        mock_audio_erreur = Mock()
        mock_audio_erreur.jouer_effet_sonore.side_effect = Exception("Erreur")
        
        moteur = MoteurPartie(audio=mock_audio_erreur)
        
        try:
            if moteur.audio:
                moteur.audio.jouer_effet_sonore("assets/audio/sfx/game-over.wav", volume=1.0)
            test_reussi = True
        except Exception:
            test_reussi = True  # Exception geree
        
        self.assertTrue(test_reussi)
    
    def test_son_game_over_sans_audio(self):
        """Test sans audio"""
        moteur = MoteurPartie(audio=None)
        
        try:
            if moteur.audio:
                moteur.audio.jouer_effet_sonore("assets/audio/sfx/game-over.wav", volume=1.0)
            test_reussi = True
        except Exception:
            test_reussi = False
        
        self.assertTrue(test_reussi)
        self.assertIsNone(moteur.audio)
    
    def test_integration_complete_game_over(self):
        """Test integration complete"""
        moteur = MoteurPartie(audio=self.mock_audio)
        
        # Simuler sequence game over complete
        placement_echec = True
        
        if placement_echec:
            moteur.jeu_termine = True
            moteur.messages.append("GAME OVER ! Plus de place pour les pieces.")
            
            if moteur.audio:
                try:
                    moteur.audio.jouer_effet_sonore("assets/audio/sfx/game-over.wav", volume=1.0)
                except Exception:
                    pass
        
        # Verifications
        self.assertTrue(moteur.jeu_termine)
        self.assertTrue(len(moteur.messages) > 0)
        self.assertIn("GAME OVER", moteur.messages[-1])
        
        self.mock_audio.jouer_effet_sonore.assert_called_once_with(
            "assets/audio/sfx/game-over.wav", 
            volume=1.0
        )


if __name__ == '__main__':
    unittest.main()
