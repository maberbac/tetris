# Documentation technique - Tetris Python

Documentation technique pour comprendre l'architecture hexagonale et l'implémentation du jeu Tetris.

## Table des matières

1. [Architecture du projet](#architecture-du-projet)
   - [Structure actuelle - Architecture Hexagonale](#structure-actuelle---architecture-hexagonale)
2. [Composants principaux](#composants-principaux)
   - [1. Value Objects - Position](#1-value-objects---position)
   - [2. Entities - Pièces](#2-entities---pièces)
   - [3. Factory Pattern avec Registry](#3-factory-pattern-avec-registry)
   - [4. Services - Couche logique métier](#4-services---couche-logique-métier)
   - [5. Patterns d implémentation appris](#5-patterns-d-implémentation-appris)
   - [6. Tests et qualité](#6-tests-et-qualité)
   - [7. Moteur de partie complet](#7-moteur-de-partie-complet)
   - [8. Tests d intégration](#8-tests-d-intégration)
3. [Gestion des Exceptions](#gestion-des-exceptions)
   - [1. Exceptions du Domaine - Logique métier](#1-exceptions-du-domaine---logique-métier)
   - [2. Exceptions des Adapters - Couche technique](#2-exceptions-des-adapters---couche-technique)
   - [3. Exceptions d Infrastructure - Couche système](#3-exceptions-d-infrastructure---couche-système)
   - [4. Stratégie de Gestion d'Erreurs](#4-stratégie-de-gestion-d-erreurs)
   - [5. Messages d Erreur Utilisateur](#5-messages-d-erreur-utilisateur)
   - [6. Architecture d Exception par Couche](#6-architecture-d-exception-par-couche)
4. [Algorithmes clés](#algorithmes-clés)
   - [1. Rotation des pièces](#1-rotation-des-pièces)
   - [2. Détection de collision](#2-détection-de-collision)
   - [3. Suppression de lignes](#3-suppression-de-lignes)
   - [Configuration et constantes](#configuration-et-constantes)
   - [Contrôles de jeu](#contrôles-de-jeu)
   - [Dimensions](#dimensions)
   - [Couleurs](#couleurs)
   - [Timing](#timing)
5. [Dépendances](#dépendances)
   - [Pygame](#pygame)
   - [Modules Python standard](#modules-python-standard)
6. [Points d extension](#points-d-extension)
   - [Fonctionnalités avancées possibles](#fonctionnalités-avancées-possibles)
   - [Optimisations possibles](#optimisations-possibles)
7. [Notes de développement](#notes-de-développement)
   - [Conventions de code](#conventions-de-code)
   - [Tests recommandés](#tests-recommandés)
   - [Debugging](#debugging)
8. [État d avancement du projet](#état-d-avancement-du-projet)
   - [Phase 1 - Fondations (TERMINÉE)](#phase-1---fondations-terminée)
   - [Phase 2 - Plateau de jeu (TERMINÉE)](#phase-2---plateau-de-jeu-terminée)
   - [Phase 3 - Système de contrôles (TERMINÉE)](#phase-3---système-de-contrôles-terminée)
   - [Phase 4 - Système audio (TERMINÉE)](#phase-4---système-audio-terminée)
   - [Phase 5 - Interface utilisateur (TERMINÉE)](#phase-5---interface-utilisateur-terminée)
9. [Améliorations d Interface](#améliorations-d-interface)
   - [Masquage de la Zone Invisible](#masquage-de-la-zone-invisible)

---

## Architecture du projet

### Structure actuelle - Architecture Hexagonale
```
tetris/
├── src/                        # Code source - Architecture hexagonale
│   ├── domaine/                # DOMAINE - Logique métier pure (centre de l'hexagone)
│   │   ├── entites/            # Entités du domaine
│   │   │   ├── position.py     # Value Object pour les coordonnées
│   │   │   ├── piece.py        # Classe abstraite des pièces
│   │   │   ├── plateau.py      # Grille de jeu 10×20
│   │   │   ├── pieces/         # Implémentations des pièces
│   │   │   │   ├── piece_i.py  # Pièce ligne
│   │   │   │   ├── piece_o.py  # Pièce carrée  
│   │   │   │   ├── piece_t.py  # Pièce en T
│   │   │   │   ├── piece_s.py  # Pièce en S
│   │   │   │   ├── piece_z.py  # Pièce en Z
│   │   │   │   ├── piece_j.py  # Pièce en J
│   │   │   │   └── piece_l.py  # Pièce en L 
│   │   │   └── fabriques/      # Factory Pattern
│   │   │       ├── registre_pieces.py    # Registry avec auto-enregistrement
│   │   │       └── fabrique_pieces.py    # Factory pour créer les pièces
│   │   ├── exceptions/         # Exceptions du domaine
│   │   │   ├── exception_collision.py  # Exception pour collisions de pièces
│   │   │   ├── exception_audio.py      # Exception pour erreurs audio système
│   │   │   └── __init__.py             # Export centralisé ExceptionCollision + ExceptionAudio
│   │   └── services/           # Services métier
│   │       ├── commandes/      # Command Pattern pour actions
│   │       ├── logger_tetris.py    # Système de logging centralisé
│   │       ├── moteur_partie.py    # Moteur principal du jeu
│   │       └── statistiques/   # Gestion des statistiques
│   ├── ports/                  # PORTS - Interfaces (contrats)
│   │   ├── sortie/             # Ports de sortie
│   │   │   ├── affichage_jeu.py    # Interface pour l'affichage
│   │   │   └── audio_jeu.py        # Interface pour l'audio
│   │   └── controleur_jeu.py   # Interface pour les contrôles
│   └── adapters/               # ADAPTERS - Implémentations techniques
│       ├── entree/             # Adapters d'entrée
│       │   └── gestionnaire_partie.py  # Gestion Pygame des entrées
│       └── sortie/             # Adapters de sortie
│           ├── affichage_partie.py     # Rendu Pygame avec masquage zone invisible
│           └── audio_partie.py         # Audio Pygame
├── assets/                     # MÉDIAS - Assets du jeu
│   ├── audio/                  # Sons et musiques
│   │   ├── music/              # Musique principale (tetris-theme.wav FONCTIONNEL !)
│   │   └── sfx/                # Effets sonores (line_clear.wav, rotate.wav, tetris.wav)
│   └── images/                 # Images et textures
│       └── backgrounds/        # Arrière-plans optionnels
├── docs/                       # DOCUMENTATION COMPLÈTE
│   ├── DIRECTIVES_DEVELOPPEMENT.md  # Règles de développement
│   ├── DOC_TECHNIQUE.md              # Documentation technique détaillée
│   ├── journal-developpement.md     # Journal complet du projet
│   └── testing-strategy.md          # Stratégie TDD et métriques
├── tests/                      # Tests organisés par type
│   ├── unit/                   # Tests unitaires (145 tests)
│   │   ├── domaine/            # Tests du domaine métier
│   │   │   ├── entites/        # Tests des entités (Position, Pièces, Factory, Statistiques)
│   │   │   └── services/       # Tests des services (GestionnaireEvenements, Commandes, Restart)
│   │   └── adapters/           # Tests des adaptateurs (Audio avec mute/unmute + ExceptionAudio)
│   ├── acceptance/             # Tests d'acceptance (101 tests)
│   │   ├── test_controles_*.py # Tests des contrôles utilisateur
│   │   ├── test_fonctionnalite_mute.py # Tests mute/unmute
│   │   ├── test_fonctionnalite_restart.py # Tests restart
│   │   ├── test_correction_bug_crash_placement.py # Tests robustesse crash placement
│   │   ├── test_correction_bug_crash_reprise_partie.py # Tests robustesse crash reprise
│   │   ├── test_correction_bug_lignes_multiples.py # Tests lignes multiples
│   │   ├── test_correction_bug_gameover_premature.py # Tests game over
│   │   ├── test_bug_visuel_ligne_complete.py # Tests affichage ligne complète
│   │   ├── test_son_gain_niveau.py # Tests son gain de niveau
│   │   ├── test_son_game_over.py # Tests son game over
│   │   ├── test_son_tetris.py    # Tests son TETRIS pour 4 lignes
│   │   ├── test_audio_rotation.py # Tests audio rotation avec ExceptionAudio
│   │   ├── test_indicateur_mute.py # Tests indicateur visuel mute
│   │   ├── test_mute_game_over.py # Tests correction mute game over
│   │   └── test_masquage_zone_invisible.py # Tests masquage zone invisible
│   ├── integration/            # Tests d'intégration (26 tests)
│   │   ├── test_audio_integration.py # Tests intégration audio (6 tests)
│   │   ├── test_correction_audio.py # Tests correction audio (5 tests)
│   │   ├── test_exception_audio_integration.py # Tests intégration ExceptionAudio (4 tests)
│   │   ├── test_restart_integration.py # Tests intégration restart (3 tests)
│   │   ├── test_son_gain_niveau_integration.py # Tests intégration son gain niveau (2 tests)
│   │   ├── test_son_game_over_integration.py # Tests intégration son game over (2 tests)
│   │   └── [4 tests d'intégration directe] # Tests génération, moteur, plateau, statistiques
│   └── [4 scripts officiels]  # Scripts de lancement obligatoires
├── partie_tetris.py            # ORCHESTRATEUR - Composition root (assemble tout)
└── jouer.py                    # Point d'entrée utilisateur
```

## Composants principaux

### 1. Value Objects - Position
```python
@dataclass(frozen=True)
class Position:
    x: int
    y: int
    
    def deplacer(self, delta_x: int, delta_y: int) -> 'Position':
        return Position(self.x + delta_x, self.y + delta_y)
```
- Immutable : Ne peut pas être modifiée après création
- Equality par valeur : Deux positions avec mêmes coordonnées sont égales
- Système de coordonnées : (0,0) en haut à gauche

### 2. Entities - Pièces
```python
@piece_tetris(TypePiece.I)  # Auto-enregistrement
class PieceI(Piece):
    def tourner(self) -> None:
        # Logique de rotation spécifique à I
```

#### Pièces implémentées
- PieceI : Ligne droite (2 orientations)
- PieceO : Carré (1 orientation, pas de rotation)
- PieceT : Forme en T (4 orientations)
- PieceS : Forme en S (2 orientations)
- PieceZ : Forme en Z (2 orientations)
- PieceJ : Forme en J (4 orientations)
- PieceL : Forme en L (4 orientations)

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

PieceT (T) - 4 orientations (rotation horaire) :
Nord:  █     Ouest:  █     Sud:███    Est:█
      ███           ██          █         ██
                     █                    █

Ordre de rotation : Nord → Ouest → Sud → Est → Nord

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
- Mutables : Peuvent changer d'état (déplacement, rotation)
- Position pivot : Point fixe pour les rotations (pièce T : pivot à (5,0))
- 4 blocs par pièce selon les spécifications Tetris
- Rotation horaire : Toutes les pièces suivent l'ordre horaire standard
- Héritage : Comportement commun dans classe abstraite `Piece`

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
- Extensibilité : Nouvelles pièces sans modification du code existant
- Auto-découverte : Registry trouve automatiquement les pièces
- Découplage : Factory ne connaît pas les classes concrètes

### 4. Services - Couche logique métier

#### Command Pattern - Actions de jeu
```python
# Commandes disponibles (8 actions de jeu)
CommandeDeplacerGauche()    # ← Déplacement horizontal gauche avec ExceptionCollision
CommandeDeplacerDroite()    # → Déplacement horizontal droite avec ExceptionCollision
CommandeTourner()           # ↑ Rotation horaire avec ExceptionCollision
CommandeDescendre()         # ↓ Chute rapide (par ligne) 
CommandeChuteRapide()       # Space - Chute instantanée (jusqu'en bas) avec ExceptionCollision
CommandePause()             # P - Pause/Reprendre le jeu
CommandeBasculerMute()      # M - Mute/Unmute audio unifié
CommandeRestart()           # R - Redémarrer après game over

# Toutes les commandes de mouvement utilisent ExceptionCollision
# pour signaler les collisions au lieu de retourner True/False
try:
    commande.execute(moteur)
except ExceptionCollision as e:
    logger.info(f"Mouvement bloqué: {e}")
```
CommandePause()             # P - Pause/Reprendre
CommandeBasculerMute()      # M - Mute/Unmute audio
CommandeRedemarrer()        # R - Restart après game over
```

**Architecture des Commandes** :
- **Commandes avec ExceptionCollision** : `CommandeDeplacerGauche`, `CommandeDeplacerDroite`, `CommandeTourner`, `CommandeChuteRapide` lèvent `ExceptionCollision` en cas de collision
- **Gestionnaire d'événements** : Capture les `ExceptionCollision` et les traite silencieusement pour préserver l'expérience utilisateur
- **Conformité directives** : Toutes les commandes de mouvement utilisent maintenant les exceptions spécifiques au domaine au lieu de retourner `True`/`False`

Contrôles de jeu :
- Flèches directionnelles : Contrôles principaux intuitifs
- Touches spéciales : Actions de jeu (Space, P, M, R)
- Répétition intelligente : Déplacement fluide (200ms initial, 120ms répétition)
- Actions ponctuelles : M et R ne se répètent pas automatiquement
- Mapping complet : 8 touches essentielles couvrant tous les besoins du jeu

#### Gestionnaire d événements - Input handling
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

Fonctionnalités :
- Contrôles complets : 8 touches essentielles (déplacement, rotation, actions spéciales)
- Mapping intuitif : Flèches + Space + P + M + R
- Répétition optimisée : Délais ajustés pour le gameplay (200ms/120ms)
- Actions spécialisées : Chute rapide vs chute instantanée
- Contrôle audio : M pour basculer mute/unmute (sans répétition)
- Redémarrage rapide : R pour restart après game over (sans répétition)

## Gestion des Exceptions

Le projet utilise une approche structurée pour la gestion des erreurs, respectant l'architecture hexagonale avec des exceptions spécifiques à chaque couche.

### 1. Exceptions du Domaine - Logique métier

#### ExceptionCollision - Gestion spécifique des collisions
```python
# Plateau - Collision lors du placement
if not self.peut_placer_piece(piece):
    raise ExceptionCollision("Impossible de placer la pièce à cette position")

# Commandes - Utilisent ExceptionCollision selon les directives
try:
    commande.execute(moteur)  # CommandeDeplacerGauche, CommandeDeplacerDroite, CommandeTourner, CommandeChuteRapide
    return True
except ExceptionCollision:
    return False  # Collision gérée silencieusement
```

**Utilisation dans les Commandes** :
- **CommandeDeplacerGauche** : Lève `ExceptionCollision` si déplacement gauche impossible
- **CommandeDeplacerDroite** : Lève `ExceptionCollision` si déplacement droite impossible  
- **CommandeTourner** : Lève `ExceptionCollision` si rotation impossible
- **CommandeChuteRapide** : Lève `ExceptionCollision` si pièce immédiatement bloquée (ne peut pas descendre du tout)
- **Gestionnaire d'événements** : Capture toutes les `ExceptionCollision` et retourne `False` pour préserver l'expérience utilisateur

Utilisation :
- Collisions de placement : Pièce ne peut pas être placée (collision, hors limites)
- Situations inattendues : Collisions qui ne devraient pas arriver en conditions normales
- Débogage : Identifier précisément les problèmes de collision

#### ExceptionAudio - Gestion robuste des erreurs audio
```python
# AudioPartie - Toutes les opérations audio lèvent ExceptionAudio
def jouer_effet_sonore(self, nom_fichier: str, volume: float = 1.0) -> None:
    if not self.initialise:
        raise ExceptionAudio("Système audio non initialisé")
    
    try:
        son = pygame.mixer.Sound(nom_fichier)
        son.play()
    except pygame.error as e:
        raise ExceptionAudio(f"Impossible de jouer l'effet sonore {nom_fichier}: {e}")

# MoteurPartie - Gestion gracieuse des erreurs audio
def tourner_piece_active(self) -> bool:
    if self.plateau.peut_placer_piece(self.piece_active):
        if self.audio:
            try:
                self.audio.jouer_effet_sonore("assets/audio/sfx/rotate.wav", volume=1.0)
            except ExceptionAudio as e:
                logger_tetris.debug(f"[AUDIO] Son rotation non joué: {e}")
                # Le jeu continue sans son
        return True
    return False

# jouer.py - Gestion centralisée pour l'utilisateur final
try:
    partie.jouer()
except ExceptionAudio as e:
    logger_tetris.warning(f"⚠️ Problème audio : {e}")
    logger_tetris.info("🎮 Le jeu continuera sans audio")
    return 0  # Le jeu peut continuer sans audio
```

**Utilisation dans le Système Audio** :
- **AudioPartie** : Toutes les méthodes lèvent `ExceptionAudio` (initialiser, jouer_musique, jouer_effet_sonore)
- **MoteurPartie** : Capture `ExceptionAudio` localement pour tous les appels audio (rotation, game over, tetris, gain niveau)
- **jouer.py** : Gestion centralisée avec messages utilisateur informatifs
- **Architecture** : Permet au jeu de fonctionner avec dégradation gracieuse (sans audio)

Utilisation :
- Erreurs d'initialisation : Système audio indisponible, pygame non installé
- Erreurs de fichiers : Fichiers audio manquants ou corrompus
- Erreurs système : Problèmes de périphérique audio, permissions
- Expérience utilisateur : Messages informatifs, jeu continue sans crash

#### ValueError - Validation des données métier
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

Utilisation :
- Validation des dimensions : Plateau avec largeur/hauteur <= 0
- Validation des types : Type de pièce non supporté par le registre
- Validation du registre : Aucune pièce disponible pour génération aléatoire

### 2. Exceptions des Adapters - Couche technique

#### pygame.error - Erreurs spécifiques Pygame
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

Utilisation :
- Initialisation audio : Problèmes avec le système audio du système
- Chargement de fichiers : Fichiers audio corrompus ou formats non supportés
- Lecture audio : Problèmes de lecture en temps réel

### 3. Exceptions d Infrastructure - Couche système

#### ImportError - Dépendances manquantes
```python
# Vérification Pygame
try:
    import pygame
except ImportError:
    pygame = None

# Lanceur principal - Gestion des imports
except ImportError as e:
    print(f" Erreur d'importation: {e}")
    print("Assurez-vous que pygame est installé : pip install pygame")
```

Utilisation :
- Dépendances manquantes : Pygame non installé
- Modules introuvables : Problèmes de structure du projet
- Imports optionnels : Fonctionnalités dégradées sans dépendance

#### Exception - Gestionnaire générique
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
    print(f" Erreur durant la partie: {e}")
    traceback.print_exc()
```

Utilisation :
- Erreurs audio non critiques : Le jeu continue sans audio
- Erreurs de commandes : Retour gracieux avec feedback utilisateur
- Erreurs système imprévues : Affichage debug + stack trace complet

### 4. Stratégie de Gestion d Erreurs

#### Principe de Résilience
```python
#  CORRECT - Gestion gracieuse avec fallback
try:
    self.audio.jouer_musique("tetris-theme.ogg")
except pygame.error:
    # Tentative de fallback WAV
    try:
        self.audio.jouer_musique("tetris-theme.wav")
    except pygame.error as e2:
        print(f"[ERROR] Impossible de jouer la musique: {e2}")
        # Le jeu continue sans musique

#  CORRECT - Validation préventive
if self.largeur <= 0 or self.hauteur <= 0:
    raise ValueError(f"Dimensions invalides: {self.largeur}x{self.hauteur}")

#  CORRECT - Logging informatif
except Exception as e:
    print(f"[DEBUG] Erreur audio non critique: {e}")
    # Continue l'exécution
```

#### Anti-Patterns à Éviter
```python
#  INCORRECT - Masquer les erreurs
try:
    operation_critique()
except:
    pass  # Erreur silencieuse = problème

#  INCORRECT - Catch trop large sans action
try:
    operation_specifique()
except Exception:
    return False  # Perte d'information sur l'erreur

#  INCORRECT - Laisser crasher sans gestion
def operation_sans_validation(data):
    return data.some_property  # Peut lever AttributeError
```

### 5. Messages d Erreur Utilisateur

#### Messages Français et Informatifs
```python
#  Messages clairs pour l'utilisateur
"Impossible de placer la pièce à cette position"
"Dimensions invalides: 10x-5"  
"Type de pièce non supporté : X. Types disponibles : ['I', 'O', 'T']"
"Pygame n'est pas installé. Utilisez: pip install pygame"

#  Messages de debug pour les développeurs  
"[ERROR] Erreur lors de l'initialisation audio: [Errno 2] No such file"
"[DEBUG] Erreur audio non critique: mixer not initialized"
" Erreur durant la partie: 'NoneType' object has no attribute 'play'"
```

### 6. Architecture d Exception par Couche

#### Couche Domaine - Exceptions métier
```python
# ExceptionCollision - Gestion des collisions de jeu
class ExceptionCollision(Exception):
    def __init__(self, message: str = "Collision détectée"):
        super().__init__(message)

# ExceptionAudio - Gestion des erreurs audio système
class ExceptionAudio(Exception):
    def __init__(self, message: str = "Erreur audio"):
        super().__init__(message)
```

#### Couche Application - Gestion locale et centralisée
```python
# GestionnaireEvenements - Capture ExceptionCollision (locale)
try:
    return commande.execute(moteur)
except ExceptionCollision:
    return False  # Gestion silencieuse des collisions

# MoteurPartie - Capture ExceptionAudio (locale)
try:
    self.audio.jouer_effet_sonore("rotate.wav")
except ExceptionAudio as e:
    logger_tetris.debug(f"[AUDIO] Son non joué: {e}")
    # Le jeu continue sans son

# jouer.py - Capture ExceptionAudio (centralisée)
try:
    partie.jouer()
except ExceptionAudio as e:
    logger_tetris.warning(f"⚠️ Problème audio : {e}")
    logger_tetris.info("🎮 Le jeu continuera sans audio")
    return 0  # Permet au jeu de continuer
```

#### Couche Infrastructure - Lancement des exceptions
```python
# AudioPartie - Lève ExceptionAudio pour toutes les erreurs audio
def jouer_effet_sonore(self, nom_fichier: str, volume: float = 1.0) -> None:
    try:
        son = pygame.mixer.Sound(nom_fichier)
        son.set_volume(volume)
        son.play()
    except pygame.error as e:
        raise ExceptionAudio(f"Impossible de jouer {nom_fichier}: {e}")

# Commandes - Lèvent ExceptionCollision pour les mouvements impossibles
def execute(self, moteur: MoteurJeu) -> bool:
    if not moteur.deplacer_piece_active(-1, 0):
        raise ExceptionCollision("Impossible de déplacer la pièce vers la gauche")
```

#### Patterns de Gestion
- **ExceptionCollision** : Gestion locale silencieuse (normale dans le gameplay)
- **ExceptionAudio** : Gestion locale + centralisée (erreur système informative)
- **Séparation claire** : Chaque couche gère ses responsabilités
- **Dégradation gracieuse** : Le jeu continue même en cas d'erreur non-critique

```
 Architecture des Exceptions
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
-  Robustesse : Le jeu ne crash pas pour des erreurs non critiques
-  Debugabilité : Messages clairs pour identifier les problèmes
-  UX : Feedback utilisateur approprié selon le contexte
-  Architecture : Exceptions appropriées à chaque couche hexagonale

Architecture :
- Bridge Pattern : Sépare abstraction (gestionnaire) de l'implémentation (Pygame)
- Mapping automatique : Touches Pygame → Noms génériques
- Extensibilité : Facile d'ajouter d'autres bibliothèques (tkinter, etc.)

### 5. Patterns d implémentation appris

#### Registry Pattern avec décorateurs
- Auto-enregistrement : `@piece_tetris(TypePiece.X)` enregistre automatiquement les classes
- Découverte dynamique : Pas besoin de modifier le registre pour chaque nouvelle pièce
- Type safety : Vérification des types à l'exécution

#### Rotation systématique
- Pivot fixe : Chaque pièce a un point de rotation constant
- Cycle d'orientations : Nord → Ouest → Sud → Est → Nord (rotation horaire)
- Calculs géométriques : Transformations matricielles pour les rotations

#### TDD avec patterns métier
- RED-GREEN-REFACTOR : Cycle systématique pour chaque nouvelle pièce
- Tests par comportement : Création, mouvement, rotation, type
- Différenciation : Tests pour distinguer les pièces similaires (S/Z, J/L)

#### Command Pattern pour les contrôles
- Encapsulation d'actions : Chaque input devient une commande exécutable
- Découplage UI/logique : Interface indépendante de l'implémentation
- Extensibilité : Nouvelles commandes sans modification du moteur
- Testabilité : Chaque commande testable individuellement

#### Bridge Pattern pour l input
- Abstraction/Implémentation : Gestionnaire générique + Adaptateur Pygame
- Mapping configurable : Touches physiques → Touches logiques → Commandes
- Multi-plateforme : Facilite l'ajout d'autres bibliothèques graphiques

### 6. Tests et qualité
```bash
# Exécuter tous les tests
python tests/run_suite_tests.py

# Tests par catégorie
python tests/run_all_unit_tests.py       # Tests unitaires (145 tests)
python tests/run_all_acceptance_tests.py # Tests d'acceptance (101 tests)
python tests/run_all_integration_tests.py # Tests d'intégration (26 tests)
```

Métriques actuelles : 272 tests, 100% de réussite
- Architecture hexagonale : Complètement implémentée
- Couverture TDD : Toutes les fonctionnalités testées
- Performance : Exécution complète en ~3.4s
- Fonctionnalités : Jeu complet avec contrôles, audio, indicateur mute, correction mute game over, et redémarrage

#### CommandeRedemarrer - Fonctionnalité restart

Responsabilité : Permettre de redémarrer une nouvelle partie avec la touche R.

```python
class CommandeRedemarrer(Commande):
    def execute(self, moteur: MoteurJeu) -> bool:
        if not moteur.est_game_over():
            return False  # Ignore si pas en game over
        
        moteur.redemarrer_partie()  # Réinitialise tout
        return True
```

Caractéristiques :
- Activation conditionnelle : Fonctionne uniquement après game over
- Réinitialisation complète : Score=0, niveau=1, plateau vide, nouvelle pièce
- État de pause : Redémarre en pause selon la configuration
- Intégration Command Pattern : Respecte l'architecture existante

Mapping clavier : `"r" → ToucheClavier.RESTART → CommandeRedemarrer()`

# Tests spécifiques par pièce
python -m unittest tests.unit.domaine.test_entites.test_pieces.test_piece_j -v


État actuel : 138/138 tests réussis (100% )

#### Métriques actuelles
- 92 tests passent (100% )
- Couverture : Value Objects, Entities, Services, Factory, Registry, Command Pattern, Moteur complet, Debug TDD
- TDD : Cycle RED-GREEN-REFACTOR respecté systématiquement
- 7 pièces complètement implémentées : I, O, T, S, Z, J, L
- Plateau fonctionnel : Collisions, lignes complètes, gravité
- Système de contrôles complet : 7 commandes + gestionnaire d'événements
- Architecture découplée : Command Pattern + Bridge Pattern
- Interface Pygame complète : 60 FPS, couleurs, statistiques
- Moteur de partie : Génération automatique, chute, scoring
- Tests entièrement corrigés : Tous les imports et assertions réparés
- Debug méthodique : Bug descente accélérée résolu avec TDD strict
- Vérification des blocs déjà placés
- Validation avant chaque mouvement

### 7. Moteur de partie complet 

#### Génération automatique des pièces
- Fabrique intégrée avec génération aléatoire équitable
- Preview de la pièce suivante
- Positionnement automatique au centre du plateau

#### Système de score et niveaux
- Ligne simple : 100 points × niveau
- Double ligne : 300 points × niveau  
- Triple ligne : 500 points × niveau
- Tetris (4 lignes) : 800 points × niveau
- Progression automatique : Niveau +1 tous les 10 lignes
- Accélération : Chute plus rapide selon le niveau

#### Interface Pygame complète
- Affichage 60 FPS avec boucle de jeu optimisée
- Couleurs distinctives par type de pièce
- Panneau statistiques : Score, niveau, lignes, compteurs
- Preview pièce suivante en temps réel
- Grille de jeu 10×20 avec bordures

### 8. Tests d intégration 

#### Suite complète de validation système
- test_generation_aleatoire : Distribution équitable des 7 types
- test_moteur_partie : Mécaniques complètes du jeu
- test_plateau_collision : Détection de collisions
- test_statistiques : Système de score et progression

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
R                : Redémarrer après game over
```

Touches répétables : ←, →, ↓ (pour un déplacement fluide)  
Délais optimisés : 200ms initial, 120ms répétition

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

## Points d extension

### Fonctionnalités avancées possibles
1. Mode multijoueur : Jeu en réseau
2. Niveaux de difficulté : Vitesse progressive
3. Effets visuels : Animations et particules
4. Son : Musique et effets sonores
5. Sauvegarde : Progression et meilleurs scores

### Optimisations possibles
1. Cache des rotations : Précalcul des positions
2. Prédiction de collision : Optimisation des calculs
3. Rendu optimisé : Mise à jour partielle de l'écran

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


## État d avancement du projet

### Phase 1 - Fondations (TERMINÉE)
Objectif : Implémenter toutes les pièces de Tetris avec TDD

Réalisations :
- 7/7 pièces Tetris complètes : I, O, T, S, Z, J, L
- Tests TDD complets avec 100% de réussite
- Registry Pattern avec auto-enregistrement
- Factory Pattern pour création centralisée
- Architecture hexagonale respectée
- Symétrie J/L parfaitement implémentée

Architecture stable : Fondations solides pour les fonctionnalités avancées

### Phase 2 - Plateau de jeu (TERMINÉE)
Objectifs :
- Grille de jeu 10×20 implémentée
- Détection de collision avec le plateau
- Placement définitif des pièces
- Détection de lignes complètes et suppression
- Descente automatique des lignes supérieures

Réalisations :
- Plateau : Entity avec grille 10×20, optimisation O(1) pour collision detection
- Intégration : Compatible avec toutes les pièces existantes
- Ligne complète : Algorithme de détection et suppression
- Gravité : Logique de descente des blocs

### Phase 3 - Système de contrôles (TERMINÉE)
Objectifs :
- Command Pattern pour les actions de jeu
- Gestionnaire d'événements générique
- Contrôles simplifiés (8 touches essentielles)
- Répétition optimisée (délais ajustés pour le gameplay)
- Adaptateur Pygame pour l'intégration

Réalisations :
- 8 Commandes essentielles : Gauche, Droite, Rotation, Chute rapide, Chute instantanée, Pause, Mute, Restart
- Mapping intuitif : Flèches directionnelles + Space + P + M
- Répétition fluide : 200ms initial, 120ms répétition pour déplacement continu
- Architecture découplée : Bridge Pattern vers Pygame
- Contrôle audio intégré : M pour basculer mute/unmute

### Phase 4 - Système audio (TERMINÉE)
Objectifs :
- Port audio avec interface AudioJeu
- Adapter Pygame pour la gestion sonore
- Musique de fond avec tetris-theme.wav (format compatible)
- Effets sonores rotate.wav lors des rotations de pièces
- Intégration architecture hexagonale
- Contrôles audio (pause/reprise intégrés)
- Système mute/unmute global pour tous les sons
- Système de fallback automatique (OGG → WAV)
- Gestion d'erreurs robuste

Réalisations :
- Interface AudioJeu : 9 méthodes pour musique et effets sonores
- AudioPartie Adapter : Implémentation Pygame avec gestion des assets et mute
- Intégration MoteurPartie : Injection de dépendance + effets sonores rotation
- Contrôles intégrés : Pause affecte aussi la musique (touche P)
- Mute global : Touche M bascule mute/unmute pour TOUS les sons
- Audio rotation : rotate.wav joué à chaque rotation réussie (volume 100%)
- Audio gain de niveau : gained-a-new-level.wav joué à chaque passage de niveau
- Architecture respectée : Port/Adapter pattern pour l'audio
- Fallback automatique : Tentative WAV si OGG échoue

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
    def jouer_effet_sonore(self, nom_fichier: str, volume: float = 1.0): pass

# Utilisation avec injection de dépendance et gestion d'erreurs
audio = AudioPartie()
moteur = MoteurPartie(audio=audio)

# Audio rotation intégré dans le moteur
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

### Phase 5 - Interface utilisateur (TERMINÉE)
Objectifs :
-  Interface Pygame complète
-  Contrôles clavier fonctionnels
-  Affichage graphique avec masquage zone invisible
-  Game loop principal optimisé

## Améliorations d Interface

### Masquage de la Zone Invisible
Fonctionnalité : Les pièces ne sont visibles que dans la zone de jeu principale (y ≥ 0).

Implémentation :
```python
# Dans AffichagePartie._dessiner_piece_active()
for pos in moteur.piece_active.positions:
    if pos.y >= 0:  # Masquage de la zone invisible
        # Afficher seulement les positions visibles
        self._dessiner_position(pos, couleur)
```

Avantages :
-  Expérience utilisateur propre : Seules les parties visibles des pièces sont affichées
-  Réalisme accru : Simulation correcte de la zone invisible du Tetris
-  Spawn naturel : Les pièces apparaissent progressivement depuis le haut
-  Compatibilité : Fonctionne avec toutes les pièces et orientations

Tests :
- `tests/acceptance/test_masquage_zone_invisible.py` : Validation complète
- Démonstrations visuelles disponibles
