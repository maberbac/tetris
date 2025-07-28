"""
Module des fabriques pour le domaine Tetris.

Ce module assure que les pièces sont importées pour l'auto-enregistrement
avant que la fabrique ne soit utilisée.
"""

# Importer le registre en premier
from .registre_pieces import RegistrePieces, piece_tetris

# Importer toutes les pièces pour déclencher l'auto-enregistrement
from ..pieces import *

# Importer la fabrique après l'enregistrement des pièces
from .fabrique_pieces import FabriquePieces

__all__ = [
    'FabriquePieces',
    'RegistrePieces', 
    'piece_tetris',
]
