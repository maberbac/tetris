"""
Module d'exceptions du domaine Tetris.
CONFORME AUX DIRECTIVES : Point d'accès centralisé pour toutes les exceptions du domaine
"""

from .exception_collision import ExceptionCollision

__all__ = ['ExceptionCollision']
