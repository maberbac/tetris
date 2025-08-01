# 🛠️ Directives de Développement

## � RÈGLE ABSOLUE - Organisation des Tests

### ⚠️ INTERDICTION FORMELLE
**AUCUN fichier de test à la racine du projet !**

### ✅ OBLIGATION STRICTE
**TOUS les tests dans le répertoire `tests/` avec la structure appropriée :**

```
tests/
├── integration/           # Tests d'intégration
│   └── test_*.py         # Tests de composants ensemble
├── unit/                 # Tests unitaires  
│   └── test_*.py         # Tests de composants isolés
├── acceptance/           # Tests d'acceptation
│   └── test_*.py         # Tests de scénarios utilisateur
└── run_tests.py          # Script de lancement des tests
```

### 🎯 Distinction Claire
- **`tests/`** - TOUS les tests permanents du projet
- **`tmp/`** - TOUT ce que je génère pour mes besoins de développement
- **`demo/`** - Démonstrations pour les utilisateurs

### 🚨 Signaux d'Alerte CRITIQUES
```bash
# ❌ INTERDIT - Tests à la racine
test_*.py                 # ❌ JAMAIS !
*_test.py                 # ❌ JAMAIS !
run_tests.py              # ❌ JAMAIS !

# ✅ CORRECT - Tests dans tests/
tests/integration/test_*.py    # ✅ OUI !
tests/unit/test_*.py           # ✅ OUI !
tests/run_tests.py             # ✅ OUI !
```

## 📁 Organisation des Fichiers

### Règles d'Organisation
- **Démos** : Toujours créer les démos dans le répertoire `demo/`
- **Tests officiels** : TOUS les tests dans le répertoire `tests/` avec sous-répertoires appropriés
- **Fichiers temporaires** : TOUT ce que je génère pour mes besoins dans `tmp/` (scripts, .md, analyses, notes, etc.)
- **Structure existante** : Respecter l'architecture hexagonale en place (`src/domaine/`, `src/interface/`)

### Structure des Répertoires
```
tetris/
├── src/                    # Code source principal
│   ├── domaine/           # Logique métier
│   └── interface/         # Interface utilisateur
├── demo/                  # ⭐ Démos et exemples
├── tests/                 # ⭐ TOUS les tests du projet
│   ├── integration/       # Tests d'intégration
│   ├── unit/             # Tests unitaires
│   ├── acceptance/       # Tests d'acceptation
│   └── run_tests.py      # Script de lancement des tests
├── tmp/                   # ⭐ TOUT ce que je génère pour mes besoins
└── *.py                  # Scripts principaux (jouer.py, etc.)
```

### Contenu du Répertoire `tmp/`
**TOUT ce que je génère pour mes besoins de développement :**
- 📝 Fichiers `.md` d'analyse et de notes
- 🐍 Scripts Python temporaires 
- 📊 Fichiers de données de test
- 🔍 Scripts d'exploration et de validation
- 📋 Documentation de travail
- 🧪 Prototypes et expérimentations

## 🏗️ Règles Architecturales

### Réutilisation Obligatoire
- **Plateau** : Toujours utiliser `Plateau(largeur, hauteur)` au lieu de créer des classes figées
- **Factory Pattern** : Utiliser `FabriquePieces.creer_aleatoire()` pour la génération
- **Command Pattern** : Exploiter le système de commandes existant
- **Registry Pattern** : S'appuyer sur l'auto-découverte des pièces

### Anti-Patterns à Éviter
```python
# ❌ NE PAS FAIRE - Classes figées
class PlateauDemo6x6:
    def __init__(self):
        self.largeur = 6
        self.hauteur = 6

# ✅ FAIRE - Plateau réutilisable
plateau = Plateau(6, 6)  # ou n'importe quelle taille
```

## 📚 RÈGLE CRITIQUE - Synchronisation Documentation

