# Tetris

Un jeu de Tetris classique développé en Python avec une architecture moderne et des bonnes pratiques de développement.

## 🎮 Fonctionnalités jeu de Tetris classique développé en Python avec une architecture moderne et des bonnes pratiques de développement.

> 🎓 **Pour l'apprentissage** : Voir [learning/README.md](learning/README.md) pour les leçons d'architecture et patterns.ris

Un jeu de Tetris classique développé en Python avec une architecture moderne et des bonnes pratiques de développement.

> � **Pour l'apprentissage** : Voir [LEARNING.md](LEARNING.md) pour les leçons d'architecture et patterns.

## 🎮 Fonctionnalités

- Gameplay classique de Tetris avec 7 types de pièces (tétrominos)
- Rotation et déplacement des pièces avec validation de collision
- Suppression automatique des lignes complètes
- Système de score et progression par niveaux
- Interface utilisateur intuitive avec Pygame

## 🚀 Installation et utilisation

```bash
# Cloner le repository
git clone <repository-url>
cd tetris

# Installer les dépendances
pip install pygame

# Lancer le jeu (quand implémenté)
python main.py

# Exécuter les tests
python test_runner.py
```

## 🎯 Comment jouer

- **Flèches directionnelles** : Déplacer les pièces (gauche/droite/bas)
- **Flèche du haut** ou **Espace** : Faire tourner les pièces  
- **Objectif** : Compléter des lignes horizontales pour les faire disparaître
- **Fin de partie** : Quand les pièces atteignent le haut de l'écran

## 🎲 Types de pièces

Le jeu utilise les 7 tétrominos classiques :

```
I-piece (ligne)     O-piece (carré)     T-piece (T)
    ████                ██                 █
                        ██                ███

S-piece (S)         Z-piece (Z)         J-piece (J)         L-piece (L)  
     ██               ██                   █                   █
    ██                 ██                 ███                 ███
```

## 🏗️ Architecture technique

Le projet suit une **architecture hexagonale** avec séparation claire des responsabilités :

- **Domaine** : Logique métier pure (pièces, plateau, règles)
- **Ports** : Interfaces pour les services externes
- **Adapters** : Implémentations concrètes (UI, stockage, etc.)

```
src/
├── domaine/          # Logique métier
├── ports/            # Interfaces
└── adapters/         # Implémentations
```

## 🧪 Tests

Le projet utilise une approche **TDD** (Test-Driven Development) :

```bash
# Tous les tests
python test_runner.py

# Tests spécifiques
python -m unittest tests.test_domaine.test_entites.test_pieces.test_piece_t -v
```

**Couverture actuelle** : 33 tests, 100% de réussite ✅

## 📋 État du développement

### ✅ Terminé
- Architecture de base avec TDD
- Pièces I, O, T, S avec rotations
- Factory Pattern avec auto-enregistrement (Registry Pattern)
- Tests complets du domaine

### 🔄 En cours  
- Implémentation des pièces Z, J, L
- Plateau de jeu avec détection de lignes

### ⏳ À venir
- Interface utilisateur Pygame
- Système de score et niveaux
- Sauvegarde des scores

---

> **Licence** : Projet éducatif - INF2020
5. Commencez à jouer !
