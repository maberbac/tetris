# Documentation technique - Tetris Python

Documentation technique pour comprendre l'architecture et l'implémentation du jeu Tetris.

## 🏗️ Architecture du projet

### Structure actuelle
```
tetris/
├── src/                        # Code source
│   └── domaine/                # Logique métier
│       └── entites/            # Entités du domaine
│           ├── position.py     # Value Object pour les coordonnées
│           ├── piece.py        # Classe abstraite des pièces
│           ├── pieces/         # Implémentations des pièces
│           │   ├── piece_i.py  # Pièce ligne
│           │   ├── piece_o.py  # Pièce carrée  
│           │   ├── piece_t.py  # Pièce en T
│           │   ├── piece_s.py  # Pièce en S
│           │   ├── piece_z.py  # Pièce en Z
│           │   ├── piece_j.py  # Pièce en J
│           │   └── piece_l.py  # Pièce en L
│           └── fabriques/      # Factory Pattern
│               ├── registre_pieces.py    # Registry avec auto-enregistrement
│               └── fabrique_pieces.py    # Factory pour créer les pièces
├── tests/                      # Tests automatisés
├── demo_*.py                   # Scripts de démonstration
└── test_runner.py              # Exécuteur de tests personnalisé
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

### 4. Patterns d'implémentation appris

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

### 5. Tests et qualité
```bash
# Exécuter tous les tests
python test_runner.py

# Tests spécifiques par pièce
python -m unittest tests.test_domaine.test_entites.test_pieces.test_piece_j -v
```

#### Métriques actuelles
- **56 tests** passent (100% ✅)
- **Couverture** : Value Objects, Entities, Factory, Registry
- **TDD** : Cycle RED-GREEN-REFACTOR respecté
- **7 pièces** complètement implémentées : I, O, T, S, Z, J, L
- **Symétrie J/L** : Architecture miroir parfaite
- Vérification des blocs déjà placés
- Validation avant chaque mouvement

### 6. Game Logic (futures fonctionnalités)

#### Suppression de lignes
- Détection des lignes complètes
- Animation de suppression
- Calcul du score selon le nombre de lignes

### 7. Système de score (futur)
- Ligne simple : 100 points
- Double ligne : 300 points
- Triple ligne : 500 points
- Tetris (4 lignes) : 800 points
- Bonus de vitesse selon le niveau

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

## Configuration et constantes

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

### 🔄 Phase 2 - Plateau de jeu (PROCHAINE)
**Objectifs** :
- Grille de jeu 10×20
- Détection de collision avec le plateau
- Placement définitif des pièces
- Détection de lignes complètes

### ⏳ Phase 3 - Interface utilisateur
**Objectifs** :
- Interface Pygame
- Contrôles clavier
- Affichage graphique
- Game loop principal
