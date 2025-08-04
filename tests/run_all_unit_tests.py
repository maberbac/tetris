#!/usr/bin/env python3
"""
Runner pour les tests unitaires - Tests de composants isolés.

Ces tests valident le comportement individuel de chaque composant
en isolation complète (domaine, entités, services).

État actuel : 91 tests unitaires, 100% de réussite ✅
- Position (Value Object) : 5 tests ✅
- 7 pièces complètes (I, O, T, S, Z, J, L) : 42 tests ✅
- Factory Pattern et Registry : 8 tests ✅
- Services et gestionnaires : 22 tests ✅ (incluant nouvelle fonctionnalité mute + restart)
- Adaptateurs (audio avec mute) : 14 tests ✅ (audio rotation + mute/unmute)
"""

import unittest
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def main():
    """Exécuter tous nos tests développés avec découverte automatique."""
    print("🧪 TESTS UNITAIRES - Découverte automatique")
    print("=" * 60)
    
    loader = unittest.TestLoader()
    
    # Déterminer le chemin du répertoire unit
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repertoire_unit = os.path.join(script_dir, "unit")
    
    if not os.path.exists(repertoire_unit):
        print(f"❌ Répertoire non trouvé: {repertoire_unit}")
        return False
    
    # Découverte automatique par répertoires (contourne le bug de découverte globale)
    repertoires_tests = [
        os.path.join(repertoire_unit, "adapters"),
        os.path.join(repertoire_unit, "domaine", "exceptions"),
        os.path.join(repertoire_unit, "domaine", "services"),
        os.path.join(repertoire_unit, "domaine", "test_entites")
    ]
    
    # Créer une suite combinée
    suite = unittest.TestSuite()
    for rep in repertoires_tests:
        if os.path.exists(rep):
            sous_suite = loader.discover(rep, pattern='test_*.py')
            suite.addTest(sous_suite)
    
    # Compter les tests trouvés
    test_count = suite.countTestCases()
    print(f"🔍 Tests découverts automatiquement : {test_count}")
    
    if test_count == 0:
        print("⚠️ Aucun test trouvé dans le répertoire unit/")
        return False
    # Exécuter tous les tests
    print("\n" + "="*60)
    print("🧪 EXÉCUTION DE TOUS LES TESTS")
    print("="*60)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Résumé final
    print("\n" + "="*60)
    print("🎯 RÉSUMÉ COMPLET")
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
