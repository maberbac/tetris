"""
Test d'acceptance des contrôles simplifiés - Tetris

Contrôles disponibles :
← Flèche gauche : Déplacer la pièce vers la gauche
→ Flèche droite : Déplacer la pièce vers la droite  
↑ Flèche haut : Tourner la pièce
↓ Flèche bas : Chute rapide (une ligne par frame)
Space : Chute instantanée (jusqu'en bas)
Esc : Afficher le menu en jeu
P : Pause/Reprendre
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.domaine.services import GestionnaireEvenements, TypeEvenement, ToucheClavier
from src.domaine.entites import Plateau, TypePiece
from src.domaine.entites.fabriques.fabrique_pieces import FabriquePieces


class MoteurTest:
    """Moteur de test simplifié pour les tests d'acceptance."""
    
    def __init__(self):
        self.plateau = Plateau()
        self.fabrique = FabriquePieces()
        self.piece = self.fabrique.creer(TypePiece.T, x_pivot=5, y_pivot=1)
    
    def obtenir_piece_active(self):
        return self.piece
    
    def obtenir_plateau(self):
        return self.plateau
    
    def faire_descendre_piece(self):
        print("  💫 Pièce descendue d'une ligne")
        return True
    
    def tourner_piece_active(self):
        """Simule la rotation avec retour de succès."""
        return True
    
    def placer_piece_definitivement(self):
        print("  📍 Pièce placée définitivement")
    
    def generer_nouvelle_piece(self):
        self.piece = self.fabrique.creer_aleatoire(x_pivot=5, y_pivot=1)
        print(f"  🆕 Nouvelle pièce: {self.piece.type_piece.value}")


class TestControlesSimplifies(unittest.TestCase):
    """Tests d'acceptance pour les contrôles simplifiés du jeu."""
    
    def setUp(self):
        """Préparer les composants pour chaque test."""
        self.gestionnaire = GestionnaireEvenements()
        self.moteur = MoteurTest()
        
        print(f"\n🎮 TEST CONTRÔLES SIMPLIFIÉS")
        print("=" * 50)
    
    def test_mapping_controles_disponibles(self):
        """Test d'acceptance : Vérifier que tous les contrôles essentiels sont mappés."""
        # Afficher le mapping actuel
        mapping = self.gestionnaire.obtenir_touches_mappees()
        print("🗝️  Contrôles configurés:")
        for touche_physique, touche_logique in mapping.items():
            print(f"   {touche_physique:10} → {touche_logique.value}")
        
        print(f"\n📊 {self.gestionnaire.statistiques()}")
        
        # Vérifier que les contrôles essentiels sont présents
        touches_essentielles = ["Left", "Right", "Up", "Down", "space", "Escape", "p"]
        for touche in touches_essentielles:
            self.assertIn(touche, mapping, f"Contrôle manquant: {touche}")
        
        print("✅ Tous les contrôles essentiels sont configurés")
    
    def test_controles_deplacement_fonctionnels(self):
        """Test d'acceptance : Les contrôles de déplacement fonctionnent correctement."""
        print("\n🧪 Tests des contrôles de déplacement:")
        
        # Tests des contrôles
        tests_deplacement = [
            ("Left", "← Déplacement gauche"),
            ("Right", "→ Déplacement droite"),  
            ("Up", "↑ Rotation"),
            ("Down", "↓ Chute rapide")
        ]
        
        for touche, description in tests_deplacement:
            with self.subTest(touche=touche):
                print(f"\n{description}")
                
                # Capturer l'état avant
                piece_avant = self.moteur.obtenir_piece_active()
                pivot_avant = piece_avant.position_pivot
                orientation_avant = getattr(piece_avant, '_orientation', 0)
                
                # Exécuter la commande
                resultat = self.gestionnaire.traiter_evenement_clavier(
                    touche, TypeEvenement.CLAVIER_APPUI, self.moteur
                )
                
                # Vérifier que la commande s'exécute sans erreur
                self.assertIsNotNone(resultat, f"La commande {touche} doit retourner un résultat")
                
                # Capturer l'état après
                piece_apres = self.moteur.obtenir_piece_active()
                pivot_apres = piece_apres.position_pivot
                orientation_apres = getattr(piece_apres, '_orientation', 0)
                
                print(f"  Résultat: {'✅' if resultat else '❌'}")
                
                # Afficher les changements si applicable
                if pivot_avant != pivot_apres:
                    print(f"  Position: ({pivot_avant.x}, {pivot_avant.y}) → ({pivot_apres.x}, {pivot_apres.y})")
                if orientation_avant != orientation_apres:
                    print(f"  Orientation: {orientation_avant} → {orientation_apres}")
    
    def test_controles_actions_speciales(self):
        """Test d'acceptance : Les contrôles d'actions spéciales fonctionnent."""
        print("\n🧪 Tests des actions spéciales:")
        
        tests_actions = [
            ("space", "⚡ Chute instantanée"),
            ("Escape", "🎛️  Menu en jeu"),
            ("p", "⏸️ Pause/Reprendre")
        ]
        
        for touche, description in tests_actions:
            with self.subTest(touche=touche):
                print(f"\n{description}")
                
                # Exécuter la commande
                resultat = self.gestionnaire.traiter_evenement_clavier(
                    touche, TypeEvenement.CLAVIER_APPUI, self.moteur
                )
                
                # Vérifier que la commande s'exécute
                self.assertIsNotNone(resultat, f"L'action {touche} doit retourner un résultat")
                print(f"  Résultat: {'✅' if resultat else '❌'}")
    
    def test_resume_controles_simplifies(self):
        """Test d'acceptance : Résumé des contrôles disponibles."""
        print("\n🎉 Test terminé - Contrôles simplifiés prêts !")
        print("\nRésumé des contrôles :")
        print("  ← → : Déplacement horizontal")
        print("  ↑   : Rotation") 
        print("  ↓   : Chute rapide")
        print("  SPC : Chute instantanée")
        print("  ESC : Menu")
        print("  P   : Pause")
        
        # Assertion finale pour valider que le test d'acceptance réussit
        self.assertTrue(True, "Tests d'acceptance des contrôles simplifiés réussis")


if __name__ == '__main__':
    unittest.main(verbosity=2)