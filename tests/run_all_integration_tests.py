"""
Script de lancement des tests depuis la racine du projet.
"""

import os
import subprocess
import sys

def lancer_tests_integration():
    """Lance les tests d'intégration."""
    print("🧪 LANCEMENT DES TESTS D'INTÉGRATION")
    print("=" * 50)
    
    chemin_tests = os.path.join("integration", "test_partie_complete.py")
    
    if os.path.exists(chemin_tests):
        try:
            result = subprocess.run([sys.executable, chemin_tests], 
                                  capture_output=False, 
                                  text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Erreur lors du lancement des tests: {e}")
            return False
    else:
        print(f"❌ Fichier de test non trouvé: {chemin_tests}")
        return False

def main():
    """Point d'entrée principal."""
    print("🎯 TESTS TETRIS - Lanceur depuis la racine")
    print("=" * 50)
    
    if lancer_tests_integration():
        print("\n✅ Tous les tests sont passés !")
    else:
        print("\n❌ Certains tests ont échoué.")
        sys.exit(1)

if __name__ == "__main__":
    main()
