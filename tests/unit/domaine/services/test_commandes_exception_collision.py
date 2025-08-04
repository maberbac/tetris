#!/usr/bin/env python3
"""
Tests unitaires pour l'intégration de ExceptionCollision dans les commandes.
Phase TDD RED - Tests qui vont échouer avant implémentation.
"""

import unittest
import sys
import os

# Ajouter le répertoire src au chemin depuis la racine du projet
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.insert(0, project_root)

from src.domaine.entites.plateau import Plateau
from src.domaine.entites.pieces.piece_i import PieceI
from src.domaine.entites.pieces.piece_t import PieceT
from src.domaine.entites.piece import TypePiece
from src.domaine.entites.fabriques.fabrique_pieces import FabriquePieces
from src.domaine.exceptions.exception_collision import ExceptionCollision
from src.domaine.services.commandes.commandes_base import (
    CommandeDeplacerGauche,
    CommandeDeplacerDroite, 
    CommandeTourner
)


class MoteurTest:
    """Moteur de test minimal pour les commandes."""
    
    def __init__(self, plateau: Plateau, piece_active):
        self.plateau = plateau
        self.piece_active = piece_active
        
    def obtenir_plateau(self):
        return self.plateau
        
    def obtenir_piece_active(self):
        return self.piece_active


class TestExceptionCollisionCommandes(unittest.TestCase):
    """Tests TDD RED pour ExceptionCollision dans les commandes."""
    
    def setUp(self):
        """Préparer les tests avec un plateau et des pièces."""
        self.plateau = Plateau(10, 20)
        self.fabrique = FabriquePieces()
        
    def test_commande_deplacer_gauche_leve_exception_collision_bord_gauche(self):
        """Test RED : CommandeDeplacerGauche lève ExceptionCollision au bord gauche."""
        # Créer une pièce au bord gauche (x=0)
        piece = self.fabrique.creer(TypePiece.I, x_pivot=0, y_pivot=5)
        moteur = MoteurTest(self.plateau, piece)
        commande = CommandeDeplacerGauche()
        
        # TEST RED : Doit lever ExceptionCollision
        with self.assertRaises(ExceptionCollision) as context:
            commande.execute(moteur)
            
        # Vérifier le message d'erreur
        self.assertIn("gauche", str(context.exception).lower())
        
    def test_commande_deplacer_droite_leve_exception_collision_bord_droit(self):
        """Test RED : CommandeDeplacerDroite lève ExceptionCollision au bord droit."""
        # Créer une pièce au bord droit (x=9 pour pièce I)
        piece = self.fabrique.creer(TypePiece.I, x_pivot=9, y_pivot=5)
        moteur = MoteurTest(self.plateau, piece)
        commande = CommandeDeplacerDroite()
        
        # TEST RED : Doit lever ExceptionCollision
        with self.assertRaises(ExceptionCollision) as context:
            commande.execute(moteur)
            
        # Vérifier le message d'erreur
        self.assertIn("droite", str(context.exception).lower())
        
    def test_commande_tourner_leve_exception_collision_pas_de_place(self):
        """Test RED : CommandeTourner lève ExceptionCollision quand pas de place."""
        # Créer une pièce I horizontale très proche du bord gauche
        piece = self.fabrique.creer(TypePiece.I, x_pivot=1, y_pivot=5)
        # Forcer horizontale puis tenter rotation vers verticale
        piece.tourner()  # Maintenant horizontale
        
        moteur = MoteurTest(self.plateau, piece)
        commande = CommandeTourner()
        
        # TEST RED : Doit lever ExceptionCollision
        with self.assertRaises(ExceptionCollision) as context:
            commande.execute(moteur)
            
        # Vérifier le message d'erreur
        self.assertIn("tourner", str(context.exception).lower())
        
    def test_commande_deplacer_gauche_reussit_si_pas_collision(self):
        """Test : CommandeDeplacerGauche réussit si pas de collision."""
        # Créer une pièce avec de la place à gauche
        piece = self.fabrique.creer(TypePiece.I, x_pivot=5, y_pivot=5)
        moteur = MoteurTest(self.plateau, piece)
        commande = CommandeDeplacerGauche()
        
        # Ne doit PAS lever d'exception
        try:
            resultat = commande.execute(moteur)
            self.assertTrue(resultat)  # Commande réussie
        except ExceptionCollision:
            self.fail("ExceptionCollision levée pour un déplacement valide")
            
    def test_commande_deplacer_droite_reussit_si_pas_collision(self):
        """Test : CommandeDeplacerDroite réussit si pas de collision.""" 
        # Créer une pièce avec de la place à droite
        piece = self.fabrique.creer(TypePiece.I, x_pivot=5, y_pivot=5)
        moteur = MoteurTest(self.plateau, piece)
        commande = CommandeDeplacerDroite()
        
        # Ne doit PAS lever d'exception
        try:
            resultat = commande.execute(moteur)
            self.assertTrue(resultat)  # Commande réussie
        except ExceptionCollision:
            self.fail("ExceptionCollision levée pour un déplacement valide")
            
    def test_commande_tourner_reussit_si_pas_collision(self):
        """Test : CommandeTourner réussit si pas de collision."""
        # Créer une pièce T avec de la place pour tourner
        piece = self.fabrique.creer(TypePiece.T, x_pivot=5, y_pivot=5)
        moteur = MoteurTest(self.plateau, piece)
        commande = CommandeTourner()
        
        # Ne doit PAS lever d'exception
        try:
            resultat = commande.execute(moteur)
            self.assertTrue(resultat)  # Commande réussie
        except ExceptionCollision:
            self.fail("ExceptionCollision levée pour une rotation valide")
            
    def test_commande_deplacer_gauche_avec_plateau_plein(self):
        """Test RED : CommandeDeplacerGauche avec obstacles sur le plateau."""
        # Placer une pièce
        piece = self.fabrique.creer(TypePiece.I, x_pivot=5, y_pivot=5)
        
        # Remplir le plateau à gauche de la pièce
        from src.domaine.entites.position import Position
        for y in range(4, 8):
            self.plateau._positions_occupees.add(Position(4, y))
            
        moteur = MoteurTest(self.plateau, piece)
        commande = CommandeDeplacerGauche()
        
        # TEST RED : Doit lever ExceptionCollision
        with self.assertRaises(ExceptionCollision) as context:
            commande.execute(moteur)
            
        # Vérifier le message d'erreur
        self.assertIn("gauche", str(context.exception).lower())


if __name__ == '__main__':
    print("🧪 TESTS TDD RED - ExceptionCollision dans commandes")
    print("=" * 60)
    print("Ces tests vont ÉCHOUER avant implémentation (phase RED)")
    print("=" * 60)
    unittest.main()
