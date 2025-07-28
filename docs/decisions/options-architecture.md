# Options d'architecture pour le projet Tetris

## Date : 27 juillet 2025

## Contexte
Projet Tetris en Python avec :
- Approche TDD (Test Driven Development)
- Entités métier (Pièces, Grille, Zone de jeu)
- Logique de jeu complexe
- Interface graphique (Pygame)

## Option 1 : Architecture par couches (Recommandée)

```
tetris/
├── src/                    # Code source principal
│   ├── entites/           # Entités métier (Domain)
│   │   ├── __init__.py
│   │   ├── piece.py       # Classe Piece
│   │   ├── plateau.py     # Classe Plateau
│   │   ├── zone_jeu.py    # Classe ZoneJeu
│   │   └── position.py    # Classe Position
│   ├── logique/           # Logique métier (Business Logic)
│   │   ├── __init__.py
│   │   ├── moteur_jeu.py  # Logique principale du jeu
│   │   ├── detecteur_collision.py
│   │   ├── gestionnaire_lignes.py
│   │   └── calculateur_score.py
│   ├── interface/         # Interface utilisateur (Presentation)
│   │   ├── __init__.py
│   │   ├── affichage.py   # Rendu graphique
│   │   ├── gestionnaire_evenements.py
│   │   └── interface_jeu.py
│   ├── utilitaires/       # Utilitaires transversaux
│   │   ├── __init__.py
│   │   ├── constantes.py
│   │   └── outils.py
│   └── __init__.py
├── tests/                 # Tests organisés par couches
│   ├── test_entites/
│   │   ├── test_piece.py
│   │   ├── test_plateau.py
│   │   └── test_zone_jeu.py
│   ├── test_logique/
│   │   ├── test_moteur_jeu.py
│   │   ├── test_detecteur_collision.py
│   │   └── test_gestionnaire_lignes.py
│   ├── test_interface/
│   │   └── test_affichage.py
│   └── test_integration/
│       └── test_jeu_complet.py
├── demos/                 # Fichiers de démonstration
│   ├── demo_pieces.py
│   └── demo_plateau.py
├── docs/                  # Documentation
└── tetris.py             # Point d'entrée principal
```

**Avantages :**
- Séparation claire des responsabilités
- Facilite les tests unitaires
- Code réutilisable
- Évolutif et maintenable

## Option 2 : Architecture par fonctionnalités

```
tetris/
├── pieces/
│   ├── __init__.py
│   ├── piece.py
│   ├── types_pieces.py
│   ├── test_piece.py
│   └── test_types_pieces.py
├── plateau/
│   ├── __init__.py
│   ├── plateau.py
│   ├── gestionnaire_lignes.py
│   ├── test_plateau.py
│   └── test_gestionnaire_lignes.py
├── affichage/
│   ├── __init__.py
│   ├── affichage.py
│   ├── rendu_pieces.py
│   └── test_affichage.py
├── jeu/
│   ├── __init__.py
│   ├── moteur_jeu.py
│   ├── evenements.py
│   └── test_moteur_jeu.py
├── commun/
│   ├── constantes.py
│   └── utilitaires.py
└── tetris.py
```

**Avantages :**
- Tests près du code qu'ils testent
- Fonctionnalités auto-contenues
- Facile à comprendre

## Option 3 : Architecture MVC + DDD

```
tetris/
├── domaine/              # Domain Driven Design
│   ├── entites/
│   │   ├── piece.py
│   │   └── plateau.py
│   ├── services/
│   │   ├── service_jeu.py
│   │   └── service_collision.py
│   └── valeurs/
│       ├── position.py
│       └── couleur.py
├── application/          # Cas d'usage
│   ├── commandes/
│   │   ├── deplacer_piece.py
│   │   └── faire_tourner_piece.py
│   └── requetes/
│       └── obtenir_etat_jeu.py
├── infrastructure/       # Technique
│   ├── affichage/
│   │   └── affichage_pygame.py
│   └── evenements/
│       └── gestionnaire_clavier.py
├── tests/
│   ├── domaine/
│   ├── application/
│   └── infrastructure/
└── tetris.py
```

**Avantages :**
- Architecture d'entreprise
- Très maintenable
- Testabilité maximale

## Recommandation : Option 1 (Architecture par couches)

### Pourquoi cette option ?

1. **Parfaite pour TDD** :
   - Tests unitaires faciles pour chaque couche
   - Isolation des dépendances
   - Mocking simplifié

2. **Séparation claire** :
   - **Entités** : Objets métier purs (Piece, Plateau)
   - **Logique** : Algorithmes de jeu (collision, score)
   - **Interface** : Affichage et événements

3. **Évolutive** :
   - Ajout de nouvelles fonctionnalités simple
   - Changement d'interface possible (console, web)
   - Réutilisation du code métier

4. **Apprentissage progressif** :
   - Commence par les entités simples
   - Ajoute la logique progressivement
   - Interface en dernier

### Structure détaillée recommandée

```python
# Exemple de dépendances
entites/ (pas de dépendances)
    ↑
logique/ (dépend des entités)
    ↑
interface/ (dépend de logique et entités)
```

### Plan TDD avec cette architecture

1. **Phase 1 - Entités** :
   - `test_piece.py` → `piece.py`
   - `test_plateau.py` → `plateau.py`
   - `test_position.py` → `position.py`

2. **Phase 2 - Logique** :
   - `test_detecteur_collision.py` → `detecteur_collision.py`
   - `test_moteur_jeu.py` → `moteur_jeu.py`

3. **Phase 3 - Interface** :
   - `test_affichage.py` → `affichage.py` (déjà fait !)

## Questions pour valider le choix

1. **Préférez-vous** cette architecture par couches ?
2. **Complexité** : Êtes-vous à l'aise avec cette structure ?
3. **Alternative** : Préférez-vous une structure plus simple ?
4. **Point de départ** : Par quelle entité voulez-vous commencer ?

## Étapes de migration

Si vous acceptez cette architecture :

1. Créer la structure de dossiers
2. Déplacer `affichage.py` vers `src/interface/`
3. Créer les premiers tests d'entités
4. Développer en TDD couche par couche
