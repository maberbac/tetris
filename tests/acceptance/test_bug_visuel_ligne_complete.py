"""
Tests d'Acceptance - Bug Visuel Ligne Complète
==============================================
Nature : Test d'acceptance pour correction bug utilisateur  
Scenario : L'utilisateur voit une ligne grise qui n'est pas détruite (bug visuel)
Méthode : TDD (Test-Driven Development)

Bug identifié : Timing entre placement de pièce et suppression de ligne
                → La ligne complète apparaît grise pendant un frame

Comportement attendu : Aucune ligne complète ne doit jamais être visible à l'utilisateur
"""

import unittest
import sys
sys.path.append('.')

from src.domaine.services.moteur_partie import MoteurPartie
from src.domaine.entites.position import Position
from src.domaine.entites.piece import TypePiece


class TestBugVisuelLigneComplete(unittest.TestCase):
    """Tests spécifiques pour le bug visuel de ligne complète"""
    
    def setUp(self):
        """Configuration pour chaque test"""
        self.moteur = MoteurPartie()
    
    def test_placement_piece_supprime_ligne_immediatement(self):
        """GREEN: Quand une pièce crée une ligne complète, elle doit être supprimée immédiatement"""
        # Arrange : Préparer une ligne presque complète
        plateau = self.moteur.obtenir_plateau()
        
        # Remplir 8 cellules de la ligne 19 (dernière ligne) 
        for x in range(8):
            pos = Position(x, 19)
            plateau._positions_occupees.add(pos)
        
        # Créer une pièce O qui va compléter la ligne en (8,18) -> positions (8,18), (9,18), (8,19), (9,19)
        from src.domaine.entites.pieces.piece_o import PieceO
        piece_o = PieceO.creer(8, 18)  # Carré 2x2 qui complétera la ligne 19
        
        # Forcer la pièce dans le moteur
        self.moteur.piece_active = piece_o
        
        # Act : Placer la pièce (ce qui devrait déclencher suppression immédiate)
        positions_avant = len(plateau.positions_occupees)
        resultat = self.moteur.placer_piece_et_generer_nouvelle()
        
        # Assert : La ligne doit avoir été supprimée
        self.assertTrue(resultat, "Le placement doit réussir")
        lignes_completes = plateau.obtenir_lignes_completes()
        
        # Si la ligne complète était supprimée immédiatement, il ne devrait plus y avoir de ligne complète
        self.assertEqual(lignes_completes, [], 
                        "Une ligne complète ne devrait jamais être visible après placement")
        
        # Vérifier que la ligne a bien été supprimée
        positions_apres = len(plateau.positions_occupees)
        # positions_avant (8) + piece_o (4) - ligne_supprimee (10) = positions_avant - 6
        self.assertEqual(positions_apres, positions_avant - 6,
                       "La ligne complète devrait être supprimée immédiatement")
    
    def test_etat_plateau_coherent_apres_placement(self):
        """RED: L'état du plateau doit être cohérent - pas de ligne complète résiduelle"""
        # Arrange : Créer un scénario de ligne complète
        plateau = self.moteur.obtenir_plateau()
        
        # Remplir complètement la dernière ligne
        for x in range(10):
            pos = Position(x, 19)
            plateau._positions_occupees.add(pos)
        
        positions_initiales = plateau.positions_occupees.copy()
        
        # Act : Simuler la détection et suppression
        lignes_completes = plateau.obtenir_lignes_completes()
        if lignes_completes:
            plateau.supprimer_lignes(lignes_completes)
        
        # Assert : Plus aucune ligne complète ne doit exister
        lignes_apres_suppression = plateau.obtenir_lignes_completes()
        self.assertEqual(lignes_apres_suppression, [], 
                        "Aucune ligne complète ne doit subsister après suppression")
        
        # Vérifier qu'il n'y a plus de cellules en ligne 19
        cellules_ligne_19 = [pos for pos in plateau.positions_occupees if pos.y == 19]
        self.assertEqual(len(cellules_ligne_19), 0,
                        "La ligne 19 doit être complètement vide après suppression")
    
    def test_moteur_ne_laisse_jamais_ligne_complete_visible(self):
        """GREEN: Le moteur ne doit jamais laisser une ligne complète visible dans son état final"""
        # Arrange : Créer un scénario complexe avec plusieurs lignes
        plateau = self.moteur.obtenir_plateau()
        
        # Créer 2 lignes complètes consécutives
        for y in [18, 19]:  # Deux dernières lignes
            for x in range(10):
                pos = Position(x, y)
                plateau._positions_occupees.add(pos)
        
        # Ajouter une ligne complète au-dessus qui va descendre après suppression
        for x in range(10):  # Ligne 17 complète qui va devenir ligne 19 après suppression
            pos = Position(x, 17)
            plateau._positions_occupees.add(pos)
        
        # Act : Supprimer les lignes complètes en plusieurs fois pour simuler le problème
        lignes_completes = plateau.obtenir_lignes_completes()
        if lignes_completes:
            nb_supprimees = plateau.supprimer_lignes(lignes_completes)
            self.moteur.stats.ajouter_score_selon_lignes_completees(nb_supprimees)
            
            # Vérifier immédiatement s'il y a de nouvelles lignes complètes après descente
            nouvelles_lignes_completes = plateau.obtenir_lignes_completes()
            if nouvelles_lignes_completes:
                # Supprimer ces nouvelles lignes complètes aussi
                plateau.supprimer_lignes(nouvelles_lignes_completes)
        
        # Assert : État final cohérent
        lignes_finales = plateau.obtenir_lignes_completes()
        self.assertEqual(lignes_finales, [],
                        "Le moteur ne doit jamais laisser de lignes complètes dans l'état final")
        
        # Vérifier que le plateau n'a plus que les bonnes cellules
        positions_restantes = len(plateau.positions_occupees)
        self.assertEqual(positions_restantes, 0,  # Toutes les lignes complètes ont été supprimées
                        "Toutes les lignes complètes devraient avoir été supprimées")
    
    def test_atomicite_placement_et_suppression(self):
        """GREEN: Le placement d'une pièce et la suppression de lignes doivent être atomiques"""
        # Arrange
        plateau = self.moteur.obtenir_plateau()
        
        # Créer une ligne presque complète
        for x in range(8):  # 8 cellules sur 10
            pos = Position(x, 19)
            plateau._positions_occupees.add(pos)
        
        # Créer une pièce O qui va compléter la ligne quand placée en (8, 18)
        from src.domaine.entites.pieces.piece_o import PieceO
        piece_o = PieceO.creer(8, 18)  # Carré 2x2 qui complétera la ligne 19
        
        # Act : Utiliser la nouvelle méthode atomique
        nb_lignes_supprimees = plateau.placer_piece_et_supprimer_lignes(piece_o)
        
        # Assert : Vérifier qu'aucune ligne complète n'est visible après l'opération atomique
        lignes_finales = plateau.obtenir_lignes_completes()
        self.assertEqual(lignes_finales, [],
                        "Après l'opération atomique, aucune ligne complète ne doit être visible")
        self.assertEqual(nb_lignes_supprimees, 1,
                        "Une ligne devrait avoir été supprimée")


if __name__ == '__main__':
    print("🔴 PHASE TDD RED - Tests qui doivent échouer")
    print("🎯 Objectif : Définir le comportement attendu pour corriger le bug visuel")
    print("=" * 70)
    
    unittest.main(verbosity=2)
