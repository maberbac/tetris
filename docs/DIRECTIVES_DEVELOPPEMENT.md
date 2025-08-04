# 🛠️ Directives de Développement
Règles de développement pour le LLM

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

# ❌ INTERDIT - Documentation projet à la racine (sauf README.md)
GUIDE.md                  # ❌ JAMAIS ! (doit être dans docs/)
DOC_TECHNIQUE.md          # ❌ JAMAIS ! (doit être dans docs/)
journal-developpement.md  # ❌ JAMAIS ! (doit être dans docs/)
testing-strategy.md       # ❌ JAMAIS ! (doit être dans docs/)

# ✅ CORRECT - Tests dans tests/
tests/integration/test_*.py    # ✅ OUI !
tests/unit/test_*.py           # ✅ OUI !
tests/run_tests.py             # ✅ OUI !

# ✅ CORRECT - Documentation dans docs/
docs/DOC_TECHNIQUE.md          # ✅ OUI !
docs/journal-developpement.md # ✅ OUI !
docs/testing-strategy.md      # ✅ OUI !
README.md                      # ✅ OUI ! (seule exception à la racine)
```

## 📁 Organisation des Fichiers

### Règles d'Organisation
- **Démos** : Toujours créer les démos dans le répertoire `demo/`
- **Tests officiels** : TOUS les tests dans le répertoire `tests/` avec sous-répertoires appropriés
- **Documentation projet** : TOUS les fichiers `.md` de documentation (sauf `README.md`) dans le répertoire `docs/`
- **Fichiers temporaires** : TOUT ce que je génère pour mes besoins dans `tmp/` (scripts, .md, analyses, notes, etc.)
- **Assets du jeu** : TOUS les médias dans le répertoire `assets/` (sons, images, musiques)
- **Structure existante** : Respecter l'architecture hexagonale en place (`src/domaine/`, `src/interface/`)

### Structure des Répertoires
```
tetris/
├── src/                    # Code source principal
│   ├── domaine/           # Logique métier (centre de l'hexagone)
│   ├── ports/             # Interfaces (contrats)
│   └── adapters/          # Implémentations techniques
├── assets/                # ⭐ Médias du jeu (sons, images)
│   ├── audio/             # Sons et musiques
│   │   ├── music/         # Musique principale
│   │   └── sfx/           # Effets sonores (line_clear, rotate)
│   └── images/            # Images et textures
│       └── backgrounds/   # Arrière-plans
├── docs/                  # ⭐ Documentation complète
│   ├── DIRECTIVES_DEVELOPPEMENT.md  # Règles de développement
│   ├── DOC_TECHNIQUE.md             # Documentation technique
│   ├── journal-developpement.md     # Journal complet du projet
│   └── testing-strategy.md          # Stratégie TDD
├── tests/                 # ⭐ TOUS les tests du projet
│   ├── integration/       # Tests d'intégration
│   ├── unit/             # Tests unitaires
│   ├── acceptance/       # Tests d'acceptation
│   └── [4 scripts officiels]  # Scripts de lancement obligatoires
├── tmp/                   # ⭐ TOUT ce que je génère pour mes besoins
└── *.py                  # Scripts principaux (jouer.py, partie_tetris.py)
```

### Contenu du Répertoire `tmp/`
**TOUT ce que je génère pour mes besoins de développement :**
- 📝 Fichiers `.md` d'analyse et de notes
- 🐍 Scripts Python temporaires 
- 📊 Fichiers de données de test
- 🔍 Scripts d'exploration et de validation
- 📋 Documentation de travail
- 🧪 Prototypes et expérimentations

### Organisation de la Documentation `docs/`
**TOUTE la documentation officielle du projet (sauf README.md) :**
- 📋 **`DIRECTIVES_DEVELOPPEMENT.md`** : Règles de développement et organisation du projet
- 🏗️ **`DOC_TECHNIQUE.md`** : Architecture hexagonale, composants, structure technique détaillée
- 📰 **`journal-developpement.md`** : Chronologie complète et historique du développement TDD
- 🧪 **`testing-strategy.md`** : Stratégie TDD, métriques des tests, organisation des suites
- 📚 **Autres `.md`** : Documentation spécialisée selon les besoins du projet

**RÈGLE ABSOLUE** : Seul `README.md` peut rester à la racine (vue d'ensemble utilisateur)

### Organisation des Assets `assets/`
**Structure standardisée pour les médias du jeu :**
- 🎵 **`audio/music/`** : Musique principale du jeu (`theme.ogg`)
- 🔊 **`audio/sfx/`** : Effets sonores essentiels (`line_clear.wav`, `rotate.wav`)
- 🖼️ **`images/backgrounds/`** : Arrière-plans optionnels du jeu
- 📋 **`README.md`** : Documentation complète des assets

### 🔊 RÈGLE AUDIO - Volume des Effets Sonores
**OBLIGATION : Tous les effets sonores dans `assets/audio/sfx/` doivent être joués à 100% de volume par défaut.**

```python
# ✅ CORRECT - Volume 100% par défaut pour les effets sonores
self.audio.jouer_effet_sonore("assets/audio/sfx/rotate.wav")  # Volume 1.0 par défaut
self.audio.jouer_effet_sonore("assets/audio/sfx/line_clear.wav")  # Volume 1.0 par défaut

