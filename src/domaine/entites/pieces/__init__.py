"""
Module des pièces spécialisées pour Tetris.

Ce module importe automatiquement toutes les pièces pour déclencher
leur auto-enregistrement via le décorateur @piece_tetris.
"""

# Import de toutes les pièces implémentées pour déclencher l'auto-enregistrement
from .piece_i import PieceI
from .piece_o import PieceO
from .piece_t import PieceT

__all__ = [
    'PieceI',
    'PieceO',
    'PieceT',
    # À ajouter lors de l'implémentation :
    # 'PieceS',  # À implémenter
    # 'PieceZ',  # À implémenter
    # 'PieceJ',  # À implémenter
    # 'PieceL'   # À implémenter
]