### ⚠️ OBLIGATION ABSOLUE
**Toute modification du code doit IMMÉDIATEMENT être reflétée dans la documentation appropriée !**

### 🎯 Documentation à Maintenir Systématiquement

#### Lors de changements dans `tests/`
- **`tests/README.md`** : Structure, runners, organisation
- **`DOC_TECHNIQUE.md`** : Architecture de tests, pyramide

#### Lors de changements dans `src/`
- **`DOC_TECHNIQUE.md`** : Architecture, composants, structure
- **`README.md` principal** : Vue d'ensemble du projet

#### Lors de renommage/déplacement de fichiers
- **TOUS les `.md` concernés** : Chemins, noms, références
- **Scripts de runners** : Imports, chemins relatifs

#### Lors d'ajout de nouveaux patterns/composants
- **`DOC_TECHNIQUE.md`** : Nouveaux patterns, exemples
- **`docs/`** : Guides spécialisés si nécessaire

### ✅ Check-list OBLIGATOIRE Avant Commit
```bash
# 1. Code modifié ✅
# 2. Tests mis à jour ✅  
# 3. Documentation synchronisée ✅
# 4. Runners de tests fonctionnels ✅
```

### 🚨 Signaux d'Alerte CRITIQUES
- ❌ Documentation qui mentionne des fichiers inexistants
- ❌ Structure documentée différente de la réalité
- ❌ Runners qui pointent vers de mauvais chemins
- ❌ Exemples de code obsolètes dans les `.md`

---

## 🌍 Règles de Francisation

### Principe Général
- **Tout en français sauf exceptions justifiées**
- **Code français** : Classes, méthodes, variables, constantes, commentaires
- **Documentation française** : Tous les `.md`, docstrings, messages

### Exceptions Justifiées
- **Conventions universelles** : `main()`, `__init__()`, `__str__()`, `__repr__()`
- **Mots-clés imposés** : Framework/bibliothèque (pygame, unittest)
- **Termes techniques** : Sans équivalent français approprié ou très établis

### Exemples de Francisation
```python
# ✅ CORRECT - Code français avec exceptions justifiées
class AffichagePartie:
    def __init__(self):              # ✅ Exception : convention universelle
        self.ecran = None
        self.largeur_ecran = 800
    
    def dessiner_grille(self):       # ✅ Français
        """Dessine la grille de jeu."""
        pass
    
    def main(self):                  # ✅ Exception : convention universelle
        """Point d'entrée principal."""
        pass

# ❌ INCORRECT - Mélange incohérent
class GameDisplay:                   # ❌ Anglais sans justification
    def dessiner_grid(self):         # ❌ Mélange français/anglais
        pass
```

### Nommage Français
- **Classes** : `AffichagePartie`, `MoteurJeu`, `FabriquePieces`
- **Méthodes** : `dessiner_grille()`, `mettre_a_jour()`, `nettoyer()`
- **Variables** : `ecran`, `largeur_ecran`, `position_grille_x`
- **Constantes** : `COULEUR_NOIR`, `TAILLE_CELLULE`, `LARGEUR_GRILLE`
- **Tests** : `test_affichage_peut_etre_cree`, `test_plateau_detecte_collision`

## 🧪 Règles de Test et TDD

### Méthodologie TDD (Test-Driven Development)
- **Red-Green-Refactor** : Écrire le test d'abord, puis le code, puis refactoriser
- **Tests d'abord** : Définir le comportement attendu avant l'implémentation
- **Cycle court** : Petites étapes itératives avec validation continue
- **Couverture totale** : Chaque fonctionnalité doit avoir ses tests

### Organisation des Tests
- **Tests officiels** : OBLIGATOIREMENT dans `tests/` avec sous-répertoires appropriés
  - `tests/integration/` - Tests d'intégration (composants ensemble)
  - `tests/unit/` - Tests unitaires (composants isolés)
  - `tests/acceptance/` - Tests d'acceptation (scénarios utilisateur)
  - `tests/run_tests.py` - Script de lancement
