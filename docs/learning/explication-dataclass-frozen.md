# Explication détaillée : @dataclass(frozen=True)

## Date : 27 juillet 2025

## 🎯 **Qu'est-ce que @dataclass(frozen=True) ?**

### **@dataclass** - Le décorateur Python moderne

```python
from dataclasses import dataclass

@dataclass
class Position:
    x: int
    y: int
```

**Ce que fait @dataclass automatiquement :**
1. **Génère `__init__()`** automatiquement
2. **Génère `__repr__()`** pour l'affichage
3. **Génère `__eq__()`** pour les comparaisons
4. **Génère `__hash__()`** (si frozen=True)

### **frozen=True** - L'immutabilité

```python
@dataclass(frozen=True)
class Position:
    x: int
    y: int
```

**Ce que fait frozen=True :**
- Rend la classe **immutable** (impossible à modifier après création)
- Génère automatiquement `__hash__()` 
- Bloque toute tentative de modification des attributs

## 🔍 **Comparaison : Avec et sans @dataclass**

### **SANS @dataclass (Code traditionnel)**
```python
class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Position(x={self.x}, y={self.y})"
    
    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    # Pour l'immutabilité, il faudrait surcharger __setattr__
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError("Position is immutable")
        super().__setattr__(name, value)
```

### **AVEC @dataclass(frozen=True) (Code moderne)**
```python
@dataclass(frozen=True)
class Position:
    x: int
    y: int
```

**Résultat identique avec 90% moins de code !**

## 🧪 **Démonstration pratique**

### **1. Création et affichage automatiques**
```python
# Création
pos = Position(5, 10)
print(pos)  # Position(x=5, y=10) <- __repr__ automatique

# __init__ généré automatiquement :
# def __init__(self, x: int, y: int):
#     self.x = x
#     self.y = y
```

### **2. Égalité par valeur automatique**
```python
pos1 = Position(5, 10)
pos2 = Position(5, 10)
pos3 = Position(3, 7)

print(pos1 == pos2)  # True <- __eq__ automatique
print(pos1 == pos3)  # False
print(pos1 is pos2)  # False (objets différents, mais valeurs égales)
```

### **3. Immutabilité avec frozen=True**
```python
pos = Position(5, 10)

# Tentative de modification
try:
    pos.x = 20  # ❌ ERREUR !
except AttributeError as e:
    print(f"Erreur : {e}")  # "cannot assign to field 'x'"

# La seule façon de "changer" : créer une nouvelle instance
nouvelle_pos = Position(pos.x + 1, pos.y - 1)  # ✅ OK
print(nouvelle_pos)  # Position(x=6, y=9)
```

### **4. Hashable automatiquement (grâce à frozen=True)**
```python
pos1 = Position(5, 10)
pos2 = Position(5, 10)

# Peut être utilisé comme clé de dictionnaire
positions_visitees = {pos1: "première visite"}
positions_visitees[pos2] = "deuxième visite"

print(len(positions_visitees))  # 1 (même hash car mêmes valeurs)
```

## 🎮 **Pourquoi c'est parfait pour Tetris ?**

### **1. Positions de blocs**
```python
# Les blocs d'une pièce ne bougent pas individuellement
bloc_1 = Position(5, 10)
bloc_2 = Position(6, 10)
bloc_3 = Position(7, 10)

# Si on veut "déplacer" la pièce, on crée de nouvelles positions
nouvelle_piece = [
    bloc.deplacer(0, 1)  # Chute d'une ligne
    for bloc in [bloc_1, bloc_2, bloc_3]
]
```

### **2. Cache et optimisations**
```python
# Grâce à __hash__, on peut mettre en cache
positions_calculees = {}

def calculer_collision(position: Position) -> bool:
    if position in positions_calculees:
        return positions_calculees[position]
    
    resultat = # ... calcul complexe
    positions_calculees[position] = resultat
    return resultat
```

### **3. Sécurité et prédictabilité**
```python
def deplacer_piece(piece_positions: List[Position], dx: int, dy: int):
    # Garantie : les positions originales ne changeront JAMAIS
    return [pos.deplacer(dx, dy) for pos in piece_positions]

# Aucun risque d'effets de bord !
```

## 🔧 **Options de @dataclass expliquées**

```python
@dataclass(
    frozen=True,     # Immutable (recommandé pour Value Objects)
    order=True,      # Génère __lt__, __le__, __gt__, __ge__
    slots=True,      # Optimisation mémoire (Python 3.10+)
    kw_only=True     # Force l'utilisation de mots-clés
)
class Position:
    x: int
    y: int
```

### **frozen=True vs frozen=False**
```python
# Mutable (par défaut)
@dataclass
class PositionMutable:
    x: int
    y: int

pos = PositionMutable(5, 10)
pos.x = 20  # ✅ OK, mais dangereux !

# Immutable (recommandé)
@dataclass(frozen=True)
class PositionImmutable:
    x: int
    y: int

pos = PositionImmutable(5, 10)
pos.x = 20  # ❌ AttributeError
```

## 💡 **Conseils pour Tetris**

### **1. Utilisez frozen=True pour Value Objects**
```python
@dataclass(frozen=True)
class Position: ...       # ✅ Value Object

@dataclass(frozen=True)
class Couleur: ...        # ✅ Value Object

@dataclass(frozen=True)
class Dimension: ...      # ✅ Value Object
```

### **2. N'utilisez PAS frozen=True pour les Entités**
```python
@dataclass  # Pas frozen !
class Piece:              # ❌ Entité, peut changer d'état
    type_piece: TypePiece
    positions: List[Position]
    rotation: int = 0
    
    def tourner(self):
        self.rotation = (self.rotation + 90) % 360  # ✅ Modification OK
```

## 🎯 **Résumé**

### **@dataclass(frozen=True) donne :**
- ✅ **Moins de code** (90% en moins)
- ✅ **Immutabilité** automatique
- ✅ **Égalité par valeur** automatique
- ✅ **Hashable** (utilisable en dict/set)
- ✅ **Représentation** lisible automatique
- ✅ **Type hints** intégrés

### **Parfait pour :**
- Value Objects (Position, Couleur, Dimension)
- Données immutables
- Cache et optimisations
- Sécurité et prédictibilité

**C'est pourquoi Position utilise @dataclass(frozen=True) : c'est un Value Object parfait !** 🎯
