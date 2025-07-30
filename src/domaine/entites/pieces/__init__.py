"""
Module des pièces spécialisées pour Tetris.

Ce module importe automatiquement toutes les pièces pour déclencher
leur auto-enregistrement via le décorateur @piece_tetris.
"""

# Import de toutes les pièces implémentées pour déclencher l'auto-enregistrement
from .piece_i import PieceI
from .piece_o import PieceO
from .piece_t import PieceT
from .piece_s import PieceS
from .piece_z import PieceZ
from .piece_j import PieceJ
from .piece_l import PieceL

__all__ = [
    'PieceI',
    'PieceO',
    'PieceT',
    'PieceS',
    'PieceZ',
    'PieceJ',
    'PieceL'
    # 'PieceL'   # À implémenter
]
