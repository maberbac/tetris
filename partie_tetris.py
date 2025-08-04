"""
Orchestrateur principal de la partie de Tetris complète.

Architecture hexagonale respectée :
- Domaine : MoteurPartie, StatistiquesJeu, Commandes
- Ports : Interfaces ControleurJeu, AffichageJeu  
- Adaptateurs : GestionnairePartie (pygame), AffichagePartie (pygame)
"""

import pygame
import sys
import os
import time

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.domaine.services.moteur_partie import MoteurPartie
from src.adapters.entree.gestionnaire_partie import GestionnairePartie
from src.adapters.sortie.affichage_partie import AffichagePartie
from src.adapters.sortie.audio_partie import AudioPartie
from src.domaine.services.logger_tetris import logger_tetris


class PartieTetris:
    """
    Orchestrateur principal de la partie de Tetris.
    
    🏗️ ARCHITECTURE HEXAGONALE :
    - Cœur métier : MoteurPartie (domaine)
    - Contrôle : GestionnairePartie (adaptateur d'entrée)
    - Affichage : AffichagePartie (adaptateur de sortie)
    """
    
    def __init__(self):
        # Adaptateurs - Infrastructure
        self.audio = AudioPartie()
        
        # Cœur métier - Domaine (avec injection de dépendance audio)
        self.moteur = MoteurPartie(audio=self.audio)
        
        # Autres adaptateurs
        self.affichage = AffichagePartie()
        self.gestionnaire = GestionnairePartie()
        
        # Configuration des délais optimisés pour le gameplay
        self.gestionnaire.configurer_delais_repetition(
            delai_initial=0.2,  # Plus rapide pour le jeu réel
            delai_repetition=0.12
        )
        
        logger_tetris.info("🚀 Partie complète de Tetris initialisée !")
        logger_tetris.info("🏗️ Architecture hexagonale respectée :")
        logger_tetris.info("   🎯 Domaine : Logique métier pure")
        logger_tetris.info("   🔌 Ports : Interfaces définies")  
        logger_tetris.info("   🔧 Adaptateurs : Implémentations pygame")
        logger_tetris.info("🎯 Toutes les fonctionnalités sont actives :")
        logger_tetris.info("   🎲 Génération aléatoire des 7 types de pièces")
        logger_tetris.info("   🏗️ Plateau refactorisé 10x20")
        logger_tetris.info("   🎉 Détection automatique des lignes complètes")
        logger_tetris.info("   📊 Score et statistiques complètes")
        logger_tetris.info("   ⏱️ Chute automatique avec accélération")
        logger_tetris.info("   🎵 Système audio intégré")
    
    def jouer(self):
        """Lance la partie principale."""
        # Initialiser l'affichage
        self.affichage.initialiser()
        
        # Démarrer la musique de fond
        logger_tetris.debug("🎵 Démarrage de la musique...")
        if self.moteur.demarrer_musique():
            logger_tetris.info("✅ Musique de fond lancée")
        else:
            logger_tetris.warning("⚠️ Impossible de lancer la musique (fichier manquant ?)")
        
        horloge = pygame.time.Clock()
        actif = True
        
        logger_tetris.info("\n" + "="*60)
        logger_tetris.info("🎮 TETRIS - PARTIE COMPLÈTE")
        logger_tetris.info("="*60)
        logger_tetris.info("🎯 Objectif : Complétez des lignes pour marquer des points !")
        logger_tetris.info("📈 Le jeu accélère tous les 10 lignes complétées")
        logger_tetris.info("")
        
        try:
            while actif:
                temps_actuel = time.time()
                
                # Mise à jour du jeu - CHUTE AUTOMATIQUE D'ABORD
                if not self.moteur.en_pause and not self.moteur.jeu_termine:
                    # Chute automatique AVANT les événements utilisateur
                    self.moteur.mettre_a_jour_chute_automatique()
                
                # Traiter les événements via l'adaptateur d'entrée
                actif = self.gestionnaire.traiter_evenements(self.moteur, temps_actuel)
                
                # Répétition des touches (après les événements principaux)
                if not self.moteur.en_pause and not self.moteur.jeu_termine:
                    self.gestionnaire.mettre_a_jour_repetitions(self.moteur, temps_actuel)
                
                # Affichage via l'adaptateur de sortie
                self.affichage.dessiner(self.moteur)
                horloge.tick(60)
        
        finally:
            # Nettoyage des ressources
            self.affichage.nettoyer()
            self.moteur.fermer()  # Nettoie l'audio
        



if __name__ == "__main__":

    try:
        partie = PartieTetris()
        partie.jouer()
    except KeyboardInterrupt:
        logger_tetris.info("⚠️ Partie interrompue par l'utilisateur")
    except Exception as e:
        logger_tetris.error(f"❌ Erreur durant la partie: {e}")
        import traceback
        traceback.print_exc()
