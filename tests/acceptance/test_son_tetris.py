"""
Tests d'acceptance pour le son tetris.wav lors de l'élimination de 4 lignes simultanées.

Ces tests valident que le joueur entend bien le son TETRIS spécial
quand il réalise un "TETRIS" (élimination de 4 lignes d'un coup).

CONFORMITÉ DIRECTIVES :
- Tests placés dans tests/acceptance/ selon l'organisation stricte
- Volume à 100% selon la règle audio des directives
- Architecture hexagonale respectée avec ports et adaptateurs
"""

import unittest
import sys
import os

# Ajouter le chemin du projet pour les tests
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.domaine.services.moteur_partie import MoteurPartie
from src.ports.sortie.audio_jeu import AudioJeu


class AudioSpyTetris(AudioJeu):
    """Spy audio spécialement conçu pour capturer les sons tetris.wav."""
    
    def __init__(self):
        self.sons_tetris_joues = []
        self.tous_les_sons = []
        self.erreurs_audio = []
    
    def initialiser(self) -> None:
        pass
    
    def jouer_effet_sonore(self, chemin_fichier: str, volume: float = 1.0) -> None:
        self.tous_les_sons.append((chemin_fichier, volume))
        
        # Capturer spécialement les sons tetris.wav
        if "tetris.wav" in chemin_fichier:
            self.sons_tetris_joues.append({
                'fichier': chemin_fichier,
                'volume': volume,
                'appel_count': len(self.sons_tetris_joues) + 1
            })
            print(f"🎵 TETRIS SOUND CAPTURED: {chemin_fichier} (volume: {volume})")
    
    def jouer_musique(self, chemin_fichier: str, volume: float = 0.7, boucle: bool = False) -> None:
        pass
    
    def arreter_musique(self) -> None:
        pass
    
    def mettre_en_pause_musique(self) -> None:
        pass
    
    def reprendre_musique(self) -> None:
        pass
    
    def basculer_mute_musique(self) -> bool:
        return False
    
    def definir_volume_musique(self, volume: float) -> None:
        pass
    
    def est_musique_en_cours(self) -> bool:
        return False
    
    def obtenir_etat_mute(self) -> bool:
        """Retourne l'état de mute (pour compatibilité avec l'interface)."""
        return False
    
    def nettoyer(self) -> None:
        pass
    
    def obtenir_sons_tetris(self):
        """Retourne la liste des sons tetris.wav joués."""
        return self.sons_tetris_joues
    
    def a_joue_tetris_wav(self) -> bool:
        """Vérifie si au moins un son tetris.wav a été joué."""
        return len(self.sons_tetris_joues) > 0


