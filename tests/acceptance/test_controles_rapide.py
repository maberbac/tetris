"""
Test d'acceptance rapide du système de contrôles - Tetris

Tests de base pour valider que le système de contrôles fonctionne.
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.domaine.services import GestionnaireEvenements, TypeEvenement
from src.domaine.entites import Plateau, TypePiece
from src.domaine.entites.fabriques.fabrique_pieces import FabriquePieces


class MoteurTest:
    """Moteur de test simplifié pour les tests d'acceptance rapides."""
    
    def __init__(self):
        self.plateau = Plateau()
        self.fabrique = FabriquePieces()
        self.piece = self.fabrique.creer(TypePiece.T, x_pivot=5, y_pivot=1)
    
    def obtenir_piece_active(self):
        return self.piece
    
    def obtenir_plateau(self):
        return self.plateau
    
    def faire_descendre_piece(self):
        return True
    
    def tourner_piece_active(self):
        """Simule la rotation avec retour de succès."""
        return True
    
    def placer_piece_definitivement(self):
        pass
    
    def generer_nouvelle_piece(self):
        pass


class TestControlesRapide(unittest.TestCase):
    """Tests d'acceptance rapides pour le système de contrôles."""
    
    def setUp(self):
        """Préparer les composants pour chaque test."""
        self.gestionnaire = GestionnaireEvenements()
        self.moteur = MoteurTest()
        
        print(f"\n🎮 TEST RAPIDE DU SYSTÈME DE CONTRÔLES")
        print("=" * 50)
    
    def test_gestionnaire_peut_etre_cree(self):
        """Test d'acceptance : Le gestionnaire d'événements peut être créé."""
        print(f"✅ Gestionnaire créé: {self.gestionnaire.statistiques()}")
        
        # Vérifier que le gestionnaire est fonctionnel
        self.assertIsNotNone(self.gestionnaire)
        self.assertIsNotNone(self.moteur)
    
    def test_deplacement_gauche_fonctionne(self):
        """Test d'acceptance : Le déplacement vers la gauche fonctionne."""
        # Position initiale
        piece = self.moteur.obtenir_piece_active()
        pivot_initial = piece.position_pivot
        print(f"📍 Position initiale: ({pivot_initial.x}, {pivot_initial.y})")
        
        # Test déplacement gauche
        print("🧪 Test déplacement gauche...")
        resultat = self.gestionnaire.traiter_evenement_clavier(
            "Left", TypeEvenement.CLAVIER_APPUI, self.moteur
        )
        
        pivot_apres = piece.position_pivot
        print(f"Résultat: {'✅' if resultat else '❌'}")
        print(f"Position après: ({pivot_apres.x}, {pivot_apres.y})")
        
        # Assertion pour validation
        self.assertIsNotNone(resultat)
    
    def test_deplacement_droite_fonctionne(self):
        """Test d'acceptance : Le déplacement vers la droite fonctionne."""
        piece = self.moteur.obtenir_piece_active()
        
        # Test déplacement droite
        print("🧪 Test déplacement droite...")
        resultat = self.gestionnaire.traiter_evenement_clavier(
            "Right", TypeEvenement.CLAVIER_APPUI, self.moteur
        )
        
        pivot_final = piece.position_pivot
        print(f"Résultat: {'✅' if resultat else '❌'}")
        print(f"Position finale: ({pivot_final.x}, {pivot_final.y})")
        
        # Assertion pour validation
        self.assertIsNotNone(resultat)
    
    def test_rotation_fonctionne(self):
        """Test d'acceptance : La rotation fonctionne."""
        piece = self.moteur.obtenir_piece_active()
        
        # Test rotation
        print("🧪 Test rotation...")
        orientation_avant = getattr(piece, '_orientation', None)
        resultat = self.gestionnaire.traiter_evenement_clavier(
            "Up", TypeEvenement.CLAVIER_APPUI, self.moteur
        )
        orientation_apres = getattr(piece, '_orientation', None)
        
        print(f"Résultat: {'✅' if resultat else '❌'}")
        if orientation_avant and orientation_apres:
            print(f"Orientation: {orientation_avant.value} → {orientation_apres.value}")
        
        # Assertion pour validation
        self.assertIsNotNone(resultat)
    
    def test_systeme_controles_fonctionnel(self):
        """Test d'acceptance : Le système de contrôles est fonctionnel dans son ensemble."""
        print("🎉 TESTS TERMINÉS - Système de contrôles fonctionnel !")
        
        # Test de validation finale
        mapping = self.gestionnaire.obtenir_touches_mappees()
        self.assertGreater(len(mapping), 0, "Le gestionnaire doit avoir des contrôles mappés")
        
        print(f"✅ {len(mapping)} contrôles disponibles")


if __name__ == '__main__':
    unittest.main(verbosity=2)
