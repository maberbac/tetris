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
        
        print("🚀 Partie complète de Tetris initialisée !")
        print("🏗️ Architecture hexagonale respectée :")
        print("   🎯 Domaine : Logique métier pure")
        print("   🔌 Ports : Interfaces définies")  
        print("   🔧 Adaptateurs : Implémentations pygame")
        print("🎯 Toutes les fonctionnalités sont actives :")
        print("   🎲 Génération aléatoire des 7 types de pièces")
        print("   🏗️ Plateau refactorisé 10x20")
        print("   🎉 Détection automatique des lignes complètes")
        print("   📊 Score et statistiques complètes")
        print("   ⏱️ Chute automatique avec accélération")
        print("   🎵 Système audio intégré")
    
    def jouer(self):
        """Lance la partie principale."""
        # Initialiser l'affichage
        self.affichage.initialiser()
        
        # Démarrer la musique de fond
        print("🎵 Démarrage de la musique...")
        if self.moteur.demarrer_musique():
            print("✅ Musique de fond lancée")
        else:
            print("⚠️ Impossible de lancer la musique (fichier manquant ?)")
        
        horloge = pygame.time.Clock()
        actif = True
        
        print("\n" + "="*60)
        print("🎮 TETRIS - PARTIE COMPLÈTE")
        print("="*60)
        print("🎯 Objectif : Complétez des lignes pour marquer des points !")
        print("📈 Le jeu accélère tous les 10 lignes complétées")
        print()
        print("Contrôles :")
        print("  ← → : Déplacer | ↑ : Rotation | ↓ : Chute rapide")
        print("  ESPACE : Chute instantanée | P : Pause")
        print("  ESC : Menu/Quitter | ENTRÉE : Placer manuellement")
        print()
        print("Démarrage de la partie...")
        print("="*60)
        
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
        
        # Affichage des statistiques finales
        print("\n" + "="*60)
        print("🏁 PARTIE TERMINÉE")
        print("="*60)
        stats = self.moteur.stats
        print(f"📊 Score final: {stats.score:,} points")
        print(f"📈 Niveau atteint: {stats.niveau}")
        print(f"📝 Lignes complétées: {stats.lignes_completees}")
        print(f"🧩 Pièces placées: {stats.pieces_placees}")
        print()
        print("Répartition des pièces utilisées :")
        for type_piece, count in stats.pieces_par_type.items():
            if count > 0:
                print(f"  {type_piece.value}: {count} pièces")
        print("="*60)
        print("Merci d'avoir joué ! 🎮")


if __name__ == "__main__":
    print("🚀 Démarrage de la partie complète de Tetris...")
    print("🏗️ Architecture hexagonale + Génération aléatoire + Interface complète")
    
    try:
        partie = PartieTetris()
        partie.jouer()
    except KeyboardInterrupt:
        print("\n⚠️ Partie interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur durant la partie: {e}")
        import traceback
        traceback.print_exc()
