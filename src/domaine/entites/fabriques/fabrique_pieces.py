"""
FabriquePieces - Factory Pattern refactorisé avec Registry Pattern.

Cette fabrique utilise maintenant un registre pour découvrir automatiquement
les pièces disponibles, rendant l'ajout de nouvelles pièces plus fluide.

Avantages du refactoring :
- Auto-discovery des pièces via Registry Pattern
- Pas besoin de modifier la fabrique pour ajouter des pièces
- Meilleure séparation des responsabilités
- Extension facilitée pour de nouveaux types

Exemple d'usage :
    fabrique = FabriquePieces()
    piece_i = fabrique.creer(TypePiece.I)
    piece_aleatoire = fabrique.creer_aleatoire()
"""

import random
from typing import List
from ..piece import Piece, TypePiece
from .registre_pieces import RegistrePieces


class FabriquePieces:
    """
    Factory Pattern refactorisé avec Registry Pattern.
    
    Utilise le RegistrePieces pour découvrir automatiquement
    les pièces disponibles sans couplage fort.
    
    Responsabilités :
    - Interface uniforme de création via Registry
    - Gestion des positions de spawn par défaut
    - Création aléatoire basée sur les pièces disponibles
    - Validation des types supportés
    """
    
    # Position de spawn par défaut (centre du plateau Tetris 10x20)
    X_SPAWN_DEFAUT = 5
    Y_SPAWN_DEFAUT = -3  # Zone invisible : 3 lignes au-dessus du plateau visible
    
    
    def __init__(self):
        """Initialise la fabrique en utilisant le registre des pièces."""
        # Plus besoin de mapping manuel ! Le registre gère tout
        pass
    
    def creer(self, type_piece: TypePiece, 
              x_pivot: int = None, y_pivot: int = None) -> Piece:
        """
        Créer une pièce du type spécifié via le registre.
        
        Args:
            type_piece: Type de pièce à créer
            x_pivot: Position X du pivot (utilise défaut si None)
            y_pivot: Position Y du pivot (utilise défaut si None)
            
        Returns:
            Instance de la pièce demandée
            
        Raises:
            ValueError: Si le type de pièce n'est pas supporté
        """
        # Utiliser les valeurs par défaut si non spécifiées
        x = x_pivot if x_pivot is not None else self.X_SPAWN_DEFAUT
        y = y_pivot if y_pivot is not None else self.Y_SPAWN_DEFAUT
        
        # Obtenir la classe via le registre
        classe_piece = RegistrePieces.obtenir_classe_piece(type_piece)
        
        # Créer l'instance
        return classe_piece.creer(x_pivot=x, y_pivot=y)
    
    
    def creer_aleatoire(self, x_pivot: int = None, y_pivot: int = None) -> Piece:
        """
        Créer une pièce aléatoire parmi les types supportés.
        
        Args:
            x_pivot: Position X du pivot (utilise défaut si None)
            y_pivot: Position Y du pivot (utilise défaut si None)
            
        Returns:
            Instance d'une pièce aléatoire
            
        Raises:
            ValueError: Si aucune pièce n'est enregistrée
        """
        types_disponibles = list(RegistrePieces.obtenir_types_supportes())
        
        if not types_disponibles:
            raise ValueError("Aucune pièce enregistrée dans le registre")
        
        type_choisi = random.choice(types_disponibles)
        return self.creer(type_choisi, x_pivot, y_pivot)
    
    def obtenir_types_supportes(self) -> List[TypePiece]:
        """Obtenir la liste des types de pièces supportés."""
        return list(RegistrePieces.obtenir_types_supportes())
    
    def statistiques(self) -> str:
        """Obtenir des statistiques sur la fabrique."""
        return f"FabriquePieces - {RegistrePieces.statistiques()}"
