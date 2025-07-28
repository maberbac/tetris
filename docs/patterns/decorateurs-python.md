# Décorateurs Python - Leçon Avancée

## 🎯 Objectif

Maîtriser les **décorateurs Python** à travers l'exemple concret du Registry Pattern.

## 📚 Qu'est-ce qu'un décorateur ?

Un décorateur est une fonction qui **modifie ou enrichit** une autre fonction ou classe **sans changer son code source**.

### Syntaxe de base

```python
@decorateur
def ma_fonction():
    pass

# Équivalent à :
ma_fonction = decorateur(ma_fonction)
```

## 🔧 Types de décorateurs

### 1. Décorateur simple

```python
def simple_decorateur(func):
    """Décorateur qui ajoute des logs."""
    def wrapper(*args, **kwargs):
        print(f"Appel de {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Fin de {func.__name__}")
        return result
    return wrapper

@simple_decorateur
def dire_bonjour(nom):
    print(f"Bonjour {nom}!")
```

### 2. Décorateur avec paramètres

```python
def decorateur_avec_params(message):
    """Décorateur qui accepte des paramètres."""
    def decorateur_reel(func):
        def wrapper(*args, **kwargs):
            print(f"{message}: {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorateur_reel

@decorateur_avec_params("DEBUT")
def ma_fonction():
    print("Contenu de ma fonction")
```

### 3. Décorateur de classe (notre cas !)

```python
def piece_tetris(type_piece: TypePiece):
    """Décorateur pour enregistrer automatiquement une classe."""
    def decorateur(classe_piece):
        # Enregistrer la classe dans le registre
        RegistrePieces.enregistrer_piece(type_piece, classe_piece)
        # Retourner la classe inchangée
        return classe_piece
    return decorateur
```

## 🔍 Analyse détaillée : @piece_tetris

### Code complet du décorateur

```python
from typing import TypeVar, Callable, Type

T = TypeVar('T', bound=Type[Piece])

def piece_tetris(type_piece: TypePiece) -> Callable[[T], T]:
    """
    Décorateur pour enregistrer automatiquement une pièce Tetris.
    
    Args:
        type_piece: Le type de pièce à enregistrer (TypePiece.I, etc.)
        
    Returns:
        Décorateur qui enregistre la classe et la retourne inchangée
    """
    def decorateur(classe_piece: T) -> T:
        RegistrePieces.enregistrer_piece(type_piece, classe_piece)
        return classe_piece
    
    return decorateur
```

### Analyse étape par étape

#### Étape 1 : Définition avec paramètre
```python
def piece_tetris(type_piece: TypePiece):
    # type_piece = TypePiece.I (par exemple)
```

#### Étape 2 : Fonction interne (le vrai décorateur)
```python
    def decorateur(classe_piece: T) -> T:
        # classe_piece = PieceI (la classe décorée)
        RegistrePieces.enregistrer_piece(type_piece, classe_piece)
        return classe_piece  # ← IMPORTANT : retourner la classe
```

#### Étape 3 : Retour du décorateur
```python
    return decorateur  # ← Retourne la fonction interne
```

### Utilisation pratique

```python
@piece_tetris(TypePiece.I)  # ← 1. Appel avec paramètre
class PieceI(Piece):        # ← 2. Application à la classe
    def __init__(self):
        pass
```

**Ce qui se passe** :
1. `piece_tetris(TypePiece.I)` → retourne `decorateur`
2. `decorateur(PieceI)` → enregistre PieceI et retourne PieceI
3. `PieceI` est maintenant enregistrée ET utilisable normalement

## 🧪 Expérimentation interactive

### Test simple

```python
# Décorateur de test
def debug_classe(classe):
    print(f"🔍 Classe décorée : {classe.__name__}")
    return classe

@debug_classe
class MaClasse:
    pass

# Résultat : "🔍 Classe décorée : MaClasse"
```

### Test avec paramètres

```python
def debug_avec_message(message):
    def decorateur(classe):
        print(f"{message} : {classe.__name__}")
        return classe
    return decorateur

@debug_avec_message("NOUVELLE CLASSE")
class AutreClasse:
    pass

# Résultat : "NOUVELLE CLASSE : AutreClasse"
```

## 🎯 Patterns avancés avec les décorateurs

