"""
Test des contrôles simplifiés - Tetris

Contrôles disponibles :
← Flèche gauche : Déplacer la pièce vers la gauche
→ Flèche droite : Déplacer la pièce vers la droite  
↑ Flèche haut : Tourner la pièce
↓ Flèche bas : Chute rapide (une ligne par frame)
Space : Chute instantanée (jusqu'en bas)
Esc : Afficher le menu en jeu
P : Pause/Reprendre
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from domaine.services import GestionnaireEvenements, TypeEvenement, ToucheClavier
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
            print("  💫 Pièce descendue d'une ligne")
            return True
        
        def placer_piece_definitivement(self):
            print("  📍 Pièce placée définitivement")
        
        def generer_nouvelle_piece(self):
            self.piece = self.fabrique.creer_aleatoire(x_pivot=5, y_pivot=1)
            print(f"  🆕 Nouvelle pièce: {self.piece.type_piece.value}")
    
    def test_controles_simplifies():
        print("🎮 TEST CONTRÔLES SIMPLIFIÉS")
        print("=" * 50)
        
        gestionnaire = GestionnaireEvenements()
        moteur = MoteurTest()
        
        # Afficher le mapping actuel
        mapping = gestionnaire.obtenir_touches_mappees()
        print("🗝️  Contrôles configurés:")
        for touche_physique, touche_logique in mapping.items():
            print(f"   {touche_physique:10} → {touche_logique.value}")
        
        print(f"\n📊 {gestionnaire.statistiques()}")
        
        # Tests des contrôles
        tests = [
            ("Left", "← Déplacement gauche"),
            ("Right", "→ Déplacement droite"),  
            ("Up", "↑ Rotation"),
            ("Down", "↓ Chute rapide"),
            ("space", "⚡ Chute instantanée"),
            ("Escape", "🎛️  Menu en jeu"),
            ("p", "⏸️ Pause/Reprendre")
        ]
        
        print("\n🧪 Tests des contrôles:")
        for touche, description in tests:
            print(f"\n{description}")
            
            pivot_avant = moteur.piece.obtenir_pivot()
            orientation_avant = moteur.piece._orientation
            
            resultat = gestionnaire.traiter_evenement_clavier(
                touche, TypeEvenement.CLAVIER_APPUI, moteur
            )
            
            pivot_apres = moteur.piece.obtenir_pivot()
            orientation_apres = moteur.piece._orientation
            
            print(f"  Résultat: {'✅' if resultat else '❌'}")
            
            # Afficher les changements si applicable
            if pivot_avant != pivot_apres:
                print(f"  Position: ({pivot_avant.x}, {pivot_avant.y}) → ({pivot_apres.x}, {pivot_apres.y})")
            if orientation_avant != orientation_apres:
                print(f"  Orientation: {orientation_avant.value} → {orientation_apres.value}")
        
        print("\n🎉 Test terminé - Contrôles simplifiés prêts !")
        print("\nRésumé des contrôles :")
        print("  ← → : Déplacement horizontal")
        print("  ↑   : Rotation") 
        print("  ↓   : Chute rapide")
        print("  SPC : Chute instantanée")
        print("  ESC : Menu")
        print("  P   : Pause")
    
    test_controles_simplifies()
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
