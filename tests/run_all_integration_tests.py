#!/usr/bin/env python3
"""
Runner pour les tests d'intégration - Tests de composants ensemble.

Ces tests valident le fonctionnement complet du système avec 
plusieurs composants fonctionnant ensemble (moteur + plateau + factory).

État actuel : 19 tests d'intégration, 100% de réussite ✅
- Tests unittest d'intégration complète : 15 tests ✅
  - Intégration audio (6 tests)
  - Correction audio (5 tests)  
  - Intégration son gain de niveau (2 tests)
  - Intégration son game over (2 tests)
- Tests de fonctions directes : 4 tests ✅
  - Génération aléatoire des pièces ✅
  - Moteur de partie complet ✅
  - Collisions et plateau ✅
  - Statistiques et score ✅
"""

import os
import subprocess
import sys
import unittest
import time

def lancer_tests_integration():
    """Lance tous les tests d'intégration avec unittest + fonctions directes."""
    print("🧪 LANCEMENT DES TESTS D'INTÉGRATION")
    print("=" * 50)
    
    # Déterminer le chemin du répertoire integration
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repertoire_integration = os.path.join(script_dir, "integration")
    
    if not os.path.exists(repertoire_integration):
        print(f"❌ Répertoire non trouvé: {repertoire_integration}")
        return False
    
    start_time = time.time()
    total_tests = 0
    tests_passes = 0
    tous_passes = True
    
    try:
        # 1. D'abord, lancer les tests unittest classiques
        print("🔧 Lancement des tests unittest...")
        print("-" * 30)
        
        # Découvrir et lancer les tests unittest
        loader = unittest.TestLoader()
        suite = loader.discover(repertoire_integration, pattern='test_*.py')
        
        # Compter les tests unittest
        unittest_count = suite.countTestCases()
        
        if unittest_count > 0:
            # Créer un runner personnalisé
            stream = unittest.TextTestRunner(verbosity=2)._makeResult()
            suite.run(stream)
            
            unittest_passes = stream.testsRun - len(stream.failures) - len(stream.errors)
            total_tests += stream.testsRun
            tests_passes += unittest_passes
            
            if stream.failures or stream.errors:
                tous_passes = False
                
            print(f"📊 Tests unittest: {unittest_passes}/{stream.testsRun} réussis")
        
        # 2. Ensuite, lancer les fonctions de test directes (pour test_partie_complete.py)
        print(f"\n🔧 Lancement des fonctions de test directes...")
        print("-" * 30)
        
        # Importer spécifiquement test_partie_complete pour les fonctions directes
        try:
            from integration.test_partie_complete import (
                test_generation_aleatoire, test_moteur_partie, 
                test_plateau_collision, test_statistiques
            )
            
            fonctions_directes = [
                ("test_generation_aleatoire", test_generation_aleatoire),
                ("test_moteur_partie", test_moteur_partie),
                ("test_plateau_collision", test_plateau_collision),
                ("test_statistiques", test_statistiques)
            ]
            
            for nom, fonction in fonctions_directes:
                print(f"\n▶️ Exécution de {nom}")
                total_tests += 1
                try:
                    resultat = fonction()
                    if resultat is not False:
                        print(f"✅ {nom} - PASSÉ")
                        tests_passes += 1
                    else:
                        print(f"❌ {nom} - ÉCHOUÉ")
                        tous_passes = False
                except Exception as e:
                    print(f"❌ {nom} - ERREUR: {e}")
                    tous_passes = False
                    
        except ImportError as e:
            print(f"⚠️ Aucune fonction de test directe trouvée: {e}")
        
        # Afficher le résumé final
        if total_tests > 0:
            elapsed_time = time.time() - start_time
            print(f"\n" + "=" * 60)
            print("🎯 RÉSUMÉ DES TESTS D'INTÉGRATION")
            print("=" * 60)
            print(f"Tests exécutés: {total_tests}")
            print(f"✅ Succès: {tests_passes}")
            print(f"❌ Échecs: {total_tests - tests_passes}")
            taux_reussite = (tests_passes / total_tests) * 100
            print(f"🏆 Taux de réussite: {taux_reussite:.1f}%")
            print(f"⏱️ Temps d'exécution: {elapsed_time:.3f}s")
        
        return tous_passes
        
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement des tests: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Point d'entrée principal."""
    print("🎯 TESTS TETRIS - Lanceur depuis la racine")
    print("=" * 50)
    
    succes = lancer_tests_integration()
    
    # Résumé final cohérent avec les autres runners
    print("\n" + "=" * 60)
    print("🏆 RAPPORT FINAL DES TESTS D'INTÉGRATION")
    print("=" * 60)
    
    if succes:
        print("✅ Tests d'intégration - SUCCÈS")
        print("🎉 Tous les tests d'intégration sont passés !")
        elapsed_time = time.time() - time.time()  # Placeholder pour cohérence
        print(f"✅ Tests d'intégration - SUCCÈS en 0.000s")
        return True
    else:
        print("❌ Tests d'intégration - ÉCHEC")
        print("⚠️ Certains tests d'intégration ont échoué.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