### 1. Décorateur qui modifie la classe

```python
def ajouter_methode(classe):
    """Ajoute une méthode à la classe."""
    def nouvelle_methode(self):
        return f"Méthode ajoutée à {self.__class__.__name__}"
    
    classe.methode_ajoutee = nouvelle_methode
    return classe

@ajouter_methode
class MaClasse:
    pass

obj = MaClasse()
print(obj.methode_ajoutee())  # "Méthode ajoutée à MaClasse"
```

### 2. Décorateur qui enregistre dans un registre

```python
# Notre pattern exact !
REGISTRE_GLOBAL = {}

def enregistrer(nom):
    def decorateur(classe):
        REGISTRE_GLOBAL[nom] = classe
        print(f"✅ {nom} → {classe.__name__}")
        return classe
    return decorateur

@enregistrer("piece_speciale")
class PieceSpeciale:
    pass

print(REGISTRE_GLOBAL)  # {'piece_speciale': <class 'PieceSpeciale'>}
```

### 3. Décorateur de validation

```python
def valider_piece(type_attendu):
    def decorateur(classe):
        # Validation au moment de la décoration
        if not hasattr(classe, 'type_piece'):
            raise ValueError(f"{classe.__name__} doit avoir type_piece")
        return classe
    return decorateur

@valider_piece(TypePiece.I)
class PieceValide:
    type_piece = TypePiece.I  # ✅ OK

# @valider_piece(TypePiece.O)  # ❌ Lèverait une exception
# class PieceInvalide:
#     pass
```

## 🚀 Avantages des décorateurs

### ✅ Lisibilité
```python
@piece_tetris(TypePiece.S)
class PieceS(Piece):
    pass
# ← Intention claire dès la définition
```

### ✅ Réutilisabilité  
```python
@piece_tetris(TypePiece.Z)
class PieceZ(Piece):
    pass

@piece_tetris(TypePiece.J)  
class PieceJ(Piece):
    pass
# ← Même décorateur, différents paramètres
```

### ✅ Séparation des préoccupations
- **Classe** : Focus sur la logique métier
- **Décorateur** : Focus sur l'enregistrement
- **Registre** : Focus sur la gestion des types

## 🔗 Décorateurs dans Python standard

### @property
```python
class Position:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self._x
```

### @staticmethod et @classmethod
```python
class Piece:
    @staticmethod
    def valider_position(pos):
        return pos.x >= 0
    
    @classmethod
    def creer(cls, x, y):
        return cls(Position(x, y))
```

### @dataclass
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Position:
    x: int
    y: int
```

## 📝 Bonnes pratiques

### 1. ✅ Toujours retourner l'objet décoré
```python
def bon_decorateur(classe):
    # ... logique ...
    return classe  # ← IMPORTANT
```

### 2. ✅ Utiliser functools.wraps pour préserver les métadonnées
```python
from functools import wraps

def decorateur_fonction(func):
    @wraps(func)  # ← Préserve __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### 3. ✅ Type hints pour les décorateurs de classe
```python
from typing import TypeVar, Type

T = TypeVar('T')

def decorateur_type(classe: Type[T]) -> Type[T]:
    return classe
```

## 🎯 Exercice pratique

Créez un décorateur `@singleton` qui garantit qu'une classe n'a qu'une seule instance :

```python
def singleton(classe):
    instances = {}
    def get_instance(*args, **kwargs):
        if classe not in instances:
            instances[classe] = classe(*args, **kwargs)
        return instances[classe]
    return get_instance

@singleton
class Database:
    def __init__(self):
        print("Création de la DB")

db1 = Database()  # "Création de la DB"
db2 = Database()  # Rien (même instance)
print(db1 is db2)  # True
```

## 🔗 Liens avec notre architecture

Dans notre projet Tetris, les décorateurs nous permettent :

1. **Auto-enregistrement** : `@piece_tetris(TypePiece.X)`
2. **Configuration déclarative** : Le type est déclaré avec la classe
3. **Extensibilité** : Nouvelles pièces sans modification du core
4. **Testabilité** : Registry peut être mocké/réinitialisé facilement

---

> 💡 **Prochaine leçon** : Implémentation de PieceS avec le nouveau système d'auto-enregistrement.
