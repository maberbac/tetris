# 🎮 Démonstrations Tetris

Ce répertoire contient toutes les démonstrations et scripts d'exemple pour le projet Tetris.

## 📁 Organisation

### 🧩 Démonstrations des pièces et patterns
- `demo_pieces.py` - Démonstration complète de toutes les pièces Tetris
- `demo_decorateur.py` - Fonctionnement du décorateur @piece_tetris
- `demo_decorateur_detaille.py` - Analyse détaillée du décorateur
- `demo_extensibilite_piece_s.py` - Extensibilité avec Registry Pattern

### 📚 Pattern Command (déplacé vers docs/learning/)
- Les tutoriels du Pattern Command sont maintenant dans `docs/learning/`
- `apprentissage_pattern_command.py` - Tutoriel complet
- `guide_visuel_pattern_command.py` - Guide visuel avec diagrammes

### 🎮 Démonstrations du plateau et contrôles
- `demo_plateau.py` - Test du plateau et des collisions
- `demo_controles.py` - Système de contrôles complet
- `demo_simple_6x6.py` - ✨ **NOUVEAU** : Plateau 6x6 avec pièce L (approche simple)
- `demo_6x6_avec_gestionnaire.py` - ✨ **NOUVEAU** : Version avec gestionnaire d'événements complet
- `demo_plateau_6x6_piece_l.py` - Version alternative avec architecture complète
- `demo_integration.py` - Jeu intégré avec toutes les fonctionnalités

### 🖼️ Démonstrations d'affichage
- `demo_grille.py` - Test d'affichage de la grille Tetris
- `demo_fenetre.py` - Grille en mode fenêtré

### 🎹 Démonstrations des contrôles
- `demo_controles.py` - Test du système de contrôles
- `demo_commandes.py` - Exemples d'utilisation des commandes
- `demo_pygame_controls.py` - Intégration avec Pygame

### 🔧 Outils de développement
- `benchmark_performance.py` - Tests de performance
- `debug_visualizer.py` - Visualisation pour le debugging
- `test_integration.py` - Tests d'intégration manuels

## 🚀 Utilisation

Tous les scripts peuvent être exécutés directement depuis la racine du projet :

```bash
# Démonstrations des pièces et patterns
python demo/demo_pieces.py
python demo/demo_decorateur.py
python demo/demo_decorateur_detaille.py
python demo/demo_extensibilite_piece_s.py

# Tutoriels des Design Patterns (voir docs/learning/)
python docs/learning/apprentissage_pattern_command.py  # 🎯 Recommandé pour apprendre !
python docs/learning/guide_visuel_pattern_command.py

# Démonstrations du plateau et contrôles
python demo/demo_plateau.py
python demo/demo_controles.py
python demo/demo_integration.py

# Démonstrations d'affichage
python demo/demo_grille.py
python demo/demo_fenetre.py
```

## 🎓 Apprentissage des Design Patterns

### 🎯 Pattern Command - Tutoriel Complet
Le fichier `apprentissage_pattern_command.py` offre un **tutoriel interactif complet** du Pattern Command :

- 🤔 **Problème résolu** - Pourquoi utiliser ce pattern ?
- 🏗️ **Structure** - Diagrammes et composants
- 💻 **Implémentation** - Exemples de code progressifs
- 🚀 **Avantages** - UNDO/REDO, extensibilité, tests
- 🎮 **Application Tetris** - Comment c'est utilisé dans le projet
- 🎓 **Exercices** - Pour pratiquer vos nouvelles connaissances

### 🎨 Guide Visuel
Le fichier `guide_visuel_pattern_command.py` complète avec :
- 📊 Diagrammes avant/après
- 🔄 Flux d'exécution détaillé  
- 📈 Évolution du code étape par étape
- 🔗 Patterns complémentaires
- ⚠️ Anti-patterns à éviter
- 🧠 Quiz interactif pour tester vos connaissances

**💡 Recommandation : Commencez par le tutoriel principal, puis explorez le guide visuel !**

---

## 🎮 **NOUVEAU** : Deux Démonstrations Plateau 6x6 avec Pièce L

### 🎯 Deux approches complémentaires

#### 1. **Version Simple** : `demo_simple_6x6.py`
- ✅ **Rapide et direct** : Gestion pygame native
- ✅ **Facile à comprendre** : Code minimal
- ✅ **Indépendant** : Aucune dépendance aux services

#### 2. **Version avec Gestionnaire** : `demo_6x6_avec_gestionnaire.py`
- ✅ **Architecture complète** : Utilise le vrai `GestionnaireEvenements`
- ✅ **Pattern Command** : Commandes découplées
- ✅ **Fonctionnalités avancées** : Répétition touches, pause, menu

### ✨ Fonctionnalités communes
- **Plateau 6x6** : Plus petit que le plateau Tetris classique
- **Pièce L interactive** : Utilise la vraie implémentation `PieceL`
- **Collision** : Empêche les mouvements invalides
- **Feedback temps réel** : Console + interface graphique

### 🎮 Contrôles

#### Version Simple
```
Flèches : Déplacer | Espace : Rotation | ESC : Quitter
```

#### Version avec Gestionnaire
```
← → : Déplacer (avec répétition) | ↑ : Rotation | ↓ : Descendre
P : Pause | ESC : Menu/Quitter
```

### 🚀 Lancement
```bash
cd c:\src\INF2020\tetris

# Version simple (recommandée pour débuter)
python demo\demo_simple_6x6.py

# Version avec gestionnaire (architecture complète)
python demo\demo_6x6_avec_gestionnaire.py
```

### 📊 Comparaison détaillée
Voir `COMPARAISON_DEMOS.md` pour une analyse complète des deux approches.

---

## 📝 Notes

- Chaque démo est autonome et inclut ses propres imports
- Les démos utilisent le code source depuis `src/`
- Parfait pour comprendre et tester les fonctionnalités
- Idéal pour les présentations et l'apprentissage

## 🎯 Objectifs

1. **Pédagogique** : Comprendre chaque composant
2. **Test manuel** : Validation interactive
3. **Présentation** : Montrer les fonctionnalités
4. **Debug** : Identifier les problèmes rapidement
