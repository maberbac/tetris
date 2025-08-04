#!/usr/bin/env python3
"""
Lanceur simple pour la partie complète de Tetris.

Ce script lance directement la partie avec génération aléatoire
des pièces et plateau refactorisé.
"""

import sys
import os

# Ajouter le répertoire src au path si nécessaire
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.domaine.services.logger_tetris import logger_tetris

def main():
    """Lance la partie de Tetris."""
    logger_tetris.info("🚀 Lancement de Tetris...")
    logger_tetris.info("🏗️ Architecture hexagonale respectée")
    logger_tetris.info("🎮 Contrôles : Flèches, Space, P (pause), M (mute), R (restart)")
    logger_tetris.info("=" * 50)
    
    try:
        # Importer et lancer la partie avec architecture hexagonale
        from partie_tetris import PartieTetris
        
        partie = PartieTetris()
        partie.jouer()
        
    except KeyboardInterrupt:
        logger_tetris.info("\n⚠️ Partie interrompue par l'utilisateur")
        return 0
    except ImportError as e:
        logger_tetris.error(f"❌ Erreur d'importation: {e}")
        logger_tetris.error("Assurez-vous que pygame est installé : pip install pygame")
        return 1
    except Exception as e:
        logger_tetris.error(f"❌ Erreur durant la partie: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