# ✅ CORRECT - Volume personnalisé uniquement si spécifié explicitement
self.audio.jouer_effet_sonore("assets/audio/sfx/rotate.wav", volume=0.8)  # Volume réduit si nécessaire

# ❌ INCORRECT - Ne pas spécifier de volume inférieur sans justification
self.audio.jouer_effet_sonore("assets/audio/sfx/rotate.wav", volume=0.6)  # Trop faible sans raison
```

**Justification** : Les effets sonores doivent être audibles et percutants pour améliorer l'expérience utilisateur. Le volume 100% assure une excellente perception des événements du jeu.

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

#### Organisation de la Documentation
- **`docs/DIRECTIVES_DEVELOPPEMENT.md`** : Règles de développement et organisation
- **`docs/DOC_TECHNIQUE.md`** : Architecture, composants, structure technique  
- **`docs/journal-developpement.md`** : Chronologie complète du projet
- **`docs/testing-strategy.md`** : Stratégie TDD et métriques des tests
- **`README.md`** (racine) : Vue d'ensemble utilisateur du projet

#### Lors de changements dans `tests/`
- **`docs/testing-strategy.md`** : Métriques, structure, runners
- **`docs/DOC_TECHNIQUE.md`** : Architecture de tests, pyramide
- **`README.md`** : Métriques globales

#### Lors de changements dans `src/`
- **`docs/DOC_TECHNIQUE.md`** : Architecture, composants, structure
- **`README.md`** : Vue d'ensemble du projet

#### Lors de renommage/déplacement de fichiers
- **TOUS les `.md` dans `docs/`** : Chemins, noms, références
- **Scripts de runners** : Imports, chemins relatifs
- **`README.md`** : Structure projet

#### Lors d'ajout de nouveaux patterns/composants
- **`docs/DOC_TECHNIQUE.md`** : Nouveaux patterns, exemples
- **`docs/journal-developpement.md`** : Évolution du projet

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

### 🎯 RÈGLE OBLIGATOIRE - Scripts de Tests Standards

**TOUJOURS utiliser ces 4 scripts officiels pour lancer les tests :**

```bash
# Tests unitaires (composants isolés)
python tests/run_all_unit_tests.py

# Tests d'acceptance (scénarios utilisateur) 
python tests/run_all_acceptance_tests.py

# Tests d'intégration (composants ensemble)
python tests/run_all_integration_tests.py

# Suite complète (tous les tests)
python tests/run_suite_tests.py
```

**Interdiction de créer d'autres scripts de tests** - Ces 4 scripts suffisent pour tous les besoins.

### Validation Obligatoire
- **Toujours tester avant de livrer** - Créer des tests pour valider que tout fonctionne
- **Tests complets** - Couvrir tous les aspects : génération, plateau, moteur, statistiques
- **Messages clairs** - Tests avec émojis et descriptions explicites
- **Debug TDD systématique** - En cas de bug, appliquer cycle RED-GREEN-REFACTOR strict

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
- **Debug non méthodique** - En cas de bug, appliquer TDD strict : exploration → reproduction → tests → correction

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
