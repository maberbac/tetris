# 🎨 Assets du Jeu Tetris

Documentation des médias et ressources du jeu Tetris.

## 📁 Structure des Assets

```
assets/
├── audio/                 # 🎵 Sons et musiques
│   ├── music/             # Musiques de fond
│   │   └── theme.ogg      # Musique principale du jeu
│   └── sfx/               # Effets sonores
│       ├── line_clear.wav # Son de ligne complétée
│       └── rotate.wav     # Son de rotation de pièce
├── images/                # 🖼️ Images et textures
│   └── backgrounds/       # Arrière-plans du jeu
└── README.md              # Cette documentation
```

## 🎵 Audio

### Musique (`music/`)
- **`theme.ogg`** : Musique principale du jeu (format OGG recommandé pour pygame)

### Effets sonores (`sfx/`)
- **`line_clear.wav`** : Son joué quand une ou plusieurs lignes sont complétées
- **`rotate.wav`** : Son joué lors de la rotation d'une pièce

## 🖼️ Images

### Arrière-plans (`backgrounds/`)
- Arrière-plans optionnels pour le jeu
- Formats recommandés : PNG, JPG

## 🔧 Standards Techniques

### Formats Audio
- **Musique** : Format OGG (meilleure compression, bonne qualité)
- **Effets sonores** : Format WAV (faible latence, idéal pour les SFX courts)

### Formats Images
- **PNG** : Pour les images avec transparence
- **JPG** : Pour les arrière-plans sans transparence

### Conventions de Nommage
- **Nom descriptif** : `line_clear.wav`, `rotate.wav`
- **Snake_case** : Underscore pour séparer les mots
- **Français** : Noms en français si possible (`rotation.wav`)

## 🎮 Intégration avec le Code

Les assets sont chargés via pygame dans les adapters d'affichage :

```python
# Exemple d'intégration
import pygame
import os

# Chemin vers les assets
ASSETS_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets')
AUDIO_PATH = os.path.join(ASSETS_PATH, 'audio')
IMAGES_PATH = os.path.join(ASSETS_PATH, 'images')

# Chargement des sons
son_ligne = pygame.mixer.Sound(os.path.join(AUDIO_PATH, 'sfx', 'line_clear.wav'))
son_rotation = pygame.mixer.Sound(os.path.join(AUDIO_PATH, 'sfx', 'rotate.wav'))

# Chargement de la musique
pygame.mixer.music.load(os.path.join(AUDIO_PATH, 'music', 'theme.ogg'))
```

## 📏 Spécifications Recommandées

### Audio
- **Musique** : 44.1 kHz, stéréo, OGG Vorbis
- **SFX** : 44.1 kHz, mono/stéréo, WAV 16-bit

### Images
- **Arrière-plans** : Résolution adaptée à la fenêtre du jeu
- **Formats** : PNG pour transparence, JPG pour arrière-plans simples

---

> **Note** : Cette structure est évolutive. De nouveaux types d'assets peuvent être ajoutés selon les besoins du développement.
