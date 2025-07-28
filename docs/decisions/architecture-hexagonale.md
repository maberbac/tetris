# Architecture Hexagonale pour Tetris

## Date : 27 juillet 2025

## Qu'est-ce que l'architecture hexagonale ?

L'architecture hexagonale (Ports & Adapters) de Alistair Cockburn isole complètement la logique métier des détails techniques externes.

### Principe central
```
Extérieur → Port → Logique Métier → Port → Extérieur
```

## 🎮 **Architecture Hexagonale pour Tetris**

### Vue d'ensemble
```
                    ┌─────────────────────────────────────┐
                    │              ADAPTERS               │
                    │                                     │
        ┌───────────┼─────────────────────────────────────┼───────────┐
        │           │                                     │           │
        │  UI       │              PORTS                  │  Storage  │
        │ Pygame    │                                     │   JSON    │
        │ Console   │    ┌─────────────────────────────┐  │   DB      │
        │           │    │                             │  │           │
        └───────────┼────┤      DOMAINE MÉTIER         ├──┼───────────┘
                    │    │                             │  │
        ┌───────────┼────┤  - Piece                    ├──┼───────────┐
        │           │    │  - Plateau                  │  │           │
        │  Input    │    │  - MoteurJeu                │  │  Audio    │
        │ Clavier   │    │  - ServiceScore             │  │  Pygame   │
        │ Réseau    │    │  - ServiceCollision         │  │  Silent   │
        │           │    │                             │  │           │
        └───────────┼────└─────────────────────────────┘──┼───────────┘
                    │                                     │
                    │              ADAPTERS               │
                    └─────────────────────────────────────┘
```

## 🏗️ **Structure détaillée**

### Core (Domaine) - Centre de l'hexagone
```
src/
├── domaine/                    # CŒUR - Logique métier pure
│   ├── entites/
│   │   ├── piece.py           # Entité Piece (sans dépendances)
│   │   ├── plateau.py         # Entité Plateau  
│   │   ├── partie.py          # Agrégat racine
│   │   └── position.py        # Value Object
│   ├── services/
│   │   ├── service_jeu.py     # Logique principale
│   │   ├── service_collision.py
│   │   └── service_score.py
│   └── exceptions/
│       └── exceptions_jeu.py
```

### Ports - Interfaces du domaine
```
├── ports/                      # INTERFACES - Contrats
│   ├── primaires/             # Ports d'entrée (use cases)
│   │   ├── commencer_partie.py
│   │   ├── deplacer_piece.py
│   │   ├── faire_tourner_piece.py
│   │   └── obtenir_etat_jeu.py
│   └── secondaires/           # Ports de sortie (dépendances)
│       ├── affichage_port.py  # Interface affichage
│       ├── input_port.py      # Interface entrées
│       ├── audio_port.py      # Interface son
│       └── stockage_port.py   # Interface sauvegarde
```

### Adapters - Implémentations techniques
```
├── adapters/                   # IMPLÉMENTATIONS - Détails techniques
│   ├── primaires/             # Adapters d'entrée (drivers)
│   │   ├── ui_pygame/
│   │   │   ├── interface_pygame.py
│   │   │   └── gestionnaire_events.py
│   │   ├── ui_console/
│   │   │   └── interface_console.py
│   │   └── api_web/
│   │       └── controleur_web.py
│   └── secondaires/           # Adapters de sortie (driven)
│       ├── affichage/
│       │   ├── affichage_pygame.py
│       │   ├── affichage_console.py
│       │   └── affichage_web.py
│       ├── input/
│       │   ├── clavier_pygame.py
│       │   └── input_reseau.py
│       ├── audio/
│       │   ├── audio_pygame.py
│       │   └── audio_silencieux.py
│       └── stockage/
│           ├── fichier_json.py
│           └── base_donnees.py
```

## 🔌 **Exemples de Ports et Adapters**

