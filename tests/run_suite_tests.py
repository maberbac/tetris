"""
Script principal pour exécuter la suite complète de tests Tetris.
Exécute tous les types de tests dans l'ordre optimal.

État actuel du projet :
- 75 tests unitaires : Domaine, entités, services, zone invisible (100% ✅)
- 22 tests d'acceptance : Scénarios utilisateur + corrections de bugs (100% ✅)
- 4 tests d'intégration : Système complet avec audio (100% ✅)
Total : 101 tests, 101/101 réussis (100% ✅)
"""

import os
import subprocess
import sys
import time

def executer_script_test(nom_script, description):
    """Exécute un script de test et retourne le résultat."""
    print(f"\n🚀 EXÉCUTION : {description}")
    print("=" * 60)
    
    chemin_script = os.path.join(os.path.dirname(__file__), nom_script)
    
    if not os.path.exists(chemin_script):
        print(f"❌ Script non trouvé : {nom_script}")
        return False
    
    try:
        debut = time.time()
        result = subprocess.run([sys.executable, chemin_script], 
                              capture_output=False, 
                              text=True,
                              cwd=os.path.dirname(__file__))
        
        duree = time.time() - debut
        
        if result.returncode == 0:
            print(f"✅ {description} - SUCCÈS en {duree:.3f}s")
            return True
        else:
            print(f"❌ {description} - ÉCHEC (code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution de {nom_script}: {e}")
        return False

def main():
    """Point d'entrée principal - Exécute toute la suite de tests."""
    print("🎮 TETRIS - SUITE COMPLÈTE DE TESTS")
    print("=" * 60)
    print("📋 Ordre d'exécution :")
    print("   1. Tests unitaires")
    print("   2. Tests d'acceptance") 
    print("   3. Tests d'intégration")
    print("=" * 60)
    
    debut_total = time.time()
    
    # Définition des tests à exécuter dans l'ordre
    tests_a_executer = [
        ("run_all_unit_tests.py", "Tests unitaires"),
        ("run_all_acceptance_tests.py", "Tests d'acceptance"),
        ("run_all_integration_tests.py", "Tests d'intégration")
    ]
    
    resultats = []
    
    # Exécution séquentielle de tous les tests
    for script, description in tests_a_executer:
        succes = executer_script_test(script, description)
        resultats.append((description, succes))
        
        # Note: Continuer même en cas d'échec pour avoir un rapport complet
        if not succes:
            print(f"\n⚠️ ATTENTION : Échec dans {description} - Continuation pour rapport complet")
    
    # Rapport final
    duree_totale = time.time() - debut_total
    print("\n" + "=" * 60)
    print("🏆 RAPPORT FINAL DE LA SUITE DE TESTS")
    print("=" * 60)
    
    tests_reussis = sum(1 for _, succes in resultats if succes)
    tests_totaux = len(resultats)
    
    for description, succes in resultats:
        statut = "✅ RÉUSSI" if succes else "❌ ÉCHOUÉ"
        print(f"   {description:<20} : {statut}")
    
    print("-" * 60)
    print(f"📊 Résultats : {tests_reussis}/{tests_totaux} catégories réussies")
    print(f"⏱️  Temps total : {duree_totale:.3f}s")
    
    if tests_reussis == tests_totaux:
        print("🎉 SUITE DE TESTS COMPLÈTE - TOUS LES TESTS RÉUSSIS !")
        sys.exit(0)
    else:
        print("💥 SUITE DE TESTS ÉCHOUÉE - Des corrections sont nécessaires")
        sys.exit(1)

if __name__ == "__main__":
    main()
