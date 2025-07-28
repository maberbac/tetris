# Documentation Tetris - Apprentissage Architecture & Patterns

📚 **Documentation complète du projet Tetris** développé avec une approche **TDD** et **architecture hexagonale**.

## 📖 Table des matières

### 🏗️ Architecture
- [Architecture Hexagonale](architecture/architecture-hexagonale.md)
- [Séparation des couches](architecture/separation-couches.md)
- [Value Objects vs Entities](architecture/value-objects-entities.md)

### 🎨 Design Patterns  
- [Registry Pattern avec Auto-enregistrement](patterns/registry-pattern.md) ⭐ **NOUVEAU**
- [Factory Pattern](patterns/factory-pattern.md)
- [Template Method Pattern](patterns/template-method.md)
- [Decorator Pattern](patterns/decorator-pattern.md) ⭐ **NOUVEAU**

### 🧪 TDD (Test-Driven Development)
- [Méthodologie TDD](tdd/methodologie-tdd.md)
- [RED-GREEN-REFACTOR](tdd/red-green-refactor.md)
- [Tests de régression](tdd/tests-regression.md)

### 🐍 Python Avancé
- [Décorateurs Python](patterns/decorateurs-python.md) ⭐ **NOUVEAU**
- [Dataclasses et immutabilité](architecture/dataclasses-immutabilite.md)
- [Type Hints avancés](architecture/type-hints.md)

### 📋 Conventions & Bonnes Pratiques
- [Conventions de nommage en français](conventions/nommage-francais.md)
- [Structure de projet](conventions/structure-projet.md)
- [Organisation des tests](conventions/organisation-tests.md)

## 🎯 Progression du projet

### ✅ Phase 1 : Fondations (TERMINÉE)
- Position (Value Object) - 5 tests ✅
- Architecture de base avec héritage
- TDD strict RED-GREEN-REFACTOR

### ✅ Phase 2 : Pièces de base (TERMINÉE)  
- PieceI (ligne droite) - 5 tests ✅
- PieceO (carré) - 3 tests ✅
- PieceT (T à 4 orientations) - 6 tests ✅
- Polymorphisme démontré - 2 tests ✅

### ✅ Phase 3 : Factory & Registry (TERMINÉE)
- Factory Pattern classique - 4 tests ✅
- Registry Pattern avec auto-enregistrement - 4 tests ✅
- Décorateur @piece_tetris - 0 tests (intégré)

### 🔄 Phase 4 : Pièces restantes (EN COURS)
- PieceS (S shape) - ⏳ À implémenter
- PieceZ (Z shape) - ⏳ À implémenter  
- PieceJ (J shape) - ⏳ À implémenter
- PieceL (L shape) - ⏳ À implémenter

### ⏳ Phase 5 : Plateau & Logique de jeu (FUTURE)
- Plateau (Entity) avec détection de lignes
- Ports & Adapters (interfaces)
- Logique de collision et rotation

## 📊 Métriques actuelles

- **Tests totaux** : 27/27 (100% SUCCESS) ✅
- **Couverture** : Domaine complet
- **Architecture** : Hexagonale avec DDD
- **Patterns utilisés** : 5+ patterns différents

## 🚀 Commandes utiles

```bash
# Exécuter tous les tests
python test_runner.py

# Tests spécifiques
python -m unittest tests.test_domaine.test_entites.test_pieces.test_piece_t -v

# Démonstration des patterns
python demo_decorateur_detaille.py
```

---

> 💡 **Objectif pédagogique** : Apprendre l'architecture logicielle à travers un projet concret en utilisant Python moderne et les meilleures pratiques.
