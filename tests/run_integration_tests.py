#!/usr/bin/env python3
"""
🎯 TETRIS - TESTS D'INTÉGRATION SEULEMENT
============================================================
Ce script lance uniquement les tests d'intégration du projet Tetris.
Il utilise une approche personnalisée pour découvrir et lancer les tests d'intégration.

Architecture des tests :
- Tests d'intégration : Validation de l'interaction entre composants (11 tests)
- Tests de bout en bout avec le moteur complet
- Utilise le système audio et graphique réel

Commandes :
  python tests/run_integration_tests.py   # Lancer tous les tests d'intégration
  python tests/integration/test_*.py      # Lancer un test spécifique
============================================================
"""

import sys
import os
import time
from pathlib import Path
import subprocess
import glob

# Configuration des chemins pour import des modules du projet
projet_racine = Path(__file__).parent.parent
sys.path.insert(0, str(projet_racine))

def afficher_entete():
    """Affiche l'en-tête des tests d'intégration."""
    print("🎯 TETRIS - TESTS D'INTÉGRATION")
    print("=" * 60)
    print("🔗 Tests ciblés : Validation de l'intégration des composants")
    print("📂 Répertoire : tests/integration/")
    print("🎯 Objectif : Tester les interactions entre modules")
    print("=" * 60)

def afficher_informations_environnement():
    """Affiche les informations sur l'environnement de test."""
    print(f"🐍 Python : {sys.version.split()[0]}")
    print(f"📁 Projet : {projet_racine}")
    print(f"🔧 Exécution : Scripts personnalisés")
    print("🎲 Moteur : PyGame + Audio + Moteur complet")
    print("=" * 60)

def decouvrir_fichiers_tests():
    """
    Découvre tous les fichiers de tests d'intégration.
    
    Returns:
        list: Liste des fichiers de test trouvés
    """
    repertoire_integration = projet_racine / "tests" / "integration"
    
    if not repertoire_integration.exists():
        print(f"❌ ERREUR : Répertoire de tests non trouvé : {repertoire_integration}")
        return []
    
    print(f"🔍 Découverte des tests dans : {repertoire_integration}")
    
    # Chercher tous les fichiers test_*.py
    pattern = str(repertoire_integration / "test_*.py")
    fichiers_tests = glob.glob(pattern)
    
    # Convertir en chemins relatifs pour l'affichage
    fichiers_relatifs = [Path(f).name for f in fichiers_tests]
    
    print(f"📊 {len(fichiers_relatifs)} fichiers de test découverts: {fichiers_relatifs}")
    
    return fichiers_tests

def executer_test_integration(fichier_test):
    """
    Exécute un fichier de test d'intégration spécifique.
    
    Args:
        fichier_test (str): Chemin vers le fichier de test
        
    Returns:
        tuple: (success, output, error)
    """
    nom_fichier = Path(fichier_test).name
    print(f"🔧 Exécution de {nom_fichier}")
    print("-" * 30)
    
    try:
        # Exécuter le test avec Python
        resultat = subprocess.run(
            [sys.executable, fichier_test],
            cwd=str(projet_racine),
            capture_output=True,
            text=True,
            timeout=30  # Timeout de 30 secondes
        )
        
        # Afficher la sortie
        if resultat.stdout:
            print(resultat.stdout)
        
        if resultat.stderr:
            print(f"⚠️  Erreurs/Avertissements :")
            print(resultat.stderr)
        
        success = resultat.returncode == 0
        return success, resultat.stdout, resultat.stderr
        
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT : {nom_fichier} a dépassé 30 secondes")
        return False, "", "Timeout"
    except Exception as e:
        print(f"❌ ERREUR lors de l'exécution de {nom_fichier} : {e}")
        return False, "", str(e)

def lancer_tous_les_tests():
    """
    Lance tous les tests d'intégration et collecte les résultats.
    
    Returns:
        tuple: (total, succès, échecs, durée)
    """
    fichiers_tests = decouvrir_fichiers_tests()
    
    if not fichiers_tests:
        print("⚠️  Aucun test d'intégration trouvé")
        return 0, 0, 0, 0
    
    print("=" * 60)
    print("🚀 EXÉCUTION DES TESTS D'INTÉGRATION")
    print("=" * 60)
    
    debut_execution = time.time()
    total_tests = len(fichiers_tests)
    tests_reussis = 0
    tests_echecs = 0
    resultats_details = []
    
    for fichier_test in fichiers_tests:
        success, output, error = executer_test_integration(fichier_test)
        
        nom_fichier = Path(fichier_test).name
        if success:
            tests_reussis += 1
            print(f"✅ {nom_fichier} - SUCCÈS")
        else:
            tests_echecs += 1
            print(f"❌ {nom_fichier} - ÉCHEC")
        
        resultats_details.append({
            'fichier': nom_fichier,
            'success': success,
            'output': output,
            'error': error
        })
        
        print()  # Ligne vide entre les tests
    
    duree_execution = time.time() - debut_execution
    
    return total_tests, tests_reussis, tests_echecs, duree_execution, resultats_details

def afficher_resume_resultats(total, succes, echecs, duree, details):
    """
    Affiche un résumé des résultats des tests.
    
    Args:
        total: Nombre total de tests
        succes: Nombre de tests réussis
        echecs: Nombre de tests échoués
        duree: Durée d'exécution en secondes
        details: Détails des résultats
    """
    print("=" * 60)
    print("🎯 RÉSUMÉ DES TESTS D'INTÉGRATION")
    print("=" * 60)
    
    print(f"Tests exécutés: {total}")
    print(f"✅ Succès: {succes}")
    print(f"❌ Échecs: {echecs}")
    
    if total > 0:
        taux_reussite = (succes / total) * 100
        print(f"🏆 Taux de réussite: {taux_reussite:.1f}%")
    
    print(f"⏱️  Durée: {duree:.3f}s")
    
    # Détails des catégories testées
    print("\n🎮 Catégories testées :")
    print("   • Intégration audio/moteur")
    print("   • Tests de partie complète")
    print("   • Interactions composants multiples")
    print("   • Tests de performance")
    
    # Afficher les détails des échecs s'il y en a
    if echecs > 0:
        print("\n💥 DÉTAILS DES ÉCHECS :")
        for detail in details:
            if not detail['success']:
                print(f"   • {detail['fichier']}: {detail['error'][:100]}...")
    
    # Statut final
    if echecs == 0:
        print("\n🎉 TOUS LES TESTS D'INTÉGRATION RÉUSSIS !")
        print("   L'intégration des composants est validée !")
        status_code = 0
    else:
        print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ")
        print("   L'intégration nécessite des corrections")
        status_code = 1
    
    return status_code

def main():
    """Fonction principale du script de tests d'intégration."""
    try:
        afficher_entete()
        afficher_informations_environnement()
        
        # Lancer les tests
        total, succes, echecs, duree, details = lancer_tous_les_tests()
        
        if total == 0:
            print("❌ Aucun test d'intégration trouvé")
            return 1
        
        # Afficher le résumé
        status_code = afficher_resume_resultats(total, succes, echecs, duree, details)
        
        return status_code
        
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrompus par l'utilisateur")
        return 1
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE : {e}")
        return 1

if __name__ == "__main__":
    # Exécuter et retourner le code de statut
    code_sortie = main()
    sys.exit(code_sortie)
