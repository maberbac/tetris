"""
Plateau - Grille de jeu Tetris

Le plateau représente la grille de jeu où les pièces tombent et se placent.
Dimensions standard : 10 colonnes × 20 lignes.
Coordonnées : (0,0) en haut-gauche, (9,19) en bas-droite.

Responsabilités :
- Gérer l'état des cellules (vide/occupée)
- Vérifier les collisions
- Placer les pièces
- Détecter et supprimer les lignes complètes
- Faire descendre les lignes au-dessus
"""

from typing import List, Set, Optional
from .position import Position
from .piece import Piece, TypePiece


class Plateau:
    """
    Plateau de jeu Tetris avec grille 10×20.
    
    Pattern utilisé :
    - Entity (gère son propre état)
    - Value Object (Position pour les coordonnées)
    """
    
    # Dimensions standard du plateau Tetris (pour compatibilité)
    LARGEUR_STANDARD = 10
    HAUTEUR_STANDARD = 20
    
    def __init__(self, largeur: int = None, hauteur: int = None):
        """
        Initialise un plateau avec dimensions personnalisables.
        
        Args:
            largeur: Largeur du plateau (défaut: 10 - standard Tetris)
            hauteur: Hauteur du plateau (défaut: 20 - standard Tetris)
        
        La grille est représentée par un set de positions occupées.
        Cela permet des vérifications rapides de collision O(1).
        """
        # Utiliser les dimensions standard si non spécifiées
        self.largeur = largeur if largeur is not None else self.LARGEUR_STANDARD
        self.hauteur = hauteur if hauteur is not None else self.HAUTEUR_STANDARD
        
        # Validation des dimensions
        if self.largeur <= 0 or self.hauteur <= 0:
            raise ValueError(f"Dimensions invalides: {self.largeur}x{self.hauteur}")
        
        self._positions_occupees: Set[Position] = set()
    
    @property
    def positions_occupees(self) -> Set[Position]:
        """Retourne les positions actuellement occupées (lecture seule)."""
        return self._positions_occupees.copy()
    
    def est_position_valide(self, position: Position) -> bool:
        """
        Vérifie si une position est dans les limites du plateau.
        
        Args:
            position: Position à vérifier
            
        Returns:
            True si la position est valide, False sinon
        """
        return (0 <= position.x < self.largeur and 
                0 <= position.y < self.hauteur)
    
    def est_position_libre(self, position: Position) -> bool:
        """
        Vérifie si une position est libre (dans les limites et non occupée).
        
        Args:
            position: Position à vérifier
            
        Returns:
            True si la position est libre, False sinon
        """
        return (self.est_position_valide(position) and 
                position not in self._positions_occupees)
    
    def peut_placer_piece(self, piece: Piece) -> bool:
        """
        Vérifie si une pièce peut être placée à sa position actuelle.
        
        Args:
            piece: Pièce à vérifier
            
        Returns:
            True si la pièce peut être placée, False sinon
        """
        return all(self.est_position_libre(pos) for pos in piece.positions)
    
    def placer_piece(self, piece: Piece) -> None:
        """
        Place une pièce sur le plateau (marque ses positions comme occupées).
        
        Args:
            piece: Pièce à placer
            
        Raises:
            ValueError: Si la pièce ne peut pas être placée
        """
        if not self.peut_placer_piece(piece):
            raise ValueError("Impossible de placer la pièce à cette position")
        
        # Marquer toutes les positions de la pièce comme occupées
        for position in piece.positions:
            self._positions_occupees.add(position)
    
    def obtenir_lignes_completes(self) -> List[int]:
        """
        Retourne la liste des numéros de lignes complètes (y-coordonnées).
        
        Returns:
            Liste des numéros de lignes complètes, triée par ordre croissant
        """
        lignes_completes = []
        
        # Vérifier chaque ligne de haut en bas
        for y in range(self.hauteur):
            positions_ligne = [Position(x, y) for x in range(self.largeur)]
            
            # Si toutes les positions de la ligne sont occupées
            if all(pos in self._positions_occupees for pos in positions_ligne):
                lignes_completes.append(y)
        
        return lignes_completes
    
    def supprimer_lignes(self, numeros_lignes: List[int]) -> int:
        """
        Supprime les lignes spécifiées et fait descendre les lignes au-dessus.
        
        Args:
            numeros_lignes: Liste des numéros de lignes à supprimer
            
        Returns:
            Nombre de lignes supprimées
        """
        if not numeros_lignes:
            return 0
        
        # Trier les lignes par ordre décroissant pour éviter les problèmes d'index
        lignes_triees = sorted(numeros_lignes, reverse=True)
        
        for y_ligne in lignes_triees:
            self._supprimer_ligne(y_ligne)
            self._faire_descendre_lignes_au_dessus(y_ligne)
        
        return len(lignes_triees)
    
    def _supprimer_ligne(self, y_ligne: int) -> None:
        """
        Supprime toutes les positions occupées d'une ligne.
        
        Args:
            y_ligne: Numéro de la ligne à supprimer
        """
        positions_a_supprimer = {pos for pos in self._positions_occupees 
                                if pos.y == y_ligne}
        self._positions_occupees -= positions_a_supprimer
    
    def _faire_descendre_lignes_au_dessus(self, y_ligne_supprimee: int) -> None:
        """
        Fait descendre d'une ligne toutes les positions au-dessus de la ligne supprimée.
        
        Args:
            y_ligne_supprimee: Numéro de la ligne qui a été supprimée
        """
        positions_a_deplacer = {pos for pos in self._positions_occupees 
                               if pos.y < y_ligne_supprimee}
        
        # Supprimer les anciennes positions
        self._positions_occupees -= positions_a_deplacer
        
        # Ajouter les nouvelles positions (descendues d'une ligne)
        nouvelles_positions = {Position(pos.x, pos.y + 1) 
                              for pos in positions_a_deplacer}
        self._positions_occupees |= nouvelles_positions
    
    def est_vide(self) -> bool:
        """
        Vérifie si le plateau est vide.
        
        Returns:
            True si le plateau est vide, False sinon
        """
        return len(self._positions_occupees) == 0
    
    def est_ligne_superieure_occupee(self) -> bool:
        """
        Vérifie si la ligne supérieure (y=0) contient des positions occupées.
        Utile pour détecter la fin de partie (Game Over).
        
        Returns:
            True si la ligne supérieure est occupée, False sinon
        """
        return any(pos.y == 0 for pos in self._positions_occupees)
    
    def __str__(self) -> str:
        """
        Représentation textuelle du plateau pour debug.
        
        Returns:
            Chaîne représentant le plateau ('.' = vide, '█' = occupé)
        """
        lignes = []
        for y in range(self.hauteur):
            ligne = ""
            for x in range(self.largeur):
                if Position(x, y) in self._positions_occupees:
                    ligne += "█"
                else:
                    ligne += "."
            lignes.append(ligne)
        return "\n".join(lignes)
