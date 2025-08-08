# Tetris

Un jeu de Tetris classique développé en Python avec l'aide de Github Copilot (Claude 4.0)

## 📋 Table des matières

1. [🎬 Démonstration du gameplay](#-démonstration-du-gameplay)
   - [🕹️ Contrôles de jeu](#️-contrôles-de-jeu)
   - [🎮 Règles du jeu](#-règles-du-jeu)
   - [🎯 Système de score](#-système-de-score)
2. [🎮 Fonctionnalités](#-fonctionnalités)
3. [🚀 Installation et utilisation](#-installation-et-utilisation)
4. [🎯 Comment jouer](#-comment-jouer)
   - [Contrôles](#contrôles)
   - [Gameplay](#gameplay)
   - [Scoring](#scoring)
5. [🎵 Audio](#-audio)
6. [🎲 Types de pièces](#-types-de-pièces)
7. [🏗️ Architecture technique](#️-architecture-technique)
8. [🧪 Tests](#-tests)
9. [📋 État du développement](#-état-du-développement)

---

## 🎬 Démonstration du gameplay

[![Démonstration Tetris](https://img.youtube.com/vi/4wGwvLoQEzo/0.jpg)](https://youtu.be/4wGwvLoQEzo)

*Cliquez sur l'image ci-dessus pour voir une démonstration vidéo du jeu en action !*

### 🕹️ Contrôles de jeu
- Flèche Gauche (←) : Déplacer la pièce vers la gauche
- Flèche Droite (→) : Déplacer la pièce vers la droite
- Flèche Haut (↑) : Faire tourner la pièce (rotation horaire)
- Flèche Bas (↓) : Chute rapide (descente accélérée ligne par ligne)
- Barre d'Espace : Chute instantanée (dépose immédiatement la pièce)
- P : Pause/Reprendre la partie (met aussi la musique en pause)
- M : Mute/Unmute la musique ET les effets sonores
- R : Redémarrer une nouvelle partie (disponible seulement après game over)
- X (fenêtre) : Fermer le jeu proprement

### 🎮 Règles du jeu
- Démarrage : Le jeu démarre automatiquement en pause pour permettre au joueur de se préparer
- Objectif : Compléter des lignes horizontales pour les faire disparaître et marquer des points
- Plateau de jeu : Grille de 10 colonnes × 20 lignes (dimensions standard Tetris)
- Pièces (Tétrominos) : 7 formes différentes (I, O, T, S, Z, J, L) qui descendent automatiquement
- Rotation : Toutes les pièces peuvent tourner (sauf le carré O) dans le sens horaire
- Placement : Une pièce se fixe quand elle ne peut plus descendre
- Lignes complètes : Éliminées automatiquement avec descente des lignes au-dessus
- Accélération : La vitesse de chute augmente progressivement avec le niveau
- Fin de partie : Quand une nouvelle pièce ne peut pas être placée (sommet atteint)
- Score : Points attribués selon les lignes éliminées et le niveau actuel
- Restart : Appuyez sur R après un game over pour commencer une nouvelle partie instantanément
- Fermer le jeu : Cliquez simplement sur le X de la fenêtre pour quitter proprement

### 🎯 Système de score
- 1 ligne : 100 × niveau points
- 2 lignes simultanées : 300 × niveau points  
- 3 lignes simultanées : 500 × niveau points
- 4 lignes simultanées (TETRIS) : 800 × niveau points + son spécial
- Niveau : Augmente toutes les 10 lignes éliminées

## 🎮 Fonctionnalités

- Gameplay classique de Tetris avec les 7 tétrominos complets (I, O, T, S, Z, J, L)
- Rotation et déplacement des pièces avec validation de collision
- Zone invisible masquée : Seules les parties visibles des pièces (y ≥ 0) sont affichées pour une expérience utilisateur propre
- Système audio complet avec musique de fond et effets sonores
  - Musique de fond intégrée avec le thème classique de Tetris
  - Son de rotation : Effet sonore rotate.wav à chaque rotation réussie ✅
  - Son de gain de niveau : Effet sonore gained-a-new-level.wav à chaque passage de niveau ✅
  - Son de game over : Effet sonore game-over.wav à chaque fin de partie ✅
  - Contrôle mute/unmute : Touche M pour basculer le son (musique ET effets)
- Factory Pattern avec auto-enregistrement des pièces (Registry Pattern)
- Architecture hexagonale avec séparation claire des responsabilités
- Tests complets avec approche TDD (Test-Driven Development)
- Rotation horaire : Pièce T avec rotation dans le sens horaire (Nord → Ouest → Sud → Est → Nord) ✅ CORRIGÉ !

### Tests implémentés (272 tests - 100% ✅)
```
tests/
├── unit/                           # Tests unitaires (145 tests ✅)
│   ├── domaine/                    # Tests du domaine métier
│   │   ├── entites/               # Tests des entités (Position + 7 pièces + Factory + Statistiques)
│   │   └── services/              # Tests des services (GestionnaireEvenements + Commandes + ExceptionCollision + Restart)
│   └── adapters/                  # Tests des adaptateurs (Audio avec mute/unmute + ExceptionAudio ✅)
├── integration/                   # Tests d'intégration (26 tests ✅) 
│   ├── test_audio_integration.py  # Tests intégration audio (6 tests)
│   ├── test_correction_audio.py   # Tests correction audio (5 tests)
│   ├── test_exception_audio_integration.py # Tests intégration ExceptionAudio (4 tests) ✅
│   ├── test_restart_integration.py # Tests intégration restart (3 tests) ✅
│   ├── test_son_gain_niveau_integration.py # Tests intégration son gain niveau (2 tests)
│   ├── test_son_game_over_integration.py # Tests intégration son game over (2 tests) ✅
│   └── [4 tests d'intégration directe] # Tests génération aléatoire, moteur, plateau, statistiques ✅
├── acceptance/                    # Tests d'acceptance (101 tests ✅)
│   ├── test_controles_rapide.py  # Tests contrôles complets
│   ├── test_controles_simplifies.py # Tests contrôles simplifiés
│   ├── test_fonctionnalite_mute.py # Tests fonctionnalité mute/unmute ✅
│   ├── test_fonctionnalite_restart.py # Tests fonctionnalité restart ✅
│   ├── test_correction_bug_crash_placement.py # Tests correction bug crash placement ✅
│   ├── test_correction_bug_crash_reprise_partie.py # Tests correction bug crash reprise ✅
│   ├── test_correction_bug_lignes_multiples.py # Tests bug lignes multiples ✅
│   ├── test_correction_bug_gameover_premature.py # Tests bug game over prématuré ✅
│   ├── test_bug_visuel_ligne_complete.py # Tests bug visuel ligne complète ✅
│   ├── test_son_gain_niveau.py   # Tests son gain de niveau ✅
│   ├── test_son_game_over.py     # Tests son game over ✅
│   ├── test_son_tetris.py        # Tests son TETRIS pour 4 lignes ✅
│   ├── test_audio_rotation.py    # Tests audio rotation avec ExceptionAudio ✅
│   ├── test_indicateur_mute.py   # Tests indicateur visuel mute ✅
│   ├── test_mute_game_over.py    # Tests correction mute game over ✅
│   └── test_masquage_zone_invisible.py # Tests masquage zone invisible ✅
└── [4 scripts officiels]          # Scripts de lancement avec découverte dynamique ✅
```

Performance : 272 tests en temps rapide (100% succès - Suite complète validée ✅)

### 🔧 Découverte dynamique des tests ✅
Les scripts de test utilisent maintenant `unittest.TestLoader.discover()` pour découvrir automatiquement tous les tests, éliminant le besoin de maintenir des listes manuelles de modules.

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

### Contrôles
- Flèche Gauche (←) : Déplacer la pièce vers la gauche
- Flèche Droite (→) : Déplacer la pièce vers la droite  
- Flèche Haut (↑) : Faire tourner la pièce (rotation horaire)
- Flèche Bas (↓) : Chute rapide (descente accélérée ligne par ligne)
- Barre d'Espace : Chute instantanée (dépose immédiatement la pièce)
- P : Pause/Reprendre la partie
- M : Mute/Unmute la musique ET les effets sonores
- R : Redémarrer une nouvelle partie (seulement après game over)
- X (fenêtre) : Fermer le jeu proprement

### Gameplay
- Démarrage : Le jeu démarre automatiquement en pause - appuyez sur P pour commencer à jouer
- Objectif : Compléter des lignes horizontales pour les faire disparaître et marquer des points
- Plateau : Grille de 10×20 avec zone invisible au-dessus pour l'apparition des pièces
- Fin de partie : Quand une nouvelle pièce ne peut pas être placée
- Progression : Le niveau augmente toutes les 10 lignes éliminées avec accélération automatique

### Scoring
- 1 ligne : 100 × niveau
- 2 lignes : 300 × niveau  
- 3 lignes : 500 × niveau
- 4 lignes (TETRIS) : 800 × niveau + son spécial

## 🎵 Audio

Le jeu inclut maintenant un système audio complet et interactif :
- Musique de fond : Thème classique de Tetris (`tetris-theme.wav` - format compatible)
- Effets sonores : Son de rotation (`rotate.wav`) joué à chaque rotation réussie
- Son de gain de niveau : Son (`gained-a-new-level.wav`) joué à chaque passage de niveau
- Son de game over : Son (`game-over.wav`) joué à chaque fin de partie
- Son TETRIS spécial : Son (`tetris.wav`) joué exclusivement lors de l'élimination de 4 lignes simultanées
- Contrôle mute/unmute unifié : Touche M pour basculer le son de TOUT l'audio
- Feedback utilisateur : Messages visuels lors du basculement mute/unmute
- Système de fallback : Tentative automatique WAV si OGG échoue
- Contrôle automatique : La musique se met en pause avec le jeu (touche P)
- Volume optimisé : Musique 70%, effets sonores 100% pour une expérience équilibrée
- Architecture hexagonale : Audio intégré via des ports et adaptateurs
- Gestion d'erreurs robuste : Le jeu fonctionne même sans audio avec ExceptionAudio
- Respect du mute : Les effets sonores sont automatiquement mutés quand le mode mute est activé
- Gestion centralisée des erreurs : ExceptionAudio capturée dans jouer.py avec messages informatifs

## 🎲 Types de pièces

Le jeu a maintenant toutes les 7 tétrominos classiques complètement implémentées :

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

✅ Toutes les pièces sont maintenant implémentées avec leurs rotations complètes :
- Rotation horaire : Toutes les pièces suivent l'ordre horaire (sauf O qui ne tourne pas)
- Pièce T spécialement corrigée : Nord → Ouest → Sud → Est → Nord ✅
- Pivot cohérent : Chaque pièce a un pivot fixe et correct pour ses rotations

## 🏗️ Architecture technique

Le projet suit une architecture hexagonale avec séparation claire des responsabilités :

- Domaine : Logique métier pure (pièces, plateau, règles)
- Ports : Interfaces pour les services externes (affichage, audio, contrôles)
- Adapters : Implémentations concrètes (UI, audio, stockage, etc.)
- Assets : Médias du jeu (sons, images, musiques)

```
tetris/
├── src/              # Code source - Architecture hexagonale
│   ├── domaine/      # Logique métier pure
│   ├── ports/        # Interfaces (contrats)
│   └── adapters/     # Implémentations techniques
├── assets/           # Médias du jeu
│   ├── audio/        # Sons et musiques
│   └── images/       # Images et textures
├── docs/             # Documentation complète
│   ├── DIRECTIVES_DEVELOPPEMENT.md  # Règles de développement
│   ├── DOC_TECHNIQUE.md              # Documentation technique
│   ├── journal-developpement.md     # Journal du projet
│   └── testing-strategy.md          # Stratégie TDD
├── tests/            # Tests organisés par type
│   ├── unit/         # Tests unitaires (145 tests)
│   ├── acceptance/   # Tests d'acceptance (101 tests)
│   └── integration/  # Tests d'intégration (26 tests)
├── tmp/              # Scripts temporaires et outils de développement
├── jouer.py          # Point d'entrée principal
└── partie_tetris.py  # Orchestrateur du jeu
```

## 🧪 Tests

Le projet utilise une approche TDD (Test-Driven Development) avec respect strict des directives :

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

Organisation conforme aux directives :
- Structure stricte : `tests/unit/`, `tests/acceptance/`, `tests/integration/`
- 4 scripts officiels : Exactement ceux spécifiés dans les directives
- Outils de développement : Déplacés dans `tmp/` (comme `metriques_tests.py`)
- AUCUN test à la racine : Règle absolue respectée

Couverture actuelle : 272 tests, 100% de réussite
- 145 tests unitaires : Domaine, entités, services, statistiques, zone invisible, mute/unmute, restart, ExceptionAudio
- 101 tests d'acceptance : Scénarios utilisateur + corrections de bugs + fonctionnalité mute + son gain niveau + son game over + son TETRIS + fonctionnalité restart + audio rotation avec ExceptionAudio
- 26 tests d'intégration : Intégration audio, restart, génération aléatoire, moteur, plateau, statistiques, ExceptionAudio

## 📋 État du développement

### ✅ Terminé
- Architecture de base avec TDD
- Toutes les 7 pièces complètes : I, O, T, S, Z, J, L avec rotations horaires complètes 
- Rotation horaire corrigée : Pièce T maintenant conforme à l'ordre horaire (Nord → Ouest → Sud → Est)
- Factory Pattern avec auto-enregistrement (Registry Pattern)
- Tests complets du domaine et validation TDD complète 
- Value Objects et Entities avec comportements métier
- Symétrie parfaite entre pièces J et L
- Suite de tests complètement validée et fonctionnelle
- Plateau de jeu complet avec détection de lignes complètes
- Interface utilisateur Pygame complète avec affichage 60 FPS
- Zone invisible masquée : Affichage propre avec masquage des positions y < 0
- Système de score et niveaux fonctionnel
- Command Pattern pour les contrôles avec exceptions métier
- Gestion des exceptions : ExceptionCollision utilisée par toutes les commandes de mouvement (gauche, droite, rotation, chute rapide)
- Architecture hexagonale respectée avec gestionnaire centralisé des collisions
- Moteur de partie complet avec statistiques
- Système audio intégré avec musique de fond fonctionnelle
- Gestion d'erreurs audio : Fallback automatique et fonctionnement sans son
- Zone invisible : Système de spawn réaliste avec Y_SPAWN_DEFAUT = -3
- Suite de tests complète : 272/272 tests passent (100% réussite) 
