# Analyse d'architecture : Héritage vs Composition pour les pièces Tetris

## Date : 27 juillet 2025

## 🎯 **Question architecturale : Héritage ou Composition ?**

### **Option 1 : Héritage avec classes spécialisées**

#### **Avantages :**
- ✅ **Polymorphisme naturel** : Chaque pièce a ses propres méthodes
- ✅ **Comportements spécifiques** : `PieceO.tourner()` peut ne rien faire (carré)
- ✅ **Factory Pattern** : `PieceFactory.creer(TypePiece.I)` → `PieceI`
- ✅ **Extensibilité** : Nouvelles pièces = nouvelles classes
- ✅ **Principe Open/Closed** : Fermer pour modification, ouvert pour extension

#### **Inconvénients :**
- ❌ **Plus de classes** : 7 classes au lieu d'1
- ❌ **Duplication possible** : Code commun dans classe abstraite
- ❌ **Complexité** : Plus de fichiers, plus de structure

### **Option 2 : Composition avec Enum (actuel)**

#### **Avantages :**
- ✅ **Simplicité** : Une seule classe `Piece`
- ✅ **Données centralisées** : Toutes les formes dans un endroit
- ✅ **Moins de code** : Moins de classes à maintenir
- ✅ **Configuration** : Formes définies par des données

#### **Inconvénients :**
- ❌ **Switch/Case** : `if type_piece == TypePiece.I: ...`
- ❌ **Violation SRP** : Une classe fait tout
- ❌ **Extension difficile** : Ajouter un type = modifier la classe

## 🧠 **Analyse Domain-Driven Design**

### **Question fondamentale : "Les types de pièces sont-ils des concepts métier distincts ?"**

**Arguments pour l'héritage :**
- Une pièce I se **comporte différemment** d'une pièce O
- Rotation de O = no-op, rotation de I = 90°/180°
- Création : positions initiales différentes
- **Chaque type a sa propre logique métier**

**Arguments pour la composition :**
- Toutes les pièces **partagent les mêmes opérations** : déplacer, tourner, tomber
- Seules les **données changent** (forme, positions)
- **Même interface, différentes configurations**

## 🎮 **Impact concret sur Tetris**

### **Avec héritage : Comportements spécialisés**

```python
# Chaque pièce définit sa propre logique
class PieceI(Piece):
    def tourner(self) -> None:
        # Logique spécifique rotation I (horizontal ↔ vertical)
        if self._est_horizontale():
            self._devenir_verticale()
        else:
            self._devenir_horizontale()

class PieceO(Piece):
    def tourner(self) -> None:
        # Carré : rotation = rien !
        pass

class PieceT(Piece):
    def tourner(self) -> None:
        # T : 4 orientations possibles
        self._rotation_4_etats()

# Usage polymorphe
def faire_tourner_piece(piece: Piece):
    piece.tourner()  # Chaque type fait sa propre logique !
```

### **Avec composition : Logique centralisée**

```python
class Piece:
    def tourner(self) -> None:
        if self.type_piece == TypePiece.O:
            return  # Carré ne tourne pas
        elif self.type_piece == TypePiece.I:
            self._rotation_ligne()
        elif self.type_piece == TypePiece.T:
            self._rotation_4_etats()
        # ... etc pour chaque type

# Toute la logique dans une méthode
```

## 🏗️ **Recommandation architecturale**

### **Pour Tetris : JE RECOMMANDE L'HÉRITAGE ! 🎯**

#### **Pourquoi ?**

1. **Métier distinct** : Chaque pièce a sa logique de rotation unique
2. **Factory naturel** : `PieceFactory.creer_aleatoire()`
3. **Tests isolés** : `TestPieceI`, `TestPieceO`, etc.
4. **Extensibilité** : Nouvelles pièces sans toucher l'existant
5. **Principe de responsabilité unique** : Une classe = un type de pièce

#### **Structure proposée :**

```
src/domaine/entites/
├── piece.py              # Classe abstraite Piece
├── pieces/
│   ├── __init__.py
│   ├── piece_i.py        # PieceI hérite de Piece
│   ├── piece_o.py        # PieceO hérite de Piece
│   ├── piece_t.py        # PieceT hérite de Piece
│   ├── piece_s.py        # etc...
│   ├── piece_z.py
│   ├── piece_j.py
│   └── piece_l.py
└── position.py           # Value Object (inchangé)
```

#### **Avantages concrets :**
- **TDD par pièce** : Tests focalisés sur chaque comportement
- **Maintenance** : Bug sur rotation T ? → Seule `PieceT` affectée
- **Lisibilité** : `piece.tourner()` au lieu de `piece.tourner(piece.type_piece)`
- **Performance** : Pas de switch/case à chaque opération

## 💡 **Conclusion**

**L'héritage est justifié ici car :**
1. **Comportements vraiment différents** (pas juste des données)
2. **Logique métier spécialisée** par type
3. **Architecture hexagonale** favorise les concepts métier clairs
4. **TDD** plus facile avec classes spécialisées

**La composition serait mieux si :**
- Toutes les pièces avaient le même comportement
- Seules les formes/données changeaient
- Le jeu était très simple

### **Prochaine étape :**
Refactoriser vers l'héritage avec une approche TDD ?
