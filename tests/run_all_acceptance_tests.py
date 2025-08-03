#!/usr/bin/env python3
"""
Runner pour les tests d'acceptance - Tests de comportement utilisateur.

Ces tests valident que le jeu répond correctement aux actions
de l'utilisateur et aux scénarios d'usage réels.

État actuel : 64 tests d'acceptance incluant les corrections de bugs :
- Contrôles et gameplay (100% ✅)
- Corrections bug lignes multiples ✅ 
- Corrections bug game over prématuré ✅
- Tests bug visuel ligne complète ✅
- Nouvelle fonctionnalité mute/unmute ✅
- Tests son gain de niveau ✅
- Tests son game over ✅
- Tests correction bugs divers ✅
"""

import unittest
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def main():
    """Exécuter tous les tests d'acceptance avec découverte automatique."""
    print("🎭 TESTS D'ACCEPTANCE - Découverte automatique")
    print("=" * 60)
    
    loader = unittest.TestLoader()
    
    # Déterminer le chemin du répertoire acceptance
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repertoire_acceptance = os.path.join(script_dir, "acceptance")
    
    if not os.path.exists(repertoire_acceptance):
        print(f"❌ Répertoire non trouvé: {repertoire_acceptance}")
        return False
    
    # Découverte automatique de tous les tests d'acceptance
    suite = loader.discover(repertoire_acceptance, pattern='test_*.py')
    
    # Compter les tests trouvés
    test_count = suite.countTestCases()
    print(f"🔍 Tests découverts automatiquement : {test_count}")
    
    if test_count == 0:
        print("⚠️ Aucun test trouvé dans le répertoire acceptance/")
        return False
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
