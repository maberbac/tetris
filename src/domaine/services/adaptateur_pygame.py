"""
Adaptateur Pygame - Bridge Pattern pour l'intégration avec Pygame

Ce module fait le pont entre les événements Pygame et notre gestionnaire
d'événements générique, permettant une architecture découplée.

Architecture :
- Bridge Pattern : Sépare l'abstraction (GestionnaireEvenements) de l'implémentation (Pygame)
- Adapter Pattern : Convertit l'interface Pygame vers notre interface
- Extensibilité : Facilite l'ajout d'autres bibliothèques graphiques
"""

import time
from typing import Dict, List, Optional, Union
from .gestionnaire_evenements import GestionnaireEvenements, TypeEvenement, MoteurJeu

# Import conditionnel de pygame pour éviter les erreurs si non installé
try:
    import pygame
    PYGAME_DISPONIBLE = True
except ImportError:
    PYGAME_DISPONIBLE = False
    pygame = None


class AdaptateurPygame:
    """
    Adaptateur pour intégrer Pygame avec notre gestionnaire d'événements.
    
    Responsabilités :
    - Convertir les événements Pygame en événements génériques
    - Gérer la boucle d'événements Pygame
    - Fournir une interface simple pour le moteur de jeu
    """
    
    # Mapping des touches Pygame vers nos noms génériques (simplifié)
    MAPPING_TOUCHES_PYGAME = {
        # Touches fléchées (contrôles principaux)
        pygame.K_LEFT: "Left" if PYGAME_DISPONIBLE else None,     # ← Gauche
        pygame.K_RIGHT: "Right" if PYGAME_DISPONIBLE else None,   # → Droite
        pygame.K_UP: "Up" if PYGAME_DISPONIBLE else None,         # ↑ Rotation
        pygame.K_DOWN: "Down" if PYGAME_DISPONIBLE else None,     # ↓ Chute rapide
        
        # Actions spéciales
        pygame.K_SPACE: "space" if PYGAME_DISPONIBLE else None,   # Space - Chute instantanée
        pygame.K_ESCAPE: "Escape" if PYGAME_DISPONIBLE else None, # Esc - Menu
        pygame.K_p: "p" if PYGAME_DISPONIBLE else None,           # P - Pause
    } if PYGAME_DISPONIBLE else {}
    
    def __init__(self, gestionnaire: Optional[GestionnaireEvenements] = None):
        """
        Initialise l'adaptateur Pygame.
        
        Args:
            gestionnaire: Gestionnaire d'événements (créé automatiquement si None)
            
        Raises:
            ImportError: Si Pygame n'est pas disponible
        """
        if not PYGAME_DISPONIBLE:
            raise ImportError("Pygame n'est pas installé. Utilisez: pip install pygame")
        
        self._gestionnaire = gestionnaire or GestionnaireEvenements()
        self._actif = False
        self._evenements_personnalises = {}
        
        # Initialiser Pygame si nécessaire
        if not pygame.get_init():
            pygame.init()
    
    @property
    def gestionnaire(self) -> GestionnaireEvenements:
        """Accès au gestionnaire d'événements."""
        return self._gestionnaire
    
    def demarrer(self) -> None:
        """Démarre la capture d'événements."""
        self._actif = True
    
    def arreter(self) -> None:
        """Arrête la capture d'événements."""
        self._actif = False
        self._gestionnaire.reinitialiser_touches_maintenues()
    
    def traiter_evenements(self, moteur: MoteurJeu) -> Dict[str, int]:
        """
        Traite tous les événements Pygame en attente.
        
        Args:
            moteur: Instance du moteur de jeu
            
        Returns:
            Dictionnaire avec les statistiques des événements traités
        """
        if not self._actif:
            return {"traites": 0, "ignores": 0, "erreurs": 0}
        
        stats = {"traites": 0, "ignores": 0, "erreurs": 0}
        temps_actuel = time.time()
        
        # Traiter les événements Pygame
        for evenement in pygame.event.get():
            try:
                if self._traiter_evenement_pygame(evenement, moteur, temps_actuel):
                    stats["traites"] += 1
                else:
                    stats["ignores"] += 1
            except Exception:
                stats["erreurs"] += 1
        
        # Mettre à jour la répétition des touches maintenues
        self._gestionnaire.mettre_a_jour_repetition(moteur, temps_actuel)
        
        return stats
    
    def _traiter_evenement_pygame(self, 
                                 evenement: 'pygame.event.Event', 
                                 moteur: MoteurJeu, 
                                 temps_actuel: float) -> bool:
        """
        Traite un événement Pygame spécifique.
        
        Args:
            evenement: Événement Pygame
            moteur: Instance du moteur de jeu
            temps_actuel: Temps actuel
            
        Returns:
            True si l'événement a été traité, False sinon
        """
        # Traiter les événements de clavier
        if evenement.type == pygame.KEYDOWN:
            return self._traiter_appui_touche(evenement.key, moteur, temps_actuel)
        elif evenement.type == pygame.KEYUP:
            return self._traiter_relache_touche(evenement.key, moteur, temps_actuel)
        elif evenement.type == pygame.QUIT:
            return self._traiter_fermeture(moteur)
        
        # Événements personnalisés
        if evenement.type in self._evenements_personnalises:
            return self._traiter_evenement_personnalise(evenement, moteur, temps_actuel)
        
        return False
    
    def _traiter_appui_touche(self, 
                             touche_pygame: int, 
                             moteur: MoteurJeu, 
                             temps_actuel: float) -> bool:
        """Traite l'appui d'une touche."""
        touche_generique = self.MAPPING_TOUCHES_PYGAME.get(touche_pygame)
        if not touche_generique:
            return False
        
        return self._gestionnaire.traiter_evenement_clavier(
            touche_generique, 
            TypeEvenement.CLAVIER_APPUI, 
            moteur, 
            temps_actuel
        )
    
    def _traiter_relache_touche(self, 
                               touche_pygame: int, 
                               moteur: MoteurJeu, 
                               temps_actuel: float) -> bool:
        """Traite le relâchement d'une touche."""
        touche_generique = self.MAPPING_TOUCHES_PYGAME.get(touche_pygame)
        if not touche_generique:
            return False
        
        return self._gestionnaire.traiter_evenement_clavier(
            touche_generique, 
            TypeEvenement.CLAVIER_RELACHE, 
            moteur, 
            temps_actuel
        )
    
    def _traiter_fermeture(self, moteur: MoteurJeu) -> bool:
        """Traite la fermeture de la fenêtre."""
        # Traiter comme une commande Menu (pour demander confirmation)
        return self._gestionnaire.traiter_evenement_clavier(
            "Escape", 
            TypeEvenement.CLAVIER_APPUI, 
            moteur
        )
    
    def _traiter_evenement_personnalise(self, 
                                       evenement: 'pygame.event.Event', 
                                       moteur: MoteurJeu, 
                                       temps_actuel: float) -> bool:
        """Traite un événement personnalisé."""
        handler = self._evenements_personnalises.get(evenement.type)
        if handler:
            return handler(evenement, moteur, temps_actuel)
        return False
    
    def ajouter_evenement_personnalise(self, 
                                      type_evenement: int, 
                                      handler: callable) -> None:
        """
        Ajoute un gestionnaire pour un événement personnalisé.
        
        Args:
            type_evenement: Type d'événement Pygame
            handler: Fonction de traitement (evenement, moteur, temps) -> bool
        """
        self._evenements_personnalises[type_evenement] = handler
    
    def supprimer_evenement_personnalise(self, type_evenement: int) -> None:
        """Supprime un gestionnaire d'événement personnalisé."""
        self._evenements_personnalises.pop(type_evenement, None)
    
    def ajouter_mapping_touche_pygame(self, touche_pygame: int, nom_generique: str) -> None:
        """
        Ajoute un mapping entre une touche Pygame et un nom générique.
        
        Args:
            touche_pygame: Constante de touche Pygame (ex: pygame.K_w)
            nom_generique: Nom générique de la touche (ex: "w")
        """
        self.MAPPING_TOUCHES_PYGAME[touche_pygame] = nom_generique
    
    def obtenir_touches_pressees(self) -> List[str]:
        """
        Retourne la liste des touches actuellement pressées.
        
        Returns:
            Liste des noms génériques des touches pressées
        """
        touches_pressees = []
        
        if PYGAME_DISPONIBLE:
            etat_clavier = pygame.key.get_pressed()
            
            for touche_pygame, nom_generique in self.MAPPING_TOUCHES_PYGAME.items():
                if etat_clavier[touche_pygame]:
                    touches_pressees.append(nom_generique)
        
        return touches_pressees
    
    def est_touche_pressee(self, nom_touche: str) -> bool:
        """
        Vérifie si une touche spécifique est actuellement pressée.
        
        Args:
            nom_touche: Nom générique de la touche
            
        Returns:
            True si la touche est pressée, False sinon
        """
        return nom_touche in self.obtenir_touches_pressees()
    
    def forcer_relachement_toutes_touches(self) -> None:
        """Force le relâchement de toutes les touches maintenues."""
        self._gestionnaire.reinitialiser_touches_maintenues()
    
    def statistiques(self) -> str:
        """Retourne des statistiques sur l'adaptateur."""
        nb_mappings = len(self.MAPPING_TOUCHES_PYGAME)
        nb_personnalises = len(self._evenements_personnalises)
        statut = "Actif" if self._actif else "Inactif"
        
        return (f"AdaptateurPygame - {statut}, "
                f"{nb_mappings} mappings touches, "
                f"{nb_personnalises} événements personnalisés")
