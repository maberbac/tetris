# Notes d'apprentissage - Configuration initiale

## Choix techniques expliqués

### 1. Architecture hybride (OOP + MVC + Observer + Listener)

**Pourquoi cette combinaison ?**
- **OOP** : Encapsulation des données et comportements (pièces, plateau)
- **MVC** : Séparation claire des responsabilités
  - **Model** : Logique de jeu (plateau, pièces, score)
  - **View** : Affichage Pygame
  - **Controller** : Gestion des événements et coordination
- **Observer** : Communication découplée entre composants
- **Listener** : Gestion des entrées clavier

### 2. Approche TDD pour débutants

**Avantages pour l'apprentissage :**
- Force à réfléchir aux spécifications avant le code
- Tests servent de documentation vivante
- Confiance dans les refactorings
- Détection rapide des régressions

**Cycle Red-Green-Refactor expliqué :**
1. **Red** : Test qui échoue (définit ce qu'on veut)
2. **Green** : Code minimal qui marche (fait passer le test)
3. **Refactor** : Améliore sans casser (tests restent verts)

### 3. unittest vs pytest

**unittest** (standard Python) :
```python
import unittest

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
    
    def test_board_creation(self):
        self.assertEqual(self.board.width, 10)
```

**pytest** (plus moderne) :
```python
import pytest

def test_board_creation():
    board = Board()
    assert board.width == 10
```

**Différences clés :**
- pytest : syntaxe plus simple, fixtures puissantes
- unittest : plus verbeux mais standard Python

## Concepts Python importants pour notre projet

### 1. Properties et getters/setters
```python
class Piece:
    def __init__(self):
        self._x = 0
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        if 0 <= value < 10:  # Validation
            self._x = value
```

### 2. Enum pour les types de pièces
```python
from enum import Enum

class PieceType(Enum):
    I = "I"
    O = "O"
    T = "T"
    # etc.
```

### 3. Dataclasses pour structures simples
```python
from dataclasses import dataclass

@dataclass
class Position:
    x: int
    y: int
```

## Concepts de game development

### 1. Game Loop (Boucle de jeu)
```
while running:
    1. Handle Events (input)
    2. Update Game State
    3. Render Graphics
    4. Control Frame Rate
```

### 2. Delta Time
- Temps écoulé depuis la dernière frame
- Permet un jeu fluide indépendant du framerate

### 3. State Management
- États du jeu : Menu, Playing, Paused, GameOver
- Transitions entre états

### 4. Event System
- Pattern Observer pour découpler les composants
- Exemple : Ligne complétée → Événement → Score mis à jour
