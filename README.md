# Tetris

Un jeu de Tetris classique développé en Python avec une architecture moderne et des bonnes pratiques de développement.

## 🎮 Fonctionnalités

- Gameplay classique de Tetris avec **les 7 tétrominos complets** (I, O, T, S, Z, J, L)
- Rotation et déplacement des pièces avec validation de collision
- **Zone invisible masquée** : Seules les parties visibles des pièces (y ≥ 0) sont affichées pour une expérience utilisateur propre
- **Système audio complet** avec musique de fond et effets sonores
  - **Musique de fond intégrée** avec le thème classique de Tetris
  - **Son de rotation** : Effet sonore rotate.wav à chaque rotation réussie ✅ **NOUVEAU !**
  - **Contrôle mute/unmute** : Touche M pour basculer le son (musique ET effets)
- Factory Pattern avec auto-enregistrement des pièces (Registry Pattern)
- Architecture hexagonale avec séparation claire des responsabilités
- Tests complets avec approche TDD (Test-Driven Development)
- **Rotation horaire** : Pièce T avec rotation dans le sens horaire (Nord → Ouest → Sud → Est → Nord) ✅ **CORRIGÉ !**

### **Tests implémentés (131 tests - 100% ✅)**
```
tests/
├── unit/                           # Tests unitaires (92 tests ✅)
│   ├── domaine/                    # Tests du domaine métier
│   │   ├── entites/               # Tests des entités (Position + 7 pièces + Factory + Statistiques)
│   │   └── services/              # Tests des services (GestionnaireEvenements + Commandes)
│   └── adapters/                  # Tests des adaptateurs (Audio avec mute/unmute ✅)
├── integration/                   # Tests d'intégration (4 tests ✅)
│   └── test_partie_complete.py   # Tests système complet
├── acceptance/                    # Tests d'acceptance (35 tests ✅)
│   ├── test_controles_rapide.py  # Tests contrôles complets
│   ├── test_controles_simplifies.py # Tests contrôles simplifiés
│   ├── test_fonctionnalite_mute.py # Tests fonctionnalité mute/unmute ✅
│   ├── test_correction_bug_lignes_multiples.py # Tests bug lignes multiples ✅
│   ├── test_correction_bug_gameover_premature.py # Tests bug game over prématuré ✅
│   └── test_bug_visuel_ligne_complete.py # Tests bug visuel ligne complète ✅
└── [4 scripts officiels]          # Scripts de lancement obligatoires
```

**Performance** : 131 tests en 0.640s (100% succès - Suite complète validée ✅)

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
- **Flèche du haut** ou **Espace** : Faire tourner les pièces (rotation horaire) �
- **Touche P** : Pause/reprendre (met aussi la musique en pause)
- **Touche M** : Mute/unmute la musique ET les effets sonores ✅
- **Objectif** : Compléter des lignes horizontales pour les faire disparaître
- **Fin de partie** : Quand les pièces atteignent le haut de l'écran

**Rotation horaire** : La pièce T suit maintenant l'ordre de rotation horaire : Nord → Ouest → Sud → Est → Nord ✅

## 🎵 Audio

Le jeu inclut maintenant un **système audio complet et interactif** :
- **Musique de fond** : Thème classique de Tetris (`tetris-theme.wav` - format compatible)
- **Effets sonores** : Son de rotation (`rotate.wav`) joué à chaque rotation réussie ✅
- **Contrôle mute/unmute unifié** : Touche M pour basculer le son de TOUT l'audio ✅
- **Feedback utilisateur** : Messages visuels lors du basculement mute/unmute
- **Système de fallback** : Tentative automatique WAV si OGG échoue
- **Contrôle automatique** : La musique se met en pause avec le jeu (touche P)
- **Volume optimisé** : Musique 70%, effets sonores 100% pour une expérience équilibrée
- **Architecture hexagonale** : Audio intégré via des ports et adaptateurs
- **Gestion d'erreurs robuste** : Le jeu fonctionne même sans audio
- **Respect du mute** : Les effets sonores sont automatiquement mutés quand le mode mute est activé

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

