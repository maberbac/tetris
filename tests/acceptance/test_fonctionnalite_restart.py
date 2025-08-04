"""
Tests d'acceptance pour la fonctionnalité restart.
Ces tests documentent le comportement attendu du point de vue utilisateur.
"""
import unittest
from unittest.mock import Mock

from src.domaine.services.moteur_partie import MoteurPartie
from src.adapters.entree.gestionnaire_partie import GestionnairePartie
from src.domaine.services.gestionnaire_evenements import TypeEvenement


class TestAcceptanceRestart(unittest.TestCase):
    """Tests d'acceptance pour la fonctionnalité restart."""
    
    def setUp(self):
        """Configuration des tests."""
        self.moteur = MoteurPartie()
        self.gestionnaire = GestionnairePartie()
    
    def test_touche_r_redémarre_apres_game_over(self):
        """
        Scénario : L'utilisateur termine une partie et veut redémarrer.
        
        Étant donné que le jeu est terminé (game over)
        Quand l'utilisateur appuie sur la touche R
        Alors une nouvelle partie commence
        Et le score est remis à zéro
        Et une nouvelle pièce est générée
        """
        print("\n🧪 TEST ACCEPTANCE: Restart après game over")
        print("=" * 50)
        
        # Arrange - Simuler game over
        self.moteur.jeu_termine = True
        self.moteur.stats.score = 1500  # Score d'une partie précédente
        score_initial = self.moteur.stats.score
        
        print(f"📊 État initial:")
        print(f"   Game Over: {self.moteur.est_game_over()}")
        print(f"   Score: {score_initial}")
        
        # Act - Appuyer sur R
        result = self.gestionnaire.traiter_evenement_clavier('r', TypeEvenement.CLAVIER_APPUI, self.moteur)
        
        print(f"📊 État après restart:")
        print(f"   Game Over: {self.moteur.est_game_over()}")
        print(f"   Score: {self.moteur.stats.score}")
        print(f"   Commande réussie: {result}")
        
        # Assert
        self.assertTrue(result, "La commande restart doit réussir")
        self.assertFalse(self.moteur.est_game_over(), "Le jeu ne doit plus être terminé")
        self.assertEqual(self.moteur.stats.score, 0, "Le score doit être remis à zéro")
        self.assertIsNotNone(self.moteur.piece_active, "Une nouvelle pièce doit être générée")
        self.assertGreater(score_initial, self.moteur.stats.score, "Le score doit avoir été reset")
        print("✅ Test d'acceptance RÉUSSI : Restart après game over")
    
    def test_touche_r_ignorée_pendant_partie_en_cours(self):
        """
        Scénario : L'utilisateur appuie accidentellement sur R pendant le jeu.
        
        Étant donné que le jeu est en cours (pas de game over)
        Quand l'utilisateur appuie sur la touche R
        Alors rien ne se passe
        Et la partie continue normalement
        """
        print("\n🧪 TEST ACCEPTANCE: R ignoré pendant partie")
        print("=" * 50)
        
        # Arrange - Jeu en cours
        self.assertFalse(self.moteur.est_game_over(), "Le jeu doit être en cours")
        piece_avant = self.moteur.piece_active
        score_avant = self.moteur.stats.score
        
        print(f"📊 État initial:")
        print(f"   Game Over: {self.moteur.est_game_over()}")
        print(f"   Score: {score_avant}")
        print(f"   Pièce: {piece_avant.type_piece}")
        
        # Act - Appuyer sur R
        result = self.gestionnaire.traiter_evenement_clavier('r', TypeEvenement.CLAVIER_APPUI, self.moteur)
        
        print(f"📊 État après tentative R:")
        print(f"   Game Over: {self.moteur.est_game_over()}")
        print(f"   Score: {self.moteur.stats.score}")
        print(f"   Commande ignorée: {not result}")
        
        # Assert
        self.assertFalse(result, "La commande restart doit être ignorée")
        self.assertFalse(self.moteur.est_game_over(), "Le jeu doit toujours être en cours")
        self.assertEqual(self.moteur.piece_active.type_piece, piece_avant.type_piece, "La pièce ne doit pas changer")
        self.assertEqual(self.moteur.stats.score, score_avant, "Le score ne doit pas changer")
        print("✅ Test d'acceptance RÉUSSI : R ignoré pendant partie")
    
    def test_restart_préserve_architecture_jeu(self):
        """
        Scénario : Le restart doit préserver l'intégrité architecturale.
        
        Étant donné un jeu terminé avec un état complexe
        Quand l'utilisateur redémarre
        Alors tous les composants sont correctement réinitialisés
        """
        print("\n🧪 TEST ACCEPTANCE: Architecture préservée")
        print("=" * 50)
        
        # Arrange - Créer un état complexe puis terminer
        self.moteur.stats.score = 5000
        self.moteur.stats.niveau = 3
        self.moteur.stats.lignes_completees = 25
        self.moteur.jeu_termine = True
        
        print(f"📊 État complexe initial:")
        print(f"   Score: {self.moteur.stats.score}")
        print(f"   Niveau: {self.moteur.stats.niveau}")
        print(f"   Lignes: {self.moteur.stats.lignes_completees}")
        
        # Act - Restart
        result = self.gestionnaire.traiter_evenement_clavier('r', TypeEvenement.CLAVIER_APPUI, self.moteur)
        
        print(f"📊 État après restart:")
        print(f"   Score: {self.moteur.stats.score}")
        print(f"   Niveau: {self.moteur.stats.niveau}")
        print(f"   Lignes: {self.moteur.stats.lignes_completees}")
        print(f"   Game Over: {self.moteur.est_game_over()}")
        
        # Assert - Vérifier réinitialisation complète
        self.assertTrue(result, "Restart doit réussir")
        self.assertEqual(self.moteur.stats.score, 0, "Score reset")
        self.assertEqual(self.moteur.stats.niveau, 1, "Niveau reset")
        self.assertEqual(self.moteur.stats.lignes_completees, 0, "Lignes reset")
        self.assertFalse(self.moteur.est_game_over(), "Game over reset")
        self.assertIsNotNone(self.moteur.piece_active, "Nouvelle pièce générée")
        self.assertIsNotNone(self.moteur.piece_suivante, "Prochaine pièce générée")
        print("✅ Test d'acceptance RÉUSSI : Architecture préservée")
    
    def test_restart_fonctionne_plusieurs_fois_consecutives(self):
        """
        Scénario : L'utilisateur redémarre plusieurs parties de suite.
        
        Étant donné plusieurs redémarrages consécutifs
        Quand l'utilisateur appuie sur R à chaque game over
        Alors chaque restart fonctionne correctement
        """
        print("\n🧪 TEST ACCEPTANCE: Multiples restarts")
        print("=" * 50)
        
        for i in range(3):
            print(f"   🔄 Restart #{i+1}")
            
            # Simuler game over
            self.moteur.jeu_termine = True
            self.moteur.stats.score = (i + 1) * 1000
            
            # Restart
            result = self.gestionnaire.traiter_evenement_clavier('r', TypeEvenement.CLAVIER_APPUI, self.moteur)
            
            # Vérifier
            self.assertTrue(result, f"Restart #{i+1} doit réussir")
            self.assertFalse(self.moteur.est_game_over(), f"Game over reset #{i+1}")
            self.assertEqual(self.moteur.stats.score, 0, f"Score reset #{i+1}")
            print(f"     ✅ Restart #{i+1} réussi")
        
        print("✅ Test d'acceptance RÉUSSI : Multiples restarts")
    
    def test_mapping_touche_r_correct(self):
        """
        Scénario : La touche R doit être correctement mappée.
        
        Étant donné le système de mapping des touches
        Quand on vérifie le mapping de la touche R
        Alors elle doit être associée à la commande restart
        """
        print("\n🧪 TEST ACCEPTANCE: Mapping touche R")
        print("=" * 50)
        
        # Vérifier que 'r' est dans le mapping pygame
        from src.adapters.entree.gestionnaire_partie import convertir_touche_pygame
        import pygame
        
        # Test du mapping pygame vers string
        touche_string = convertir_touche_pygame(pygame.K_r)
        self.assertEqual(touche_string, "r", "pygame.K_r doit se convertir en 'r'")
        print(f"   📋 Mapping pygame: K_r → '{touche_string}'")
        
        # Vérifier que le gestionnaire traite correctement la touche R
        from src.domaine.services.gestionnaire_evenements import ToucheClavier
        from src.domaine.services.commandes.commande_redemarrer import CommandeRedemarrer
        
        # Créer un moteur en état de game over pour tester la commande
        moteur_test = MoteurPartie()
        moteur_test.jeu_termine = True  # Mettre en état game over
        
        # Essayer d'exécuter la commande restart via le gestionnaire
        result = self.gestionnaire.traiter_evenement_clavier('r', TypeEvenement.CLAVIER_APPUI, moteur_test)
        
        # Vérifier que la commande s'exécute (résultat True = succès)
        self.assertTrue(result, "La commande restart doit être trouvée et exécutée")
        print(f"   📋 Commande: Touche 'r' → Commande exécutée avec succès")
        
        print("✅ Test d'acceptance RÉUSSI : Mapping touche R correct")