class TestAcceptanceSonTetris(unittest.TestCase):
    """Tests d'acceptance pour le son tetris.wav lors des TETRIS (4 lignes)."""
    
    def setUp(self):
        """Configuration commune pour tous les tests."""
        self.audio_spy = AudioSpyTetris()
        self.moteur = MoteurPartie(audio=self.audio_spy)
        self.moteur.en_pause = False  # Activer le jeu pour les tests
    
    def test_son_tetris_joue_pour_4_lignes_eliminees(self):
        """
        Test d'acceptance : Le son tetris.wav est joué quand le joueur élimine exactement 4 lignes.
        
        Scénario utilisateur :
        1. Le joueur joue normalement
        2. Il réussit à éliminer 4 lignes d'un coup (TETRIS)
        3. Il entend le son spécial tetris.wav
        4. Le volume est à 100% selon les directives
        """
        print("\n🎮 TEST D'ACCEPTANCE: Son TETRIS pour 4 lignes")
        print("=" * 55)
        
        # Simuler l'élimination de 4 lignes (TETRIS)
        nb_lignes_eliminees = 4
        
        # Utiliser la méthode officielle du moteur pour simuler la suppression de lignes
        self.moteur.simuler_lignes_supprimees(nb_lignes_eliminees)
        print("🎵 Son TETRIS joué ! (4 lignes éliminées)")
        
        # Vérifications d'acceptance
        print(f"📊 Analyse des résultats:")
        print(f"   Lignes éliminées: {nb_lignes_eliminees}")
        print(f"   Sons tetris.wav joués: {len(self.audio_spy.obtenir_sons_tetris())}")
        print(f"   Détails sons: {self.audio_spy.obtenir_sons_tetris()}")
        
        # Assertions d'acceptance
        self.assertTrue(self.audio_spy.a_joue_tetris_wav(), 
                       "Le son tetris.wav devrait être joué pour un TETRIS (4 lignes)")
        
        sons_tetris = self.audio_spy.obtenir_sons_tetris()
        self.assertEqual(len(sons_tetris), 1, "Exactement un son tetris.wav devrait être joué")
        
        # Vérifier le volume (100% selon directives)
        son_tetris = sons_tetris[0]
        self.assertEqual(son_tetris['volume'], 1.0, 
                        "Le volume du son TETRIS doit être à 100% selon les directives")
        
        # Vérifier le fichier correct
        self.assertIn("tetris.wav", son_tetris['fichier'],
                     "Le fichier doit être tetris.wav")
        
        print("✅ Test d'acceptance RÉUSSI : Son TETRIS pour 4 lignes")
    
    def test_son_tetris_pas_joue_pour_1_2_3_lignes(self):
        """
        Test d'acceptance : Le son tetris.wav n'est PAS joué pour moins de 4 lignes.
        
        Scénario utilisateur :
        1. Le joueur élimine 1, 2 ou 3 lignes
        2. Il n'entend PAS le son tetris.wav spécial
        3. Seuls les TETRIS (4 lignes) déclenchent ce son
        """
        print("\n🎮 TEST D'ACCEPTANCE: Pas de son TETRIS pour 1-3 lignes")
        print("=" * 60)
        
        for nb_lignes in [1, 2, 3]:
            with self.subTest(lignes=nb_lignes):
                # Réinitialiser le spy pour chaque test
                audio_spy_local = AudioSpyTetris()
                moteur_local = MoteurPartie(audio=audio_spy_local)
                moteur_local.en_pause = False
                
                print(f"  📊 Test pour {nb_lignes} ligne(s)...")
                
                # Simuler l'élimination de nb_lignes lignes via la méthode officielle du moteur
                if nb_lignes > 0:
                    moteur_local.simuler_lignes_supprimees(nb_lignes)
                
                # Vérifier qu'AUCUN son tetris.wav n'est joué
                self.assertFalse(audio_spy_local.a_joue_tetris_wav(),
                               f"Le son tetris.wav ne devrait PAS être joué pour {nb_lignes} ligne(s)")
                
                print(f"    ✅ Pas de son TETRIS pour {nb_lignes} ligne(s) - Correct")
        
        print("✅ Test d'acceptance RÉUSSI : Pas de son TETRIS pour 1-3 lignes")
    
    def test_message_tetris_toujours_present_avec_son(self):
        """
        Test d'acceptance : Le son TETRIS est joué pour 4 lignes (sans messages).
        
        Scénario utilisateur :
        1. Le joueur réalise un TETRIS (4 lignes)
        2. Il entend le son tetris.wav spécial
        3. Aucun message n'est affiché (gameplay épuré)
        4. L'expérience audio est complète
        """
        print("\n🎮 TEST D'ACCEPTANCE: Son TETRIS sans messages")
        print("=" * 55)
        
        # Simuler un TETRIS complet via la méthode officielle du moteur
        nb_lignes = 4
        self.moteur.simuler_lignes_supprimees(nb_lignes)
        print("🎵 Son TETRIS joué ! (4 lignes éliminées)")
        
        # Vérifier que le son est joué
        print(f"🎵 Sons TETRIS joués: {len(self.audio_spy.obtenir_sons_tetris())}")
        
        # Assertion d'acceptance - seul le son compte
        self.assertTrue(self.audio_spy.a_joue_tetris_wav(), "Le son TETRIS doit être joué")
        
        print("✅ Test d'acceptance RÉUSSI : Son TETRIS joué (gameplay épuré sans messages)")
    
    def test_integration_complete_tetris_dans_moteur(self):
        """
        Test d'acceptance : Intégration complète du son TETRIS dans le moteur de partie.
        
        Scénario réaliste :
        1. Le moteur fonctionne normalement
        2. Une pièce est placée et génère 4 lignes complètes  
        3. Le son TETRIS est automatiquement joué
        4. Tout fonctionne sans intervention manuelle
        """
        print("\n🎮 TEST D'ACCEPTANCE: Intégration complète TETRIS")
        print("=" * 55)
        
        # Test avec la méthode réelle du moteur (simulation complète)
        print("📊 Simulation d'un placement avec 4 lignes complètes...")
        
        # Utiliser la méthode officielle du moteur pour simuler 4 lignes supprimées
        nb_lignes_supprimees = 4
        self.moteur.simuler_lignes_supprimees(nb_lignes_supprimees)
        print("🎵 Son TETRIS joué ! (4 lignes éliminées)")
        print(f"[PARTY] {nb_lignes_supprimees} ligne(s) complétée(s) ! Score: {self.moteur.stats.score}")
        
        # Vérifications d'intégration
        print(f"📊 Résultats d'intégration:")
        print(f"   Score obtenu: {self.moteur.stats.score}")
        print(f"   Sons TETRIS joués: {len(self.audio_spy.obtenir_sons_tetris())}")
        
        # Assertions d'intégration
        self.assertEqual(self.moteur.stats.score, 800, "Le score TETRIS doit être de 800 points")
        self.assertTrue(self.audio_spy.a_joue_tetris_wav(), 
                       "Le son TETRIS doit être joué automatiquement")
        
        print("✅ Test d'acceptance RÉUSSI : Intégration complète TETRIS dans le moteur")
    
    def test_fichier_tetris_wav_existe_et_accessible(self):
        """
        Test d'acceptance : Le fichier tetris.wav existe et est accessible.
        
        Prérequis technique :
        1. Le fichier assets/audio/sfx/tetris.wav doit exister
        2. Il doit être accessible en lecture
        3. L'implémentation peut l'utiliser sans erreur
        """
        print("\n🎮 TEST D'ACCEPTANCE: Fichier tetris.wav accessible")
        print("=" * 55)
        
        chemin_tetris = "assets/audio/sfx/tetris.wav"
        chemin_absolu = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), chemin_tetris)
        
        print(f"🔍 Vérification fichier tetris.wav:")
        print(f"   Chemin relatif: {chemin_tetris}")
        print(f"   Chemin absolu: {chemin_absolu}")
        print(f"   Working directory: {os.getcwd()}")
        
        # Essayer les deux chemins possibles
        fichier_trouve = False
        chemin_final = None
        
        if os.path.exists(chemin_tetris):
            fichier_trouve = True
            chemin_final = chemin_tetris
        elif os.path.exists(chemin_absolu):
            fichier_trouve = True
            chemin_final = chemin_absolu
        
        # Vérifier que le fichier existe (l'un des deux chemins)
        self.assertTrue(fichier_trouve,
                       f"Le fichier tetris.wav doit exister. Chemins testés:\n- {chemin_tetris}\n- {chemin_absolu}")
        
        # Vérifier qu'il est lisible
        self.assertTrue(os.access(chemin_final, os.R_OK),
                       f"Le fichier {chemin_final} doit être lisible")
        
        # Vérifier la taille (un fichier audio ne peut pas être vide)
        taille = os.path.getsize(chemin_final)
        self.assertGreater(taille, 0, 
                          f"Le fichier {chemin_final} ne peut pas être vide")
        
        print(f"📁 Fichier tetris.wav:")
        print(f"   Chemin utilisé: {chemin_final}")
        print(f"   Existe: ✅")
        print(f"   Lisible: ✅")
        print(f"   Taille: {taille} bytes")
        
        print("✅ Test d'acceptance RÉUSSI : Fichier tetris.wav accessible")


def run_acceptance_tests():
    """Lance tous les tests d'acceptance pour le son TETRIS."""
    print("🎵 TESTS D'ACCEPTANCE - SON TETRIS.WAV POUR 4 LIGNES")
    print("=" * 65)
    
    # Créer la suite de tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAcceptanceSonTetris)
    
    # Exécuter les tests avec un rapport détaillé
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Rapport final
    print("\n" + "=" * 65)
    print("🏆 RAPPORT FINAL - TESTS D'ACCEPTANCE SON TETRIS")
    print("=" * 65)
    print(f"Tests exécutés: {result.testsRun}")
    print(f"✅ Succès: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Échecs: {len(result.failures)}")
    print(f"⚠️  Erreurs: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("🎉 TOUS LES TESTS D'ACCEPTANCE RÉUSSIS !")
        print("✨ Le son tetris.wav est correctement implémenté pour les TETRIS (4 lignes)")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        if result.failures:
            print("\nÉchecs:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback}")
        if result.errors:
            print("\nErreurs:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Lancer les tests d'acceptance
    success = run_acceptance_tests()
    sys.exit(0 if success else 1)
