"""
Tests d'acceptance pour la fonctionnalité de pause par défaut au démarrage.

Selon les directives de développement :
- Tests d'acceptance dans tests/acceptance/
- TDD strict : Red -> Green -> Refactor
- Code en français
- Architecture hexagonale respectée
"""

import unittest
import sys
import os

# Ajouter le répertoire racine au path pour les imports (conforme aux directives)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.domaine.services.moteur_partie import MoteurPartie


class TestPauseParDefautAuDemarrage(unittest.TestCase):
    """Tests d'acceptance pour la pause par défaut au démarrage."""
    
    def test_moteur_demarre_en_pause_par_defaut(self):
        """✅ Le moteur doit démarrer en pause par défaut."""
        print("🧪 Test : Le moteur démarre en pause par défaut")
        print("-" * 50)
        
        # GIVEN : Un nouveau moteur de jeu vient d'être créé
        moteur = MoteurPartie()
        
        # THEN : Il doit être en pause par défaut
        self.assertTrue(moteur.en_pause, 
                       "Le moteur doit démarrer en pause par défaut pour permettre à l'utilisateur de se préparer")
        print("✅ Le moteur démarre bien en pause par défaut")
    
    def test_utilisateur_peut_reprendre_apres_pause_defaut(self):
        """✅ L'utilisateur peut reprendre le jeu après la pause par défaut."""
        print("🧪 Test : L'utilisateur peut reprendre après pause par défaut")
        print("-" * 50)
        
        # GIVEN : Un moteur qui démarre en pause par défaut
        moteur = MoteurPartie()
        self.assertTrue(moteur.en_pause, "Le moteur doit démarrer en pause")
        
        # WHEN : L'utilisateur appuie sur pause pour reprendre
        moteur.basculer_pause()
        
        # THEN : Le jeu n'est plus en pause
        self.assertFalse(moteur.en_pause, "Le jeu doit pouvoir être repris après la pause par défaut")
        print("✅ L'utilisateur peut bien reprendre le jeu")
    
    def test_basculement_pause_fonctionne_depuis_etat_defaut(self):
        """✅ Le basculement de pause fonctionne depuis l'état par défaut."""
        print("🧪 Test : Basculement pause depuis état par défaut")
        print("-" * 50)
        
        # GIVEN : Un moteur en pause par défaut
        moteur = MoteurPartie()
        etat_initial = moteur.en_pause
        self.assertTrue(etat_initial, "État initial doit être en pause")
        
        # WHEN : On bascule la pause deux fois
        moteur.basculer_pause()  # Première bascule : pause -> jeu
        etat_apres_premiere_bascule = moteur.en_pause
        
        moteur.basculer_pause()  # Deuxième bascule : jeu -> pause
        etat_apres_deuxieme_bascule = moteur.en_pause
        
        # THEN : Le basculement doit fonctionner correctement
        self.assertFalse(etat_apres_premiere_bascule, "Première bascule doit mettre en jeu")
        self.assertTrue(etat_apres_deuxieme_bascule, "Deuxième bascule doit remettre en pause")
        print("✅ Le basculement de pause fonctionne parfaitement")


def run_tests():
    """Lance les tests d'acceptance de pause par défaut au démarrage."""
    print("🎯 TESTS D'ACCEPTANCE - PAUSE PAR DÉFAUT AU DÉMARRAGE")
    print("=" * 60)
    print("Validation de la fonctionnalité :")
    print("- Démarrage en pause par défaut")
    print("- Basculement pause/jeu fonctionnel")
    print("- Respect des directives de développement")
    print("=" * 60)
    
    # Créer la suite de tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPauseParDefautAuDemarrage)
    
    # Exécuter les tests avec verbosité
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Résumé
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 TOUS LES TESTS D'ACCEPTANCE RÉUSSIS !")
        print("✅ La fonctionnalité pause par défaut est validée")
    else:
        print("❌ Certains tests ont échoué - Phase TDD RED confirmée")
        print(f"Échecs: {len(result.failures)}")
        print(f"Erreurs: {len(result.errors)}")
        for failure in result.failures:
            print(f"Échec: {failure[0]} - {failure[1]}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
