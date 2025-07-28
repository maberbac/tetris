"""
RegistrePieces - Registry Pattern pour l'enregistrement automatique des pièces.

Ce registre permet aux pièces de s'auto-enregistrer et simplifie
l'ajout de nouvelles pièces sans modifier la fabrique principale.
"""

from typing import Dict, Type, Set, TypeVar, Callable
from ..piece import Piece, TypePiece

# Type générique pour le décorateur
T = TypeVar('T', bound=Type[Piece])


def piece_tetris(type_piece: TypePiece) -> Callable[[T], T]:
    """
    Décorateur pour enregistrer automatiquement une pièce Tetris.
    
    Usage:
        @piece_tetris(TypePiece.I)
        class PieceI(Piece):
            ...
    
    Args:
        type_piece: Le type de pièce à enregistrer
        
    Returns:
        Décorateur qui enregistre la classe
    """
    def decorateur(classe_piece: T) -> T:
        RegistrePieces.enregistrer_piece(type_piece, classe_piece)
        return classe_piece
    
    return decorateur


class RegistrePieces:
    """
    Registry Pattern pour l'enregistrement automatique des pièces.
    
    Permet aux classes de pièces de s'enregistrer automatiquement
    sans avoir besoin de modifier manuellement la fabrique.
    """
    
    _pieces_enregistrees: Dict[TypePiece, Type[Piece]] = {}
    _types_supportes: Set[TypePiece] = set()
    
    @classmethod
    def enregistrer_piece(cls, type_piece: TypePiece, classe_piece: Type[Piece]) -> None:
        """
        Enregistrer une nouvelle classe de pièce.
        
        Args:
            type_piece: Le type de pièce (TypePiece.I, TypePiece.O, etc.)
            classe_piece: La classe concrète qui implémente cette pièce
        """
        cls._pieces_enregistrees[type_piece] = classe_piece
        cls._types_supportes.add(type_piece)
        print(f"🔧 Pièce enregistrée : {type_piece.value} -> {classe_piece.__name__}")
    
    @classmethod
    def obtenir_classe_piece(cls, type_piece: TypePiece) -> Type[Piece]:
        """
        Obtenir la classe correspondant à un type de pièce.
        
        Args:
            type_piece: Le type de pièce recherché
            
        Returns:
            La classe de pièce correspondante
            
        Raises:
            ValueError: Si le type de pièce n'est pas supporté
        """
        if type_piece not in cls._pieces_enregistrees:
            types_disponibles = [t.value for t in cls._types_supportes]
            raise ValueError(
                f"Type de pièce non supporté : {type_piece.value}. "
                f"Types disponibles : {types_disponibles}"
            )
        
        return cls._pieces_enregistrees[type_piece]
    
    @classmethod
    def obtenir_types_supportes(cls) -> Set[TypePiece]:
        """Obtenir tous les types de pièces supportés."""
        return cls._types_supportes.copy()
    
    @classmethod
    def est_type_supporte(cls, type_piece: TypePiece) -> bool:
        """Vérifier si un type de pièce est supporté."""
        return type_piece in cls._types_supportes
    
    @classmethod
    def reinitialiser(cls) -> None:
        """Réinitialiser le registre (utile pour les tests)."""
        cls._pieces_enregistrees.clear()
        cls._types_supportes.clear()
    
    @classmethod
    def statistiques(cls) -> str:
        """Obtenir des statistiques sur le registre."""
        total = len(cls._pieces_enregistrees)
        types = [t.value for t in sorted(cls._types_supportes, key=lambda x: x.value)]
        return f"Registre : {total} pièces enregistrées [{', '.join(types)}]"
