"""
Tests d'acceptance pour l'indicateur visuel de mute.

Ces tests valident que l'utilisateur dispose d'un indicateur visuel clair
quand le son est en mode mute.
"""

import unittest
import sys
from pathlib import Path

# Ajouter le chemin racine pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.adapters.sortie.audio_partie import AudioPartie
from src.adapters.sortie.affichage_partie import AffichagePartie
from src.domaine.services.moteur_partie import MoteurPartie


class TestIndicateurMute(unittest.TestCase):
    """Tests d'acceptance pour l'indicateur visuel de mute."""
    
    def setUp(self):
        """Configuration avant chaque test."""
        self.audio = AudioPartie()
        self.moteur = MoteurPartie(self.audio)
        self.affichage = AffichagePartie()
    
    def tearDown(self):
        """Nettoyage après chaque test."""
        try:
            self.audio.nettoyer()
            self.affichage.nettoyer()
        except:
            pass
    
    def test_audio_possede_methode_obtenir_etat_mute(self):
        """ACCEPTANCE: L'audio doit pouvoir indiquer son état de mute."""
        # L'audio doit avoir une méthode pour obtenir l'état mute
        self.assertTrue(hasattr(self.audio, 'obtenir_etat_mute'))
        
        # La méthode doit retourner un booléen
        etat = self.audio.obtenir_etat_mute()
        self.assertIsInstance(etat, bool)
        
        # État initial doit être False (unmute)
        self.assertFalse(etat)
    
    def test_basculement_mute_change_etat(self):
        """ACCEPTANCE: Le basculement mute doit changer l'état observable."""
        # État initial
        etat_initial = self.audio.obtenir_etat_mute()
        self.assertFalse(etat_initial)
        
        # Basculer vers mute
        self.audio.basculer_mute_musique()
        etat_mute = self.audio.obtenir_etat_mute()
        self.assertTrue(etat_mute)
        
        # Basculer vers unmute
        self.audio.basculer_mute_musique()
        etat_unmute = self.audio.obtenir_etat_mute()
        self.assertFalse(etat_unmute)
    
    def test_affichage_possede_methode_indicateur_mute(self):
        """ACCEPTANCE: L'affichage doit pouvoir dessiner l'indicateur mute."""
        # L'affichage doit avoir une méthode pour dessiner l'indicateur
        self.assertTrue(hasattr(self.affichage, '_dessiner_indicateur_mute'))
        
        # La méthode doit être callable
        self.assertTrue(callable(getattr(self.affichage, '_dessiner_indicateur_mute')))
    
    def test_indicateur_mute_ne_genere_pas_erreur(self):
        """ACCEPTANCE: L'indicateur mute ne doit pas générer d'erreur."""
        # Test avec état unmute
        try:
            self.affichage._dessiner_indicateur_mute(self.moteur)
        except Exception as e:
            self.fail(f"L'indicateur mute ne devrait pas générer d'erreur en état unmute: {e}")
        
        # Test avec état mute
        self.audio.basculer_mute_musique()
        try:
            self.affichage._dessiner_indicateur_mute(self.moteur)
        except Exception as e:
            self.fail(f"L'indicateur mute ne devrait pas générer d'erreur en état mute: {e}")
    
    def test_moteur_obtient_audio_avec_etat_mute(self):
        """ACCEPTANCE: Le moteur doit pouvoir obtenir l'état mute de l'audio."""
        # Le moteur doit avoir accès à l'audio
        audio_moteur = self.moteur.obtenir_audio()
        self.assertIsNotNone(audio_moteur)
        
        # L'audio du moteur doit avoir la méthode obtenir_etat_mute
        self.assertTrue(hasattr(audio_moteur, 'obtenir_etat_mute'))
        
        # Test de cohérence entre audio direct et audio du moteur
        etat_direct = self.audio.obtenir_etat_mute()
        etat_moteur = audio_moteur.obtenir_etat_mute()
        self.assertEqual(etat_direct, etat_moteur)
    
    def test_integration_complete_indicateur_mute(self):
        """ACCEPTANCE: Intégration complète de l'indicateur dans le workflow du jeu."""
        # 1. Vérifier l'état initial
        self.assertFalse(self.audio.obtenir_etat_mute())
        
        # 2. Simuler l'action utilisateur : appuyer sur M
        self.audio.basculer_mute_musique()
        
        # 3. Vérifier que l'état a changé
        self.assertTrue(self.audio.obtenir_etat_mute())
        
        # 4. Vérifier que l'affichage peut utiliser cette information
        audio_pour_affichage = self.moteur.obtenir_audio()
        self.assertTrue(audio_pour_affichage.obtenir_etat_mute())
        
        # 5. Vérifier que l'indicateur peut être dessiné sans erreur
        try:
            self.affichage._dessiner_indicateur_mute(self.moteur)
        except Exception as e:
            self.fail(f"Erreur lors du dessin de l'indicateur: {e}")
        
        # 6. Retour à l'état unmute
        self.audio.basculer_mute_musique()
        self.assertFalse(self.audio.obtenir_etat_mute())
    
    def test_robustesse_audio_indisponible(self):
        """ACCEPTANCE: L'indicateur doit être robuste si l'audio n'est pas disponible."""
        # Créer un moteur sans audio
        moteur_sans_audio = MoteurPartie(audio=None)
        
        # L'indicateur ne doit pas générer d'erreur même sans audio
        try:
            self.affichage._dessiner_indicateur_mute(moteur_sans_audio)
        except Exception as e:
            self.fail(f"L'indicateur devrait être robuste sans audio: {e}")


class TestComportementUtilisateur(unittest.TestCase):
    """Tests du comportement attendu par l'utilisateur."""
    
    def setUp(self):
        """Configuration avant chaque test."""
        self.audio = AudioPartie()
        self.moteur = MoteurPartie(self.audio)
    
    def tearDown(self):
        """Nettoyage après chaque test."""
        try:
            self.audio.nettoyer()
        except:
            pass
    
    def test_utilisateur_voit_mute_quand_active(self):
        """ACCEPTANCE: L'utilisateur doit voir l'indicateur quand le mute est activé."""
        # Simuler l'activation du mute par l'utilisateur
        self.audio.basculer_mute_musique()
        
        # L'état doit être observable pour l'affichage
        etat_mute = self.moteur.obtenir_audio().obtenir_etat_mute()
        self.assertTrue(etat_mute, "L'utilisateur doit pouvoir voir que le mute est activé")
    
    def test_utilisateur_ne_voit_pas_mute_quand_inactive(self):
        """ACCEPTANCE: L'utilisateur ne doit pas voir l'indicateur quand le mute est inactif."""
        # S'assurer que le mute est inactif
        if self.audio.obtenir_etat_mute():
            self.audio.basculer_mute_musique()
        
        # L'état doit indiquer unmute
        etat_mute = self.moteur.obtenir_audio().obtenir_etat_mute()
        self.assertFalse(etat_mute, "L'utilisateur ne doit pas voir l'indicateur quand le son est actif")
    
    def test_coherence_etat_mute_pendant_session(self):
        """ACCEPTANCE: L'état mute doit rester cohérent pendant toute la session."""
        # Séquence de basculements multiples
        etats_attendus = [False, True, False, True, False]
        
        for i, etat_attendu in enumerate(etats_attendus):
            if i > 0:  # Ne pas basculer avant le premier test
                self.audio.basculer_mute_musique()
            
            etat_actuel = self.audio.obtenir_etat_mute()
            self.assertEqual(etat_actuel, etat_attendu, 
                           f"Étape {i}: État attendu {etat_attendu}, obtenu {etat_actuel}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
