# Décision technique - Spécifications de la grille

## Date : 27 juillet 2025

## Contexte
Première fonctionnalité à implémenter : affichage d'une grille vide pour le plateau de Tetris.

## Spécifications validées

### Fenêtre de jeu
- **Taille** : Plein écran automatique (utiliser `pygame.FULLSCREEN`)
- **Arrière-plan** : Noir (#000000)
- **Titre** : "Tetris"

### Grille de jeu
- **Dimensions logiques** : 10 colonnes × 20 lignes
- **Taille cellule** : 30px × 30px
- **Taille totale grille** : 300px × 600px
- **Fond des cellules** : Gris (#C0C0C0)
- **Contours des cellules** : Blanc (#FFFFFF)
- **Épaisseur contours** : 1px

### Positionnement
- **Centrage** : Grille centrée dans la fenêtre plein écran
- **Calcul position** : 
  - x = (largeur_écran - 300) / 2
  - y = (hauteur_écran - 600) / 2

## Implications techniques

### Couleurs constantes
```python
BLACK = (0, 0, 0)        # #000000
GRAY = (192, 192, 192)   # #C0C0C0  
WHITE = (255, 255, 255)  # #FFFFFF
```

### Calculs de rendu
- Position de chaque cellule : `(x_grid + col * 30, y_grid + row * 30)`
- Rectangle cellule : `pygame.Rect(x, y, 30, 30)`
- Contour : `pygame.draw.rect(surface, WHITE, rect, 1)`

## Justification des choix

1. **Plein écran** : Expérience immersive, pas de distraction
2. **30px par cellule** : Taille confortable, lisible
3. **Contours blancs** : Contraste maximal avec le gris
4. **Centrage** : Équilibre visuel sur tous les écrans

## Tests à implémenter

1. Création fenêtre plein écran
2. Calcul correct des dimensions de grille
3. Positionnement centré
4. Rendu des cellules avec bonnes couleurs
5. Affichage des contours

## Prochaines étapes

Après validation de cette grille :
1. Ajout des pièces de base
2. Système de coordonnées logiques
3. Gestion des événements clavier
