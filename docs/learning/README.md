# Tetris - Apprentissage Architecture & Patterns 🎓

Un projet **pédagogique** pour apprendre l'**architecture logicielle** et les **design patterns** à travers le développement d'un jeu Tetris en Python.

> 🎯 **Objectif** : Maîtriser l'architecture hexagonale, TDD, et les patterns avancés à travers un projet concret.

## 📚 Documentation & Leçons

### 🎓 Leçons d'architecture disponibles

Toute la progression pédagogique est documentée dans ce répertoire `docs/` :

- 📖 **[Guide complet](../README.md)** : Vue d'ensemble et table des matières
- 📋 **[Index des leçons](../INDEX_LECONS.md)** : Chronologie complète des apprentissages
- 🔧 **[Registry Pattern](../patterns/registry-pattern.md)** : Auto-enregistrement avec décorateurs ⭐ **NOUVEAU**
- 🐍 **[Décorateurs Python](../patterns/decorateurs-python.md)** : Méta-programmation avancée ⭐ **NOUVEAU**

### 🎯 Concepts maîtrisés

- ✅ **Architecture Hexagonale** avec Domain-Driven Design
- ✅ **TDD** strict avec cycle RED-GREEN-REFACTOR  
- ✅ **Design Patterns** : Registry, Factory, Template Method, Decorator
- ✅ **Python Avancé** : ABC, Décorateurs, Type hints, Dataclasses

## 🧪 Tests & Qualité

```bash
# Exécuter tous les tests (33 tests actuellement, 100% de réussite)
python test_runner.py

# Tests spécifiques  
python -m unittest tests.test_domaine.test_entites.test_pieces.test_piece_s -v

# Démonstration des patterns
python demo_decorateur_detaille.py
python demo_extensibilite_piece_s.py
```

**Métriques actuelles** :
- **33/33 tests** passent (100% ✅) ⭐ **MIS À JOUR**
- **4 pièces implémentées** : I, O, T, S ⭐ **NOUVEAU**
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
│       │   ├── piece_t.py      # T-shape (4 orientations)
│       │   └── piece_s.py      # S-shape (2 orientations) ⭐ NOUVEAU
│       └── fabriques/          # Factory & Registry Patterns
│           ├── registre_pieces.py    # Auto-enregistrement
│           └── fabrique_pieces.py    # Factory refactorisée
├── ports/                      # 🔌 Interfaces (futures)
└── adapters/                   # 🔧 Implémentations (futures)

tests/                          # 🧪 Tests par couche
├── test_domaine/
│   └── test_entites/
│       ├── test_position.py         # 5 tests ✅
│       ├── test_pieces/             # 20 tests ✅ (I:5, O:3, T:6, S:6)
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
- Refactoring sans régression (33/33 tests ✅)
- Architecture extensible pour nouvelles pièces

### ✅ Phase 5A : PieceS (TERMINÉE) ⭐ **NOUVEAU**
- Implémentation complète avec Registry Pattern
- 6 nouveaux tests TDD (création, déplacement, rotation)
- Démonstration d'extensibilité sans modification de code
- Intégration automatique dans création aléatoire

### 🔄 Phase 5B : Pièces restantes (EN COURS)
- PieceZ, PieceJ, PieceL avec le même système
- Poursuite de la démonstration d'extensibilité

### ⏳ Phase 6 : Plateau & Logique (FUTURE)  
- Plateau Entity avec détection de lignes
- Ports & Adapters (UI, persistence)

## 🎯 Leçons apprises avec PieceS

### ✅ Registry Pattern prouvé
```bash
🔧 Pièce enregistrée : S -> PieceS
Types supportés : ['I', 'O', 'S', 'T']
✅ Création : TypePiece.S
🔄 Rotation : S horizontal ↔ S vertical
```

### ✅ Extensibilité sans modification
- **0 ligne modifiée** dans les classes existantes
- **Auto-intégration** dans la fabrique
- **Tests automatiquement étendus** pour inclure S
- **Création aléatoire** enrichie automatiquement

### ✅ TDD respecté
1. **RED** : Tests écrivent d'abord → Échec
2. **GREEN** : Implémentation minimale → Tests passent
3. **REFACTOR** : Code propre → Tests toujours verts

## 📖 Pour les étudiants

Ce projet est conçu comme un **parcours d'apprentissage progressif** :

1. **Commencez par** [Vue d'ensemble](../README.md) pour comprendre l'architecture
2. **Suivez** [Chronologie des leçons](../INDEX_LECONS.md) pour la progression
3. **Expérimentez** avec les démos interactives  
4. **Pratiquez** en implémentant les nouvelles pièces

### 🎮 Démonstrations interactives

```bash
# Registry Pattern détaillé
python demo_decorateur_detaille.py

# Extensibilité avec PieceS
python demo_extensibilite_piece_s.py
```

Chaque leçon s'appuie sur les précédentes pour construire une architecture robuste et extensible.

---

> 🎓 **Projet pédagogique INF2020** - Architecture logicielle avancée avec Python
