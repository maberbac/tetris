# Index des Leçons Apprises - Projet Tetris

📚 **Historique complet des leçons d'architecture et patterns** apprises lors du développement.

## 🗓️ Chronologie des leçons

### 📅 Leçon 1 : Architecture Hexagonale & TDD (Séance 1)
**Fichier** : [architecture/architecture-hexagonale.md](architecture/architecture-hexagonale.md)
- **Concepts** : Domain-Driven Design, couches séparées
- **TDD** : Méthodologie RED-GREEN-REFACTOR  
- **Value Objects** : Position immutable avec @dataclass(frozen=True)
- **Résultat** : 5 tests Position ✅

### 📅 Leçon 2 : Héritage & Polymorphisme (Séance 2)
**Fichier** : [architecture/heritage-polymorphisme.md](architecture/heritage-polymorphisme.md)  
- **Concepts** : Classe abstraite, Template Method Pattern
- **Python** : ABC (Abstract Base Classes)
- **TDD** : PieceI avec rotation horizontale/verticale
- **Résultat** : +5 tests PieceI ✅

### 📅 Leçon 3 : Polymorphisme en action (Séance 3)
**Fichier** : [patterns/polymorphisme-pratique.md](patterns/polymorphisme-pratique.md)
- **Concepts** : PieceO avec no-op rotation
- **Design** : Interface commune, comportements différents  
- **Tests** : Démonstration polymorphique avec 2 pièces
- **Résultat** : +3 tests PieceO + 2 tests polymorphisme ✅

### 📅 Leçon 4 : Factory Pattern classique (Séance 4)
**Fichier** : [patterns/factory-pattern.md](patterns/factory-pattern.md)
- **Concepts** : Centralisation de la création d'objets
- **Design** : Mapping TypePiece → Classe concrète
- **TDD** : Factory avec création par type et aléatoire
- **Résultat** : +4 tests FabriquePieces ✅

### 📅 Leçon 5 : Registry Pattern & Décorateurs (Séance 5) ⭐ **NOUVELLE**
**Fichier** : [patterns/registry-pattern.md](patterns/registry-pattern.md)
- **Concepts** : Auto-enregistrement, découplage total
- **Python** : Décorateurs avancés, méta-programmation
- **Refactoring** : Migration Factory classique → Registry Pattern
- **Résultat** : +4 tests Registry, 0 régression ✅

### 📅 Leçon 6 : Décorateurs Python (Séance 5) ⭐ **NOUVELLE**  
**Fichier** : [patterns/decorateurs-python.md](patterns/decorateurs-python.md)
- **Concepts** : @piece_tetris(TypePiece.X), auto-enregistrement
- **Python** : Décorateurs avec paramètres, Type hints avancés
- **Demo** : `demo_decorateur_detaille.py`
- **Résultat** : Architecture extensible sans modification ✅

## 📊 Progression des métriques

| Séance | Tests Total | Nouveaux Tests | Architecture | Patterns Utilisés |
|--------|-------------|----------------|--------------|-------------------|
| 1      | 5           | +5             | Hexagonale   | Value Object      |
| 2      | 10          | +5             | + Héritage   | + ABC, Template   |
| 3      | 15          | +5             | + Polymorphisme | + No-op Pattern |
| 4      | 19          | +4             | + Factory    | + Factory Pattern |
| 5      | 27          | +8             | + Registry   | + Registry, Decorator |

## 🎯 Concepts maîtrisés

### 🏗️ Architecture
- ✅ **Architecture Hexagonale** : Séparation domain/ports/adapters
- ✅ **Domain-Driven Design** : Value Objects vs Entities  
- ✅ **Couches séparées** : Tests isolés par couche
- ✅ **Inversions de dépendances** : Registry vs Factory directe

### 🎨 Design Patterns
- ✅ **Value Object Pattern** : Position immutable
- ✅ **Template Method Pattern** : Piece abstraite  
- ✅ **Factory Pattern** : Création centralisée
- ✅ **Registry Pattern** : Auto-discovery et enregistrement
- ✅ **Decorator Pattern** : @piece_tetris pour méta-programmation

### 🐍 Python Avancé
- ✅ **@dataclass(frozen=True)** : Value Objects immutables
- ✅ **ABC (Abstract Base Classes)** : Classes abstraites
- ✅ **Type Hints avancés** : TypeVar, Callable, Type[T]
- ✅ **Décorateurs avec paramètres** : @decorator(param)
- ✅ **Import hooks** : Auto-enregistrement via imports

### 🧪 TDD & Testing
- ✅ **RED-GREEN-REFACTOR** : Cycle TDD strict
- ✅ **Tests de régression** : Maintien 100% après refactoring
- ✅ **Test runner personnalisé** : Script de test complet
- ✅ **Tests isolés** : Chaque composant testé séparément

## 🚀 Prochaines leçons prévues

### 📅 Leçon 7 : Extension avec nouvelles pièces (Prochaine)
- **Objectif** : Démontrer la simplicité du nouveau système
- **Implémentation** : PieceS avec @piece_tetris(TypePiece.S)
- **Concepts** : Extension sans modification (Open/Closed)

### 📅 Leçon 8 : Patterns de forme complexes
- **Objectif** : Pièces avec rotations asymétriques (S, Z, J, L)
- **Concepts** : Patterns géométriques, symétries

### 📅 Leçon 9 : Entity vs Value Object avancé  
- **Objectif** : Plateau comme Entity avec state mutable
- **Concepts** : Gestion d'état, détection de lignes complètes

### 📅 Leçon 10 : Ports & Adapters
- **Objectif** : Interfaces pour UI, persistence, etc.
- **Concepts** : Inversion of Control, Dependency Injection

## 📁 Structure de documentation

```
docs/
├── README.md                    # Index principal
├── TEMPLATE_LECON.md           # Template pour nouvelles leçons
├── INDEX_LECONS.md             # Ce fichier
├── architecture/               # Leçons d'architecture
│   ├── architecture-hexagonale.md
│   ├── heritage-polymorphisme.md
│   └── value-objects-entities.md
├── patterns/                   # Design patterns
│   ├── registry-pattern.md     ⭐ NOUVEAU
│   ├── decorateurs-python.md   ⭐ NOUVEAU  
│   ├── factory-pattern.md
│   └── template-method.md
└── tdd/                       # Méthodologie TDD
    ├── methodologie-tdd.md
    └── red-green-refactor.md
```

## 🎓 Objectifs pédagogiques atteints

### 🎯 Niveau Débutant → Intermédiaire
- [x] Comprendre l'architecture en couches
- [x] Maîtriser TDD avec RED-GREEN-REFACTOR
- [x] Utiliser l'héritage et le polymorphisme correctement

### 🎯 Niveau Intermédiaire → Avancé  
- [x] Implémenter des design patterns complexes
- [x] Refactoring sans casser les tests existants
- [x] Méta-programmation avec décorateurs Python

### 🎯 Niveau Avancé → Expert
- [ ] Architecture complète avec Ports & Adapters
- [ ] Patterns de persistence et UI découplées
- [ ] Performance et optimisations

---

> 💡 **Note** : Chaque leçon s'appuie sur les précédentes pour construire progressivement une architecture robuste et extensible.
