"""
Service de logging pour Tetris utilisant la librairie standard Python logging.

Ce service remplace les print() par un système de logging configurable,
similaire à Log4J en Java, permettant d'activer/désactiver les logs debug.
"""

import logging
import sys
from typing import Optional


class LoggerTetris:
    """
    Logger personnalisé pour Tetris utilisant la librairie logging de Python.
    
    Fonctionnalités:
    - Logging configurable avec niveaux (DEBUG, INFO, WARNING, ERROR)
    - Mode debug activable/désactivable 
    - Format personnalisé pour les messages Tetris
    - Compatible avec les patterns existants [GAME], [DICE], etc.
    """
    
    def __init__(self, nom_logger: str = "tetris"):
        """
        Initialise le logger Tetris.
        
        Args:
            nom_logger: Nom du logger (par défaut "tetris")
        """
        self._logger = logging.getLogger(nom_logger)
        self._logger.setLevel(logging.DEBUG)
        
        # Éviter les doublons si déjà configuré
        if not self._logger.handlers:
            self._configurer_handler()
        
        self._mode_debug = False  # Debug activé par défaut
    
    def _configurer_handler(self) -> None:
        """Configure le handler pour l'affichage des logs."""
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        
        # Format personnalisé pour Tetris (sans timestamp pour rester simple)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        
        self._logger.addHandler(handler)
    
    def set_debug_mode(self, actif: bool) -> None:
        """
        Active ou désactive le mode debug.
        
        Quand actif=False, TOUS les logs sont désactivés pour avoir
        une console complètement silencieuse.
        
        Args:
            actif: True pour activer debug, False pour désactiver TOUS les logs
        """
        self._mode_debug = actif
        if actif:
            self._logger.setLevel(logging.DEBUG)
        else:
            # Désactiver TOUS les logs comme demandé par l'utilisateur
            self._logger.setLevel(logging.CRITICAL + 1)  # Plus haut que CRITICAL
    
    def set_silent_mode(self, actif: bool) -> None:
        """
        Active ou désactive le mode silencieux complet.
        En mode silencieux, seules les erreurs critiques sont affichées.
        
        Args:
            actif: True pour activer mode silencieux, False pour mode normal
        """
        if actif:
            self._logger.setLevel(logging.ERROR)
            self._mode_debug = False
        else:
            # Restaurer le mode normal
            if self._mode_debug:
                self._logger.setLevel(logging.DEBUG)
            else:
                self._logger.setLevel(logging.INFO)
    
    def is_debug_enabled(self) -> bool:
        """
        Retourne si le mode debug est activé.
        
        Returns:
            True si debug activé, False sinon
        """
        return self._mode_debug
    
    def debug(self, message: str) -> None:
        """
        Log un message de debug (affiché seulement si debug activé).
        
        Args:
            message: Message à logger
        """
        if self._mode_debug:
            self._logger.debug(message)
    
    def info(self, message: str) -> None:
        """
        Log un message d'information (toujours affiché).
        
        Args:
            message: Message à logger
        """
        self._logger.info(message)
    
    def warning(self, message: str) -> None:
        """
        Log un message d'avertissement (toujours affiché).
        
        Args:
            message: Message à logger
        """
        self._logger.warning(message)
    
    def error(self, message: str) -> None:
        """
        Log un message d'erreur (toujours affiché).
        
        Args:
            message: Message à logger
        """
        self._logger.error(message)


# Instance globale du logger (pattern Singleton simplifié)
logger_tetris = LoggerTetris()
# Mode principal : permettre les messages INFO et plus élevés
logger_tetris.set_silent_mode(False)  # Messages INFO, WARNING, ERROR
