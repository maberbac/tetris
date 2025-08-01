#!/usr/bin/env python3
"""
Runner principal pour tous les tests du projet Tetris.
"""

import unittest
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("🎮 TETRIS - SUITE COMPLÈTE DE TESTS")
print("=" * 60)

# Tests unitaires
print("\n🧪 TESTS UNITAIRES")
print("-" * 40)

loader = unittest.TestLoader()
suite = unittest.TestSuite()

# Modules de tests unitaires
modules_unitaires = [
    'tests.unit.domaine.test_entites.test_position',
    'tests.unit.domaine.test_entites.test_pieces.test_piece_i',
    'tests.unit.domaine.test_entites.test_pieces.test_piece_o', 
    'tests.unit.domaine.test_entites.test_pieces.test_piece_t',
    'tests.unit.domaine.test_entites.test_pieces.test_piece_s',
    'tests.unit.domaine.test_entites.test_pieces.test_piece_z',
    'tests.unit.domaine.test_entites.test_pieces.test_piece_j',
    'tests.unit.domaine.test_entites.test_pieces.test_piece_l',
    'tests.unit.domaine.test_entites.test_fabriques.test_registre_pieces',
    'tests.unit.domaine.test_entites.test_fabriques.test_fabrique_pieces',
    'tests.unit.domaine.services.test_gestionnaire_evenements',
]

for module in modules_unitaires:
    try:
        suite.addTests(loader.loadTestsFromName(module))
        print(f"✅ {module}")
    except Exception as e:
        print(f"❌ {module}: {str(e)[:100]}...")

# Tests d'intégration
print("\n🔗 TESTS D'INTÉGRATION")
print("-" * 40)

modules_integration = [
    'tests.integration.test_partie_complete',
]

for module in modules_integration:
    try:
        suite.addTests(loader.loadTestsFromName(module))
        print(f"✅ {module}")
    except Exception as e:
        print(f"❌ {module}: {str(e)[:100]}...")

# Tests d'acceptance
print("\n🎭 TESTS D'ACCEPTANCE")
print("-" * 40)

modules_acceptance = [
    'tests.acceptance.test_controles_rapide',
    'tests.acceptance.test_controles_simplifies',
]

for module in modules_acceptance:
    try:
        suite.addTests(loader.loadTestsFromName(module))
        print(f"✅ {module}")
    except Exception as e:
        print(f"❌ {module}: {str(e)[:100]}...")

# Exécution des tests
print("\n" + "=" * 60)
print("🚀 EXÉCUTION DES TESTS")
print("=" * 60)

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# Rapport final
print("\n" + "=" * 60)
print("🏆 RAPPORT FINAL")
print("=" * 60)

total_tests = result.testsRun
total_successes = result.testsRun - len(result.failures) - len(result.errors)
total_failures = len(result.failures)
total_errors = len(result.errors)

print(f"📋 Total tests: {total_tests}")
print(f"✅ Succès: {total_successes}")
print(f"❌ Échecs: {total_failures}")
print(f"⚠️  Erreurs: {total_errors}")

if total_tests > 0:
    success_rate = (total_successes / total_tests) * 100
    print(f"🎯 Taux de réussite: {success_rate:.1f}%")

if result.wasSuccessful():
    print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
else:
    print("\n⚠️  CERTAINS TESTS ONT ÉCHOUÉ")

print("=" * 60)
