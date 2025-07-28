# Registry Pattern avec Auto-enregistrement

## 🎯 Objectif de la leçon

Comprendre le **Registry Pattern** et son implémentation en Python avec des **décorateurs** pour l'auto-enregistrement automatique.

## 📚 Contexte

### Problème initial (Factory Pattern classique)

```python
# ❌ AVANT : Couplage fort dans FabriquePieces
class FabriquePieces:
    def __init__(self):
        self._fabriques = {
            TypePiece.I: PieceI,  # ← Il faut ajouter manuellement !
            TypePiece.O: PieceO,  # ← Chaque nouvelle pièce
            TypePiece.T: PieceT,  # ← Couplage fort !
        }
```

**Problèmes identifiés** :
- 😞 Couplage fort entre Factory et classes concrètes
- 😞 Il faut modifier `FabriquePieces` pour chaque nouvelle pièce  
- 😞 Risque d'oubli lors de l'ajout de nouvelles pièces
- 😞 Violation du principe Open/Closed

## 🔧 Solution : Registry Pattern

### Architecture de la solution

```
┌─────────────────┐    utilise    ┌──────────────────┐
│  FabriquePieces │ ──────────────▶│  RegistrePieces  │
└─────────────────┘               └──────────────────┘
                                           △
                                           │ enregistrement via décorateur
                                           │
┌─────────────────┐    @piece_tetris       │
│     PieceI      │ ─────────────────────────┘
└─────────────────┘
┌─────────────────┐    @piece_tetris       │
│     PieceO      │ ─────────────────────────┘  
└─────────────────┘
┌─────────────────┐    @piece_tetris       │
│     PieceT      │ ─────────────────────────┘
└─────────────────┘
```

### 1. RegistrePieces (Registry)

```python
class RegistrePieces:
    """Registry Pattern pour l'auto-enregistrement des pièces."""
    
    _pieces_enregistrees: Dict[TypePiece, Type[Piece]] = {}
    _types_supportes: Set[TypePiece] = set()
    
    @classmethod
    def enregistrer_piece(cls, type_piece: TypePiece, classe_piece: Type[Piece]) -> None:
        """Enregistrer une pièce dans le registre."""
        cls._pieces_enregistrees[type_piece] = classe_piece
        cls._types_supportes.add(type_piece)
        print(f"🔧 Pièce enregistrée : {type_piece.value} -> {classe_piece.__name__}")
    
    @classmethod
    def obtenir_classe_piece(cls, type_piece: TypePiece) -> Type[Piece]:
        """Obtenir la classe pour un type donné."""
        if type_piece not in cls._pieces_enregistrees:
            raise ValueError(f"Type non supporté : {type_piece.value}")
        return cls._pieces_enregistrees[type_piece]
```

### 2. Décorateur @piece_tetris

```python
def piece_tetris(type_piece: TypePiece) -> Callable[[T], T]:
    """
    Décorateur pour auto-enregistrement.
    
    Usage:
        @piece_tetris(TypePiece.I)
        class PieceI(Piece):
            ...
    """
    def decorateur(classe_piece: T) -> T:
        RegistrePieces.enregistrer_piece(type_piece, classe_piece)
        return classe_piece
    
    return decorateur
```

### 3. Utilisation sur les pièces

```python
@piece_tetris(TypePiece.I)  # ← Auto-enregistrement !
class PieceI(Piece):
    """Pièce I - ligne droite."""
    # ... implémentation normale
```

## 🔄 Processus d'exécution

### Analyse étape par étape

Quand Python lit cette ligne :
```python
@piece_tetris(TypePiece.I)
class PieceI(Piece):
    ...
```

**Étape 1** : Python appelle `piece_tetris(TypePiece.I)`
- Retourne un décorateur spécialisé pour `TypePiece.I`

**Étape 2** : Python applique ce décorateur à la classe `PieceI`  
- `decorateur(PieceI)` s'exécute

**Étape 3** : Dans `decorateur()` :
- `RegistrePieces.enregistrer_piece(TypePiece.I, PieceI)`
- `return PieceI`  ← La classe reste inchangée

**Étape 4** : Python termine la définition de classe
- `PieceI` est disponible ET enregistrée automatiquement

### Démonstration pratique

```python
# ✅ APRÈS : Factory découplée
class FabriquePieces:
    def creer(self, type_piece: TypePiece) -> Piece:
        # Découverte automatique via le registre !
        classe_piece = RegistrePieces.obtenir_classe_piece(type_piece)
        return classe_piece.creer(x_spawn=5, y_spawn=0)
```

## 🎉 Avantages obtenus

### ✅ Pour le développeur
- **Simplicité** : Juste ajouter `@piece_tetris(TypeXXX)` 
- **Impossible d'oublier** : Le décorateur force l'enregistrement
- **Zéro modification** de la Factory pour nouvelles pièces

### ✅ Pour l'architecture  
- **Découplage total** : Factory ne connaît pas les classes concrètes
- **Extensibilité parfaite** : Nouvelles pièces en 2 lignes
- **Principe Open/Closed** : Ouvert à l'extension, fermé à la modification

### ✅ Pour le testing
- **Auto-discovery** : Les tests découvrent automatiquement les nouvelles pièces
- **Registry isolé** : Peut être testé indépendamment  
- **Mocks facilités** : Registry peut être mocké pour les tests

## 🧪 Code de démonstration

Voir `demo_decorateur_detaille.py` pour une démonstration interactive complète.

```bash
python demo_decorateur_detaille.py
```

## 🚀 Exemple d'extension

Pour ajouter `PieceS` maintenant :

```python
@piece_tetris(TypePiece.S)  # ← Juste ça !
class PieceS(Piece):
    """Pièce S - forme en S."""
    
    def obtenir_positions_initiales(self, x_spawn: int, y_spawn: int) -> List[Position]:
        # ... implémentation normale
```

**Et automatiquement** :
- ✅ PieceS sera dans le registre
- ✅ La fabrique pourra la créer  
- ✅ Elle sera incluse dans `creer_aleatoire()`
- ✅ Les tests l'incluront automatiquement

## 📝 Leçons apprises

1. **Registry Pattern** = Solution élégante pour le découplage
2. **Décorateurs Python** = Outil puissant pour la méta-programmation  
3. **Auto-enregistrement** = Réduit drastiquement le code boilerplate
4. **Import hooks** = Les imports Python peuvent déclencher du code
5. **Extensibilité** = Une bonne architecture rend l'extension triviale

## 🔗 Patterns connexes

- **Factory Pattern** : Utilisé par la fabrique après découverte
- **Decorator Pattern** : Implémenté avec des décorateurs Python
- **Plugin Architecture** : Registry peut servir de base pour des plugins
- **Dependency Injection** : Registry peut être injecté où nécessaire

---

> 💡 **Prochaine leçon** : Implémentation de PieceS pour démontrer la simplicité du nouveau système.
