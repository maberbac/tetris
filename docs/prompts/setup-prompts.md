# Historique des prompts - Configuration initiale

## Date : 27 juillet 2025

### Prompt 1 : Modification du README initial
**Demande** : "Je veux modifier le readme pour ajouter une description à mon jeu Tetris."
**Action** : Ajout d'une description complète du jeu Tetris avec fonctionnalités, instructions et installation.

### Prompt 2 : Changement de langage
**Demande** : "il sera développé en python"
**Action** : Modification du README pour remplacer JavaScript par Python et adapter les instructions d'installation.

### Prompt 3 : Création du guide technique
**Demande** : "je veux que tu crée un autre .md qui va te servir d'un guide pour mieux connaitre mon programme"
**Action** : Création du fichier GUIDE.md avec l'architecture technique complète du projet.

### Prompt 4 : Définition des règles d'interaction
**Demande** : Création d'un répertoire avec règles d'interaction incluant :
- Documentation des prompts
- Clarification systématique
- Choix collaboratif
- Mise à jour README
- Organisation thématique
- Documentation du code
- Apprentissage Python/GameDev
- Support développement IA
- Méthodologie TDD

**Action** : 
- Création du répertoire `docs/` avec structure complète
- Création du fichier `interaction-rules.md` avec toutes les règles
- Création des sous-répertoires : prompts/, decisions/, learning/, tdd/
- Création de ce fichier d'historique

### Réponses aux questions de configuration

1. **Fonctionnalité de départ** : Affichage basique d'une grille vide
2. **Complexité** : Version minimale fonctionnelle puis enrichissement progressif
3. **Framework graphique** : Pygame (confirmé)
4. **Tests** : unittest principalement + quelques tests pytest pour apprentissage
5. **Structure** : Combinaison OOP + MVC + Observer + Listener pour touches
6. **Environnement** : Python installé, exécution via bouton Run de VS Code

### Spécifications détaillées - Grille d'affichage

**Fenêtre** :
- Taille : Plein écran automatique
- Arrière-plan : Noir (#000000)

**Grille** :
- Dimensions : 10x20 cellules
- Taille cellule : 30px × 30px
- Fond grille : Gris (#C0C0C0)
- Contours cellules : Blanc (#FFFFFF)
- Lignes : Fines mais visibles

**Approche** : TDD strict - créer seulement ce qui est nécessaire à chaque itération

**Pygame** : Déjà installé

### Prompt 5 : Convention de nommage en français
**Demande** : "ajoute une règle de toujours choisir les nom de méthodes et variables en français"
**Action** : 
- Ajout de la règle 6.1 dans interaction-rules.md
- Refactorisation du code existant :
  - `display.py` → `affichage.py`
  - `test_display.py` → `test_affichage.py`
  - Variables anglaises → françaises (screen → ecran, etc.)
  - Méthodes anglaises → françaises (draw_grid → dessiner_grille, etc.)
- Mise à jour du GUIDE.md avec la nouvelle structure
- Création de `demo_grille.py` pour tester l'affichage

### Prompt 7 : Francisation complète et exception pour main
**Demande** : "avant de continuer je veux que d'abord on repasse toutes les méthodes, variables, nom de fichiers en français et aussi met à jour la règle concernant le français pour qu'on utilise l'anglais seulement s'il n'y a aucun équivalent en français"
**Action** :
- Mise à jour de la règle 6.1 pour être plus stricte sur le français
- Francisation complète de tous les noms :
  - Classes : Display → Affichage
  - Méthodes : draw_grid → dessiner_grille, etc.
  - Variables : screen → ecran, etc.
  - Constantes : BLACK → COULEUR_NOIR, etc.
  - Tests : test_display → test_affichage, etc.

**Demande** : "ajoute une exception pour les méthodes main, je préfère les gardé en anglais (main) au lieu de les traduire."
**Action** :
- Ajout d'exceptions pour les conventions universelles (main, __init__, etc.)
- Correction des fichiers demo pour utiliser main() au lieu de principal()
- Création du rapport de francisation complet

### État actuel
- ✅ Convention française stricte établie
- ✅ Code 100% francisé (sauf exceptions justifiées)
- ✅ Tests fonctionnels avec noms français
- ✅ Prêt pour continuer le développement TDD
