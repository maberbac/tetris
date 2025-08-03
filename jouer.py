#!/usr/bin/env python3
"""
Lanceur simple pour la partie complète de Tetris.

Ce script lance directement la partie avec génération aléatoire
des pièces et plateau refactorisé.
"""

import sys
import os

def main():
    """Lance la partie de Tetris."""
    print("🚀 Lancement de Tetris...")
    print("🏗️ Architecture hexagonale respectée")
    print("🎮 Contrôles : Flèches, Space, P (pause), M (mute), R (restart)")
    print("=" * 50)
    
    try:
        # Importer et lancer la partie avec architecture hexagonale
        from partie_tetris import PartieTetris
        
        partie = PartieTetris()
        partie.jouer()
        
    except KeyboardInterrupt:
        print("\n⚠️ Partie interrompue par l'utilisateur")
        return 0
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        print("Assurez-vous que pygame est installé : pip install pygame")
        return 1
    except Exception as e:
        print(f"❌ Erreur durant la partie: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