### 1. Port d'affichage (interface)
```python
# ports/secondaires/affichage_port.py
from abc import ABC, abstractmethod
from typing import List
from domaine.entites.piece import Piece
from domaine.entites.plateau import Plateau

class AffichagePort(ABC):
    @abstractmethod
    def dessiner_plateau(self, plateau: Plateau) -> None:
        """Dessine le plateau de jeu."""
        pass
    
    @abstractmethod
    def dessiner_piece(self, piece: Piece) -> None:
        """Dessine une pièce."""
        pass
    
    @abstractmethod
    def afficher_score(self, score: int) -> None:
        """Affiche le score."""
        pass
    
    @abstractmethod
    def mettre_a_jour(self) -> None:
        """Met à jour l'affichage."""
        pass
```

### 2. Adapter Pygame (implémentation)
```python
# adapters/secondaires/affichage/affichage_pygame.py
import pygame
from ports.secondaires.affichage_port import AffichagePort
from domaine.entites.piece import Piece
from domaine.entites.plateau import Plateau

class AffichagePygame(AffichagePort):
    def __init__(self):
        pygame.init()
        self.ecran = pygame.display.set_mode((800, 600))
        self.police = pygame.font.Font(None, 36)
    
    def dessiner_plateau(self, plateau: Plateau) -> None:
        """Implémentation Pygame du dessin du plateau."""
        self.ecran.fill((0, 0, 0))  # Fond noir
        
        for y in range(plateau.hauteur):
            for x in range(plateau.largeur):
                if plateau.cellule_occupee(x, y):
                    couleur = plateau.obtenir_couleur_cellule(x, y)
                    rect = pygame.Rect(x * 30, y * 30, 30, 30)
                    pygame.draw.rect(self.ecran, couleur, rect)
                    pygame.draw.rect(self.ecran, (255, 255, 255), rect, 1)
    
    def dessiner_piece(self, piece: Piece) -> None:
        """Implémentation Pygame du dessin de pièce."""
        for bloc in piece.obtenir_blocs():
            x, y = bloc.position.x * 30, bloc.position.y * 30
            rect = pygame.Rect(x, y, 30, 30)
            pygame.draw.rect(self.ecran, piece.couleur, rect)
            pygame.draw.rect(self.ecran, (255, 255, 255), rect, 1)
    
    def afficher_score(self, score: int) -> None:
        texte = self.police.render(f"Score: {score}", True, (255, 255, 255))
        self.ecran.blit(texte, (400, 50))
    
    def mettre_a_jour(self) -> None:
        pygame.display.flip()
```

### 3. Adapter Console (alternative)
```python
# adapters/secondaires/affichage/affichage_console.py
from ports.secondaires.affichage_port import AffichagePort
from domaine.entites.piece import Piece
from domaine.entites.plateau import Plateau

class AffichageConsole(AffichagePort):
    def dessiner_plateau(self, plateau: Plateau) -> None:
        """Affichage texte du plateau."""
        print("\n" + "="*20)
        for y in range(plateau.hauteur):
            ligne = "|"
            for x in range(plateau.largeur):
                if plateau.cellule_occupee(x, y):
                    ligne += "■"
                else:
                    ligne += " "
            ligne += "|"
            print(ligne)
        print("="*20)
    
    def dessiner_piece(self, piece: Piece) -> None:
        # La pièce sera incluse dans dessiner_plateau
        pass
    
    def afficher_score(self, score: int) -> None:
        print(f"Score: {score}")
    
    def mettre_a_jour(self) -> None:
        # Pas besoin de mise à jour en console
        pass
```

### 4. Port d'entrée (use case)
```python
# ports/primaires/deplacer_piece.py
from abc import ABC, abstractmethod
from domaine.entites.position import Position

class DeplacerPiecePort(ABC):
    @abstractmethod
    def deplacer_gauche(self) -> bool:
        """Déplace la pièce vers la gauche. Retourne True si réussi."""
        pass
    
    @abstractmethod
    def deplacer_droite(self) -> bool:
        """Déplace la pièce vers la droite. Retourne True si réussi."""
        pass
    
    @abstractmethod
    def deplacer_bas(self) -> bool:
        """Déplace la pièce vers le bas. Retourne True si réussi."""
        pass
```

