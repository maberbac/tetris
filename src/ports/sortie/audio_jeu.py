"""
Interface audio pour le jeu de Tetris.

Port de sortie selon l'architecture hexagonale pour la gestion audio.
"""

from abc import ABC, abstractmethod
from typing import Optional


class AudioJeu(ABC):
    """Interface pour la gestion audio du jeu."""
    
    @abstractmethod
    def initialiser(self) -> None:
        """Initialise le système audio."""
        pass
    
    @abstractmethod
    def jouer_musique(self, chemin_fichier: str, volume: float = 0.7, boucle: bool = True) -> None:
        """
        Joue une musique de fond.
        
        Args:
            chemin_fichier: Chemin vers le fichier audio
            volume: Volume de la musique (0.0 à 1.0)
            boucle: Si True, joue en boucle infinie
        """
        pass
    
    @abstractmethod
    def arreter_musique(self) -> None:
        """Arrête la musique de fond."""
        pass
    
    @abstractmethod
    def mettre_en_pause_musique(self) -> None:
        """Met en pause la musique de fond."""
        pass
    
    @abstractmethod
    def reprendre_musique(self) -> None:
        """Reprend la musique de fond."""
        pass
    
    @abstractmethod
    def definir_volume_musique(self, volume: float) -> None:
        """
        Définit le volume de la musique.
        
        Args:
            volume: Volume (0.0 à 1.0)
        """
        pass
    
    @abstractmethod
    def jouer_effet_sonore(self, chemin_fichier: str, volume: float = 0.8) -> None:
        """
        Joue un effet sonore.
        
        Args:
            chemin_fichier: Chemin vers le fichier audio
            volume: Volume de l'effet (0.0 à 1.0)
        """
        pass
    
    @abstractmethod
    def est_musique_en_cours(self) -> bool:
        """
        Vérifie si la musique est en cours de lecture.
        
        Returns:
            True si la musique joue, False sinon
        """
        pass
    
    @abstractmethod
    def nettoyer(self) -> None:
        """Nettoie les ressources audio."""
        pass
