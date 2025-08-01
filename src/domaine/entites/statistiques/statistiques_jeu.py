"""
Entité pour les statistiques et scores de la partie de Tetris.

Fait partie du domaine métier.
"""

from src.domaine.entites.piece import TypePiece


class StatistiquesJeu:
    """Statistiques et scores de la partie."""
    
    def __init__(self):
        self.score = 0
        self.lignes_completees = 0
        self.pieces_placees = 0
        self.niveau = 1
        
        # Statistiques par type de pièce
        self.pieces_par_type = {
            TypePiece.I: 0,
            TypePiece.O: 0, 
            TypePiece.T: 0,
            TypePiece.S: 0,
            TypePiece.Z: 0,
            TypePiece.J: 0,
            TypePiece.L: 0
        }
    
    def ajouter_piece(self, type_piece: TypePiece) -> None:
        """Ajoute une pièce aux statistiques."""
        self.pieces_par_type[type_piece] += 1
        self.pieces_placees += 1
    
    def ajouter_score_selon_lignes_completees(self, nb_lignes: int) -> None:
        """Ajoute le score aux statistiques selon le nombre de lignes complétées simultanément."""
        self.lignes_completees += nb_lignes
        
        # Calcul du score selon le nombre de lignes
        if nb_lignes == 1:
            self.score += 100 * self.niveau
        elif nb_lignes == 2:
            self.score += 300 * self.niveau
        elif nb_lignes == 3:
            self.score += 500 * self.niveau
        elif nb_lignes == 4:  # Tetris !
            self.score += 800 * self.niveau
        
        # Calcul du niveau (tous les 10 lignes)
        self.niveau = (self.lignes_completees // 10) + 1
