"""
Interface de contrôle pour le jeu de Tetris.

Port d'entrée selon l'architecture hexagonale.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domaine.services.moteur_partie import MoteurPartie


class ControleurJeu(ABC):
    """Interface pour contrôler le jeu."""
    
    @abstractmethod
    def traiter_evenements(self, moteur: 'MoteurPartie', temps_actuel: float) -> bool:
        """
        Traite les événements d'entrée.
        
        Returns:
            bool: True si le jeu doit continuer, False pour quitter
        """
        pass
    
    @abstractmethod
    def mettre_a_jour_repetitions(self, moteur: 'MoteurPartie', temps_actuel: float) -> None:
        """Met à jour les répétitions des touches."""
        pass
