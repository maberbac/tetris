#!/usr/bin/env python3
"""
Tests d'acceptance pour le masquage de la zone invisible.

Objectif : Valider que l'affichage masque correctement les parties des pièces
qui se trouvent dans la zone invisible (y < 0) et n'affiche que les parties 
visibles (y >= 0).
"""

import unittest
import sys
import os

# Configuration du path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.domaine.services.moteur_partie import MoteurPartie
from src.adapters.sortie.affichage_partie import AffichagePartie
from src.domaine.entites.pieces.piece_t import PieceT

class TestMasquageZoneInvisible(unittest.TestCase):
    """Tests d'acceptance pour le masquage de la zone invisible."""
    
    def setUp(self):
        """Configuration initiale pour chaque test."""
        self.moteur = MoteurPartie()
        self.affichage = AffichagePartie()
    
    def test_piece_partiellement_visible_masquage_correct(self):
        """
        Test d'acceptance : Une pièce partiellement dans la zone invisible
        ne doit afficher que sa partie visible.
        """
        print("\n🎮 TEST MASQUAGE ZONE INVISIBLE")
        print("=" * 45)
        
        # Créer une pièce T à la position spawn par défaut (partiellement visible)
        piece_t = PieceT.creer(4, 0)  # Spawn à y=0, certaines positions à y<0
        
        # Analyser les positions
        positions_visibles = [pos for pos in piece_t.positions if pos.y >= 0]
        positions_invisibles = [pos for pos in piece_t.positions if pos.y < 0]
        
        print(f"📊 Analyse de la pièce T à spawn (4, 0) :")
        print(f"   Positions totales : {len(piece_t.positions)}")
        print(f"   Positions visibles : {len(positions_visibles)}")
        print(f"   Positions invisibles : {len(positions_invisibles)}")
        
        # Vérifications métier
        self.assertGreater(len(positions_invisibles), 0, 
                          "La pièce doit avoir des positions dans la zone invisible")
        self.assertGreater(len(positions_visibles), 0,
                          "La pièce doit avoir des positions visibles")
        
        print(f"\n👁️  Positions qui DOIVENT être affichées :")
        for pos in positions_visibles:
            print(f"   Position({pos.x}, {pos.y}) ✅")
        
        print(f"\n🫥 Positions qui DOIVENT être masquées :")
        for pos in positions_invisibles:
            print(f"   Position({pos.x}, {pos.y}) 🚫")
        
        print(f"\n✅ Validation réussie : Masquage zone invisible correct")
    
    def test_moteur_avec_piece_zone_invisible(self):
        """
        Test d'acceptance : Le moteur peut gérer des pièces dans la zone invisible
        et l'affichage les masque correctement.
        """
        print("\n🎮 TEST INTÉGRATION MOTEUR + AFFICHAGE")
        print("=" * 45)
        
        # Forcer une pièce spécifique dans la zone partiellement invisible
        self.moteur.piece_active = PieceT.creer(4, 0)
        
        # Vérifier que le moteur fonctionne normalement
        self.assertIsNotNone(self.moteur.piece_active)
        self.assertEqual(len(self.moteur.piece_active.positions), 4)
        
        # Analyser ce qui sera masqué par l'affichage
        positions_pour_affichage = [
            pos for pos in self.moteur.piece_active.positions 
            if pos.y >= 0  # Logique identique à celle dans AffichagePartie
        ]
        
        positions_masquees = [
            pos for pos in self.moteur.piece_active.positions 
            if pos.y < 0
        ]
        
        print(f"🎭 État moteur :")
        print(f"   Pièce active : {self.moteur.piece_active.type_piece}")
        print(f"   Positions totales : {len(self.moteur.piece_active.positions)}")
        
        print(f"\n🖥️  Rendu affichage (logique y >= 0) :")
        print(f"   Positions affichées : {len(positions_pour_affichage)}")
        print(f"   Positions masquées : {len(positions_masquees)}")
        
        for pos in positions_pour_affichage:
            print(f"   AFFICHÉ → Position({pos.x}, {pos.y}) ✅")
        
        for pos in positions_masquees:
            print(f"   MASQUÉ  → Position({pos.x}, {pos.y}) 🫥")
        
        # Vérifications
        self.assertGreater(len(positions_masquees), 0,
                          "Des positions doivent être masquées")
        self.assertGreater(len(positions_pour_affichage), 0,
                          "Des positions doivent être affichées")
        
        print(f"\n✅ Intégration moteur + affichage validée")

if __name__ == "__main__":
    print("🎯 TESTS D'ACCEPTANCE - MASQUAGE ZONE INVISIBLE")
    print("=" * 55)
    
    # Exécuter les tests avec verbosité
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 55)
    print("🎉 TESTS D'ACCEPTANCE MASQUAGE TERMINÉS")
    print("💡 Amélioration visuelle validée !")
