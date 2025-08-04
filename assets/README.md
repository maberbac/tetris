# 🎨 Assets du Jeu Tetris

Documentation des médias et ressources du jeu Tetris selon les directives de développement.

## 📁 Structure des Assets

```
assets/
├── audio/                          # 🎵 Sons et musiques
│   ├── music/                      # Musiques de fond
│   │   └── tetris-theme.wav        # Musique principale du jeu
│   └── sfx/                        # Effets sonores
│       ├── gained-a-new-level.wav  # Son de gain de niveau
│       ├── game-over.wav           # Son de fin de partie
│       ├── rotate.wav              # Son de rotation de pièce
│       └── tetris.wav              # Son spécial TETRIS (4 lignes)
├── images/                         # 🖼️ Images et textures
│   └── backgrounds/                # Arrière-plans du jeu
└── README.md                       # Cette documentation
```

## 🎵 Audio

### Musique (`music/`)
- **`tetris-theme.wav`** : Musique principale du jeu (thème classique de Tetris)
  - Format : WAV 16-bit, compatible pygame
  - Volume : 70% pour équilibrage avec les effets sonores
  - Utilisation : Boucle continue pendant le jeu, pause avec la partie

### Effets sonores (`sfx/`)
- **`rotate.wav`** : Son joué lors de la rotation réussie d'une pièce
- **`gained-a-new-level.wav`** : Son joué lors du passage au niveau suivant (toutes les 10 lignes)
- **`game-over.wav`** : Son joué à la fin de partie (game over)
- **`tetris.wav`** : Son spécial joué exclusivement lors de l'élimination de 4 lignes simultanées (TETRIS)

### Système Audio Complet ✅
- **Contrôle unifié** : Touche M pour mute/unmute TOUT l'audio (musique + effets)
- **Gestion d'erreurs** : Le jeu fonctionne même sans audio disponible
- **Architecture hexagonale** : Audio intégré via ports (`AudioJeu`) et adaptateurs (`AudioPartie`)
- **Fallback automatique** : Tentative WAV si OGG échoue

## 🖼️ Images

### Arrière-plans (`backgrounds/`)
- **Répertoire vide actuellement** : Arrière-plans optionnels pour le jeu
- **Formats recommandés** : PNG (avec transparence), JPG (sans transparence)
- **Utilisation future** : Peut contenir des fonds d'écran thématiques pour le jeu

## 🔧 Standards Techniques

### Formats Audio Utilisés
- **Musique** : Format WAV (tetris-theme.wav) - Compatible, faible latence
- **Effets sonores** : Format WAV exclusivement - Idéal pour les SFX courts et réactifs
- **Qualité** : 44.1 kHz, 16-bit pour tous les fichiers audio

### Formats Images Supportés
- **PNG** : Pour les images avec transparence (recommandé)
- **JPG** : Pour les arrière-plans sans transparence (plus léger)

### Conventions de Nommage (Directives de Développement)
- **Descriptif en anglais** : `rotate.wav`, `game-over.wav` (noms techniques universels)
- **Kebab-case** : Tirets pour séparer les mots (`tetris-theme.wav`)
- **Extensions explicites** : `.wav` pour audio, `.png`/`.jpg` pour images

## 🎮 Intégration avec le Code

Les assets sont chargés via pygame dans l'architecture hexagonale (adaptateurs d'audio) :

```python
# Exemple d'intégration conforme à l'architecture hexagonale
import pygame
import os

# Chemin vers les assets (depuis src/adapters/sortie/)
ASSETS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets')
AUDIO_PATH = os.path.join(ASSETS_PATH, 'audio')

class AudioPartie:  # Adaptateur de sortie
    def __init__(self):
        pygame.mixer.init()
        
        # Chargement des effets sonores
        self.son_rotation = pygame.mixer.Sound(
            os.path.join(AUDIO_PATH, 'sfx', 'rotate.wav')
        )
        self.son_niveau = pygame.mixer.Sound(
            os.path.join(AUDIO_PATH, 'sfx', 'gained-a-new-level.wav')
        )
        self.son_game_over = pygame.mixer.Sound(
            os.path.join(AUDIO_PATH, 'sfx', 'game-over.wav')
        )
        self.son_tetris = pygame.mixer.Sound(
            os.path.join(AUDIO_PATH, 'sfx', 'tetris.wav')
        )
        
        # Chargement de la musique de fond
        pygame.mixer.music.load(
            os.path.join(AUDIO_PATH, 'music', 'tetris-theme.wav')
        )
        pygame.mixer.music.set_volume(0.7)  # Volume musique 70%
        
    def jouer_son_rotation(self):
        """Joue le son de rotation selon l'interface AudioJeu."""
        if not self.mute:
            self.son_rotation.play()
```

## 📏 Spécifications Recommandées

### Audio (Standards Appliqués)
- **Musique** : 44.1 kHz, 16-bit, WAV (tetris-theme.wav ✅ FONCTIONNEL)
- **SFX** : 44.1 kHz, 16-bit, WAV mono/stéréo (tous les effets ✅ FONCTIONNELS)
- **Volume optimisé** : Musique 70%, effets 100% pour équilibrage parfait

### Images (Standards pour Extensions Futures)
- **Arrière-plans** : Résolution 800×600 pixels (taille fenêtre du jeu)
- **Formats** : PNG pour transparence, JPG pour arrière-plans simples

## 🚀 État des Assets

### ✅ Complètement Implémenté
- **Système audio complet** : 4 effets sonores + musique de fond
- **Intégration architecture hexagonale** : Via ports et adaptateurs
- **Contrôle utilisateur** : Mute/unmute unifié (touche M)
- **Gestion d'erreurs** : Fallback gracieux si audio indisponible
