"""
Script de lancement de tous les tests d'intégration.
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
                print(f"� Fonctions de test trouvées: {fonctions_test}")
                
                # Exécuter chaque fonction de test
                for nom_fonction in fonctions_test:
                    print(f"\n▶️ Exécution de {nom_fonction}")
                    fonction = getattr(module, nom_fonction)
                    try:
                        resultat = fonction()
                        if resultat is not False:  # Considérer True ou None comme succès
                            print(f"✅ {nom_fonction} - PASSÉ")
                        else:
                            print(f"❌ {nom_fonction} - ÉCHOUÉ")
                            tous_passes = False
                    except Exception as e:
                        print(f"❌ {nom_fonction} - ERREUR: {e}")
                        tous_passes = False
                        
            except Exception as e:
                print(f"❌ Erreur lors de l'import de {fichier}: {e}")
                tous_passes = False
        
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
    
    if lancer_tests_integration():
        print("\n✅ Tous les tests sont passés !")
    else:
        print("\n❌ Certains tests ont échoué.")
        sys.exit(1)

if __name__ == "__main__":
    main()
