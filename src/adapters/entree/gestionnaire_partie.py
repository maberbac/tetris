"""
Adaptateur d'entrée pygame pour contrôler la partie de Tetris.

Implémentation concrète utilisant pygame pour la gestion des événements.
"""

import pygame
import time
from typing import TYPE_CHECKING

from src.domaine.services.gestionnaire_evenements import GestionnaireEvenements, TypeEvenement, ToucheClavier
from src.domaine.services.commandes.commandes_partie import (
    CommandePlacerPiecePartie, CommandeChuteRapidePartie, CommandeDeplacerGauchePartie,
    CommandeDeplacerDroitePartie, CommandeTournerPartie
)
from src.ports.entree.controleur_jeu import ControleurJeu

if TYPE_CHECKING:
    from src.domaine.services.moteur_partie import MoteurPartie


def convertir_touche_pygame(touche_pygame: int) -> str:
    """Convertit une touche pygame en nom de touche pour le gestionnaire."""
    mapping_pygame = {
        pygame.K_LEFT: "Left",
        pygame.K_RIGHT: "Right", 
        pygame.K_UP: "Up",
        pygame.K_DOWN: "Down",
        pygame.K_SPACE: "space",
        pygame.K_p: "p",
        pygame.K_m: "m",
    }
    return mapping_pygame.get(touche_pygame, "")


class GestionnairePartie(GestionnaireEvenements, ControleurJeu):
    """Gestionnaire d'événements pygame pour la partie complète."""
    
    def _creer_commandes(self):
        """Crée le mapping des commandes pour la partie."""
        from src.domaine.services.commandes import (
            CommandeDescendre, CommandePause, CommandeBasculerMute
        )
        
        return {
            ToucheClavier.GAUCHE: CommandeDeplacerGauchePartie(),
            ToucheClavier.DROITE: CommandeDeplacerDroitePartie(),
            ToucheClavier.ROTATION: CommandeTournerPartie(),
            ToucheClavier.CHUTE_RAPIDE: CommandeDescendre(),
            ToucheClavier.CHUTE_INSTANTANEE: CommandeChuteRapidePartie(),
            ToucheClavier.PAUSE: CommandePause(),
            ToucheClavier.MUTE: CommandeBasculerMute(),
        }
    
    def traiter_evenements(self, moteur: 'MoteurPartie', temps_actuel: float) -> bool:
        """
        Traite les événements pygame.
        
        Returns:
            bool: True si le jeu doit continuer, False pour quitter
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                nom_touche = convertir_touche_pygame(event.key)
                if nom_touche:
                    self.traiter_evenement_clavier(
                        nom_touche,
                        TypeEvenement.CLAVIER_APPUI,
                        moteur,
                        temps_actuel
                    )
                    
                    # Gestion spéciale pour P
                    if nom_touche == "p":
                        moteur.basculer_pause()
            
            elif event.type == pygame.KEYUP:
                nom_touche = convertir_touche_pygame(event.key)
                if nom_touche:
                    self.traiter_evenement_clavier(
                        nom_touche,
                        TypeEvenement.CLAVIER_RELACHE,
                        moteur,
                        temps_actuel
                    )
        
        return True
    
    def mettre_a_jour_repetitions(self, moteur: 'MoteurPartie', temps_actuel: float) -> None:
        """Met à jour les répétitions des touches."""
        self.mettre_a_jour_repetition(moteur, temps_actuel)
