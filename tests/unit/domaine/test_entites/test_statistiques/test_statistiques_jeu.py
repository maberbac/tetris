"""
Tests unitaires pour la classe StatistiquesJeu - Entity

Tests TDD pour le système de score et statistiques de Tetris.
Architecture hexagonale - Domaine métier.
"""

import unittest
import sys
import os

# Ajouter src au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'src'))

from src.domaine.entites.statistiques.statistiques_jeu import StatistiquesJeu
from src.domaine.entites.piece import TypePiece


class TestStatistiquesJeu(unittest.TestCase):
    """Tests unitaires pour l'entité StatistiquesJeu."""

    def setUp(self):
        """Préparation avant chaque test."""
        self.stats = StatistiquesJeu()

    def test_statistiques_peuvent_etre_creees(self):
        """Test RED : Création des statistiques avec valeurs initiales."""
        self.assertEqual(self.stats.score, 0)
        self.assertEqual(self.stats.niveau, 1)
        self.assertEqual(self.stats.lignes_completees, 0)
        self.assertEqual(self.stats.pieces_placees, 0)

    def test_statistiques_initialisent_compteurs_pieces(self):
        """Test : Initialisation des compteurs pour tous les types de pièces."""
        # Vérifier que tous les types de pièces sont initialisés à 0
        for type_piece in TypePiece:
            self.assertEqual(self.stats.pieces_par_type[type_piece], 0)
        
        # Vérifier qu'on a bien 7 types de pièces
        self.assertEqual(len(self.stats.pieces_par_type), 7)

    def test_ajouter_piece_incremente_compteurs(self):
        """Test : Ajouter une pièce incrémente les bons compteurs."""
        # Ajouter une pièce I
        self.stats.ajouter_piece(TypePiece.I)
        
        self.assertEqual(self.stats.pieces_par_type[TypePiece.I], 1)
        self.assertEqual(self.stats.pieces_placees, 1)
        
        # Ajouter une autre pièce I
        self.stats.ajouter_piece(TypePiece.I)
        
        self.assertEqual(self.stats.pieces_par_type[TypePiece.I], 2)
        self.assertEqual(self.stats.pieces_placees, 2)

    def test_ajouter_piece_types_differents(self):
        """Test : Ajouter différents types de pièces."""
        self.stats.ajouter_piece(TypePiece.I)
        self.stats.ajouter_piece(TypePiece.O)
        self.stats.ajouter_piece(TypePiece.T)
        
        self.assertEqual(self.stats.pieces_par_type[TypePiece.I], 1)
        self.assertEqual(self.stats.pieces_par_type[TypePiece.O], 1)
        self.assertEqual(self.stats.pieces_par_type[TypePiece.T], 1)
        self.assertEqual(self.stats.pieces_placees, 3)

    def test_ajouter_ligne_simple_calcule_score(self):
        """Test : Une ligne simple donne 100 points × niveau."""
        self.stats.ajouter_score_selon_lignes_completees(1)
        
        self.assertEqual(self.stats.score, 100)  # 100 × niveau 1
        self.assertEqual(self.stats.lignes_completees, 1)

    def test_ajouter_double_ligne_calcule_score(self):
        """Test : Deux lignes simultanées donnent 300 points × niveau."""
        self.stats.ajouter_score_selon_lignes_completees(2)
        
        self.assertEqual(self.stats.score, 300)  # 300 × niveau 1
        self.assertEqual(self.stats.lignes_completees, 2)

    def test_ajouter_triple_ligne_calcule_score(self):
        """Test : Trois lignes simultanées donnent 500 points × niveau."""
        self.stats.ajouter_score_selon_lignes_completees(3)
        
        self.assertEqual(self.stats.score, 500)  # 500 × niveau 1
        self.assertEqual(self.stats.lignes_completees, 3)

    def test_ajouter_tetris_calcule_score(self):
        """Test : Tetris (4 lignes) donne 800 points × niveau."""
        self.stats.ajouter_score_selon_lignes_completees(4)
        
        self.assertEqual(self.stats.score, 800)  # 800 × niveau 1
        self.assertEqual(self.stats.lignes_completees, 4)

    def test_progression_niveau_tous_les_10_lignes(self):
        """Test : Le niveau augmente tous les 10 lignes complétées."""
        # Niveau 1 initialement
        self.assertEqual(self.stats.niveau, 1)
        
        # 9 lignes : toujours niveau 1
        for _ in range(9):
            self.stats.ajouter_score_selon_lignes_completees(1)
        self.assertEqual(self.stats.niveau, 1)
        
        # 10ème ligne : passage niveau 2
        self.stats.ajouter_score_selon_lignes_completees(1)
        self.assertEqual(self.stats.niveau, 2)
        
        # 15 lignes : toujours niveau 2
        for _ in range(5):
            self.stats.ajouter_score_selon_lignes_completees(1)
        self.assertEqual(self.stats.niveau, 2)
        
        # 20 lignes : passage niveau 3
        for _ in range(5):
            self.stats.ajouter_score_selon_lignes_completees(1)
        self.assertEqual(self.stats.niveau, 3)

    def test_score_multiplie_par_niveau(self):
        """Test : Le score est multiplié par le niveau actuel."""
        # Compléter 9 lignes simples une par une pour arriver à 9 lignes
        for _ in range(9):
            self.stats.ajouter_score_selon_lignes_completees(1)  # 9 × (100 × 1) = 900 points
        self.assertEqual(self.stats.niveau, 1)
        self.assertEqual(self.stats.score, 900)
        
        # Ajouter la 10ème ligne pour passer au niveau 2
        self.stats.ajouter_score_selon_lignes_completees(1)  # 100 × 1 = 100 points (niveau 1)
        self.assertEqual(self.stats.niveau, 2)  # Niveau mis à jour après
        self.assertEqual(self.stats.score, 1000)
        
        # Ajouter une ligne simple maintenant au niveau 2
        self.stats.ajouter_score_selon_lignes_completees(1)  # 100 × 2 = 200 points
        self.assertEqual(self.stats.score, 1200)

    def test_tetris_au_niveau_superieur(self):
        """Test : Tetris au niveau supérieur donne plus de points."""
        # Passer au niveau 3 (20 lignes) en ajoutant ligne par ligne
        for _ in range(20):
            self.stats.ajouter_score_selon_lignes_completees(1)
        self.assertEqual(self.stats.niveau, 3)
        
        score_avant_tetris = self.stats.score
        
        # Tetris au niveau 3
        self.stats.ajouter_score_selon_lignes_completees(4)
        bonus_tetris = 800 * 3  # 2400 points
        score_attendu = score_avant_tetris + bonus_tetris
        
        self.assertEqual(self.stats.score, score_attendu)

    def test_scenario_partie_complete(self):
        """Test : Scénario d'une partie complète avec progression."""
        # Début de partie
        self.assertEqual(self.stats.score, 0)
        self.assertEqual(self.stats.niveau, 1)
        
        # Placer quelques pièces
        for type_piece in [TypePiece.I, TypePiece.O, TypePiece.T, TypePiece.S]:
            self.stats.ajouter_piece(type_piece)
        self.assertEqual(self.stats.pieces_placees, 4)
        
        # Faire quelques lignes simples
        self.stats.ajouter_score_selon_lignes_completees(1)  # 100 × 1 = 100 points
        self.stats.ajouter_score_selon_lignes_completees(1)  # 100 × 1 = 100 points
        self.assertEqual(self.stats.score, 200)
        
        # Faire un Tetris
        self.stats.ajouter_score_selon_lignes_completees(4)  # 800 × 1 = 800 points
        self.assertEqual(self.stats.score, 1000)
        self.assertEqual(self.stats.lignes_completees, 6)
        
        # Compléter pour atteindre niveau 2 (4 lignes simples de plus = 10 total)
        self.stats.ajouter_score_selon_lignes_completees(1)  # 100 × 1 = 100 points
        self.stats.ajouter_score_selon_lignes_completees(1)  # 100 × 1 = 100 points
        self.stats.ajouter_score_selon_lignes_completees(1)  # 100 × 1 = 100 points
        self.stats.ajouter_score_selon_lignes_completees(1)  # 100 × 1 = 100 points (niveau 1)
        self.assertEqual(self.stats.niveau, 2)  # Niveau mis à jour après la 10ème ligne
        self.assertEqual(self.stats.score, 1400)
        
        # Double ligne maintenant au niveau 2
        self.stats.ajouter_score_selon_lignes_completees(2)  # 300 × 2 = 600 points
        self.assertEqual(self.stats.score, 2000)
        
        # Vérifier cohérence finale
        total_pieces = sum(self.stats.pieces_par_type.values())
        self.assertEqual(total_pieces, self.stats.pieces_placees)

    def test_detection_changement_niveau(self):
        """Test : La méthode détecte quand le niveau change."""
        # Au début, niveau 1
        self.assertEqual(self.stats.niveau, 1)
        
        # 9 lignes : pas de changement de niveau
        niveau_a_change = self.stats.ajouter_score_selon_lignes_completees(9)
        self.assertFalse(niveau_a_change)
        self.assertEqual(self.stats.niveau, 1)
        
        # 10ème ligne : changement de niveau !
        niveau_a_change = self.stats.ajouter_score_selon_lignes_completees(1)
        self.assertTrue(niveau_a_change)
        self.assertEqual(self.stats.niveau, 2)
        
        # 5 lignes de plus : pas de changement
        niveau_a_change = self.stats.ajouter_score_selon_lignes_completees(5)
        self.assertFalse(niveau_a_change)
        self.assertEqual(self.stats.niveau, 2)
        
        # 5 lignes de plus (total 20) : changement vers niveau 3
        niveau_a_change = self.stats.ajouter_score_selon_lignes_completees(5)
        self.assertTrue(niveau_a_change)
        self.assertEqual(self.stats.niveau, 3)


if __name__ == '__main__':
    unittest.main()
