# Tetris - Apprentissage Architecture & Patterns 🎓

Un projet **pédagogique** pour apprendre l'**architecture logicielle** et les **design patterns** à travers le développement d'un jeu Tetris en Python.

> 🎯 **Objectif** : Maîtriser l'architecture hexagonale, TDD, et les patterns avancés à travers un projet concret.

## 📚 Documentation & Leçons

### 🎓 Leçons d'architecture disponibles

Toute la progression pédagogique est documentée dans [`docs/`](docs/) :

- 📖 **[Guide complet](docs/README.md)** : Vue d'ensemble et table des matières
- 📋 **[Index des leçons](docs/INDEX_LECONS.md)** : Chronologie complète des apprentissages
- 🔧 **[Registry Pattern](docs/patterns/registry-pattern.md)** : Auto-enregistrement avec décorateurs ⭐ **NOUVEAU**
- 🐍 **[Décorateurs Python](docs/patterns/decorateurs-python.md)** : Méta-programmation avancée ⭐ **NOUVEAU**

### 🎯 Concepts maîtrisés

- ✅ **Architecture Hexagonale** avec Domain-Driven Design
- ✅ **TDD** strict avec cycle RED-GREEN-REFACTOR  
- ✅ **Design Patterns** : Registry, Factory, Template Method, Decorator
- ✅ **Python Avancé** : ABC, Décorateurs, Type hints, Dataclasses

## 🧪 Tests & Qualité

```bash
# Exécuter tous les tests (27 tests, 100% de réussite)
python test_runner.py

# Tests spécifiques  
python -m unittest tests.test_domaine.test_entites.test_pieces.test_piece_t -v

# Démonstration des patterns
python demo_decorateur_detaille.py
```

**Métriques actuelles** :
- **27/27 tests** passent (100% ✅)
- **5+ design patterns** implémentés
- **Architecture hexagonale** complète pour le domaine
- **0 régression** lors des refactorings

## 🏗️ Architecture

```
src/
├── domaine/                    # 🎯 Couche domaine (logique métier)
│   └── entites/
│       ├── position.py         # Value Object immutable
│       ├── piece.py            # Classe abstraite (ABC)
│       ├── pieces/             # Pièces concrètes avec @piece_tetris
│       │   ├── piece_i.py      # Ligne droite (2 orientations)
│       │   ├── piece_o.py      # Carré (no-op rotation)
│       │   └── piece_t.py      # T-shape (4 orientations)
│       └── fabriques/          # Factory & Registry Patterns
│           ├── registre_pieces.py    # Auto-enregistrement
│           └── fabrique_pieces.py    # Factory refactorisée
├── ports/                      # 🔌 Interfaces (futures)
└── adapters/                   # 🔧 Implémentations (futures)

tests/                          # 🧪 Tests par couche
├── test_domaine/
│   └── test_entites/
│       ├── test_position.py         # 5 tests ✅
│       ├── test_pieces/             # 14 tests ✅  
│       └── test_fabriques/          # 8 tests ✅
└── test_runner.py              # Runner personnalisé
```

## 🚀 Progression du projet

### ✅ Phase 1-3 : Fondations (TERMINÉES)
- Value Object Position avec TDD
- Pièces I, O, T avec héritage et polymorphisme  
- Factory Pattern classique

### ✅ Phase 4 : Registry Pattern (TERMINÉE) ⭐ **NOUVEAU**
- Auto-enregistrement avec décorateurs Python
- Refactoring sans régression (27/27 tests ✅)
- Architecture extensible pour nouvelles pièces

### 🔄 Phase 5 : Pièces restantes (EN COURS)
- PieceS, PieceZ, PieceJ, PieceL avec le nouveau système
- Démonstration de l'extensibilité

### ⏳ Phase 6 : Plateau & Logique (FUTURE)  
- Plateau Entity avec détection de lignes
- Ports & Adapters (UI, persistence)

## 📖 Pour les étudiants

Ce projet est conçu comme un **parcours d'apprentissage progressif** :

1. **Commencez par** [`docs/README.md`](docs/README.md) pour la vue d'ensemble
2. **Suivez** [`docs/INDEX_LECONS.md`](docs/INDEX_LECONS.md) pour la chronologie
3. **Expérimentez** avec les démos interactives  
4. **Pratiquez** en implémentant les nouvelles pièces

Chaque leçon s'appuie sur les précédentes pour construire une architecture robuste et extensible.

---

> 🎓 **Projet pédagogique INF2020** - Architecture logicielle avancée avec Python
