"""
Gestionnaire d'Événements - Input Handler pour Tetris

Ce module gère les événements d'entrée (clavier, souris) et les convertit
en commandes exécutables par le moteur de jeu.

Architecture :
- Observer Pattern pour les événements
- Command Pattern pour les actions
- Configuration flexible des contrôles
- Support multi-plateforme
"""

from enum import Enum
from typing import Dict, Optional, List, Callable
from .commandes import (
    Commande, CommandeDeplacerGauche, CommandeDeplacerDroite,
    CommandeDescendre, CommandeChuteRapide, CommandeTourner,
    CommandePause, CommandeAfficherMenu, CommandeBasculerMute, MoteurJeu
)


class TypeEvenement(Enum):
    """Types d'événements d'entrée supportés."""
    CLAVIER_APPUI = "clavier_appui"
    CLAVIER_RELACHE = "clavier_relache"
    CLAVIER_MAINTENU = "clavier_maintenu"


class ToucheClavier(Enum):
    """
    Enumération des touches de contrôle simplifiées.
    
    Contrôles essentiels seulement pour une expérience fluide.
    """
    GAUCHE = "gauche"             # ← Déplacer vers la gauche
    DROITE = "droite"             # → Déplacer vers la droite  
    ROTATION = "rotation"         # ↑ Tourner la pièce
    CHUTE_RAPIDE = "chute_rapide" # ↓ Chute rapide (une ligne par frame)
    CHUTE_INSTANTANEE = "chute_instantanee"  # Space - Chute jusqu'en bas
    MENU = "menu"                 # Esc - Afficher le menu en jeu
    PAUSE = "pause"               # P - Pause/Reprendre
    MUTE = "mute"                 # M - Basculer mute/unmute musique


class ConfigurationControles:
    """
    Configuration des contrôles simplifiée.
    
    Mapping intuitif et minimaliste pour une expérience de jeu fluide.
    """
    
    # Configuration simplifiée (touches essentielles uniquement)
    MAPPING_DEFAUT = {
        # Touches fléchées (contrôles principaux)
        "Left": ToucheClavier.GAUCHE,           # ← Déplacer gauche
        "Right": ToucheClavier.DROITE,          # → Déplacer droite
        "Up": ToucheClavier.ROTATION,           # ↑ Tourner
        "Down": ToucheClavier.CHUTE_RAPIDE,     # ↓ Chute rapide
        
        # Actions spéciales
        "space": ToucheClavier.CHUTE_INSTANTANEE,  # Space - Chute instantanée
        "Escape": ToucheClavier.MENU,              # Esc - Menu en jeu
        "p": ToucheClavier.PAUSE,                  # P - Pause/Reprendre
        "m": ToucheClavier.MUTE,                   # M - Mute/Unmute musique
    }
    
    @classmethod
    def obtenir_mapping_defaut(cls) -> Dict[str, ToucheClavier]:
        """Retourne le mapping par défaut."""
        return cls.MAPPING_DEFAUT.copy()


