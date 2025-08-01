"""
Lanceur de démonstrations avec Plateau Refactorisé

Ce script permet de lancer facilement toutes les démonstrations 6x6
utilisant le vrai plateau refactorisé.

✨ AVANTAGES du plateau refactorisé :
- 🎯 Pas de code dupliqué (PlateauDemoX)
- 🎉 Détection automatique des lignes complètes
- 🧹 Code plus propre et maintenable
- ⚡ Intégration complète avec l'architecture
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def afficher_menu():
    """Affiche le menu de sélection des démonstrations."""
    print("\n" + "="*60)
    print("🎮 DÉMONSTRATIONS TETRIS - PLATEAU REFACTORISÉ")
    print("="*60)
    print()
    print("✨ Ces démos utilisent le vrai Plateau(6, 6) refactorisé !")
    print("🎯 Avantages : lignes complètes, code propre, intégration totale")
    print()
    print("Sélectionnez une pièce à démontrer :")
    print()
    print("  [I] - Pièce I (Cyan) - Barre droite")
    print("  [O] - Pièce O (Jaune) - Carré")
    print("  [T] - Pièce T (Violet) - T")
    print("  [S] - Pièce S (Vert) - S")
    print("  [Z] - Pièce Z (Rouge) - Z")
    print("  [J] - Pièce J (Bleu) - J")
    print("  [L] - Pièce L (Orange) - L")
    print()
    print("  [A] - Toutes les pièces (cycle automatique)")
    print("  [Q] - Quitter")
    print()
    print("="*60)

def lancer_demo_piece(piece: str):
    """Lance la démonstration pour une pièce spécifique."""
    print(f"\n🚀 Lancement de la démo pour la pièce {piece}...")
    
    try:
        if piece.upper() == 'I':
            from demo_i_avec_plateau import DemoIAvecPlateauRefactorise
            demo = DemoIAvecPlateauRefactorise()
            demo.executer()
            
        elif piece.upper() == 'O':
            from demo_o_avec_plateau import DemoOAvecPlateauRefactorise
            demo = DemoOAvecPlateauRefactorise()
            demo.executer()
            
        elif piece.upper() == 'T':
            from demo_t_avec_plateau import DemoTAvecPlateauRefactorise
            demo = DemoTAvecPlateauRefactorise()
            demo.executer()
            
        elif piece.upper() == 'S':
            from demo_s_avec_plateau import DemoSAvecPlateauRefactorise
            demo = DemoSAvecPlateauRefactorise()
            demo.executer()
            
        elif piece.upper() == 'Z':
            from demo_z_avec_plateau import DemoZAvecPlateauRefactorise
            demo = DemoZAvecPlateauRefactorise()
            demo.executer()
            
        elif piece.upper() == 'J':
            from demo_j_avec_plateau import DemoJAvecPlateauRefactorise
            demo = DemoJAvecPlateauRefactorise()
            demo.executer()
            
        elif piece.upper() == 'L':
            from demo_l_avec_plateau import DemoLAvecPlateauRefactorise
            demo = DemoLAvecPlateauRefactorise()
            demo.executer()
            
        elif piece.upper() == 'L':
            from demo_l_avec_plateau import DemoLAvecPlateauRefactorise
            demo = DemoLAvecPlateauRefactorise()
            demo.executer()
            
        elif piece.upper() == 'A':
            print("🚧 Mode cycle automatique en cours de développement...")
            # lancer_cycle_automatique()
            
        else:
            print(f"❌ Pièce '{piece}' non reconnue.")
            return False
            
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import : {e}")
        print(f"🚧 La démo pour la pièce {piece} n'est pas encore implémentée.")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du lancement : {e}")
        return False

def main():
    """Fonction principale du lanceur."""
    print("🎮 Lanceur de démonstrations Tetris avec plateau refactorisé")
    
    while True:
        afficher_menu()
        
        try:
            choix = input("Votre choix : ").strip()
            
            if not choix:
                continue
                
            if choix.upper() == 'Q':
                print("\n👋 Au revoir !")
                break
                
            if choix.upper() in ['I', 'O', 'T', 'S', 'Z', 'J', 'L', 'A']:
                success = lancer_demo_piece(choix)
                if success:
                    print(f"\n✨ Démo {choix.upper()} terminée.")
                else:
                    print(f"\n⚠️ Impossible de lancer la démo {choix.upper()}.")
                
                input("\nAppuyez sur Entrée pour continuer...")
            else:
                print(f"\n❌ Choix '{choix}' invalide. Utilisez I, O, T, S, Z, J, L, A ou Q.")
                input("Appuyez sur Entrée pour continuer...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interruption clavier - Au revoir !")
            break
        except Exception as e:
            print(f"\n❌ Erreur inattendue : {e}")
            input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    # Changer le répertoire de travail vers le répertoire du script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