✅ **Toutes les pièces sont maintenant implémentées avec leurs rotations complètes** :
- **Rotation horaire** : Toutes les pièces suivent l'ordre horaire (sauf O qui ne tourne pas)
- **Pièce T spécialement corrigée** : Nord → Ouest → Sud → Est → Nord ✅
- **Pivot cohérent** : Chaque pièce a un pivot fixe et correct pour ses rotations

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

Le projet utilise une approche **TDD** (Test-Driven Development) avec respect strict des directives :

```bash
# SCRIPTS OFFICIELS OBLIGATOIRES (selon directives)

# Tests unitaires (composants isolés)
python tests/run_all_unit_tests.py

# Tests d'acceptance (scénarios utilisateur) 
python tests/run_all_acceptance_tests.py

# Tests d'intégration (composants ensemble)
python tests/run_all_integration_tests.py

# Suite complète (tous les tests)
python tests/run_suite_tests.py
```

**Organisation conforme aux directives** :
- **Structure stricte** : `tests/unit/`, `tests/acceptance/`, `tests/integration/`
- **4 scripts officiels** : Exactement ceux spécifiés dans les directives
- **Outils de développement** : Déplacés dans `tmp/` (comme `metriques_tests.py`)
- **AUCUN test à la racine** : Règle absolue respectée

**Couverture actuelle** : **131 tests, 100% de réussite ✅**
- **92 tests unitaires** : Domaine, entités, services, statistiques, zone invisible, mute/unmute
- **35 tests d'acceptance** : Scénarios utilisateur + corrections de bugs + fonctionnalité mute
- **4 tests d'intégration** : Système complet avec audio

## 📋 État du développement

### ✅ Terminé
- Architecture de base avec TDD
- **Toutes les 7 pièces complètes** : I, O, T, S, Z, J, L avec rotations horaires complètes ✅
- **Rotation horaire corrigée** : Pièce T maintenant conforme à l'ordre horaire (Nord → Ouest → Sud → Est)
- Factory Pattern avec auto-enregistrement (Registry Pattern)
- Tests complets du domaine et validation TDD complète ✅
- Value Objects et Entities avec comportements métier
- Symétrie parfaite entre pièces J et L
- **Suite de tests complètement validée et fonctionnelle**
- **Plateau de jeu complet** avec détection de lignes complètes
- **Interface utilisateur Pygame complète** avec affichage 60 FPS
- **Zone invisible masquée** : Affichage propre avec masquage des positions y < 0
- **Système de score et niveaux fonctionnel**
- **Command Pattern** pour les contrôles
- **Architecture hexagonale** respectée
- **Moteur de partie complet** avec statistiques
- **Système audio intégré** avec musique de fond fonctionnelle
- **Gestion d'erreurs audio** : Fallback automatique et fonctionnement sans son
- **Organisation des fichiers** : Structure propre avec `tmp/` pour les outils de développement
- **Debug TDD systématique** : Corrections de bugs avec méthodologie stricte
- **Zone invisible** : Système de spawn réaliste avec Y_SPAWN_DEFAUT = -3
- **Corrections TDD** : Corrections des pièces T avec pivot et rotation horaire parfaits
- **Suite de tests complète** : 131/131 tests passent (100% réussite) ✅

### 🎮 **Projet TERMINÉ et FONCTIONNEL**
Le jeu Tetris est maintenant **complet et jouable** avec toutes les fonctionnalités :
- ✅ **Interface graphique** : Affichage Pygame avec couleurs et masquage zone invisible
- ✅ **Contrôles** : 8 commandes (flèches, espace, esc, p, m) avec rotation horaire ✅
- ✅ **Gameplay** : Chute des pièces, rotations horaires, lignes complètes
- ✅ **Scoring** : Système de points et progression de niveaux
- ✅ **Statistics** : Compteurs de pièces et performances
- ✅ **Audio** : Musique de fond avec contrôles intégrés et gestion d'erreurs
- ✅ **Tests TDD** : 131 tests validés (100% succès) avec corrections complètes
- ✅ **Organisation** : Structure de projet professionnelle avec séparation claire

---

> **Licence** : Projet éducatif  
> **Status** : 🎉 **PROJET TETRIS COMPLET** - Jeu fonctionnel avec architecture hexagonale et TDD
