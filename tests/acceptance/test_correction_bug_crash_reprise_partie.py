#!/usr/bin/env python3
"""
Tests d'acceptance - Correction bug crash reprise partie

Ce test valide la correction du bug qui causait un crash lors de la reprise
de partie après le démarrage du jeu.

Bugs corrigés :
1. AttributeError: 'MoteurPartie' object has no attribute 'afficher_menu'
2. Gestion robuste du système audio

Conformité aux directives de développement :
- Test d'acceptance dans tests/acceptance/
- Méthodologie TDD (RED-GREEN-REFACTOR) appliquée
- Architecture hexagonale respectée
"""

import unittest
import sys
import os

# Configuration du path pour l'architecture hexagonale
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.domaine.services.moteur_partie import MoteurPartie
from src.adapters.sortie.audio_partie import AudioPartie


class TestCorrectionBugCrashReprisePartie(unittest.TestCase):
    """Tests d'acceptance pour la correction du bug de crash à la reprise."""
    
    def test_moteur_partie_a_attribut_afficher_menu(self):
        """✅ ACCEPTANCE : MoteurPartie doit avoir l'attribut afficher_menu"""
        # GIVEN
        moteur = MoteurPartie()
        
        # WHEN & THEN
        self.assertTrue(hasattr(moteur, 'afficher_menu'), 
                       "MoteurPartie doit avoir l'attribut afficher_menu")
        self.assertIsInstance(moteur.afficher_menu, bool,
                             "afficher_menu doit être un booléen")
        self.assertFalse(moteur.afficher_menu,
                        "afficher_menu doit être False par défaut")
    
    def test_code_affichage_peut_acceder_a_afficher_menu(self):
        """✅ ACCEPTANCE : Le code d'affichage peut accéder à afficher_menu sans crash"""
        # GIVEN
        moteur = MoteurPartie()
        
        # WHEN - Simulation du code d'affichage_partie.py ligne 285
        try:
            if moteur.jeu_termine:
                texte = "GAME OVER"
            elif moteur.en_pause:
                texte = "PAUSE"
            elif moteur.afficher_menu:  # Cette ligne crashait avant
                texte = "MENU"
            else:
                texte = "EN JEU"
            
            access_reussi = True
        except AttributeError:
            access_reussi = False
        
        # THEN
        self.assertTrue(access_reussi, "L'accès à moteur.afficher_menu ne doit pas crasher")
    
    def test_modification_afficher_menu_fonctionne(self):
        """✅ ACCEPTANCE : On peut modifier l'état afficher_menu"""
        # GIVEN
        moteur = MoteurPartie()
        
        # WHEN
        moteur.afficher_menu = True
        
        # THEN
        self.assertTrue(moteur.afficher_menu, "afficher_menu doit pouvoir être modifié")
        
        # WHEN
        moteur.afficher_menu = False
        
        # THEN
        self.assertFalse(moteur.afficher_menu, "afficher_menu doit pouvoir être remis à False")
    
    def test_nettoyage_audio_sans_crash(self):
        """✅ ACCEPTANCE : Le nettoyage audio ne crash pas même sans initialisation"""
        # GIVEN
        audio = AudioPartie()
        
        # WHEN & THEN - Ne doit pas lever d'exception
        try:
            audio.nettoyer()
            nettoyage_reussi = True
        except Exception:
            nettoyage_reussi = False
            
        self.assertTrue(nettoyage_reussi, "Le nettoyage audio ne doit pas crasher")
    
    def test_scenario_complet_reprise_partie(self):
        """✅ ACCEPTANCE : Scénario complet de reprise de partie sans crash"""
        # GIVEN - Création d'un moteur comme au démarrage
        moteur = MoteurPartie()
        
        # WHEN - Simulation des opérations qui crashaient
        try:
            # 1. Accès aux attributs d'état (comme dans l'affichage)
            _ = moteur.jeu_termine
            _ = moteur.en_pause
            _ = moteur.afficher_menu  # Crashait avant
            
            # 2. Modification des états
            moteur.afficher_menu = True
            moteur.en_pause = False
            
            # 3. Nettoyage (comme dans partie_tetris.py ligne 116)
            if moteur.audio:
                moteur.audio.nettoyer()
            
            scenario_reussi = True
            
        except Exception as e:
            scenario_reussi = False
            print(f"Échec du scénario : {e}")
        
        # THEN
        self.assertTrue(scenario_reussi, 
                       "Le scénario complet de reprise de partie doit fonctionner sans crash")
    
    def test_conformite_directives_architecture_hexagonale(self):
        """✅ ACCEPTANCE : La correction respecte l'architecture hexagonale"""
        # GIVEN
        moteur = MoteurPartie()
        
        # THEN - Vérifier que l'attribut est dans le domaine (pas dans un adapter)
        self.assertTrue(hasattr(moteur, 'afficher_menu'),
                       "L'attribut afficher_menu doit être dans le domaine (MoteurPartie)")
        
        # THEN - Vérifier que l'état fait partie de la logique métier
        self.assertIn('afficher_menu', moteur.__dict__,
                     "afficher_menu doit être un attribut d'instance du domaine")


if __name__ == '__main__':
    print("🧪 Tests d'acceptance - Correction bug crash reprise partie")
    print("=" * 70)
    
    # Configuration du test runner avec émojis
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCorrectionBugCrashReprisePartie)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print("✅ TOUS LES TESTS D'ACCEPTANCE RÉUSSIS")
        print("   → Bug crash reprise partie corrigé et validé")
        print("   → Conformité aux directives de développement respectée")
    else:
        print("❌ ÉCHECS DÉTECTÉS")
        print(f"   → {len(result.failures)} échec(s)")
        print(f"   → {len(result.errors)} erreur(s)")
