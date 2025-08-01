"""
Interface d'affichage pour le jeu de Tetris.

Port de sortie selon l'architecture hexagonale.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domaine.services.moteur_partie import MoteurPartie


class AffichageJeu(ABC):
    """Interface pour l'affichage du jeu."""
    
    @abstractmethod
    def dessiner(self, moteur: 'MoteurPartie') -> None:
        """Dessine l'interface complète du jeu."""
        pass
    
    @abstractmethod
    def initialiser(self) -> None:
        """Initialise l'affichage."""
        pass
    
    @abstractmethod
    def nettoyer(self) -> None:
        """Nettoie les ressources d'affichage."""
        pass