class TestAcceptanceRestartAvecAudio(unittest.TestCase):
    """Tests d'acceptance pour restart avec système audio."""
    
    def setUp(self):
        """Configuration avec audio mock."""
        self.moteur = MoteurPartie()
        self.gestionnaire = GestionnairePartie()
        
        # Mock audio pour éviter les dépendances
        self.audio_mock = Mock()
        self.moteur.audio = self.audio_mock
    
    def test_restart_preserve_état_audio(self):
        """
        Scénario : Le restart doit préserver l'état audio (mute/unmute).
        
        Étant donné que l'audio est en mode mute
        Quand l'utilisateur redémarre après game over
        Alors l'état mute doit être préservé
        """
        print("\n🧪 TEST ACCEPTANCE: État audio préservé")
        print("=" * 50)
        
        # Arrange - Simuler état mute
        self.audio_mock.est_mute = True
        self.moteur.jeu_termine = True
        
        print(f"   🔇 État mute initial: {self.audio_mock.est_mute}")
        
        # Act - Restart
        result = self.gestionnaire.traiter_evenement_clavier('r', TypeEvenement.CLAVIER_APPUI, self.moteur)
        
        print(f"   🔇 État mute après restart: {self.audio_mock.est_mute}")
        
        # Assert
        self.assertTrue(result, "Restart doit réussir")
        self.assertTrue(self.audio_mock.est_mute, "État mute doit être préservé")
        print("✅ Test d'acceptance RÉUSSI : État audio préservé")
    
    def test_restart_ne_perturbe_pas_audio(self):
        """
        Scénario : Le restart ne doit pas perturber le système audio.
        
        Étant donné un système audio fonctionnel
        Quand l'utilisateur redémarre
        Alors l'audio continue de fonctionner normalement
        """
        print("\n🧪 TEST ACCEPTANCE: Audio non perturbé")
        print("=" * 50)
        
        # Arrange
        self.moteur.jeu_termine = True
        audio_reference = self.moteur.audio
        
        # Act
        result = self.gestionnaire.traiter_evenement_clavier('r', TypeEvenement.CLAVIER_APPUI, self.moteur)
        
        # Assert - Vérifier que l'audio n'a pas été perturbé
        self.assertTrue(result, "Restart doit réussir")
        self.assertEqual(self.moteur.audio, audio_reference, "Référence audio préservée")
        print("✅ Test d'acceptance RÉUSSI : Audio non perturbé")


if __name__ == '__main__':
    unittest.main()
