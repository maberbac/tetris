# 🧪 Tests Tetris - Architecture Hexagonale

Ce répertoire contient tous les tests du projet Tetris, organisés selon l'architecture hexagonale et la pyramide de tests.

## 📁 Structure Réelle des Tests

```
tests/
├── README.md                        # Ce fichier
├── run_all_unit_tests.py           # 🧪 Runner pour TOUS les tests unitaires
├── run_all_integration_tests.py    # 🔗 Runner pour TOUS les tests d'intégration
├── run_all_acceptance_tests.py     # 🎭 Runner pour TOUS les tests d'acceptance
│
├── unit/                           # Tests unitaires (logique métier)
│   └── domaine/                    # Tests du domaine métier
│       ├── test_entites/          # Tests des entités organisés
│       │   ├── test_position.py            # Value Object Position
│       │   ├── test_pieces/               # Tests de toutes les pièces
│       │   │   ├── test_piece_i.py        # Pièce ligne
│       │   │   ├── test_piece_o.py        # Pièce carrée
│       │   │   ├── test_piece_t.py        # Pièce T
│       │   │   ├── test_piece_s.py        # Pièce S
│       │   │   ├── test_piece_z.py        # Pièce Z
│       │   │   ├── test_piece_j.py        # Pièce J
│       │   │   ├── test_piece_l.py        # Pièce L
│       │   │   └── test_polymorphisme.py  # Tests polymorphisme
│       │   └── test_fabriques/           # Factory & Registry Pattern
│       │       ├── test_fabrique_pieces.py    # Factory Pattern
│       │       └── test_registre_pieces.py    # Registry avec décorateurs
│       └── services/              # Tests des services métier
│           └── test_gestionnaire_evenements.py   # Input handling
│
├── integration/                   # Tests d'intégration (système complet)
│   └── test_partie_complete.py           # Test partie complète end-to-end
│
└── acceptance/                    # Tests d'acceptance (comportement utilisateur)
    ├── test_controles_rapide.py          # Tests contrôles rapides
    └── test_controles_simplifies.py      # Tests contrôles simplifiés
```

## 🎯 Types de Tests

### 🧪 **Tests Unitaires** (`unit/`)
- **Domaine** : Tests de la logique métier pure
  - Entités : Position, Pièces (7 types), Polymorphisme
  - Fabriques : Factory Pattern, Registry Pattern
  - Services : Gestionnaire d'événements

### 🔗 **Tests d'Intégration** (`integration/`)
- Tests du système complet assemblé
- Validation de l'architecture hexagonale

### 🎭 **Tests d'Acceptance** (`acceptance/`) 
- Tests du comportement utilisateur
- Validation des contrôles et interactions

## 🚀 Lancement des Tests

### Tests unitaires (développement TDD quotidien)
```bash
python tests/run_all_unit_tests.py
```

### Tests d'intégration (validation système)
```bash
python tests/run_all_integration_tests.py
```

### Tests d'acceptance (validation utilisateur)
```bash
python tests/run_all_acceptance_tests.py
```

## 📊 Pyramide de Tests

```
        🎭 Acceptance
      (Comportement utilisateur)
         2 tests
    
      🔗 Integration  
    (Système complet)
        1 test

  🧪 Unit Tests
 (Logique métier)
   13+ tests
```

### Utilisation recommandée :
- **Développement TDD** : `run_all_unit_tests.py` (le plus fréquent)
- **Validation système** : `run_all_integration_tests.py` (avant commits)
- **Validation utilisateur** : `run_all_acceptance_tests.py` (avant releases)

## 🏗️ Architecture Respectée

Cette organisation de tests respecte parfaitement :
- ✅ **Architecture hexagonale** : Tests séparés par couche (domaine/interface)
- ✅ **Pyramide de tests** : Beaucoup d'unitaires, peu d'intégration, minimal d'acceptance
- ✅ **TDD** : Tests organisés pour faciliter le développement Red-Green-Refactor
- ✅ **Directives projet** : Tous les tests dans `tests/`, runners explicites

## 🚀 Exécution des Tests

### 🎯 Tests Unitaires (Recommandé)
```bash
# Exécuter tous les tests avec le runner principal
python tests/test_runner.py
```

### 🔧 Tests Individuels
```bash
# Tests d'affichage
python tests/test_affichage.py

# Tests de contrôles rapides
python tests/test_controles_rapide.py

# Tests de contrôles simplifiés
python tests/test_controles_simplifies.py

# Tests simples
python tests/test_simple.py
python tests/test_simple_controles.py
```

### 🏭 Tests de Domaine
```bash
# Tests des entités
python -m pytest tests/test_domaine/test_entites/

# Tests des pièces
python -m pytest tests/test_domaine/test_entites/test_pieces/

# Tests des fabriques
python -m pytest tests/test_domaine/test_entites/test_fabriques/

# Tests des services
python -m pytest tests/test_domaine/test_services/
```

## 📊 Types de Tests

### 🎮 Tests d'Interface
- **test_affichage.py** : Tests TDD pour le système d'affichage Pygame
- **test_controles_*.py** : Tests du système de contrôles avec différents niveaux de complexité

### 🏗️ Tests de Domaine
- **test_entites/** : Tests des entités métier (Position, Pièces, Plateau)
- **test_fabriques/** : Tests des patterns de création (Factory, Registry)
- **test_services/** : Tests des services métier (Gestionnaire d'événements, Commandes)

### ⚡ Tests Rapides
- **test_simple*.py** : Tests de fumée pour validation rapide
- **test_*_rapide.py** : Tests d'intégration légers

## 🧩 Conventions de Test

### 📝 Nommage
- `test_*.py` : Fichiers de test
- `TestNomClasse` : Classes de test unittest
- `test_fonction_specifique()` : Méthodes de test

### 🎯 Organisation
1. **Arrange** : Préparation des données de test
2. **Act** : Exécution de l'action à tester
3. **Assert** : Vérification des résultats

### 🔧 Imports
Tous les tests utilisent un chemin relatif pour importer les modules :
```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
```

## 🎉 Résultats Attendus

Le runner principal (`test_runner.py`) fournit :
- ✅ Nombre de tests réussis
- ❌ Détails des échecs
- ⚠️ Erreurs rencontrées
- 📊 Taux de réussite global
- 🏆 Résumé complet

Utilisez `python tests/test_runner.py` pour une vue d'ensemble complète de la santé du projet !