class GestionnaireEvenements:
    """
    Gestionnaire principal des événements d'entrée.
    
    Responsabilités :
    - Capturer les événements de la bibliothèque graphique
    - Les convertir en touches logiques
    - Créer les commandes appropriées
    - Gérer la répétition des touches
    """
    
    def __init__(self, mapping_touches: Optional[Dict[str, ToucheClavier]] = None):
        """
        Initialise le gestionnaire avec un mapping de touches.
        
        Args:
            mapping_touches: Mapping personnalisé des touches (optionnel)
        """
        self._mapping_touches = mapping_touches or ConfigurationControles.obtenir_mapping_defaut()
        self._commandes: Dict[ToucheClavier, Commande] = self._creer_commandes()
        self._touches_repetables = {
            ToucheClavier.GAUCHE, ToucheClavier.DROITE, ToucheClavier.CHUTE_RAPIDE
        }
        
        # Gestion de la répétition (délais optimisés pour le gameplay)
        self._touches_maintenues: Dict[ToucheClavier, float] = {}
        self._delai_repetition = 0.12  # 120ms entre les répétitions (plus rapide)
        self._delai_initial = 0.20     # 200ms avant la première répétition (plus court)
    
    def _creer_commandes(self) -> Dict[ToucheClavier, Commande]:
        """Crée le mapping entre touches logiques et commandes."""
        return {
            ToucheClavier.GAUCHE: CommandeDeplacerGauche(),
            ToucheClavier.DROITE: CommandeDeplacerDroite(),
            ToucheClavier.ROTATION: CommandeTourner(), 
            ToucheClavier.CHUTE_RAPIDE: CommandeDescendre(),
            ToucheClavier.CHUTE_INSTANTANEE: CommandeChuteRapide(),
            ToucheClavier.MENU: CommandeAfficherMenu(),
            ToucheClavier.PAUSE: CommandePause(),
            ToucheClavier.MUTE: CommandeBasculerMute(),
        }
    
    def traiter_evenement_clavier(self, 
                                 touche_physique: str, 
                                 type_evenement: TypeEvenement,
                                 moteur: MoteurJeu,
                                 temps_actuel: float = 0.0) -> bool:
        """
        Traite un événement clavier et exécute la commande correspondante.
        
        Args:
            touche_physique: Nom de la touche physique (ex: "Left", "space")
            type_evenement: Type d'événement (appui, relâche, maintenu)
            moteur: Instance du moteur de jeu
            temps_actuel: Temps actuel en secondes (pour la répétition)
            
        Returns:
            True si une commande a été exécutée, False sinon
        """
        # Convertir la touche physique en touche logique
        touche_logique = self._mapping_touches.get(touche_physique)
        if not touche_logique:
            return False
        
        # Obtenir la commande correspondante
        commande = self._commandes.get(touche_logique)
        if not commande:
            return False
        
        # Traiter selon le type d'événement
        if type_evenement == TypeEvenement.CLAVIER_APPUI:
            return self._traiter_appui(touche_logique, commande, moteur, temps_actuel)
        elif type_evenement == TypeEvenement.CLAVIER_RELACHE:
            return self._traiter_relache(touche_logique)
        elif type_evenement == TypeEvenement.CLAVIER_MAINTENU:
            return self._traiter_maintenu(touche_logique, commande, moteur, temps_actuel)
        
        return False
    
    def _traiter_appui(self, 
                      touche: ToucheClavier, 
                      commande: Commande, 
                      moteur: MoteurJeu,
                      temps_actuel: float) -> bool:
        """Traite l'appui initial d'une touche."""
        # Marquer la touche comme maintenue si répétable
        if touche in self._touches_repetables:
            self._touches_maintenues[touche] = temps_actuel
        
        # Exécuter la commande immédiatement
        return commande.execute(moteur)
    
    def _traiter_relache(self, touche: ToucheClavier) -> bool:
        """Traite le relâchement d'une touche."""
        # Arrêter la répétition si applicable
        if touche in self._touches_maintenues:
            del self._touches_maintenues[touche]
        
        return True
    
    def _traiter_maintenu(self, 
                         touche: ToucheClavier, 
                         commande: Commande, 
                         moteur: MoteurJeu,
                         temps_actuel: float) -> bool:
        """Traite une touche maintenue (répétition)."""
        # Vérifier si la touche est répétable et maintenue
        if touche not in self._touches_repetables or touche not in self._touches_maintenues:
            return False
        
        temps_debut = self._touches_maintenues[touche]
        temps_ecoule = temps_actuel - temps_debut
        
        # Vérifier si assez de temps s'est écoulé pour répéter
        if temps_ecoule >= self._delai_initial:
            # Calculer si on doit répéter maintenant
            temps_depuis_initial = temps_ecoule - self._delai_initial
            if temps_depuis_initial % self._delai_repetition < 0.016:  # ~60 FPS
                return commande.execute(moteur)
        
        return False
    
    def mettre_a_jour_repetition(self, moteur: MoteurJeu, temps_actuel: float) -> List[bool]:
        """
        Met à jour la répétition des touches maintenues.
        
        Args:
            moteur: Instance du moteur de jeu
            temps_actuel: Temps actuel en secondes
            
        Returns:
            Liste des résultats d'exécution des commandes répétées
        """
        resultats = []
        
        for touche in list(self._touches_maintenues.keys()):
            commande = self._commandes.get(touche)
            if commande:
                resultat = self._traiter_maintenu(touche, commande, moteur, temps_actuel)
                if resultat:
                    resultats.append(resultat)
        
        return resultats
    
    def configurer_delais_repetition(self, delai_initial: float, delai_repetition: float) -> None:
        """
        Configure les délais de répétition des touches.
        
        Args:
            delai_initial: Délai avant la première répétition (secondes)
            delai_repetition: Délai entre les répétitions (secondes)
        """
        self._delai_initial = delai_initial
        self._delai_repetition = delai_repetition
    
    def ajouter_mapping_touche(self, touche_physique: str, touche_logique: ToucheClavier) -> None:
        """
        Ajoute ou modifie un mapping de touche.
        
        Args:
            touche_physique: Nom de la touche physique
            touche_logique: Touche logique correspondante
        """
        self._mapping_touches[touche_physique] = touche_logique
    
    def supprimer_mapping_touche(self, touche_physique: str) -> None:
        """
        Supprime un mapping de touche.
        
        Args:
            touche_physique: Nom de la touche physique à supprimer
        """
        self._mapping_touches.pop(touche_physique, None)
    
    def obtenir_touches_mappees(self) -> Dict[str, ToucheClavier]:
        """Retourne une copie du mapping actuel des touches."""
        return self._mapping_touches.copy()
    
    def reinitialiser_touches_maintenues(self) -> None:
        """Remet à zéro toutes les touches maintenues (utile en cas de pause)."""
        self._touches_maintenues.clear()
    
    def statistiques(self) -> str:
        """Retourne des statistiques sur le gestionnaire."""
        nb_mappings = len(self._mapping_touches)
        nb_commandes = len(self._commandes)
        nb_maintenues = len(self._touches_maintenues)
        
        return (f"GestionnaireEvenements - "
                f"{nb_mappings} mappings, "
                f"{nb_commandes} commandes, "
                f"{nb_maintenues} touches maintenues")
