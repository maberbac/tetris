"""
Module des pièces spécialisées pour Tetris.

Contient toutes les implémentations concrètes des différents types de pièces.
Les imports sont ajoutés au fur et à mesure de l'implémentation.
"""

# Import seulement les pièces implémentées
from .piece_i import PieceI
from .piece_o import PieceO

__all__ = [
    'PieceI',
    'PieceO',
    # 'PieceT',  # À implémenter
    # 'PieceS',  # À implémenter
    # 'PieceZ',  # À implémenter
    # 'PieceJ',  # À implémenter
    # 'PieceL'   # À implémenter
]
