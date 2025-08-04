"""
Commandes - Command Pattern pour les actions de jeu Tetris

Ce module implémente le Command Pattern pour encapsuler les actions
que le joueur peut effectuer sur les pièces et le jeu.

Avantages du Command Pattern :
- Séparation des inputs et des actions
- Facilite l'ajout de nouvelles commandes
- Permet l'historique et l'annulation (futur)
- Testabilité des actions individuellement
"""

from abc import ABC, abstractmethod
from typing import Protocol

# Import des exceptions du domaine selon les directives
from ...exceptions.exception_collision import ExceptionCollision
from ...entites.piece import Piece
from ...entites.plateau import Plateau
from ..logger_tetris import logger_tetris


class MoteurJeu(Protocol):
    """
    Interface pour le moteur de jeu.
    
    Définit les méthodes que les commandes peuvent appeler
    pour modifier l'état du jeu.
    """
    
    def obtenir_piece_active(self) -> Piece:
        """Retourne la pièce actuellement contrôlée par le joueur."""
        ...
    
    def obtenir_plateau(self) -> Plateau:
        """Retourne le plateau de jeu."""
        ...
    
    def faire_descendre_piece(self) -> bool:
        """Fait descendre la pièce d'une ligne. Retourne True si possible."""
        ...
    
    def placer_piece_definitivement(self) -> None:
        """Place la pièce active définitivement sur le plateau."""
        ...
    
    def generer_nouvelle_piece(self) -> None:
        """Génère une nouvelle pièce après placement."""
        ...


class Commande(ABC):
    """
    Interface abstraite pour toutes les commandes de jeu.
    
    Implémente le Command Pattern classique avec execute().
    """
    
    @abstractmethod
    def execute(self, moteur: MoteurJeu) -> bool:
        """
        Exécute la commande sur le moteur de jeu.
        
        Args:
            moteur: Instance du moteur de jeu
            
        Returns:
            True si la commande a été exécutée avec succès, False sinon
        """
        pass


class CommandeDeplacerGauche(Commande):
    """Commande pour déplacer la pièce vers la gauche."""
    
    def execute(self, moteur: MoteurJeu) -> bool:
        """Déplace la pièce active vers la gauche si possible."""
        piece = moteur.obtenir_piece_active()
        plateau = moteur.obtenir_plateau()
        
        # Sauvegarder la position actuelle
        positions_originales = piece.positions.copy()
        
        # Essayer le déplacement
        piece.deplacer(-1, 0)
        
        # Vérifier si le déplacement est valide
        if plateau.peut_placer_piece(piece):
            return True
        else:
            # Annuler le déplacement
            piece._positions = positions_originales
            # Lever ExceptionCollision selon les directives
            raise ExceptionCollision("Impossible de déplacer la pièce vers la gauche")


class CommandeDeplacerDroite(Commande):
    """Commande pour déplacer la pièce vers la droite."""
    
    def execute(self, moteur: MoteurJeu) -> bool:
        """Déplace la pièce active vers la droite si possible."""
        piece = moteur.obtenir_piece_active()
        plateau = moteur.obtenir_plateau()
        
        # Sauvegarder la position actuelle
        positions_originales = piece.positions.copy()
        
        # Essayer le déplacement
        piece.deplacer(1, 0)
        
        # Vérifier si le déplacement est valide
        if plateau.peut_placer_piece(piece):
            return True
        else:
            # Annuler le déplacement
            piece._positions = positions_originales
            # Lever ExceptionCollision selon les directives
            raise ExceptionCollision("Impossible de déplacer la pièce vers la droite")


class CommandeDescendre(Commande):
    """Commande pour faire descendre la pièce d'une ligne."""
    
    def execute(self, moteur: MoteurJeu) -> bool:
        """Fait descendre la pièce active d'une ligne si possible."""
        return moteur.faire_descendre_piece()


class CommandeChuteRapide(Commande):
    """Commande pour faire tomber la pièce jusqu'en bas."""
    
    def execute(self, moteur: MoteurJeu) -> bool:
        """Fait tomber la pièce jusqu'à ce qu'elle ne puisse plus descendre."""
        piece = moteur.obtenir_piece_active()
        plateau = moteur.obtenir_plateau()
        
        # Vérifier d'abord si la pièce peut descendre au moins une fois
        positions_originales = piece.positions.copy()
        pivot_original = piece.position_pivot
        
        piece.deplacer(0, 1)
        peut_descendre_initialement = plateau.peut_placer_piece(piece)
        
        # Restaurer position originale complètement
        piece._positions = positions_originales
        piece.position_pivot = pivot_original
        
        if not peut_descendre_initialement:
            # Lever ExceptionCollision selon les directives
            raise ExceptionCollision("Impossible d'effectuer une chute rapide - pièce bloquée")
        
        nb_lignes_descendues = 0
        
        while True:
            # Sauvegarder la position actuelle
            positions_actuelles = piece.positions.copy()
            pivot_actuel = piece.position_pivot
            
            # Essayer de descendre
            piece.deplacer(0, 1)
            
            # Vérifier si le déplacement est valide
            if plateau.peut_placer_piece(piece):
                nb_lignes_descendues += 1
            else:
                # Annuler le dernier déplacement et arrêter
                piece._positions = positions_actuelles
                piece.position_pivot = pivot_actuel
                break
        
        # Placer la pièce définitivement
        moteur.placer_piece_definitivement()
        moteur.generer_nouvelle_piece()
        
        return nb_lignes_descendues > 0


class CommandeTourner(Commande):
    """Commande pour faire tourner la pièce."""
    
    def execute(self, moteur: MoteurJeu) -> bool:
        """Fait tourner la pièce active si possible."""
        piece = moteur.obtenir_piece_active()
        plateau = moteur.obtenir_plateau()
        
        # Sauvegarder l'état actuel (positions seulement)
        positions_originales = piece.positions.copy()
        
        # Essayer la rotation
        piece.tourner()
        
        # Vérifier si la rotation est valide
        if plateau.peut_placer_piece(piece):
            return True
        else:
            # Annuler la rotation en restaurant les positions originales
            piece.positions = positions_originales
            # Lever ExceptionCollision selon les directives
            raise ExceptionCollision("Impossible de tourner la pièce")


class CommandePause(Commande):
    """Commande pour mettre le jeu en pause."""
    
    def execute(self, moteur: MoteurJeu) -> bool:
        """Met le jeu en pause ou le reprend."""
        # Cette commande sera implémentée selon les besoins du moteur
        # Pour l'instant, on retourne toujours True
        return True


class CommandeBasculerMute(Commande):
    """Commande pour basculer le mute/unmute de la musique."""
    
    def execute(self, moteur: MoteurJeu) -> bool:
        """Bascule l'état mute/unmute de la musique."""
        try:
            audio = moteur.obtenir_audio()
            if audio is None:
                logger_tetris.warning("❌ Audio non disponible")
                return False
            
            est_mute = audio.basculer_mute_musique()
            
            # Feedback utilisateur (directement à l'utilisateur)
            if est_mute:
                logger_tetris.info("🔇 Musique désactivée")
            else:
                logger_tetris.info("🔊 Musique réactivée")
                
            return True
            
        except Exception as e:
            logger_tetris.error(f"❌ Erreur audio: {e}")
            return False


class CommandeQuitter(Commande):
    """Commande pour quitter le jeu."""
    
    def execute(self, moteur: MoteurJeu) -> bool:
        """Déclenche la fin du jeu."""
        # Cette commande sera implémentée selon les besoins du moteur
        # Pour l'instant, on retourne toujours True
        return True
