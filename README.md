# Tetris

Un jeu de Tetris classique développé en Python avec une architecture moderne et des bonnes pratiques de développement.

## 🎮 Fonctionnalités

- Gameplay classique de Tetris avec **les 7 tétrominos complets** (I, O, T, S, Z, J, L)
- Rotation et déplacement des pièces avec validation de collision
- **Musique de fond intégrée** avec le thème classique de Tetris
- Factory Pattern avec auto-enregistrement des pièces (Registry Pattern)
- Architecture hexagonale avec séparation claire des responsabilités
- Tests complets avec approche TDD (Test-Driven Development) - ### **Tests implémentés (108+ tests - 97%+ ✅)**
```
tests/
├── unit/                           # Tests unitaires (75 tests ✅)
│   ├── domaine/                    # Tests du domaine métier
│   │   ├── entites/               # Tests des entités (Position + 7 pièces + Factory)
│   │   └── services/              # Tests des services (GestionnaireEvenements)
│   └── interface/                 # Tests de l'interface  
├── integration/                   # Tests d'intégration (11 tests ✅)
│   └── test_partie_complete.py   # Tests système complet
├── acceptance/                    # Tests d'acceptance (22 tests ✅)
│   ├── test_controles_rapide.py  # Tests contrôles complets
│   ├── test_controles_simplifies.py # Tests contrôles simplifiés
│   ├── test_correction_bug_lignes_multiples.py # Tests bug lignes multiples ✅
│   └── test_correction_bug_gameover_premature.py # Tests bug game over prématuré ✅
└── run_tests.py                  # Lanceur des tests
```

**Performance** : 108 tests en 0.6s environ (97%+ succès, corrections en cours)

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
python tests/run_suite_tests.py
```

## 🎯 Comment jouer

- **Flèches directionnelles** : Déplacer les pièces (gauche/droite/bas)
- **Flèche du haut** ou **Espace** : Faire tourner les pièces
- **Touche P** : Pause/reprendre (met aussi la musique en pause)
- **Objectif** : Compléter des lignes horizontales pour les faire disparaître
- **Fin de partie** : Quand les pièces atteignent le haut de l'écran

## 🎵 Audio

Le jeu inclut maintenant un **système audio complet** :
- **Musique de fond** : Thème classique de Tetris (`tetris-theme.wav` - format compatible)
- **Système de fallback** : Tentative automatique WAV si OGG échoue
- **Contrôle automatique** : La musique se met en pause avec le jeu (touche P)
- **Volume optimisé** : Réglé à 70% pour une expérience agréable
- **Architecture hexagonale** : Audio intégré via des ports et adaptateurs
- **Gestion d'erreurs robuste** : Le jeu fonctionne même sans audio

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
- **Ports** : Interfaces pour les services externes (affichage, audio, contrôles)
- **Adapters** : Implémentations concrètes (UI, audio, stockage, etc.)
- **Assets** : Médias du jeu (sons, images, musiques)

```
tetris/
├── src/              # Code source - Architecture hexagonale
│   ├── domaine/      # Logique métier pure
│   ├── ports/        # Interfaces (contrats)
│   └── adapters/     # Implémentations techniques
├── assets/           # Médias du jeu
│   ├── audio/        # Sons et musiques
│   └── images/       # Images et textures
├── tests/            # Tests organisés par type
├── docs/             # Documentation complète
├── tmp/              # Scripts temporaires et outils de développement
├── jouer.py          # Point d'entrée principal
└── partie_tetris.py  # Orchestrateur du jeu
```

## 🧪 Tests

Le projet utilise une approche **TDD** (Test-Driven Development) :

```bash
# Tous les tests
python tests/run_suite_tests.py

# Tests spécifiques par catégorie  
python tests/run_all_unit_tests.py       # Tests unitaires
python tests/run_all_acceptance_tests.py # Tests d'acceptance
python tests/run_all_integration_tests.py # Tests d'intégration

# Tests unitaires spécifiques
python -m unittest tests.unit.domaine.test_entites.test_pieces.test_piece_t -v
```

**Couverture actuelle** : **108 tests, 97%+ de réussite ✅**
- **75 tests unitaires** : Domaine, entités, services, zone invisible
- **22 tests d'acceptance** : Scénarios utilisateur + corrections de bugs (lignes multiples, game over prématuré)
- **11 tests d'intégration** : Système complet avec audio

## 📋 État du développement

### ✅ Terminé
- Architecture de base avec TDD
- **Toutes les 7 pièces complètes** : I, O, T, S, Z, J, L avec rotations complètes
- Factory Pattern avec auto-enregistrement (Registry Pattern)
- Tests complets du domaine (**70 tests unitaires, 100% réussite**)
- Value Objects et Entities avec comportements métier
- Symétrie parfaite entre pièces J et L
- **Suite de tests complètement corrigée et fonctionnelle**
- **Plateau de jeu complet** avec détection de lignes complètes
- **Interface utilisateur Pygame complète** avec affichage 60 FPS
- **Système de score et niveaux fonctionnel**
- **Command Pattern** pour les contrôles
- **Architecture hexagonale** respectée
- **Moteur de partie complet** avec statistiques
- **Système audio intégré** avec musique de fond fonctionnelle
- **Gestion d'erreurs audio** : Fallback automatique et fonctionnement sans son
- **Organisation des fichiers** : Structure propre avec `tmp/` pour les outils de développement
- **Debug TDD systématique** : Corrections de bugs avec méthodologie stricte (descente accélérée + lignes multiples + game over prématuré)
- **Zone invisible** : Système de spawn réaliste avec Y_SPAWN_DEFAUT = -3
- **Corrections récentes** : Pivot de la pièce S entièrement corrigé, démonstrations mises à jour

### 🎮 **Projet TERMINÉ et FONCTIONNEL**
Le jeu Tetris est maintenant **complet et jouable** avec toutes les fonctionnalités :
- ✅ **Interface graphique** : Affichage Pygame avec couleurs
- ✅ **Contrôles** : 7 commandes (flèches, espace, esc, p)
- ✅ **Gameplay** : Chute des pièces, rotations, lignes complètes
- ✅ **Scoring** : Système de points et progression de niveaux
- ✅ **Statistics** : Compteurs de pièces et performances
- ✅ **Audio** : Musique de fond avec contrôles intégrés et gestion d'erreurs
- ✅ **Organisation** : Structure de projet professionnelle avec séparation claire

---

> **Licence** : Projet éducatif  
> **Status** : 🎉 **PROJET TETRIS COMPLET** - Jeu fonctionnel avec architecture hexagonale et TDD
