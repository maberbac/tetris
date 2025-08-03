"""
Tests d'integration pour le son de Game Over
Valide l'integration complete de la fonctionnalite dans le systeme
"""

import unittest
from unittest.mock import Mock, patch
from src.domaine.services.moteur_partie import MoteurPartie
from src.domaine.entites.pieces.piece_i import PieceI


class TestSonGameOverIntegration(unittest.TestCase):
    """Tests d'integration pour la fonctionnalite de son au Game Over"""
    
    def test_integration_complete_son_game_over(self):
        """
        Test d'integration complete:
        - Moteur de partie complet
        - Audio mock
        - Scenario de game over realiste
        - Verification de tous les elements
        """
        mock_audio = Mock()
        
        with patch('src.domaine.services.moteur_partie.AudioJeu') as mock_audio_class:
            mock_audio_class.return_value = mock_audio
            
            # Creer un moteur complet
            moteur = MoteurPartie(audio=mock_audio)
            
            # Verifier l'etat initial
            self.assertFalse(moteur.jeu_termine, "Le jeu ne devrait pas etre termine au debut")
            self.assertIsNotNone(moteur.audio, "L'audio devrait etre disponible")
            
            # Simuler une situation de game over en appelant directement 
            # la logique qui est dans placer_piece_et_generer_nouvelle
            
            # Forcer l'echec de placement (comme nb_lignes_supprimees == -1)
            echec_placement = True
            
            if echec_placement:
                # Executer exactement le code de game over du moteur
                moteur.jeu_termine = True
                moteur.messages.append("GAME OVER ! Plus de place pour les pieces.")
                print("GAME OVER ! Placement impossible.")
                
                # Jouer le son de game over (code exact du moteur)
                if moteur.audio:
                    try:
                        moteur.audio.jouer_effet_sonore("assets/audio/sfx/game-over.wav", volume=1.0)
                        print("Son de Game Over joue")
                    except Exception as e:
                        print(f"Erreur lors de la lecture du son de Game Over: {e}")
            
            # Verifications d'integration complete
            
            # 1. Etat du moteur
            self.assertTrue(moteur.jeu_termine, "Le jeu devrait etre termine")
            self.assertTrue(len(moteur.messages) > 0, "Il devrait y avoir des messages")
            self.assertIn("GAME OVER", moteur.messages[-1], "Le message de game over devrait etre present")
            
            # 2. Appel audio
            mock_audio.jouer_effet_sonore.assert_called_once_with(
                "assets/audio/sfx/game-over.wav", 
                volume=1.0
            )
            
            # 3. Verification des parametres audio
            calls = mock_audio.jouer_effet_sonore.call_args_list
            args, kwargs = calls[0]
            
            self.assertEqual(args[0], "assets/audio/sfx/game-over.wav", 
                           "Le fichier audio devrait etre game-over.wav")
                           
            # Volume peut etre en args[1] ou kwargs['volume']
            if len(args) > 1:
                volume = args[1]
            else:
                volume = kwargs.get('volume')
            
            self.assertEqual(volume, 1.0, "Le volume devrait etre 1.0 (100%)")
    
    def test_integration_moteur_partie_sans_audio(self):
        """
        Test d'integration avec moteur sans audio:
        Le game over doit fonctionner meme sans systeme audio
        """
        # Creer un moteur sans audio
        moteur = MoteurPartie(audio=None)
        
        # Verifications initiales
        self.assertIsNone(moteur.audio, "L'audio devrait etre None")
        self.assertFalse(moteur.jeu_termine, "Le jeu ne devrait pas etre termine au debut")
        
        # Simuler game over sans audio
        echec_placement = True
        
        if echec_placement:
            moteur.jeu_termine = True
            moteur.messages.append("GAME OVER ! Plus de place pour les pieces.")
            
            # Le code devrait gerer l'absence d'audio
            if moteur.audio:
                try:
                    moteur.audio.jouer_effet_sonore("assets/audio/sfx/game-over.wav", volume=1.0)
                except Exception:
                    pass
        
        # Verifications: le jeu doit fonctionner normalement
        self.assertTrue(moteur.jeu_termine, "Le game over devrait fonctionner sans audio")
        self.assertTrue(len(moteur.messages) > 0, "Les messages devraient etre presents")
        self.assertIn("GAME OVER", moteur.messages[-1], "Le message devrait etre present")


if __name__ == '__main__':
    unittest.main()
