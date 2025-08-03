#!/usr/bin/env python3
"""
Tests d'acceptance : Correction bug obtenir_audio manquant

Scénarios :
- La commande mute doit pouvoir obtenir l'audio du moteur
- Le moteur doit exposer une méthode obtenir_audio()
"""

import unittest
import sys
import os
from unittest.mock import Mock

# Ajouter le répertoire racine au path pour les imports (conforme aux directives)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.domaine.services.moteur_partie import MoteurPartie
from src.domaine.services.commandes.commandes_base import CommandeBasculerMute


class TestCorrectionBugObtenirAudio(unittest.TestCase):
    """Tests d'acceptance pour la correction du bug obtenir_audio."""
    
    def setUp(self):
        """Configuration pour chaque test."""
        self.moteur = MoteurPartie()
        
    def test_moteur_a_methode_obtenir_audio(self):
        """
        Scénario : Le moteur doit avoir une méthode obtenir_audio()
        Résultat attendu : La méthode existe et retourne l'audio du moteur
        """
        # Act & Assert : La méthode doit exister
        self.assertTrue(hasattr(self.moteur, 'obtenir_audio'), 
                       "Le moteur doit avoir une méthode obtenir_audio()")
        
        # La méthode doit retourner l'attribut audio
        audio_retourne = self.moteur.obtenir_audio()
        self.assertEqual(audio_retourne, self.moteur.audio, 
                        "obtenir_audio() doit retourner self.audio")
        print("✅ Le moteur a bien la méthode obtenir_audio()")
        
    def test_commande_mute_peut_obtenir_audio_du_moteur(self):
        """
        Scénario : La commande mute doit pouvoir obtenir l'audio du moteur
        Résultat attendu : Aucune erreur lors de l'appel à moteur.obtenir_audio()
        """
        # Arrange : Mock audio
        mock_audio = Mock()
        mock_audio.basculer_mute_musique.return_value = True
        self.moteur.audio = mock_audio
        
        # Act : Exécuter la commande mute
        commande = CommandeBasculerMute()
        try:
            resultat = commande.execute(self.moteur)
            
            # Assert : La commande doit réussir
            self.assertTrue(resultat, "La commande mute doit réussir")
            mock_audio.basculer_mute_musique.assert_called_once()
            print("✅ La commande mute peut obtenir l'audio du moteur sans erreur")
            
        except AttributeError as e:
            if "'MoteurPartie' object has no attribute 'obtenir_audio'" in str(e):
                self.fail("Le moteur n'a pas la méthode obtenir_audio() - bug confirmé")
            else:
                raise
                
    def test_obtenir_audio_retourne_none_si_pas_audio(self):
        """
        Scénario : obtenir_audio() quand le moteur n'a pas d'audio
        Résultat attendu : Retourne None proprement
        """
        # Arrange : Moteur sans audio
        self.moteur.audio = None
        
        # Act : Obtenir audio
        audio_retourne = self.moteur.obtenir_audio()
        
        # Assert : Doit retourner None
        self.assertIsNone(audio_retourne, "obtenir_audio() doit retourner None si pas d'audio")
        print("✅ obtenir_audio() gère correctement le cas audio None")


if __name__ == "__main__":
    print("🎮 TESTS D'ACCEPTANCE : Correction bug obtenir_audio")
    print("=" * 60)
    unittest.main(verbosity=2)
