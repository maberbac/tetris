# Guide de développement - Tetris Python

Ce document sert de guide technique pour comprendre l'architecture et l'implémentation du jeu Tetris en Python.

## Architecture du projet

### Structure des fichiers
```
tetris/
├── tetris.py          # Fichier principal du jeu
├── jeu.py             # Logique principale du jeu
├── pieces.py          # Définition des tétrominos
├── plateau.py         # Gestion du plateau de jeu
├── utilitaires.py     # Fonctions utilitaires
├── constantes.py      # Constantes du jeu
├── affichage.py       # Système d'affichage
└── assets/            # Ressources (sons, images)
```

## Composants principaux

### 1. Système de coordonnées
- Origine (0,0) en haut à gauche
- X augmente vers la droite
- Y augmente vers le bas
- Grille de 10 colonnes × 20 lignes

### 2. Tétrominos (Pièces)
Les 7 pièces classiques :
- **I** : Ligne droite (4 blocs)
- **O** : Carré (2×2 blocs)
- **T** : Forme en T
- **S** : Forme en S
- **Z** : Forme en Z inversé
- **J** : Forme en L inversé
- **L** : Forme en L

### 3. États des pièces
- Position (x, y)
- Rotation (0°, 90°, 180°, 270°)
- Type de pièce
- Couleur

### 4. Mécaniques de jeu

#### Déplacement
- Gauche/Droite : Déplacement horizontal
- Bas : Chute accélérée
- Rotation : Pivotement de 90° dans le sens horaire

#### Détection de collision
- Vérification des limites du plateau
- Vérification des blocs déjà placés
- Validation avant chaque mouvement

#### Suppression de lignes
- Détection des lignes complètes
- Animation de suppression
- Calcul du score selon le nombre de lignes

### 5. Système de score
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
