# Règles d'interaction pour le développement Tetris

Ce document définit les règles et la méthodologie à suivre lors de nos interactions pour développer le jeu Tetris en Python.

## 📋 Règles principales

### 1. Documentation des prompts
- **Règle** : Tous les prompts doivent être documentés dans ce répertoire
- **Objectif** : Maintenir une trace complète des échanges et décisions
- **Application** : Chaque conversation sera sauvegardée dans un fichier `.md` approprié

### 2. Clarification systématique
- **Règle** : N'assume rien et pose autant de questions qu'il le faudra
- **Objectif** : Comprendre parfaitement vos demandes avant d'agir
- **Application** : Poser des questions précises sur les spécifications, contraintes, et attentes

### 3. Choix collaboratif
- **Règle** : En cas d'hésitation entre plusieurs solutions, poser la question
- **Objectif** : Prendre les meilleures décisions techniques ensemble
- **Application** : Présenter les options avec leurs avantages/inconvénients

### 4. Mise à jour du README
- **Règle** : Inclure chaque nouvelle fonctionnalité dans le README
- **Objectif** : Tenir l'utilisateur informé des capacités du programme
- **Application** : Mettre à jour automatiquement la documentation utilisateur

### 5. Organisation thématique des prompts
- **Règle** : Séparer les prompts dans différents `.md` selon le contexte
- **Structure suggérée** :
  - `gameplay-prompts.md` : Mécaniques de jeu
  - `ui-prompts.md` : Interface utilisateur
  - `tests-prompts.md` : Tests et TDD
  - `architecture-prompts.md` : Structure du code
  - `debugging-prompts.md` : Résolution de problèmes

### 6. Documentation du code
- **Règle** : Documenter tout code généré
- **Standards** :
  - Docstrings pour toutes les fonctions et classes
  - Commentaires inline pour la logique complexe
  - Documentation des algorithmes utilisés
  - Exemples d'utilisation quand pertinent

### 6.1. Convention de nommage français
- **Règle** : Utiliser le français pour TOUS les noms (fichiers, variables, méthodes, classes)
- **Exceptions** : Utiliser l'anglais UNIQUEMENT pour :
  - Les termes sans équivalent français approprié
  - Les conventions universelles : `main()`, `__init__()`, `__str__()`, etc.
  - Les mots-clés imposés par les frameworks (ex: `pygame.QUIT`)
- **Objectif** : Cohérence linguistique complète et facilité de compréhension en français
- **Application** :
  - **Fichiers** : `affichage.py`, `plateau.py`, `constantes.py`, `test_affichage.py`
  - **Classes** : `Affichage`, `Plateau`, `Piece`, `Jeu` (français prioritaire)
  - **Variables** : `position_x`, `grille_jeu`, `piece_courante`, `ecran_principal`
  - **Méthodes** : `dessiner_grille()`, `deplacer_piece()`, `detecter_collision()`
  - **Méthodes spéciales** : `main()`, `__init__()` (conventions universelles)
  - **Constantes** : `COULEUR_FOND`, `TAILLE_CELLULE`, `LARGEUR_PLATEAU`
  - **Commentaires et docstrings** : Toujours en français

### 8. Apprentissage Python et jeux vidéo
- **Règle** : Présenter les particularités Python et concepts de game dev
- **Objectif** : Approfondir vos connaissances
- **Sujets à couvrir** :
  - Concepts Python spécialisés (generators, decorators, etc.)
  - Patterns de programmation pour jeux
  - Optimisations de performance
  - Gestion des états de jeu
  - Architecture MVC pour jeux

### 9. Support développement IA
- **Règle** : Considérer que vous êtes débutant avec l'IA
- **Suggestions d'amélioration** :
  - Prompts plus précis et structurés
  - Utilisation de contexte détaillé
  - Validation étape par étape
  - Feedback continu sur les résultats

### 10. Méthodologie TDD (Test Driven Development)
- **Règle** : Développer avec l'approche TDD
- **Cycle Red-Green-Refactor** :
  1. **Red** : Écrire un test qui échoue
  2. **Green** : Écrire le code minimal pour faire passer le test
  3. **Refactor** : Améliorer le code en gardant les tests verts
- **Application** : Commencer chaque fonctionnalité par ses tests

## 🔄 Workflow type

### Pour chaque nouvelle fonctionnalité :

1. **Clarification** : Poser les questions nécessaires
2. **Test** : Écrire les tests d'abord (TDD)
3. **Implémentation** : Développer le code
4. **Documentation** : Documenter le code
5. **README** : Mettre à jour la documentation utilisateur
6. **Prompt** : Sauvegarder la conversation dans le bon fichier

### Pour les décisions techniques :

1. **Analyse** : Identifier les options possibles
2. **Présentation** : Expliquer les alternatives
3. **Question** : Demander votre préférence
4. **Justification** : Expliquer le choix retenu
5. **Documentation** : Documenter la décision

## 📚 Organisation de la documentation

```
docs/
├── interaction-rules.md     # Ce fichier
├── prompts/                 # Historique des conversations
│   ├── gameplay-prompts.md
│   ├── ui-prompts.md
│   ├── tests-prompts.md
│   ├── architecture-prompts.md
│   └── debugging-prompts.md
├── decisions/               # Décisions techniques importantes
├── learning/                # Notes d'apprentissage Python/GameDev
└── tdd/                     # Documentation TDD et stratégies de test
```

## 🎯 Objectifs de cette approche

1. **Qualité** : Code bien testé et documenté
2. **Apprentissage** : Montée en compétence continue
3. **Collaboration** : Décisions prises ensemble
4. **Traçabilité** : Historique complet du développement
5. **Maintenabilité** : Code facile à comprendre et modifier

## ❓ Questions pour commencer

Avant de continuer, j'aimerais clarifier quelques points :

1. **Priorité des fonctionnalités** : Par quelle fonctionnalité voulez-vous commencer ? (affichage de base, mouvement des pièces, détection de collision, etc.)

2. **Niveau de complexité initial** : Préférez-vous commencer par une version très simple (juste affichage) ou directement avec les mécaniques de base ?

3. **Framework graphique** : Confirmez-vous le choix de Pygame ou avez-vous une préférence pour un autre framework ?

4. **Structure des tests** : Voulez-vous utiliser unittest (standard Python) ou pytest ?

5. **Environnement de développement** : Avez-vous des préférences pour l'organisation du code (classes, modules, etc.) ?

Ces règles sont-elles claires et complètes selon vos attentes ?
