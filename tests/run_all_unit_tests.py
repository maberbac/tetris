#!/usr/bin/env python3
"""
Script pour exécuter tous nos tests et avoir un résumé complet.
"""

import unittest
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def main():
    """Exécuter tous nos tests développés."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Charger tous nos modules de tests
    modules_tests = [
        'tests.test_domaine.test_entites.test_position',
        'tests.test_domaine.test_entites.test_pieces.test_piece_i',
        'tests.test_domaine.test_entites.test_pieces.test_piece_o', 
        'tests.test_domaine.test_entites.test_pieces.test_piece_t',
        'tests.test_domaine.test_entites.test_pieces.test_piece_s',  # ← Nouvelle pièce S
        'tests.test_domaine.test_entites.test_pieces.test_piece_z',  # ← Nouvelle pièce Z
        'tests.test_domaine.test_entites.test_pieces.test_piece_j',  # ← Nouvelle pièce J
        'tests.test_domaine.test_entites.test_pieces.test_piece_l',  # ← Nouvelle pièce L
        'tests.test_domaine.test_entites.test_fabriques.test_registre_pieces',
        'tests.test_domaine.test_entites.test_fabriques.test_fabrique_pieces',
    ]
    
    for module in modules_tests:
        try:
            suite.addTests(loader.loadTestsFromName(module))
            print(f"✅ Module chargé : {module}")
        except Exception as e:
            print(f"❌ Erreur lors du chargement de {module} : {e}")
    
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
