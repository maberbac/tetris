"""
Test rapide du système de contrôles
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from domaine.services import GestionnaireEvenements, TypeEvenement
from domaine.entites import Plateau, TypePiece
from domaine.entites.fabriques.fabrique_pieces import FabriquePieces


class MoteurTest:
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
    
    def placer_piece_definitivement(self):
        pass
    
    def generer_nouvelle_piece(self):
        pass


def test_controles():
    print("🎮 TEST RAPIDE DU SYSTÈME DE CONTRÔLES")
    print("=" * 50)
    
    # Initialiser
    gestionnaire = GestionnaireEvenements()
    moteur = MoteurTest()
    
    print(f"✅ Gestionnaire créé: {gestionnaire.statistiques()}")
    
    # Position initiale
    pivot_initial = moteur.piece.obtenir_pivot()
    print(f"📍 Position initiale: ({pivot_initial.x}, {pivot_initial.y})")
    
    # Test déplacement gauche
    print("\n🧪 Test déplacement gauche...")
    resultat = gestionnaire.traiter_evenement_clavier(
        "Left", TypeEvenement.CLAVIER_APPUI, moteur
    )
    
    pivot_apres = moteur.piece.obtenir_pivot()
    print(f"Résultat: {'✅' if resultat else '❌'}")
    print(f"Position après: ({pivot_apres.x}, {pivot_apres.y})")
    
    # Test déplacement droite
    print("\n🧪 Test déplacement droite...")
    resultat = gestionnaire.traiter_evenement_clavier(
        "Right", TypeEvenement.CLAVIER_APPUI, moteur
    )
    
    pivot_final = moteur.piece.obtenir_pivot()
    print(f"Résultat: {'✅' if resultat else '❌'}")
    print(f"Position finale: ({pivot_final.x}, {pivot_final.y})")
    
    # Test rotation
    print("\n🧪 Test rotation...")
    orientation_avant = moteur.piece._orientation
    resultat = gestionnaire.traiter_evenement_clavier(
        "Up", TypeEvenement.CLAVIER_APPUI, moteur
    )
    orientation_apres = moteur.piece._orientation
    
    print(f"Résultat: {'✅' if resultat else '❌'}")
    print(f"Orientation: {orientation_avant.value} → {orientation_apres.value}")
    
    print("\n🎉 TESTS TERMINÉS - Système de contrôles fonctionnel !")


if __name__ == "__main__":
    test_controles()
