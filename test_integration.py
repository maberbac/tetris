#!/usr/bin/env python
"""Test d'intégration complet pour la fonctionnalité restart"""

import pygame
pygame.init()

from src.adapters.entree.gestionnaire_partie import GestionnairePartie
from src.domaine.services.moteur_partie import MoteurPartie

def test_integration_restart():
    """Test l'intégration complète du restart"""
    print("=== TEST D'INTÉGRATION RESTART ===")
    
    # Créer les instances
    moteur = MoteurPartie()
    gestionnaire = GestionnairePartie()
    
    # Forcer game over
    moteur.jeu_termine = True
    print(f"État initial - Game over: {moteur.est_game_over()}")
    print(f"Score initial: {moteur.stats.score}")
    
    # Simuler appui touche R
    from src.domaine.services.gestionnaire_evenements import TypeEvenement
    result = gestionnaire.traiter_evenement_clavier('r', TypeEvenement.CLAVIER_APPUI, moteur)
    
    print(f"Commande exécutée: {result}")
    print(f"État après R - Game over: {moteur.est_game_over()}")
    print(f"Score après restart: {moteur.stats.score}")
    
    # Vérifications
    if not moteur.est_game_over() and moteur.stats.score == 0:
        print("✅ RESTART FONCTIONNE PARFAITEMENT!")
        return True
    else:
        print("❌ Problème avec le restart")
        return False

if __name__ == "__main__":
    test_integration_restart()
