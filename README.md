# Tetris

Un jeu de Tetris classique développé en Python avec une architecture moderne et des bonnes pratiques de développement.

## 🎮 Fonctionnalités

- Gameplay classique de Tetris avec **les 7 tétrominos complets** (I, O, T, S, Z, J, L)
- Rotation et déplacement des pièces avec validation de collision
- Factory Pattern avec auto-enregistrement des pièces (Registry Pattern)
- Architecture hexagonale avec séparation claire des responsabilités
- Tests complets avec approche TDD (Test-Driven Development) - **88/88 tests ✅**

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
python tests/run_suite_tests.py

# Tests spécifiques par catégorie  
python tests/run_all_unit_tests.py       # Tests unitaires
python tests/run_all_acceptance_tests.py # Tests d'acceptance
python tests/run_all_integration_tests.py # Tests d'intégration

# Tests unitaires spécifiques
python -m unittest tests.unit.domaine.test_entites.test_pieces.test_piece_t -v
```

**Couverture actuelle** : **88 tests, 100% de réussite ✅**
- **75 tests unitaires** : Domaine, entités, services
- **9 tests d'acceptance** : Scénarios utilisateur
- **4 tests d'intégration** : Système complet

## 📋 État du développement

### ✅ Terminé
- Architecture de base avec TDD
- **Toutes les 7 pièces complètes** : I, O, T, S, Z, J, L avec rotations complètes
- Factory Pattern avec auto-enregistrement (Registry Pattern)
- Tests complets du domaine (**88 tests, 100% réussite**)
- Value Objects et Entities avec comportements métier
- Symétrie parfaite entre pièces J et L
- **Suite de tests complètement corrigée et fonctionnelle**
- **Plateau de jeu complet** avec détection de lignes complètes
- **Interface utilisateur Pygame complète** avec affichage 60 FPS
- **Système de score et niveaux fonctionnel**
- **Command Pattern** pour les contrôles
- **Architecture hexagonale** respectée
- **Moteur de partie complet** avec statistiques

### 🎮 **Projet TERMINÉ et FONCTIONNEL**
Le jeu Tetris est maintenant **complet et jouable** avec toutes les fonctionnalités :
- ✅ **Interface graphique** : Affichage Pygame avec couleurs
- ✅ **Contrôles** : 7 commandes (flèches, espace, esc, p)
- ✅ **Gameplay** : Chute des pièces, rotations, lignes complètes
- ✅ **Scoring** : Système de points et progression de niveaux
- ✅ **Statistics** : Compteurs de pièces et performances

---

> **Licence** : Projet éducatif  
> **Status** : 🎉 **PROJET TETRIS COMPLET** - Jeu fonctionnel avec architecture hexagonale et TDD