- **Scripts temporaires** : TOUT ce que je génère pour mes besoins dans `tmp/`
- **AUCUN test à la racine** - Tous les tests doivent être dans `tests/`

### Validation Obligatoire
- **Toujours tester avant de livrer** - Créer des tests pour valider que tout fonctionne
- **Tests complets** - Couvrir tous les aspects : génération, plateau, moteur, statistiques
- **Messages clairs** - Tests avec émojis et descriptions explicites

### Structure des Tests
```python
def test_fonction():
    """Description claire du test."""
    print("🧪 Test de [fonctionnalité]")
    print("-" * 40)
    
    # Test avec assertions claires
    resultat = fonction_testee()
    
    if resultat:
        print("✅ Test réussi")
        return True
    else:
        print("❌ Test échoué")
        return False
```

## 🎯 Méthodologie de Développement

### Approche Progressive avec TDD
1. **Analyser l'existant** - Toujours explorer ce qui est déjà en place
2. **Écrire les tests** - Définir le comportement attendu (TDD Red)
3. **Implémenter minimum** - Code juste pour faire passer les tests (TDD Green)
4. **Refactoriser** - Améliorer le code en gardant les tests verts (TDD Refactor)
5. **Tester systématiquement** - Valider chaque étape
6. **Documenter clairement** - Instructions et explications complètes

