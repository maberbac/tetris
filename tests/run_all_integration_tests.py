"""
Script de lancement de tous les tests d'intégration.

Tests d'intégration validant le fonctionnement complet du système :
- Génération aléatoire des pièces
- Moteur de partie complet
- Collisions et plateau
- Statistiques et audio
État actuel : 4 tests d'intégration, 100% de réussite ✅
"""

import os
import subprocess
import sys
import unittest

def lancer_tests_integration():
    """Lance tous les tests d'intégration."""
    print("🧪 LANCEMENT DES TESTS D'INTÉGRATION")
    print("=" * 50)
    
    # Déterminer le chemin du répertoire integration
    # Le script peut être lancé depuis la racine ou depuis tests/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repertoire_integration = os.path.join(script_dir, "integration")
    
    if not os.path.exists(repertoire_integration):
        print(f"❌ Répertoire non trouvé: {repertoire_integration}")
        return False
    
    try:
        # Découvrir tous les fichiers de test dans le répertoire
        fichiers_test = []
        for fichier in os.listdir(repertoire_integration):
            if fichier.startswith('test_') and fichier.endswith('.py'):
                fichiers_test.append(fichier)
        
        print(f"📊 {len(fichiers_test)} fichiers de test découverts: {fichiers_test}")
        
        if not fichiers_test:
            print("⚠️ Aucun fichier de test d'intégration trouvé")
            return True
        
        # Exécuter chaque fichier de test
        tous_passes = True
        total_tests = 0
        tests_passes = 0
        
        for fichier in fichiers_test:
            print(f"\n🔧 Exécution de {fichier}")
            print("-" * 30)
            
            try:
                # Importer dynamiquement le module
                nom_module = fichier[:-3]  # Enlever .py
                module_path = f"integration.{nom_module}"
                module = __import__(module_path, fromlist=[nom_module])
                
                # Trouver toutes les fonctions de test dans le module
                fonctions_test = [nom for nom in dir(module) if nom.startswith('test_')]
                print(f"🔍 Fonctions de test trouvées: {fonctions_test}")
                
                # Exécuter chaque fonction de test
                for nom_fonction in fonctions_test:
                    print(f"\n▶️ Exécution de {nom_fonction}")
                    fonction = getattr(module, nom_fonction)
                    total_tests += 1
                    try:
                        resultat = fonction()
                        if resultat is not False:  # Considérer True ou None comme succès
                            print(f"✅ {nom_fonction} - PASSÉ")
                            tests_passes += 1
                        else:
                            print(f"❌ {nom_fonction} - ÉCHOUÉ")
                            tous_passes = False
                    except Exception as e:
                        print(f"❌ {nom_fonction} - ERREUR: {e}")
                        tous_passes = False
                        
            except Exception as e:
                print(f"❌ Erreur lors de l'import de {fichier}: {e}")
                tous_passes = False
        
        # Afficher le résumé des tests
        if total_tests > 0:
            print(f"\n" + "=" * 60)
            print("🎯 RÉSUMÉ DES TESTS D'INTÉGRATION")
            print("=" * 60)
            print(f"Tests exécutés: {total_tests}")
            print(f"✅ Succès: {tests_passes}")
            print(f"❌ Échecs: {total_tests - tests_passes}")
            if total_tests > 0:
                taux_reussite = (tests_passes / total_tests) * 100
                print(f"🏆 Taux de réussite: {taux_reussite:.1f}%")
        
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
        return True
    else:
        print("❌ Tests d'intégration - ÉCHEC")
        print("⚠️ Certains tests d'intégration ont échoué.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
