# Documentation technique - Tetris Python

Documentation technique pour comprendre l'architecture hexagonale et l'implémentation du jeu Tetris.

## 📋 Table des matières

1. [🏗️ Architecture du projet](#architecture-du-projet)
2. [🎯 Composants principaux](#composants-principaux)
   - [Value Objects - Position](#1-value-objects---position)
   - [Entities - Pièces](#2-entities---pièces)
   - [Factory Pattern avec Registry](#3-factory-pattern-avec-registry)
   - [Services - Couche logique métier](#4-services---couche-logique-métier)
3. [🚨 Gestion des Exceptions](#gestion-des-exceptions)
   - [Exceptions du Domaine](#1-exceptions-du-domaine---logique-métier)
   - [Exceptions des Adapters](#2-exceptions-des-adapters---couche-technique)
   - [Exceptions d'Infrastructure](#3-exceptions-dinfrastructure---couche-système)
   - [Stratégie de Gestion d'Erreurs](#4-stratégie-de-gestion-derreurs)
4. [🧪 Tests et Validation](#tests-et-validation)

---

## 🏗️ Architecture du projet

### Structure actuelle - Architecture Hexagonale
```
tetris/
├── src/                        # Code source - Architecture hexagonale
│   ├── domaine/                # 🎯 DOMAINE - Logique métier pure (centre de l'hexagone)
│   │   ├── entites/            # Entités du domaine
│   │   │   ├── position.py     # Value Object pour les coordonnées
│   │   │   ├── piece.py        # Classe abstraite des pièces
│   │   │   ├── plateau.py      # ✅ Grille de jeu 10×20
│   │   │   ├── pieces/         # Implémentations des pièces
│   │   │   │   ├── piece_i.py  # Pièce ligne
│   │   │   │   ├── piece_o.py  # Pièce carrée  
│   │   │   │   ├── piece_t.py  # Pièce en T
│   │   │   │   ├── piece_s.py  # Pièce en S
│   │   │   │   ├── piece_z.py  # Pièce en Z
│   │   │   │   ├── piece_j.py  # Pièce en J
│   │   │   │   └── piece_l.py  # Pièce en L ✅
│   │   │   └── fabriques/      # Factory Pattern
│   │   │       ├── registre_pieces.py    # Registry avec auto-enregistrement
│   │   │       └── fabrique_pieces.py    # Factory pour créer les pièces
│   │   └── services/           # ✅ Services métier
│   │       ├── commandes/      # Command Pattern pour actions
│   │       ├── moteur_partie.py         # Moteur principal du jeu
│   │       └── statistiques/   # Gestion des statistiques
│   ├── ports/                  # 🔌 PORTS - Interfaces (contrats)
│   │   ├── sortie/             # Ports de sortie
│   │   │   ├── affichage_jeu.py    # Interface pour l'affichage
│   │   │   └── audio_jeu.py        # Interface pour l'audio ✅ NOUVEAU !
│   │   └── controleur_jeu.py   # Interface pour les contrôles
│   └── adapters/               # 🔧 ADAPTERS - Implémentations techniques
│       ├── entree/             # Adapters d'entrée
│       │   └── gestionnaire_partie.py  # Gestion Pygame des entrées
│       └── sortie/             # Adapters de sortie
│           ├── affichage_partie.py     # Rendu Pygame avec masquage zone invisible ✅
│           └── audio_partie.py         # Audio Pygame ✅ NOUVEAU !
├── assets/                     # 🎨 MÉDIAS - Assets du jeu
│   ├── audio/                  # Sons et musiques
│   │   ├── music/              # Musique principale (tetris-theme.wav ✅ FONCTIONNEL !)
│   │   └── sfx/                # Effets sonores (line_clear.wav, rotate.wav, tetris.wav ✅ NOUVEAU !)
│   └── images/                 # Images et textures
│       └── backgrounds/        # Arrière-plans optionnels
├── tests/                      # Tests organisés par type (CONFORMES AUX DIRECTIVES)
│   ├── unit/                   # Tests unitaires (91 tests ✅)
│   │   ├── domaine/            # Tests du domaine métier
│   │   │   ├── entites/        # Tests des entités (Position, Pièces, Factory, Statistiques)
│   │   │   └── services/       # Tests des services (GestionnaireEvenements, Commandes + Restart ✅)
│   │   └── adapters/           # Tests des adaptateurs (Audio avec mute/unmute ✅)
│   ├── acceptance/             # Tests d'acceptance (82 tests ✅)
│   │   ├── test_controles_*.py # Tests des contrôles utilisateur
│   │   ├── test_fonctionnalite_mute.py # Tests mute/unmute ✅
│   │   ├── test_fonctionnalite_restart.py # Tests restart ✅ **NOUVEAU !**
│   │   ├── test_correction_bug_lignes_multiples.py # Tests bug lignes multiples ✅
│   │   ├── test_correction_bug_gameover_premature.py # Tests bug game over prématuré ✅
│   │   ├── test_bug_visuel_ligne_complete.py # Tests bug visuel ligne complète ✅
│   │   ├── test_son_gain_niveau.py # Tests son gain de niveau ✅
│   │   ├── test_son_game_over.py # Tests son game over ✅
│   │   ├── test_son_tetris.py    # Tests son TETRIS pour 4 lignes ✅
│   │   └── test_correction_bug_*.py # Tests corrections de bugs ✅
│   ├── integration/            # Tests d'intégration (22 tests ✅) ✅ **NOUVEAU RECORD !**
│   │   ├── test_audio_integration.py # Tests intégration audio (6 tests)
│   │   ├── test_correction_audio.py # Tests correction audio (5 tests)
│   │   ├── test_restart_integration.py # Tests intégration restart (3 tests) ✅ **NOUVEAU !**
│   │   ├── test_son_gain_niveau_integration.py # Tests intégration son gain niveau (2 tests)
│   │   ├── test_son_game_over_integration.py # Tests intégration son game over (2 tests) ✅
│   │   └── [4 tests d'intégration directe] # Tests génération, moteur, plateau, statistiques ✅
│   └── [4 scripts officiels]  # Scripts de lancement obligatoires
├── docs/                       # Documentation complète
├── tmp/                        # 🔧 OUTILS DE DÉVELOPPEMENT - Scripts temporaires (metriques_tests.py)
├── demo/                       # Démonstrations et exemples
├── partie_tetris.py            # 🎭 ORCHESTRATEUR - Composition root (assemble tout)
└── jouer.py                    # 🚀 Point d'entrée utilisateur
```

## 🎯 Composants principaux

### 1. Value Objects - Position
```python
@dataclass(frozen=True)
class Position:
    x: int
    y: int
    
    def deplacer(self, delta_x: int, delta_y: int) -> 'Position':
        return Position(self.x + delta_x, self.y + delta_y)
```
- **Immutable** : Ne peut pas être modifiée après création
- **Equality par valeur** : Deux positions avec mêmes coordonnées sont égales
- Système de coordonnées : (0,0) en haut à gauche

### 2. Entities - Pièces
```python
@piece_tetris(TypePiece.I)  # Auto-enregistrement
class PieceI(Piece):
    def tourner(self) -> None:
        # Logique de rotation spécifique à I
```

#### Pièces implémentées
- **PieceI** : Ligne droite (2 orientations)
- **PieceO** : Carré (rotation = no-op) 
- **PieceT** : Forme en T (4 orientations) ✅ **Rotation horaire corrigée !**
- **PieceS** : Forme en S (2 orientations)
- **PieceZ** : Forme en Z (2 orientations)
- **PieceJ** : Forme en J (4 orientations)
- **PieceL** : Forme en L (4 orientations)

#### Détail des formes et rotations
```
PieceI (ligne) - 2 orientations :
Horizontal: ████        Vertical: █
                                  █
                                  █
                                  █

PieceO (carré) - 1 orientation :
██
██

PieceT (T) - 4 orientations ✅ **ROTATION HORAIRE** :
Nord:  █     Ouest: █     Sud: ███    Est: █
      ███           ██          █         ██
                    █                     █

**Ordre de rotation horaire** : Nord → Ouest → Sud → Est → Nord ✅

PieceS (S) - 2 orientations :
Horizontal:  ██    Vertical: █
            ██               ██
                              █

PieceZ (Z) - 2 orientations :
Horizontal: ██     Vertical:  █
             ██              ██
                             █

PieceJ (J) - 4 orientations :
Nord: █      Est: ██     Sud: ███    Ouest: █
      ███         █           █             █
                  █                        ██

PieceL (L) - 4 orientations :
Nord:    █     Est:  █     Sud: ███    Ouest:  ██
       ███           █          █               █
                     ██                         █
```

#### Comportement des pièces
- **Mutables** : Peuvent changer d'état (déplacement, rotation)
- **Position pivot** : Point fixe pour les rotations (corrigé pour pièce T : (5,0))
- **4 blocs** par pièce
- **Rotation horaire** : Toutes les pièces suivent l'ordre horaire ✅
- **Héritage** : Comportement commun dans classe abstraite `Piece`

### 3. Factory Pattern avec Registry
```python
# Création via fabrique
fabrique = FabriquePieces()
piece = fabrique.creer(TypePiece.J, x_spawn=5, y_spawn=0)

# Auto-enregistrement avec décorateur
@piece_tetris(TypePiece.J)
class PieceJ(Piece):
    # Implémentation...
```

#### Avantages
- **Extensibilité** : Nouvelles pièces sans modification du code existant
- **Auto-découverte** : Registry trouve automatiquement les pièces
- **Découplage** : Factory ne connaît pas les classes concrètes

### 4. Services - Couche logique métier

#### Command Pattern - Actions de jeu
```python
# Commandes complètes (8 actions essentielles) ✅ COMPLET !
CommandeDeplacerGauche()    # ← Déplacement horizontal gauche
CommandeDeplacerDroite()    # → Déplacement horizontal droite
CommandeTourner()           # ↑ Rotation horaire
CommandeDescendre()         # ↓ Chute rapide (par ligne)
CommandeChuteRapide()       # Space - Chute instantanée (jusqu'en bas)
CommandePause()             # P - Pause/Reprendre
CommandeBasculerMute()      # M - Mute/Unmute audio ✅
CommandeRedemarrer()        # R - Restart après game over ✅ **NOUVEAU !**
```

**Contrôles optimisés** :
- **Flèches directionnelles** : Contrôles principaux intuitifs
- **Touches spéciales** : Actions de jeu (Space, P, M, R) ✅
- **Répétition intelligente** : Déplacement fluide (200ms initial, 120ms répétition)
- **Actions ponctuelles** : M et R ne se répètent pas automatiquement ✅
- **Mapping complet** : 8 touches essentielles (ajout mute/unmute + restart) ✅

#### Gestionnaire d'événements - Input handling
```python
# Configuration des touches
gestionnaire = GestionnaireEvenements()

# Traitement d'un événement
resultat = gestionnaire.traiter_evenement_clavier(
    "Left", TypeEvenement.CLAVIER_APPUI, moteur
)

# Mapping personnalisé
gestionnaire.ajouter_mapping_touche("w", ToucheClavier.ROTATION)
```

**Fonctionnalités** :
- **Contrôles complets** : 8 touches essentielles (ajout mute/unmute + restart) ✅
- **Mapping intuitif** : Flèches + Space + P + M + R ✅
- **Répétition optimisée** : Délais ajustés pour le gameplay (200ms/120ms)
- **Actions spécialisées** : Chute rapide vs chute instantanée
- **Contrôle audio** : M pour basculer mute/unmute (sans répétition)
- **Redémarrage rapide** : R pour restart après game over (sans répétition) ✅ **NOUVEAU !**

#### Adaptateur Pygame - Bridge vers UI
```python
# Intégration avec Pygame
adaptateur = AdaptateurPygame(gestionnaire)
adaptateur.demarrer()

# Dans la boucle de jeu
stats = adaptateur.traiter_evenements(moteur)
# → Conversion automatique événements Pygame → commandes
```

## 🚨 Gestion des Exceptions {#gestion-des-exceptions}

Le projet utilise une approche structurée pour la gestion des erreurs, respectant l'architecture hexagonale avec des exceptions spécifiques à chaque couche.

### 1. **Exceptions du Domaine** - Logique métier

#### **ExceptionCollision** - Gestion spécifique des collisions
```python
# Plateau - Collision lors du placement
if not self.peut_placer_piece(piece):
    raise ExceptionCollision("Impossible de placer la pièce à cette position")

# Usage recommandé pour toute situation de collision inattendue
try:
    plateau.placer_piece(piece)
except ExceptionCollision as e:
    print(f"Collision non autorisée : {e}")
```

**Utilisation** :
- **Collisions de placement** : Pièce ne peut pas être placée (collision, hors limites)
- **Situations inattendues** : Collisions qui ne devraient pas arriver en conditions normales
- **Débogage** : Identifier précisément les problèmes de collision

#### **ValueError** - Validation des données métier
```python
# Plateau - Dimensions invalides
if self.largeur <= 0 or self.hauteur <= 0:
    raise ValueError(f"Dimensions invalides: {self.largeur}x{self.hauteur}")

# Factory - Type de pièce non supporté
if type_piece not in cls._pieces_enregistrees:
    raise ValueError(
        f"Type de pièce non supporté : {type_piece.value}. "
        f"Types disponibles : {types_disponibles}"
    )

# Factory - Aucune pièce enregistrée
if not types_disponibles:
    raise ValueError("Aucune pièce enregistrée dans le registre")
```

**Utilisation** :
- **Validation des dimensions** : Plateau avec largeur/hauteur <= 0
- **Validation des types** : Type de pièce non supporté par le registre
- **Validation du registre** : Aucune pièce disponible pour génération aléatoire

### 2. **Exceptions des Adapters** - Couche technique

#### **pygame.error** - Erreurs spécifiques Pygame
```python
# AudioPartie - Initialisation audio
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
except pygame.error as e:
    print(f"[ERROR] Erreur lors de l'initialisation audio: {e}")
    self._initialise = False

# AudioPartie - Chargement de fichiers audio
try:
    self._mixer.music.load(chemin_complet)
except pygame.error as e:
    print(f"[ERROR] Impossible de charger la musique: {e}")

# AudioPartie - Lecture d'effets sonores
try:
    effet = pygame.mixer.Sound(chemin_complet)
    effet.play()
except pygame.error as e:
    print(f"[ERROR] Impossible de jouer l'effet sonore: {e}")
```

**Utilisation** :
- **Initialisation audio** : Problèmes avec le système audio du système
- **Chargement de fichiers** : Fichiers audio corrompus ou formats non supportés
- **Lecture audio** : Problèmes de lecture en temps réel

### 3. **Exceptions d'Infrastructure** - Couche système

#### **ImportError** - Dépendances manquantes
```python
# Vérification Pygame
try:
    import pygame
except ImportError:
    pygame = None

# AdaptateurPygame - Validation des dépendances
if not pygame:
    raise ImportError("Pygame n'est pas installé. Utilisez: pip install pygame")

# Lanceur principal - Gestion des imports
except ImportError as e:
    print(f"❌ Erreur d'importation: {e}")
    print("Assurez-vous que pygame est installé : pip install pygame")
```

**Utilisation** :
- **Dépendances manquantes** : Pygame non installé
- **Modules introuvables** : Problèmes de structure du projet
- **Imports optionnels** : Fonctionnalités dégradées sans dépendance

#### **Exception** - Gestionnaire générique
```python
# MoteurPartie - Gestion robuste des erreurs
try:
    self.audio.jouer_effet_sonore("assets/audio/sfx/rotate.wav")
except Exception as e:
    print(f"[DEBUG] Erreur audio non critique: {e}")

# CommandeBasculerMute - Gestion des erreurs de commande
try:
    resultat_mute = moteur.basculer_mute()
except Exception as e:
    print(f"[ERROR] Erreur lors du basculement mute: {e}")
    return False

# Lanceur principal - Catch-all pour stabilité
except Exception as e:
    print(f"❌ Erreur durant la partie: {e}")
    traceback.print_exc()
```

**Utilisation** :
- **Erreurs audio non critiques** : Le jeu continue sans audio
- **Erreurs de commandes** : Retour gracieux avec feedback utilisateur
- **Erreurs système imprévues** : Affichage debug + stack trace complet

### 4. **Stratégie de Gestion d'Erreurs**

#### **Principe de Résilience**
```python
# ✅ CORRECT - Gestion gracieuse avec fallback
try:
    self.audio.jouer_musique("tetris-theme.ogg")
except pygame.error:
    # Tentative de fallback WAV
    try:
        self.audio.jouer_musique("tetris-theme.wav")
    except pygame.error as e2:
        print(f"[ERROR] Impossible de jouer la musique: {e2}")
        # Le jeu continue sans musique

# ✅ CORRECT - Validation préventive
if self.largeur <= 0 or self.hauteur <= 0:
    raise ValueError(f"Dimensions invalides: {self.largeur}x{self.hauteur}")

# ✅ CORRECT - Logging informatif
except Exception as e:
    print(f"[DEBUG] Erreur audio non critique: {e}")
    # Continue l'exécution
```

#### **Anti-Patterns à Éviter**
```python
# ❌ INCORRECT - Masquer les erreurs
try:
    operation_critique()
except:
    pass  # Erreur silencieuse = problème

# ❌ INCORRECT - Catch trop large sans action
try:
    operation_specifique()
except Exception:
    return False  # Perte d'information sur l'erreur

# ❌ INCORRECT - Laisser crasher sans gestion
def operation_sans_validation(data):
    return data.some_property  # Peut lever AttributeError
```

### 5. **Messages d'Erreur Utilisateur**

#### **Messages Français et Informatifs**
```python
# ✅ Messages clairs pour l'utilisateur
"Impossible de placer la pièce à cette position"
"Dimensions invalides: 10x-5"  
"Type de pièce non supporté : X. Types disponibles : ['I', 'O', 'T']"
"Pygame n'est pas installé. Utilisez: pip install pygame"

# ✅ Messages de debug pour les développeurs  
"[ERROR] Erreur lors de l'initialisation audio: [Errno 2] No such file"
"[DEBUG] Erreur audio non critique: mixer not initialized"
"❌ Erreur durant la partie: 'NoneType' object has no attribute 'play'"
```

### 6. **Architecture d'Exception par Couche**

```
🏗️ Architecture des Exceptions
├── Domaine/               # ValueError pour logique métier
│   ├── ValidationError    # Données invalides (dimensions, types)
│   └── BusinessRuleError  # Règles métier violées (placement impossible)
├── Adapters/              # Exceptions techniques spécifiques
│   ├── pygame.error       # Problèmes audio/vidéo Pygame
│   └── OSError           # Problèmes système (fichiers, permissions)
└── Infrastructure/        # Exceptions système
    ├── ImportError        # Dépendances manquantes
    └── Exception          # Catch-all pour stabilité
```

Cette approche garantit :
- **🛡️ Robustesse** : Le jeu ne crash pas pour des erreurs non critiques
- **🔍 Debugabilité** : Messages clairs pour identifier les problèmes
- **👤 UX** : Feedback utilisateur approprié selon le contexte
- **🏗️ Architecture** : Exceptions appropriées à chaque couche hexagonale

**Architecture** :
- **Bridge Pattern** : Sépare abstraction (gestionnaire) de l'implémentation (Pygame)
- **Mapping automatique** : Touches Pygame → Noms génériques
- **Extensibilité** : Facile d'ajouter d'autres bibliothèques (tkinter, etc.)

### 5. Patterns d'implémentation appris

#### Registry Pattern avec décorateurs
- **Auto-enregistrement** : `@piece_tetris(TypePiece.X)` enregistre automatiquement les classes
- **Découverte dynamique** : Pas besoin de modifier le registre pour chaque nouvelle pièce
- **Type safety** : Vérification des types à l'exécution

#### Rotation systématique
- **Pivot fixe** : Chaque pièce a un point de rotation constant
- **Cycle d'orientations** : Nord → Ouest → Sud → Est → Nord ✅ **ROTATION HORAIRE**
- **Calculs géométriques** : Transformations matricielles pour les rotations
- **Correction pièce T** : Pivot corrigé (5,0) et rotation horaire implémentée ✅

#### TDD avec patterns métier
- **RED-GREEN-REFACTOR** : Cycle systématique pour chaque nouvelle pièce
- **Tests par comportement** : Création, mouvement, rotation, type
- **Différenciation** : Tests pour distinguer les pièces similaires (S/Z, J/L)

#### Command Pattern pour les contrôles
- **Encapsulation d'actions** : Chaque input devient une commande exécutable
- **Découplage UI/logique** : Interface indépendante de l'implémentation
- **Extensibilité** : Nouvelles commandes sans modification du moteur
- **Testabilité** : Chaque commande testable individuellement

#### Bridge Pattern pour l'input
- **Abstraction/Implémentation** : Gestionnaire générique + Adaptateur Pygame
- **Mapping configurable** : Touches physiques → Touches logiques → Commandes
- **Multi-plateforme** : Facilite l'ajout d'autres bibliothèques graphiques

### 5. Tests et qualité
```bash
# Exécuter tous les tests
python tests/run_suite_tests.py

# Tests par catégorie
python tests/run_all_unit_tests.py       # Tests unitaires (89 tests) ✅ +5 tests restart
python tests/run_all_acceptance_tests.py # Tests d'acceptance (75 tests)
python tests/run_all_integration_tests.py # Tests d'intégration (22 tests) ✅ +3 tests restart
```

**Métriques actuelles** : **224 tests, 100% de réussite ✅**
- **Architecture hexagonale** : Complètement implémentée
- **Couverture TDD** : Toutes les fonctionnalités testées
- **Performance** : Exécution complète en ~1.4s
- **Fonctionnalité récente** : Restart avec touche R ajouté ✅

#### CommandeRedemarrer - Nouvelle fonctionnalité restart ✅

**Responsabilité** : Permettre de redémarrer une nouvelle partie avec la touche R.

```python
class CommandeRedemarrer(Commande):
    def execute(self, moteur: MoteurJeu) -> bool:
        if not moteur.est_game_over():
            return False  # Ignore si pas en game over
        
        moteur.redemarrer_partie()  # Réinitialise tout
        return True
```

**Caractéristiques** :
- **Activation conditionnelle** : Fonctionne uniquement après game over
- **Réinitialisation complète** : Score=0, niveau=1, plateau vide, nouvelle pièce
- **État de pause** : Redémarre en pause selon les directives
- **Intégration Command Pattern** : Respecte l'architecture existante

**Mapping clavier** : `"r" → ToucheClavier.RESTART → CommandeRedemarrer()`

# Tests spécifiques par pièce
python -m unittest tests.unit.domaine.test_entites.test_pieces.test_piece_j -v
```

**État actuel** : 138/138 tests réussis (100% ✅)

#### Métriques actuelles
- **92 tests** passent (100% ✅)
- **Couverture** : Value Objects, Entities, Services, Factory, Registry, Command Pattern, Moteur complet, Debug TDD
- **TDD** : Cycle RED-GREEN-REFACTOR respecté systématiquement
- **7 pièces** complètement implémentées : I, O, T, S, Z, J, L
- **Plateau fonctionnel** : Collisions, lignes complètes, gravité
- **Système de contrôles complet** : 7 commandes + gestionnaire d'événements
- **Architecture découplée** : Command Pattern + Bridge Pattern
- **Interface Pygame complète** : 60 FPS, couleurs, statistiques
- **Moteur de partie** : Génération automatique, chute, scoring
- **Tests entièrement corrigés** : Tous les imports et assertions réparés
- **Debug méthodique** : Bug descente accélérée résolu avec TDD strict
- Vérification des blocs déjà placés
- Validation avant chaque mouvement

### 6. **Moteur de partie complet** ✅

#### Génération automatique des pièces
- Fabrique intégrée avec génération aléatoire équitable
- Preview de la pièce suivante
- Positionnement automatique au centre du plateau

#### Système de score et niveaux
- **Ligne simple** : 100 points × niveau
- **Double ligne** : 300 points × niveau  
- **Triple ligne** : 500 points × niveau
- **Tetris (4 lignes)** : 800 points × niveau
- **Progression automatique** : Niveau +1 tous les 10 lignes
- **Accélération** : Chute plus rapide selon le niveau

#### Interface Pygame complète
- **Affichage 60 FPS** avec boucle de jeu optimisée
- **Couleurs distinctives** par type de pièce
- **Panneau statistiques** : Score, niveau, lignes, compteurs
- **Preview pièce suivante** en temps réel
- **Grille de jeu** 10×20 avec bordures

### 7. **Tests d'intégration** ✅

#### Suite complète de validation système
- **test_generation_aleatoire** : Distribution équitable des 7 types
- **test_moteur_partie** : Mécaniques complètes du jeu
- **test_plateau_collision** : Détection de collisions
- **test_statistiques** : Système de score et progression

## Algorithmes clés

### 1. Rotation des pièces
```
Nouvelle position = rotation_matrix × position_relative + centre_rotation
```

### 2. Détection de collision
```
Pour chaque bloc de la pièce :
    Si position_x < 0 ou position_x >= largeur_plateau :
        collision = True
    Si position_y >= hauteur_plateau :
        collision = True
    Si plateau[position_y][position_x] occupé :
        collision = True
```

### 3. Suppression de lignes
```
Pour chaque ligne du bas vers le haut :
    Si ligne complète :
        Supprimer la ligne
        Déplacer toutes les lignes au-dessus vers le bas
        Incrémenter le score
```

### Configuration et constantes

### Contrôles de jeu
```
Contrôles simplifiés et intuitifs :

← Flèche gauche  : Déplacer la pièce vers la gauche
→ Flèche droite  : Déplacer la pièce vers la droite  
↑ Flèche haut    : Tourner la pièce (rotation horaire)
↓ Flèche bas     : Chute rapide (ligne par ligne)
Space            : Chute instantanée (jusqu'en bas)
P                : Pause/Reprendre la partie
M                : Mute/Unmute audio (musique et effets)
```

**Touches répétables** : ←, →, ↓ (pour un déplacement fluide)  
**Délais optimisés** : 200ms initial, 120ms répétition

### Dimensions
- Largeur plateau : 10 blocs
- Hauteur plateau : 20 blocs
- Taille d'un bloc : 30 pixels

### Couleurs
- Arrière-plan : Noir (#000000)
- Grille : Gris foncé (#333333)
- Pièces : Couleurs vives selon le type

### Timing
- Chute normale : 500ms par ligne
- Chute rapide : 50ms par ligne
- Délai de placement : 500ms

## Dépendances

### Pygame
- Gestion de la fenêtre et des événements
- Rendu graphique
- Gestion du temps et des animations
- Gestion des entrées clavier

### Modules Python standard
- `random` : Génération aléatoire des pièces
- `time` : Gestion du timing
- `json` : Sauvegarde des scores

## Points d'extension

### Fonctionnalités avancées possibles
1. **Mode multijoueur** : Jeu en réseau
2. **Niveaux de difficulté** : Vitesse progressive
3. **Effets visuels** : Animations et particules
4. **Son** : Musique et effets sonores
5. **Sauvegarde** : Progression et meilleurs scores

### Optimisations possibles
1. **Cache des rotations** : Précalcul des positions
2. **Prédiction de collision** : Optimisation des calculs
3. **Rendu optimisé** : Mise à jour partielle de l'écran

## Notes de développement

### Conventions de code
- Nommage en snake_case
- Classes en PascalCase
- Constantes en UPPER_CASE
- Documentation avec docstrings

### Tests recommandés
- Tests unitaires pour les algorithmes de collision
- Tests de rotation des pièces
- Tests de suppression de lignes
- Tests de performance

### Debugging
- Mode debug avec affichage des coordonnées
- Logs des événements de jeu
- Visualisation des zones de collision

---

## 🎯 État d'avancement du projet

### ✅ Phase 1 - Fondations (TERMINÉE)
**Objectif** : Implémenter toutes les pièces de Tetris avec TDD

**Réalisations** :
- ✅ **7/7 pièces Tetris complètes** : I, O, T, S, Z, J, L
- ✅ **56 tests TDD** avec 100% de réussite
- ✅ **Registry Pattern** avec auto-enregistrement
- ✅ **Factory Pattern** pour création centralisée
- ✅ **Architecture hexagonale** respectée
- ✅ **Symétrie J/L** parfaitement implémentée

**Architecture stable** : Prête pour la phase suivante 🚀

### 🔄 Phase 2 - Plateau de jeu (TERMINÉE ✅)
**Objectifs** :
- ✅ **Grille de jeu 10×20** implémentée
- ✅ **Détection de collision** avec le plateau
- ✅ **Placement définitif** des pièces
- ✅ **Détection de lignes complètes** et suppression
- ✅ **Descente automatique** des lignes supérieures

**Réalisations** :
- **Plateau** : Entity avec grille 10×20, Set pour O(1) collision detection
- **Intégration** : Compatible avec toutes les pièces existantes
- **Ligne complète** : Algorithme de détection et suppression
- **Gravité** : Logique de descente des blocs

### 🎮 Phase 2.5 - Système de contrôles (TERMINÉE ✅)
**Objectifs** :
- ✅ **Command Pattern** pour les actions de jeu
- ✅ **Gestionnaire d'événements** générique
- ✅ **Contrôles simplifiés** (7 touches essentielles)
- ✅ **Répétition optimisée** (délais ajustés pour le gameplay)
- ✅ **Adaptateur Pygame** pour l'intégration

**Réalisations** :
- **7 Commandes essentielles** : Gauche, Droite, Rotation, Chute rapide, Chute instantanée, Pause, Mute
- **Mapping intuitif** : Flèches directionnelles + Space + P + M
- **Répétition fluide** : 200ms initial, 120ms répétition pour déplacement continu
- **Architecture découplée** : Bridge Pattern vers Pygame
- **Contrôle audio intégré** : M pour basculer mute/unmute

### ⏳ Phase 2.6 - Système audio (TERMINÉE ✅)
**Objectifs** :
- ✅ **Port audio** avec interface AudioJeu
- ✅ **Adapter Pygame** pour la gestion sonore
- ✅ **Musique de fond** avec tetris-theme.wav (format compatible)
- ✅ **Effets sonores** rotate.wav lors des rotations de pièces ✅ **NOUVEAU !**
- ✅ **Intégration architecture** hexagonale
- ✅ **Contrôles audio** (pause/reprise intégrés)
- ✅ **Système mute/unmute** global pour tous les sons ✅ **NOUVEAU !**
- ✅ **Système de fallback** automatique (OGG → WAV)
- ✅ **Gestion d'erreurs** robuste

**Réalisations** :
- **Interface AudioJeu** : 9 méthodes pour musique et effets sonores
- **AudioPartie Adapter** : Implémentation Pygame avec gestion des assets et mute
- **Intégration MoteurPartie** : Injection de dépendance + effets sonores rotation
- **Contrôles intégrés** : Pause affecte aussi la musique (touche P)
- **Mute global** : Touche M bascule mute/unmute pour TOUS les sons ✅
- **Audio rotation** : rotate.wav joué à chaque rotation réussie (volume 100%) ✅
- **Audio gain de niveau** : gained-a-new-level.wav joué à chaque passage de niveau ✅ **NOUVEAU !**
- **Architecture respectée** : Port/Adapter pattern pour l'audio
- **Fallback automatique** : Tentative WAV si OGG échoue
- **Problème résolu** : Chemin audio corrigé (4 remontées au lieu de 3)
- **Tests complets** : 7 nouveaux tests (acceptance + intégration) pour son gain niveau ✅ **NOUVEAU !**

```python
# Interface port audio
class AudioJeu(ABC):
    @abstractmethod
    def jouer_musique(self, nom_fichier: str, volume: float = 0.7, boucle: bool = True): pass
    
    @abstractmethod  
    def arreter_musique(self): pass
    
    @abstractmethod
    def basculer_pause_musique(self): pass
    
    @abstractmethod
    def jouer_effet_sonore(self, nom_fichier: str, volume: float = 1.0): pass  # ✅ NOUVEAU !

# Utilisation avec injection de dépendance et gestion d'erreurs
audio = AudioPartie()
moteur = MoteurPartie(audio=audio)

# Audio rotation intégré dans le moteur ✅ NOUVEAU !
def tourner_piece_active(self):
    if self._peut_tourner_piece():
        self.piece_active.tourner()
        if self.audio:  # Respect architecture hexagonale
            self.audio.jouer_effet_sonore("assets/audio/sfx/rotate.wav", volume=1.0)
        return True
    return False

# Système de fallback intégré dans l'adaptateur
# Essaie tetris-theme.ogg, puis tetris-theme.wav automatiquement
```

### ⏳ Phase 3 - Interface utilisateur (PROCHAINE)
**Objectifs** :
- Interface Pygame
- Contrôles clavier
- Affichage graphique avec masquage zone invisible
- Game loop principal

## 🎨 Améliorations d'Interface

### Masquage de la Zone Invisible
**Problème résolu** : Les pièces étaient visibles dans la zone de spawn (y < 0), créant un affichage peu réaliste.

**Solution implémentée** :
```python
# Dans AffichagePartie._dessiner_piece_active()
for pos in moteur.piece_active.positions:
    if pos.y >= 0:  # Masquage de la zone invisible
        # Afficher seulement les positions visibles
        self._dessiner_position(pos, couleur)
```

**Avantages** :
- ✅ **Expérience utilisateur propre** : Seules les parties visibles des pièces sont affichées
- ✅ **Réalisme accru** : Simulation correcte de la zone invisible du Tetris
- ✅ **Spawn naturel** : Les pièces apparaissent progressivement depuis le haut
- ✅ **Compatibilité** : Fonctionne avec toutes les pièces et orientations

**Tests** :
- `tests/acceptance/test_masquage_zone_invisible.py` : Validation complète
- `demo/demo_masquage_zone_invisible.py` : Démonstration visuelle
