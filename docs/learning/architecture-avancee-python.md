# Concepts Python avancés pour l'architecture

## Architecture par couches et TDD

### 1. Gestion des imports avec __init__.py

```python
# src/entites/__init__.py
from .piece import Piece
from .plateau import Plateau
from .position import Position

# Permet d'importer comme :
# from src.entites import Piece, Plateau
```

### 2. Abstract Base Classes (ABC) pour les interfaces

```python
from abc import ABC, abstractmethod

class RenduAbstrait(ABC):
    @abstractmethod
    def dessiner_piece(self, piece: Piece):
        pass
    
    @abstractmethod
    def dessiner_plateau(self, plateau: Plateau):
        pass

# Force l'implémentation dans les classes dérivées
class AffichagePygame(RenduAbstrait):
    def dessiner_piece(self, piece: Piece):
        # Implémentation obligatoire
        pass
```

### 3. Dependency Injection pour TDD

```python
class MoteurJeu:
    def __init__(self, plateau: Plateau, affichage: RenduAbstrait):
        self.plateau = plateau
        self.affichage = affichage
    
    def jouer_tour(self):
        # Utilise l'abstraction, pas l'implémentation
        self.affichage.dessiner_plateau(self.plateau)

# Pour les tests, on peut injecter un mock
class AffichageMock(RenduAbstrait):
    def __init__(self):
        self.appels_dessiner = []
    
    def dessiner_piece(self, piece):
        self.appels_dessiner.append(('piece', piece))
```

### 4. Dataclasses pour les entités simples

```python
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)  # Immutable
class Position:
    x: int
    y: int
    
    def deplacer(self, dx: int, dy: int) -> 'Position':
        return Position(self.x + dx, self.y + dy)

@dataclass
class ConfigurationJeu:
    largeur_plateau: int = 10
    hauteur_plateau: int = 20
    vitesse_chute: float = 1.0
```

### 5. Enum pour les types de pièces

```python
from enum import Enum, auto

class TypePiece(Enum):
    I = auto()
    O = auto()
    T = auto()
    S = auto()
    Z = auto()
    J = auto()
    L = auto()

# Utilisation type-safe
piece = Piece(TypePiece.T, Position(5, 0))
```

### 6. Pattern Observer pour les événements

```python
from typing import List, Callable

class Observable:
    def __init__(self):
        self._observateurs: List[Callable] = []
    
    def ajouter_observateur(self, observateur: Callable):
        self._observateurs.append(observateur)
    
    def notifier(self, evenement):
        for observateur in self._observateurs:
            observateur(evenement)

class MoteurJeu(Observable):
    def ligne_completee(self, numero_ligne: int):
        self.notifier(('ligne_completee', numero_ligne))
```

### 7. Context Manager pour les ressources

```python
class GestionnaireAffichage:
    def __enter__(self):
        pygame.init()
        self.ecran = pygame.display.set_mode((800, 600))
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.quit()

# Utilisation
with GestionnaireAffichage() as affichage:
    # Le cleanup est automatique
    affichage.dessiner_grille()
```

## Patterns pour Game Development

### 1. State Pattern pour les états du jeu

```python
class EtatJeu(ABC):
    @abstractmethod
    def traiter_input(self, input_):
        pass
    
    @abstractmethod
    def mettre_a_jour(self, dt: float):
        pass

class EtatEnJeu(EtatJeu):
    def traiter_input(self, input_):
        if input_ == 'pause':
            return EtatPause()
        # Traiter mouvement pièce
        
class EtatPause(EtatJeu):
    def traiter_input(self, input_):
        if input_ == 'pause':
            return EtatEnJeu()
```

### 2. Component Pattern pour les entités

```python
class Composant(ABC):
    pass

class ComposantPosition(Composant):
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

class ComposantRendu(Composant):
    def __init__(self, couleur: Tuple[int, int, int]):
        self.couleur = couleur

class Entite:
    def __init__(self):
        self.composants = {}
    
    def ajouter_composant(self, composant: Composant):
        self.composants[type(composant)] = composant
    
    def obtenir_composant(self, type_composant):
        return self.composants.get(type_composant)
```

## Conseils pour TDD avec cette architecture

### 1. Tests de l'extérieur vers l'intérieur
```python
# Commencer par tester l'interface publique
def test_piece_peut_se_deplacer_a_droite():
    piece = Piece(TypePiece.I, Position(5, 0))
    piece_deplacee = piece.deplacer_droite()
    assert piece_deplacee.position.x == 6
```

### 2. Mock des dépendances externes
```python
@patch('pygame.display.set_mode')
def test_affichage_initialise_pygame(mock_set_mode):
    affichage = Affichage()
    mock_set_mode.assert_called_once()
```

### 3. Builders pour les tests
```python
class ConstructeurPiece:
    def __init__(self):
        self._type = TypePiece.I
        self._position = Position(0, 0)
    
    def de_type(self, type_piece: TypePiece):
        self._type = type_piece
        return self
    
    def a_position(self, x: int, y: int):
        self._position = Position(x, y)
        return self
    
    def construire(self):
        return Piece(self._type, self._position)

# Utilisation en test
piece = (ConstructeurPiece()
         .de_type(TypePiece.T)
         .a_position(5, 10)
         .construire())
```
