# Tetris

Un jeu de Tetris classique développé en Python avec une architecture moderne et des bonnes pratiques de développement.

## 🎮 Fonctionnalités

- Gameplay classique de Tetris avec **les 7 tétrominos complets** (I, O, T, S, Z, J, L)
- Rotation et déplacement des pièces avec validation de collision
- Factory Pattern avec auto-enregistrement des pièces (Registry Pattern)
- Architecture hexagonale avec séparation claire des responsabilités
- Tests complets avec approche TDD (Test-Driven Development) - 56/56 tests ✅

## 🚀 Installation et utilisation

```bash
# Cloner le repository
git clone <repository-url>
cd tetris

# Installer les dépendances
pip install pygame

# Lancer le jeu avec architecture hexagonale
python jouer.py

# Ou directement
python partie_tetris.py

# Exécuter les tests
python tests/run_tests.py
```

## 🎯 Comment jouer

- **Flèches directionnelles** : Déplacer les pièces (gauche/droite/bas)
- **Flèche du haut** ou **Espace** : Faire tourner les pièces  
- **Objectif** : Compléter des lignes horizontales pour les faire disparaître
- **Fin de partie** : Quand les pièces atteignent le haut de l'écran

## 🎲 Types de pièces

Le jeu a maintenant **toutes les 7 tétrominos classiques** complètement implémentées :

```
I-piece (ligne)     O-piece (carré)     T-piece (T)
    █                   ██                ███
    █                   ██                 █
    █
    █

S-piece (S)         Z-piece (Z)         J-piece (J)     L-piece (L)
     ██               ██                   █               █
    ██                 ██                  █               █
                                          ██               ██
```

✅ **Toutes les pièces sont maintenant implémentées avec leurs 4 orientations** (ou 2 pour S/Z, 1 pour O)

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

**Couverture actuelle** : 56 tests, 100% de réussite ✅

## 📋 État du développement

### ✅ Terminé
- Architecture de base avec TDD
- **Toutes les 7 pièces complètes** : I, O, T, S, Z, J, L avec rotations complètes
- Factory Pattern avec auto-enregistrement (Registry Pattern)
- Tests complets du domaine (56 tests, 100% réussite)
- Value Objects et Entities avec comportements métier
- Symétrie parfaite entre pièces J et L

### 🔄 En cours  
- Plateau de jeu avec détection de lignes complètes

### ⏳ À venir
- Interface utilisateur Pygame
- Système de score et niveaux
- Sauvegarde des scores
- Game Loop principal

---

> **Licence** : Projet éducatif  
> **Status** : ✅ **7/7 pièces Tetris complètes** avec TDD et architecture hexagonale