### Principe de Non-Duplication
- **DRY (Don't Repeat Yourself)** - Réutiliser plutôt que recréer
- **Factorisation** - Identifier les patterns réutilisables
- **Extension** - Étendre l'existant plutôt que remplacer

## 📝 Standards de Documentation

### Structure des Fichiers
- **En-tête avec émojis** - Rendre la navigation visuelle
- **Sections claires** - Organisation logique avec `##` et `###`
- **Exemples concrets** - Code et commandes prêts à utiliser
- **Résultats attendus** - Indiquer ce qui doit se passer

### Style de Documentation
```markdown
## 🎯 Section Principale

### Sous-section Spécifique
- **Point important** : Description claire
- **Exemple** : Code illustratif
- **Résultat** : `Sortie attendue ✅`
```

## 🔄 Workflow de Développement

### Étapes Obligatoires (Cycle TDD)
1. **Explorer** - `semantic_search`, `grep_search`, `read_file` pour comprendre l'existant
2. **Red** - Écrire un test qui échoue dans `tests/` ou `tmp/`
3. **Green** - Implémenter le minimum pour faire passer le test
4. **Refactor** - Améliorer le code en gardant les tests verts
5. **Planifier** - Identifier les composants à réutiliser
6. **Documenter** - Instructions claires pour l'utilisateur

### Outils Préférés
- **Fichiers temporaires** - TOUT ce que je génère dans `tmp/` pendant développement
- **Tests officiels** - Suite complète dans `tests/` pour le projet
- **Démos organisées** - Exemples dans `demo/` avec structure claire
- **Validation TDD** - Red-Green-Refactor à chaque étape

## 🎮 Règles Spécifiques au Projet Tetris

### Architecture Obligatoire
- **Plateau refactorisé** - `Plateau(10, 20)` pour Tetris standard
- **7 types de pièces** - I, O, T, S, Z, J, L avec génération aléatoire
- **Interface séparée** - Pygame dans des classes dédiées
- **Command Pattern** - Pour tous les contrôles utilisateur

### Standards de Qualité
- **60 FPS** - Interface fluide
- **Couleurs distinctives** - Chaque pièce a sa couleur
- **Statistiques complètes** - Score, niveau, compteurs
- **Tests 4/4** - Validation complète avant livraison

## 🚨 Points d'Attention

### Erreurs Courantes à Éviter
- **Ne pas explorer l'existant** - Toujours analyser avant d'implémenter
- **Créer des doublons** - Réutiliser plutôt que recréer
- **Oublier les tests** - Valider systématiquement
- **Ignorer le TDD** - Écrire les tests AVANT le code
- **Tests mal organisés** - TOUS les tests dans `tests/`, JAMAIS à la racine
- **Documentation incomplète** - Toujours expliquer comment utiliser
- **Documentation TDD obsolète** - Maintenir `docs/tdd/` et `docs/journal-developpement.md` à jour
- **Mauvaise organisation** - Respecter `tests/` vs `tmp/` vs `demo/`

### Signaux d'Alerte
```python
# 🚨 Si vous voyez du code comme ça, STOP !
class PlateauFixe6x6:  # ❌ Duplication !
class PlateauFixe10x20:  # ❌ Pattern figé !

# ✅ Version correcte
plateau = Plateau(largeur, hauteur)  # ✅ Réutilisable !
```

```bash
# 🚨 Organisation INTERDITE
test_mon_test.py          # ❌ Test à la racine !
mon_script_test.py        # ❌ Test mal placé !
analyse_temporaire.md     # ❌ Documentation temporaire à la racine !
```

---

## 🔄 Workflow de Développement avec Documentation

### Cycle OBLIGATOIRE pour Tout Changement

#### 1. **Avant Modification**
```bash
# Identifier la documentation concernée
# README.md, DOC_TECHNIQUE.md, tests/README.md, etc.
```

#### 2. **Pendant Modification**  
```bash
# Développer en TDD
# Modifier le code
# Exécuter les tests
```

#### 3. **Après Modification - CHECK-LIST CRITIQUE**
```bash
✅ Code fonctionnel
✅ Tests passent
✅ Documentation mise à jour
✅ Noms de fichiers cohérents
✅ Structure documentée = structure réelle
```

#### 4. **Validation Finale**
```bash
# Vérifier que la documentation reflète la réalité
# Tester les commandes documentées
# S'assurer que les exemples fonctionnent
```

### ⚠️ JAMAIS de Commit Sans Documentation Synchronisée !

**Cette règle est maintenant FONDAMENTALE dans notre processus de développement.** 📚✨

# ✅ Organisation CORRECTE
tests/integration/test_mon_test.py    # ✅ Test bien placé !
tmp/mon_script_temporaire.py          # ✅ Script temporaire !
tmp/analyse_temporaire.md             # ✅ Documentation temporaire !
```

## 📋 Checklist de Livraison

### Avant de Livrer
- [ ] **Exploration complète** - Compris l'architecture existante
- [ ] **TDD respecté** - Tests écrits avant le code
- [ ] **Réutilisation maximale** - Pas de duplication de code
- [ ] **Tests passants** - Tous les tests sont verts ✅
- [ ] **Organisation STRICTE** - TOUS les tests dans `tests/`, TOUT ce que je génère dans `tmp/`, démos dans `demo/`
- [ ] **Documentation à jour** - Instructions claires pour l'utilisateur
- [ ] **Documentation TDD mise à jour** - `docs/tdd/testing-strategy.md` et `docs/journal-developpement.md` reflètent l'état actuel

### Validation Finale
- [ ] **Fonctionnalités complètes** - Tout ce qui était demandé fonctionne
- [ ] **Performance correcte** - Pas de ralentissements
- [ ] **Code propre** - Architecture respectée
- [ ] **Extensibilité** - Préparé pour futures améliorations

---

## 🎯 Résumé des Priorités

1. **EXPLORER** l'architecture existante
2. **TDD** - Tests d'abord, puis code
3. **RÉUTILISER** l'architecture existante
4. **ORGANISER** - `tests/` pour tests officiels, `tmp/` pour TOUT ce que je génère, `demo/` pour exemples
5. **TESTER** systématiquement (Red-Green-Refactor)
6. **DOCUMENTER** clairement
7. **MAINTENIR** la documentation TDD (`docs/`) à jour
8. **VALIDER** avant de livrer

**Ces directives garantissent un code de qualité et une expérience utilisateur optimale !** ✨
