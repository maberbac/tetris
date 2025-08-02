#!/usr/bin/env python3
"""
🎭 TETRIS - TESTS D'ACCEPTANCE SEULEMENT
============================================================
Ce script lance uniquement les tests d'acceptance du projet Tetris.
Il utilise une approche de découverte manuelle pour les modules de test d'acceptance.

Architecture des tests :
- Tests d'acceptance : Validation du comportement utilisateur (22 tests)
- Tests comportementaux focalisés sur l'expérience utilisateur
- Utilise le moteur de jeu réel pour valider les scénarios

Commandes :
  python tests/run_acceptance_tests.py    # Lancer tous les tests d'acceptance
  python -m pytest tests/acceptance/      # Alternative avec pytest
============================================================
"""

import sys
import os
import unittest
import time
from pathlib import Path

# Configuration des chemins pour import des modules du projet
projet_racine = Path(__file__).parent.parent
sys.path.insert(0, str(projet_racine))

def afficher_entete():
    """Affiche l'en-tête des tests d'acceptance."""
    print("🎭 TETRIS - TESTS D'ACCEPTANCE")
    print("=" * 60)
    print("🎮 Tests ciblés : Validation du comportement utilisateur")
    print("📂 Répertoire : tests/acceptance/")
    print("🎯 Objectif : Tester les scénarios d'usage réels")
    print("=" * 60)

def afficher_informations_environnement():
    """Affiche les informations sur l'environnement de test."""
    print(f"🐍 Python : {sys.version.split()[0]}")
    print(f"📁 Projet : {projet_racine}")
    print(f"🔧 Framework : unittest (Python standard)")
    print("🎲 Moteur : PyGame + Moteur Tetris réel")
    print("=" * 60)

def decouvrir_et_lancer_tests():
    """
    Découvre et lance tous les tests d'acceptance.
    
    Returns:
        tuple: (résultats, durée) ou None si erreur
    """
    # Découvrir les tests dans le répertoire acceptance
    repertoire_tests = projet_racine / "tests" / "acceptance"
    
    if not repertoire_tests.exists():
        print(f"❌ ERREUR : Répertoire de tests non trouvé : {repertoire_tests}")
        return None
    
    print(f"🔍 Découverte des tests dans : {repertoire_tests}")
    
    # Configuration du découvreur de tests
    decouvreur = unittest.TestLoader()
    
    try:
        # Découvrir tous les tests d'acceptance
        suite_tests = decouvreur.discover(
            start_dir=str(repertoire_tests),
            pattern='test_*.py',
            top_level_dir=str(projet_racine)
        )
        
        # Compter les tests
        nombre_tests = suite_tests.countTestCases()
        print(f"📊 Tests découverts : {nombre_tests}")
        
        if nombre_tests == 0:
            print("⚠️  Aucun test trouvé dans le répertoire acceptance/")
            return None
        
        print("=" * 60)
        print("🚀 EXÉCUTION DES TESTS D'ACCEPTANCE")
        print("=" * 60)
        
        # Lancer les tests avec plus de verbosité
        executeur = unittest.TextTestRunner(
            verbosity=2,
            stream=sys.stdout,
            buffer=True  # Capture les sorties print des tests
        )
        
        debut_execution = time.time()
        resultats = executeur.run(suite_tests)
        duree_execution = time.time() - debut_execution
        
        return resultats, duree_execution
        
    except Exception as e:
        print(f"❌ ERREUR lors de la découverte des tests : {e}")
        return None

def afficher_resume_resultats(resultats, duree):
    """
    Affiche un résumé des résultats des tests.
    
    Args:
        resultats: Résultats des tests unittest
        duree: Durée d'exécution en secondes
    """
    print("=" * 60)
    print("🎯 RÉSUMÉ DES TESTS D'ACCEPTANCE")
    print("=" * 60)
    
    total_tests = resultats.testsRun
    erreurs = len(resultats.errors)
    echecs = len(resultats.failures)
    ignores = len(getattr(resultats, 'skipped', []))
    succes = total_tests - erreurs - echecs
    
    print(f"Tests exécutés: {total_tests}")
    print(f"✅ Succès: {succes}")
    print(f"❌ Échecs: {echecs}")
    print(f"⚠️  Erreurs: {erreurs}")
    
    if ignores > 0:
        print(f"⏭️  Ignorés: {ignores}")
    
    if total_tests > 0:
        taux_reussite = (succes / total_tests) * 100
        print(f"🏆 Taux de réussite: {taux_reussite:.1f}%")
    
    print(f"⏱️  Durée: {duree:.3f}s")
    
    # Détails des catégories testées
    print("\n🎮 Catégories testées :")
    print("   • Contrôles utilisateur (clavier)")
    print("   • Comportements visuels")
    print("   • Corrections de bugs")
    print("   • Scénarios de jeu réels")
    
    # Statut final
    if echecs == 0 and erreurs == 0:
        print("\n🎉 TOUS LES TESTS D'ACCEPTANCE RÉUSSIS !")
        print("   L'expérience utilisateur est validée !")
        status_code = 0
    else:
        print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ")
        print("   L'expérience utilisateur nécessite des corrections")
        status_code = 1
    
    return status_code

def main():
    """Fonction principale du script de tests d'acceptance."""
    try:
        afficher_entete()
        afficher_informations_environnement()
        
        # Lancer les tests
        resultats_et_duree = decouvrir_et_lancer_tests()
        
        if resultats_et_duree is None:
            print("❌ Impossible d'exécuter les tests")
            return 1
        
        resultats, duree = resultats_et_duree
        
        # Afficher le résumé
        status_code = afficher_resume_resultats(resultats, duree)
        
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
