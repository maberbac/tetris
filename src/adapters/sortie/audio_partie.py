"""
Adaptateur Audio - Implémentation pygame pour la musique et les effets sonores.

Cet adaptateur implémente l'interface AudioJeu en utilisant pygame.mixer
pour la gestion de la musique de fond et des effets sonores.
"""

import pygame
from pathlib import Path
from typing import Optional
from src.ports.sortie.audio_jeu import AudioJeu


class AudioPartie(AudioJeu):
    """
    Adaptateur pygame pour la gestion audio du jeu Tetris.
    
    Utilise pygame.mixer pour:
    - Lecture de musique de fond en boucle
    - Gestion du volume
    - Contrôle de la lecture (pause/reprendre/arrêt)
    - Effets sonores (future extension)
    """
    
    def __init__(self) -> None:
        """Initialise l'adaptateur audio."""
        self._initialise = False
        self._musique_chargee = False
        self._volume_musique = 0.7  # Volume par défaut à 70%
        self._mute = False  # État de mute
        self._volume_avant_mute = 0.7  # Volume à restaurer après unmute
        
    def initialiser(self) -> None:
        """
        Initialise le système audio pygame.
        
        Configure pygame.mixer avec des paramètres optimaux pour Tetris.
        """
        try:
            # Initialiser pygame.mixer si pas déjà fait
            if not pygame.get_init():
                pygame.init()
            
            if not pygame.mixer.get_init():
                # Configuration audio optimisée pour les jeux
                pygame.mixer.pre_init(
                    frequency=44100,    # Qualité CD
                    size=-16,          # 16-bit signé
                    channels=2,        # Stéréo
                    buffer=512         # Buffer petit pour faible latence
                )
                pygame.mixer.init()
            
            self._initialise = True
            print("[AUDIO] Système audio initialisé avec succès")
            
        except pygame.error as e:
            print(f"[ERROR] Erreur lors de l'initialisation audio: {e}")
            self._initialise = False
    
    def jouer_musique(self, chemin_fichier: str, volume: float = 0.7, boucle: bool = True) -> None:
        """
        Joue la musique de fond depuis un fichier.
        
        Args:
            chemin_fichier: Nom du fichier audio (ex: "tetris-theme.ogg")
            volume: Volume de la musique (0.0 à 1.0)
            boucle: Si True, la musique se répète en boucle
        """
        if not self._initialise:
            self.initialiser()
        
        if not self._initialise:
            return
            
        try:
            # Construire le chemin absolu vers assets/audio/music/
            # audio_partie.py est dans src/adapters/sortie/, donc 4 remontées pour la racine du projet
            chemin_complet = Path(__file__).parent.parent.parent.parent / "assets" / "audio" / "music" / chemin_fichier
            
            if not chemin_complet.exists():
                print(f"[ERROR] Fichier audio introuvable: {chemin_complet}")
                return
            
            # Charger et jouer la musique
            pygame.mixer.music.load(str(chemin_complet))
            
            # Définir le volume
            pygame.mixer.music.set_volume(volume)
            
            # -1 = boucle infinie, 0 = une seule fois
            loops = -1 if boucle else 0
            pygame.mixer.music.play(loops)
            
            self._musique_chargee = True
            print(f"[MUSIC] Musique lancée: {chemin_complet.name}")
            
        except pygame.error as e:
            print(f"[ERROR] Erreur lecture musique: {e}")
            print(f"💡 Conseil: Le fichier {chemin_fichier} pourrait être corrompu")
            print("   Essayez avec un fichier WAV ou un autre fichier OGG")
            
            # Tentative avec un fichier WAV de fallback si c'est un OGG qui pose problème
            if chemin_fichier.endswith('.ogg'):
                fallback_file = chemin_fichier.replace('.ogg', '.wav')
                fallback_path = Path(__file__).parent.parent.parent.parent / "assets" / "audio" / "music" / fallback_file
                
                if fallback_path.exists():
                    print(f"🔄 Tentative avec fichier de fallback: {fallback_file}")
                    try:
                        pygame.mixer.music.load(str(fallback_path))
                        pygame.mixer.music.set_volume(volume)
                        loops = -1 if boucle else 0
                        pygame.mixer.music.play(loops)
                        self._musique_chargee = True
                        print(f"[CHECK_MARK] Fallback réussi: {fallback_path.name}")
                    except pygame.error as e2:
                        print(f"[ERROR] Fallback échoué aussi: {e2}")
        except Exception as e:
            print(f"[ERROR] Erreur inattendue lors de la lecture de la musique: {e}")
    
    def arreter_musique(self) -> None:
        """Arrête complètement la musique de fond."""
        if self._initialise and self._musique_chargee:
            pygame.mixer.music.stop()
            print("[MUTE] Musique arrêtée")
    
    def mettre_en_pause_musique(self) -> None:
        """Met la musique en pause (peut être reprise)."""
        if self._initialise and self._musique_chargee:
            pygame.mixer.music.pause()
            print("[PAUSE] Musique mise en pause")
    
    def reprendre_musique(self) -> None:
        """Reprend la musique après une pause."""
        if self._initialise and self._musique_chargee:
            pygame.mixer.music.unpause()
            print("[PLAY] Musique reprise")
    
    def basculer_mute_musique(self) -> bool:
        """
        Bascule entre mute et unmute de la musique.
        
        Returns:
            bool: True si la musique est maintenant mutée, False sinon
        """
        if not self._initialise:
            return False
            
        if self._mute:
            # Unmute : restaurer le volume précédent
            self._mute = False
            self._volume_musique = self._volume_avant_mute
            pygame.mixer.music.set_volume(self._volume_musique)
            print(f"[UNMUTE] Musique réactivée - Volume: {int(self._volume_musique * 100)}%")
        else:
            # Mute : sauvegarder le volume actuel et mettre à 0
            self._volume_avant_mute = self._volume_musique
            self._mute = True
            pygame.mixer.music.set_volume(0.0)
            print("[MUTE] Musique désactivée")
            
        return self._mute
    
    def definir_volume_musique(self, volume: float) -> None:
        """
        Définit le volume de la musique.
        
        Args:
            volume: Volume entre 0.0 (muet) et 1.0 (maximum)
        """
        # Clamp le volume entre 0.0 et 1.0
        self._volume_musique = max(0.0, min(1.0, volume))
        
        if self._initialise:
            pygame.mixer.music.set_volume(self._volume_musique)
            print(f"[VOLUME] Volume musique: {int(self._volume_musique * 100)}%")
    
    def jouer_effet_sonore(self, chemin_fichier: str) -> bool:
        """
        Joue un effet sonore ponctuel.
        
        Args:
            chemin_fichier: Chemin vers le fichier audio de l'effet
            
        Returns:
            True si l'effet a été joué avec succès, False sinon
        """
        if not self._initialise:
            self.initialiser()
        
        if not self._initialise:
            return False
            
        try:
            # Construire le chemin absolu
            # audio_partie.py est dans src/adapters/sortie/, donc 3 remontées pour la racine
            chemin_complet = Path(__file__).parent.parent.parent / chemin_fichier
            
            if not chemin_complet.exists():
                print(f"[ERROR] Fichier effet sonore introuvable: {chemin_complet}")
                return False
            
            # Charger et jouer l'effet sonore
            effet = pygame.mixer.Sound(str(chemin_complet))
            effet.play()
            
            print(f"[VOLUME] Effet sonore joué: {chemin_complet.name}")
            return True
            
        except pygame.error as e:
            print(f"[ERROR] Erreur lors de la lecture de l'effet sonore: {e}")
            return False
    
    def est_musique_en_cours(self) -> bool:
        """
        Vérifie si la musique est actuellement en cours de lecture.
        
        Returns:
            True si la musique joue, False sinon
        """
        if not self._initialise or not self._musique_chargee:
            return False
        
        return pygame.mixer.music.get_busy()
    
    def nettoyer(self) -> None:
        """Nettoie les ressources audio et ferme le système."""
        if self._initialise:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            self._initialise = False
            self._musique_chargee = False
            print("[CLEANUP] Système audio nettoyé")
