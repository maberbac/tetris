"""
Moteur principal de la partie de Tetris.

Service du domaine qui orchestre la logique métier du jeu.
"""

import time
from typing import Optional

from src.domaine.entites.fabriques.fabrique_pieces import FabriquePieces
from src.domaine.entites.piece import Piece
from src.domaine.entites.position import Position
from src.domaine.entites.plateau import Plateau
from src.domaine.entites.statistiques.statistiques_jeu import StatistiquesJeu
from src.ports.sortie.audio_jeu import AudioJeu


class MoteurPartie:
    """
    Moteur principal de la partie de Tetris.
    
    🎯 FONCTIONNALITÉS :
    - Plateau refactorisé 10x20
    - Génération aléatoire des pièces
    - Détection automatique des lignes complètes
    - Score et statistiques
    - Système de pause
    """
    
    def __init__(self, audio: Optional[AudioJeu] = None):
        # Plateau principal (10x20 standard Tetris)
        self.plateau = Plateau(10, 20)
        
        # Fabrique pour générer les pièces
        self.fabrique = FabriquePieces()
        
        # Pièce actuellement contrôlée
        self.piece_active: Optional[Piece] = None
        
        # Prochaine pièce (preview)
        self.piece_suivante: Optional[Piece] = None
        
        # États du jeu
        self.en_pause = False
        self.jeu_termine = False
        self.afficher_menu = False
        
        # Statistiques
        self.stats = StatistiquesJeu()
        
        # Système audio (port - injection de dépendance)
        self.audio = audio
        
        # Timer pour la chute automatique
        self.derniere_chute = time.time()
        self.intervalle_chute = 1.0  # 1 seconde au début
        
        # Messages à afficher
        self.messages = []
        
        print(f"🎮 Partie Tetris initialisée")
        print(f"📍 Plateau: {self.plateau.largeur}x{self.plateau.hauteur}")
        print(f"🎲 Types de pièces disponibles: {len(self.fabrique.obtenir_types_supportes())}")
        
        # Initialiser l'audio si disponible
        if self.audio:
            self.audio.initialiser()
            print("🎵 Système audio initialisé")
        
        # Générer les premières pièces
        self._generer_piece_suivante()
        self._faire_descendre_piece_suivante()
    
    def obtenir_piece_active(self) -> Optional[Piece]:
        """Retourne la pièce actuellement contrôlée."""
        return self.piece_active
    
    def obtenir_plateau(self) -> Plateau:
        """Retourne le plateau de jeu."""
        return self.plateau
    
    def obtenir_statistiques(self) -> StatistiquesJeu:
        """Retourne les statistiques de la partie."""
        return self.stats
    
    def deplacer_piece_active(self, delta_x: int, delta_y: int) -> bool:
        """Déplace la pièce active si possible."""
        if not self.piece_active or self.en_pause or self.jeu_termine:
            return False
        
        # Sauvegarder l'état
        positions_orig = self.piece_active.positions.copy()
        pivot_orig = Position(self.piece_active.position_pivot.x, self.piece_active.position_pivot.y)
        
        # Essayer le déplacement
        self.piece_active.deplacer(delta_x, delta_y)
        
        # Vérifier si c'est valide
        if self.plateau.peut_placer_piece(self.piece_active):
            print(f"📍 Déplacement réussi: {self.piece_active.type_piece.value} → {self.piece_active.positions}")
            return True
        else:
            # Annuler le déplacement
            self.piece_active.positions = positions_orig
            self.piece_active.position_pivot = pivot_orig
            return False
    
    def faire_descendre_piece(self) -> bool:
        """Fait descendre la pièce active d'une ligne si possible."""
        return self.deplacer_piece_active(0, 1)
    
    def tourner_piece_active(self) -> bool:
        """Fait tourner la pièce active si possible."""
        if not self.piece_active or self.en_pause or self.jeu_termine:
            return False
        
        # Sauvegarder l'état
        positions_orig = self.piece_active.positions.copy()
        orientation_orig = getattr(self.piece_active, '_orientation', None)
        
        # Essayer la rotation
        self.piece_active.tourner()
        
        # Vérifier si c'est valide
        if self.plateau.peut_placer_piece(self.piece_active):
            print(f"🔄 Rotation réussie: {self.piece_active.type_piece.value} → {self.piece_active.positions}")
            return True
        else:
            # Annuler la rotation
            self.piece_active.positions = positions_orig
            if orientation_orig is not None:
                self.piece_active._orientation = orientation_orig
            return False
    
    def chute_rapide(self) -> bool:
        """Chute rapide : descend la pièce jusqu'au contact."""
        if not self.piece_active or self.en_pause or self.jeu_termine:
            return False
        
        nb_lignes = 0
        
        while True:
            positions_orig = self.piece_active.positions.copy()
            pivot_orig = Position(self.piece_active.position_pivot.x, self.piece_active.position_pivot.y)
            
            # Essayer de descendre
            self.piece_active.deplacer(0, 1)
            
            if self.plateau.peut_placer_piece(self.piece_active):
                nb_lignes += 1
            else:
                # Remettre à la position précédente et arrêter
                self.piece_active.positions = positions_orig
                self.piece_active.position_pivot = pivot_orig
                break
        
        if nb_lignes > 0:
            print(f"🚀 Chute rapide: {nb_lignes} lignes → {self.piece_active.positions}")
            # Ajouter des points pour la chute rapide
            self.stats.score += nb_lignes * self.stats.niveau
        
        return nb_lignes > 0
    
    def placer_piece_et_generer_nouvelle(self) -> bool:
        """Place la pièce active définitivement et génère une nouvelle pièce."""
        if not self.piece_active or self.en_pause or self.jeu_termine:
            return False
        
        # Placer la pièce sur le plateau
        self.plateau.placer_piece(self.piece_active)
        print(f"📍 Pièce {self.piece_active.type_piece.value} placée: {self.piece_active.positions}")
        
        # Ajouter aux statistiques
        self.stats.ajouter_piece(self.piece_active.type_piece)
        
        # Vérifier les lignes complètes
        lignes_completes = self.plateau.obtenir_lignes_completes()
        if lignes_completes:
            nb_lignes = self.plateau.supprimer_lignes(lignes_completes)
            self.stats.ajouter_score_selon_lignes_completees(nb_lignes)
            
            if nb_lignes == 4:
                self.messages.append("🎉 TETRIS ! (+800 pts)")
            else:
                self.messages.append(f"✨ {nb_lignes} ligne(s) ! (+{100 * nb_lignes * self.stats.niveau} pts)")
            
            print(f"🎉 {nb_lignes} ligne(s) complétée(s) ! Score: {self.stats.score}")
            
            # Accélérer le jeu selon le niveau
            self.intervalle_chute = max(0.1, 1.0 - (self.stats.niveau - 1) * 0.1)
        
        # Faire descendre la pièce suivante
        self._faire_descendre_piece_suivante()
        
        return True
    
    def mettre_a_jour_chute_automatique(self) -> None:
        """Met à jour la chute automatique des pièces."""
        if self.en_pause or self.jeu_termine or not self.piece_active:
            return
        
        temps_actuel = time.time()
        
        if temps_actuel - self.derniere_chute >= self.intervalle_chute:
            # Essayer de faire descendre la pièce
            if not self.deplacer_piece_active(0, 1):
                # La pièce ne peut plus descendre, la placer
                self.placer_piece_et_generer_nouvelle()
            
            self.derniere_chute = temps_actuel
    
    def _generer_piece_suivante(self) -> None:
        """Génère la prochaine pièce aléatoire."""
        self.piece_suivante = self.fabrique.creer_aleatoire(x_pivot=5, y_pivot=1)
        print(f"🎲 Prochaine pièce générée: {self.piece_suivante.type_piece.value}")
    
    def _faire_descendre_piece_suivante(self) -> None:
        """Fait descendre la pièce suivante comme pièce active."""
        if self.piece_suivante:
            self.piece_active = self.piece_suivante
            
            # Vérifier si la nouvelle pièce peut être placée (game over)
            if not self.plateau.peut_placer_piece(self.piece_active):
                self.jeu_termine = True
                self.messages.append("💀 GAME OVER !")
                print("💀 GAME OVER ! La pièce ne peut pas être placée.")
                return
            
            print(f"⬇️ Nouvelle pièce active: {self.piece_active.type_piece.value} → {self.piece_active.positions}")
        
        # Générer la suivante
        self._generer_piece_suivante()
    
    def basculer_pause(self) -> None:
        """Bascule l'état de pause."""
        self.en_pause = not self.en_pause
        
        # Gérer la musique en fonction de la pause
        if self.audio:
            if self.en_pause:
                self.audio.mettre_en_pause_musique()
            else:
                self.audio.reprendre_musique()
        
        print(f"⏸️ Pause: {'ON' if self.en_pause else 'OFF'}")
    
    def demarrer_musique(self) -> bool:
        """Démarre la musique de fond du jeu."""
        if self.audio:
            try:
                self.audio.jouer_musique("tetris-theme.wav", volume=0.7, boucle=True)
                return True
            except Exception as e:
                print(f"❌ Erreur démarrage musique: {e}")
                return False
        return False
    
    def arreter_musique(self) -> None:
        """Arrête la musique de fond."""
        if self.audio:
            self.audio.arreter_musique()
    
    def definir_volume_musique(self, volume: float) -> None:
        """Définit le volume de la musique (0.0 à 1.0)."""
        if self.audio:
            self.audio.definir_volume_musique(volume)
    
    def musique_en_cours(self) -> bool:
        """Vérifie si la musique est en cours de lecture."""
        if self.audio:
            return self.audio.est_musique_en_cours()
        return False
    
    def basculer_menu(self) -> None:
        """Bascule l'affichage du menu."""
        self.afficher_menu = not self.afficher_menu
        print(f"📋 Menu: {'OUVERT' if self.afficher_menu else 'FERMÉ'}")
    
    def obtenir_messages(self) -> list:
        """Retourne et vide la liste des messages."""
        messages = self.messages.copy()
        self.messages.clear()
        return messages
    
    def fermer(self) -> None:
        """Ferme proprement le moteur et nettoie les ressources."""
        if self.audio:
            self.audio.nettoyer()
            print("🧹 Ressources audio nettoyées")
