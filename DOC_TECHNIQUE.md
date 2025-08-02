# Documentation technique - Tetris Python

Documentation technique pour comprendre l'architecture hexagonale et l'implémentation du jeu Tetris.

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
│   │   └── sfx/                # Effets sonores (line_clear.wav, rotate.wav)
│   └── images/                 # Images et textures
│       └── backgrounds/        # Arrière-plans optionnels
├── tests/                      # Tests organisés par type
│   ├── unit/                   # Tests unitaires
│   │   ├── domaine/            # Tests du domaine métier
│   │   │   ├── entites/        # Tests des entités
│   │   │   └── services/       # Tests des services
│   │   └── interface/          # Tests de l'interface
│   ├── integration/            # Tests d'intégration
│   └── acceptance/             # Tests d'acceptance
├── docs/                       # Documentation complète
├── tmp/                        # 🔧 OUTILS DE DÉVELOPPEMENT - Scripts temporaires
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
- **PieceT** : Forme en T (4 orientations)
- **PieceS** : Forme en S (2 orientations)
- **PieceZ** : Forme en Z (2 orientations)
- **PieceJ** : Forme en J (4 orientations)
- **PieceL** : Forme en L (4 orientations) ✅ **Nouvelle !**

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

PieceT (T) - 4 orientations :
Nord:  █     Est: █      Sud: ███    Ouest: █
      ███         ██           █            ██
                  █                         █

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
- **Position pivot** : Point fixe pour les rotations
- **4 blocs** par pièce
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
# Commandes complètes (8 actions essentielles)
CommandeDeplacerGauche()    # ← Déplacement horizontal gauche
CommandeDeplacerDroite()    # → Déplacement horizontal droite
CommandeTourner()           # ↑ Rotation horaire
CommandeDescendre()         # ↓ Chute rapide (par ligne)
CommandeChuteRapide()       # Space - Chute instantanée (jusqu'en bas)
CommandeAfficherMenu()      # Esc - Menu en jeu
CommandePause()             # P - Pause/Reprendre
CommandeBasculerMute()      # M - Mute/Unmute audio ✅ NOUVEAU !
```

**Contrôles optimisés** :
- **Flèches directionnelles** : Contrôles principaux intuitifs
- **Touches spéciales** : Actions de jeu (Space, Esc, P, M)
- **Répétition intelligente** : Déplacement fluide (200ms initial, 120ms répétition)
- **Mute non-répétable** : La touche M ne se répète pas automatiquement
- **Mapping complet** : 8 touches essentielles (ajout mute/unmute)

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
- **Contrôles complets** : 8 touches essentielles (ajout mute/unmute)
- **Mapping intuitif** : Flèches + Space + Esc + P + M
- **Répétition optimisée** : Délais ajustés pour le gameplay (200ms/120ms)
- **Actions spécialisées** : Chute rapide vs chute instantanée
- **Gestion de menu** : Esc pour ouvrir/fermer le menu en jeu
- **Contrôle audio** : M pour basculer mute/unmute (sans répétition)

#### Adaptateur Pygame - Bridge vers UI
```python
# Intégration avec Pygame
adaptateur = AdaptateurPygame(gestionnaire)
adaptateur.demarrer()

# Dans la boucle de jeu
stats = adaptateur.traiter_evenements(moteur)
# → Conversion automatique événements Pygame → commandes
```

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
- **Cycle d'orientations** : Nord → Est → Sud → Ouest → Nord
- **Calculs géométriques** : Transformations matricielles pour les rotations

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
python tests/run_all_unit_tests.py       # Tests unitaires (92 tests)
python tests/run_all_acceptance_tests.py # Tests d'acceptance (35 tests)
python tests/run_all_integration_tests.py # Tests d'intégration (4 tests)
python tests/run_all_acceptance_tests.py # Tests d'acceptance (22 tests)
python tests/run_all_integration_tests.py # Tests d'intégration (4 tests)
```

**Métriques actuelles** : **101 tests, 100% de réussite ✅**
- **Architecture hexagonale** : Complètement implémentée
- **Couverture TDD** : Toutes les fonctionnalités testées
- **Corrections récentes** : Pièces S et Z harmonisées (positions y-1)
python tests/run_all_integration_tests.py # Tests d'intégration (11 tests)

# Tests spécifiques par pièce
python -m unittest tests.unit.domaine.test_entites.test_pieces.test_piece_j -v
```

**État actuel** : 103/103 tests réussis (100% ✅)

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
Esc              : Afficher/masquer le menu en jeu
P                : Pause/Reprendre la partie
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
- **7 Commandes essentielles** : Gauche, Droite, Rotation, Chute rapide, Chute instantanée, Menu, Pause
- **Mapping intuitif** : Flèches directionnelles + Space + Esc + P
- **Répétition fluide** : 200ms initial, 120ms répétition pour déplacement continu
- **Architecture découplée** : Bridge Pattern vers Pygame
- **Menu intégré** : Esc pour accéder au menu en cours de jeu

### ⏳ Phase 2.6 - Système audio (TERMINÉE ✅)
**Objectifs** :
- ✅ **Port audio** avec interface AudioJeu
- ✅ **Adapter Pygame** pour la gestion sonore
- ✅ **Musique de fond** avec tetris-theme.wav (format compatible)
- ✅ **Intégration architecture** hexagonale
- ✅ **Contrôles audio** (pause/reprise intégrés)
- ✅ **Système de fallback** automatique (OGG → WAV)
- ✅ **Gestion d'erreurs** robuste

**Réalisations** :
- **Interface AudioJeu** : 9 méthodes pour musique et effets sonores
- **AudioPartie Adapter** : Implémentation Pygame avec gestion des assets
- **Intégration MoteurPartie** : Injection de dépendance pour découplage
- **Contrôles intégrés** : Pause affecte aussi la musique (touche P)
- **Architecture respectée** : Port/Adapter pattern pour l'audio
- **Fallback automatique** : Tentative WAV si OGG échoue
- **Problème résolu** : Chemin audio corrigé (4 remontées au lieu de 3)

```python
# Interface port audio
class AudioJeu(ABC):
    @abstractmethod
    def jouer_musique(self, nom_fichier: str, volume: float = 0.7, boucle: bool = True): pass
    
    @abstractmethod  
    def arreter_musique(self): pass
    
    @abstractmethod
    def basculer_pause_musique(self): pass

# Utilisation avec injection de dépendance et gestion d'erreurs
audio = AudioPartie()
moteur = MoteurPartie(audio=audio)

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