### 5. Service métier (implémentation du port)
```python
# domaine/services/service_jeu.py
from ports.primaires.deplacer_piece import DeplacerPiecePort
from ports.secondaires.affichage_port import AffichagePort
from domaine.entites.partie import Partie

class ServiceJeu(DeplacerPiecePort):
    def __init__(self, affichage: AffichagePort):
        self.affichage = affichage
        self.partie = Partie()
    
    def deplacer_gauche(self) -> bool:
        """Logique métier pure - pas de détails techniques."""
        piece_courante = self.partie.obtenir_piece_courante()
        if piece_courante is None:
            return False
        
        nouvelle_position = piece_courante.position.deplacer(-1, 0)
        
        if self.partie.plateau.position_valide(piece_courante, nouvelle_position):
            piece_courante.deplacer_vers(nouvelle_position)
            self.affichage.dessiner_plateau(self.partie.plateau)
            self.affichage.dessiner_piece(piece_courante)
            return True
        
        return False
```

## 🎯 **Avantages de l'architecture hexagonale pour Tetris**

### ✅ **Avantages**

1. **Isolation totale du domaine** :
   - Logique de jeu indépendante de Pygame
   - Tests sans interface graphique
   - Changement d'UI sans toucher au métier

2. **Flexibilité maximale** :
   ```python
   # Même jeu, interfaces différentes
   jeu_pygame = ServiceJeu(AffichagePygame())
   jeu_console = ServiceJeu(AffichageConsole())
   jeu_web = ServiceJeu(AffichageWeb())
   ```

3. **Testabilité parfaite** :
   ```python
   # Test sans dépendances externes
   affichage_mock = Mock(spec=AffichagePort)
   service_jeu = ServiceJeu(affichage_mock)
   
   resultat = service_jeu.deplacer_gauche()
   affichage_mock.dessiner_piece.assert_called_once()
   ```

4. **Extensibilité** :
   - Ajout de nouveaux adapters sans modifier le core
   - Support multi-plateforme facile
   - Mode multijoueur par simple ajout d'adapters

### ⚠️ **Inconvénients potentiels**

1. **Complexité initiale** :
   - Plus de fichiers et interfaces
   - Courbe d'apprentissage

2. **Over-engineering** :
   - Peut-être excessif pour un projet d'apprentissage simple

3. **Indirection** :
   - Plus de couches = debugging plus complexe

## 🤔 **Comparaison avec architecture par couches**

| Aspect | Couches | Hexagonale |
|--------|---------|------------|
| **Simplicité** | ✅ Plus simple | ⚠️ Plus complexe |
| **Isolation** | ⚠️ Partielle | ✅ Totale |
| **Testabilité** | ✅ Bonne | ✅ Excellente |
| **Flexibilité** | ⚠️ Moyenne | ✅ Maximale |
| **Apprentissage** | ✅ Facile | ⚠️ Plus difficile |

## 💡 **Ma recommandation**

Pour votre contexte (apprentissage TDD + Java background) :

### 🎯 **Commencer par couches, évoluer vers hexagonale**

1. **Phase 1** : Architecture par couches (familière)
2. **Phase 2** : Refactoring vers hexagonale (apprentissage)

Ou directement hexagonale si vous voulez maximiser l'apprentissage !

### ❓ **Questions pour vous aider à choisir :**

1. **Objectif principal** : Apprentissage ou projet rapide ?
2. **Complexité** : Préférez-vous commencer simple ou directement "à la bonne façon" ?
3. **Multiple UI** : Envisagez-vous console + pygame + web ?
4. **Apprentissage** : Voulez-vous découvrir l'architecture hexagonale ?

**Quelle approche vous attire le plus ?**
