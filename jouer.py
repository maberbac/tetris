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
from src.domaine.exceptions.exception_audio import ExceptionAudio

def main():
    """Lance la partie de Tetris."""
    logger_tetris.info("🚀 Lancement de Tetris...")
    logger_tetris.info("🏗️ Architecture hexagonale respectée")
    logger_tetris.info("🎮 Contrôles : Flèches, Space, P (pause), M (mute), R (restart)")
    logger_tetris.info("=" * 50)
    
    # Boucle de retry pour permettre au jeu de continuer sans audio
    tentatives_max = 2
    tentative = 0
    
    while tentative < tentatives_max:
        try:
            # Importer et lancer la partie avec architecture hexagonale
            from partie_tetris import PartieTetris
            
            partie = PartieTetris()
            partie.jouer()
            break  # Si on arrive ici, le jeu s'est terminé normalement
            
        except ExceptionAudio as e:
            tentative += 1
            logger_tetris.warning(f"⚠️ Problème audio (tentative {tentative}/{tentatives_max}) : {e}")
            
            if tentative < tentatives_max:
                logger_tetris.info("🎮 Tentative de redémarrage sans audio...")
                logger_tetris.info("💡 Le jeu va essayer de fonctionner en mode dégradé")
                # Continue la boucle pour une nouvelle tentative
                continue
            else:
                logger_tetris.error("❌ Impossible de démarrer le jeu même en mode dégradé")
                logger_tetris.info("💡 Vérifiez que pygame est correctement installé : pip install pygame")
                logger_tetris.info("💡 Assurez-vous que les fichiers audio sont présents dans assets/audio/")
                return 1  # Échec après toutes les tentatives
                
        except ImportError as e:
            logger_tetris.error(f"❌ Erreur d'importation: {e}")
            logger_tetris.error("Assurez-vous que pygame est installé : pip install pygame")
            return 1
        except FileNotFoundError as e:
            logger_tetris.error(f"❌ Fichier requis introuvable: {e}")
            logger_tetris.error("Vérifiez que tous les assets sont présents dans le répertoire 'assets/'")
            logger_tetris.error("Le jeu peut fonctionner sans audio si les fichiers .wav sont manquants")
            return 1
        except MemoryError as e:
            logger_tetris.error(f"❌ Mémoire insuffisante: {e}")
            logger_tetris.error("Fermez d'autres applications pour libérer de la mémoire")
            logger_tetris.error("Essayez de redémarrer votre ordinateur si le problème persiste")
            return 1
        except Exception as e:
            logger_tetris.error(f"❌ Erreur durant la partie: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
