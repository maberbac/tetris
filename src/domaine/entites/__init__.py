"""
ENTITÉS - Objets métier du domaine Tetris

Les entités représentent les concepts centraux de Tetris :
- Position : Value Object pour les coordonnées
- Piece : Entité représentant une pièce de Tetris
- Plateau : Entité représentant l'aire de jeu

RÈGLES :
- Immutable quand possible (Value Objects)
- Logique métier pure
- Aucune dépendance externe
- Tests unitaires simples
"""

from .position import Position
from .piece import Piece, TypePiece
from .plateau import Plateau

__all__ = ['Position', 'Piece', 'TypePiece', 'Plateau']
