# Guide d'implémentation - Architecture Hexagonale pour Tetris

## Date : 27 juillet 2025

## 🎯 **Plan d'apprentissage guidé**

### Phase 1 : Comprendre et structurer (MAINTENANT)
1. ✅ Créer la structure hexagonale
2. ✅ Expliquer chaque dossier et son rôle
3. ✅ Premier exemple concret avec Position

### Phase 2 : Domaine (Entités pures)
1. Position (Value Object) - **COMMENCER ICI**
2. Piece (Entité métier)
3. Plateau (Entité métier)

### Phase 3 : Services métier (Logique)
1. ServiceCollision
2. ServiceJeu

### Phase 4 : Ports (Interfaces)
1. Ports de sortie (AffichagePort, etc.)
2. Ports d'entrée (Commandes)

### Phase 5 : Adapters (Implémentations)
1. Adapter Pygame
2. Adapter Console (pour tests)

## 🏗️ **Structure hexagonale détaillée**

```
tetris/
├── src/
│   ├── domaine/                # CŒUR - Aucune dépendance externe
│   │   ├── __init__.py
│   │   ├── entites/
│   │   │   ├── __init__.py
│   │   │   ├── position.py     # ← COMMENCER ICI (Value Object)
│   │   │   ├── piece.py        # Entité Piece
│   │   │   └── plateau.py      # Entité Plateau
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── service_collision.py
│   │   │   └── service_jeu.py
│   │   └── exceptions/
│   │       ├── __init__.py
│   │       └── exceptions_tetris.py
│   ├── ports/                  # INTERFACES - Contrats
│   │   ├── __init__.py
│   │   ├── entree/            # Use Cases (ce que l'app FAIT)
│   │   │   ├── __init__.py
│   │   │   ├── commencer_partie.py
│   │   │   ├── deplacer_piece.py
│   │   │   └── obtenir_etat_jeu.py
│   │   └── sortie/            # Services externes (ce dont l'app a BESOIN)
│   │       ├── __init__.py
│   │       ├── affichage_port.py
│   │       ├── input_port.py
│   │       └── stockage_port.py
│   └── adapters/              # IMPLÉMENTATIONS - Détails techniques
│       ├── __init__.py
│       ├── entree/           # Drivers (qui UTILISE l'app)
│       │   ├── __init__.py
│       │   ├── ui_pygame.py
│       │   └── ui_console.py
│       └── sortie/           # Driven (UTILISÉ par l'app)
│           ├── __init__.py
│           ├── affichage_pygame.py
│           ├── affichage_console.py
│           └── stockage_json.py
├── tests/                     # Tests par couche hexagonale
│   ├── test_domaine/
│   │   ├── test_entites/
│   │   │   ├── test_position.py
│   │   │   ├── test_piece.py
│   │   │   └── test_plateau.py
│   │   └── test_services/
│   │       ├── test_service_collision.py
│   │       └── test_service_jeu.py
│   ├── test_ports/
│   └── test_adapters/
├── demos/                     # Démonstrations
│   ├── demo_console.py
│   └── demo_pygame.py
├── docs/                      # Documentation
└── tetris.py                  # Point d'entrée - Composition Root
```

## 🎓 **Explication de chaque couche**

### 1. **DOMAINE** (Centre - Aucune dépendance)
```python
# src/domaine/entites/position.py
# Règle : Pas d'import vers l'extérieur !
# Seule exception : modules Python standard (dataclasses, typing, etc.)
```
**Rôle** : Logique métier pure, règles business de Tetris

### 2. **PORTS** (Interfaces)
```python
# src/ports/sortie/affichage_port.py
# Règle : Que des abstractions (ABC), pas d'implémentations
```
**Rôle** : Contrats entre le domaine et l'extérieur

### 3. **ADAPTERS** (Implémentations)
```python
# src/adapters/sortie/affichage_pygame.py
# Règle : Peut importer pygame, mais respecte les interfaces
```
**Rôle** : Détails techniques (Pygame, fichiers, réseau...)

## 🚀 **Démarrage guidé - Étape 1**

### **Première entité : Position (Value Object)**

**Pourquoi commencer par Position ?**
- Simple et fondamentale
- Aucune dépendance
- Parfait pour comprendre les Value Objects
- Base pour Piece et Plateau

### **Concept Value Object :**
- Immutable (frozen)
- Égalité par valeur, pas par référence
- Pas d'identité propre
- Méthodes pures (pas d'effets de bord)

## 📋 **Prochaines étapes concrètes**

### Étape 1 : Créer la structure
**Action** : Je crée tous les dossiers et fichiers __init__.py

### Étape 2 : TDD sur Position
**Action** : 
1. Test qui échoue pour Position
2. Implémentation minimale
3. Refactoring

### Étape 3 : Guider votre compréhension
**Questions à vous poser** :
- Que fait cette couche ?
- Pourquoi cette séparation ?
- Comment tester cela ?

## ❓ **Questions pour vous**

1. **Prêt pour l'étape 1** (création structure) ?
2. **Voulez-vous que j'explique davantage** avant de commencer ?
3. **Des questions sur les concepts** hexagonaux ?

## 💡 **Conseils d'apprentissage**

### **Ne pas s'inquiéter si :**
- Ça semble complexe au début
- Vous ne voyez pas tout l'intérêt immédiatement
- Il y a beaucoup de fichiers

### **Focus sur :**
- Un fichier à la fois
- Comprendre le "pourquoi" de chaque couche
- Expérimenter et poser des questions

### **À retenir :**
```
Domaine ← ne dépend de RIEN
Ports ← interfaces (contrats)
Adapters ← implémentations (détails)
```

**Prêt à commencer ? Je crée la structure ou vous avez des questions d'abord ?** 🚀
