#!/usr/bin/env python3
"""
Runner pour les tests d'acceptance - Tests de comportement utilisateur.

Ces tests valident que le jeu répond correctement aux actions
de l'utilisateur et aux scénarios d'usage réels.

État actuel : 22 tests d'acceptance incluant les corrections de bugs :
- Contrôles et gameplay (100% ✅)
- Corrections bug lignes multiples ✅ 
- Corrections bug game over prématuré ✅
- Tests bug visuel ligne complète ✅
"""

import unittest
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def main():
    """Exécuter tous les tests d'acceptance."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Charger tous les modules de tests d'acceptance
    modules_tests = [
        'tests.acceptance.test_controles_rapide',
        'tests.acceptance.test_controles_simplifies',
        'tests.acceptance.test_descente_acceleree',
        'tests.acceptance.test_bug_visuel_ligne_complete',
        'tests.acceptance.test_correction_bug_lignes_multiples',      # ✅ Correction bug lignes multiples
        'tests.acceptance.test_correction_bug_gameover_premature',    # ✅ Correction bug game over prématuré
    ]
    
    print("🎭 TESTS D'ACCEPTANCE - Comportement utilisateur")
    print("=" * 60)
    
    for module in modules_tests:
        try:
            suite.addTests(loader.loadTestsFromName(module))
            print(f"✅ Module chargé : {module}")
        except Exception as e:
            print(f"❌ Erreur lors du chargement de {module} : {e}")
    
    # Exécuter tous les tests
    print("\n" + "="*60)
    print("🎮 EXÉCUTION DES TESTS D'ACCEPTANCE")
    print("="*60)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Résumé final
    print("\n" + "="*60)
    print("🎯 RÉSUMÉ DES TESTS D'ACCEPTANCE")
    print("="*60)
    print(f"Tests exécutés: {result.testsRun}")
    print(f"✅ Succès: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Échecs: {len(result.failures)}")
    print(f"⚠️  Erreurs: {len(result.errors)}")
    
    if result.failures:
        print("\n📋 DÉTAILS DES ÉCHECS:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n📋 DÉTAILS DES ERREURS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"\n🏆 Taux de réussite: {success_rate:.1f}%")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
