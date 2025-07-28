# Stratégie TDD pour Tetris - Architecture hexagonale

## Date de mise à jour : 28 juillet 2025

## ✅ **Phases réalisées (TDD complet)**

### Phase 1 : Value Objects du domaine ✅
1. **Position (Value Object)** - 5 tests passants
   - ✅ Création avec coordonnées x, y
   - ✅ Déplacement (immutable) → nouvelle instance
   - ✅ Égalité par valeur (@dataclass génère __eq__)
   - ✅ Immutabilité garantie (frozen=True)
   - ✅ Vérification dans limites du plateau

### Phase 2 : Entities avec héritage ✅  
1. **Piece abstraite (ABC)** - Classe de base
   - ✅ Template Method Pattern
   - ✅ Factory Method abstrait
   - ✅ Déplacement commun (Entity behavior)
   
2. **PieceI (Entity)** - 5 tests passants
   - ✅ Création via factory method
   - ✅ Déplacement mutable (Entity vs Value Object)
   - ✅ Rotation horizontal ↔ vertical
   - ✅ Pivot fixe pendant rotation
   - ✅ Type et positions correctes

## 🔄 **Phases en cours**

### Phase 3 : Comportements spécialisés (TDD) ✅
1. **Rotation PieceI** ✅
   - ✅ Test : Rotation horizontal ↔ vertical
   - ✅ Implémentation : Logic rotation autour pivot
   
2. **PieceO (carré)** ✅
   - ✅ Test : Création positions carré 2x2
   - ✅ Test : Rotation = no-op (carré)
   - ✅ Démonstration polymorphisme

### Phase 4 : Factory Pattern complet
1. **FabriquePieces** 🔄
   - 🔄 Test : Création aléatoire
   - 🔄 Test : Création par type spécifique
   - 🔄 Implémentation : Pattern Factory

## 📋 **Phases planifiées**

### Phase 5 : Plateau de jeu (Entity)
1. **Plateau** : Grille 10x20 avec état
2. **Collision** : Détection limites et blocs occupés
3. **Lignes complètes** : Détection et suppression

### Phase 6 : Ports (interfaces)
1. **AffichagePort** : Interface affichage
2. **InputPort** : Interface contrôles
3. **SauvegardePort** : Interface persistence

### Phase 7 : Adapters (implémentation)
1. **PygameAdapter** : Affichage graphique
2. **ConsoleAdapter** : Affichage texte
3. **FichierAdapter** : Sauvegarde locale

### Phase 8 : Services du domaine
1. **ServiceJeu** : Logique métier principale
2. **GestionnaireCollisions** : Détection collisions
3. **CalculateurScore** : Système de points

## 🏗️ **Structure actuelle des tests**

### Organisation par module (hexagonale)
```
tests/
├── test_domaine/
│   ├── test_entites/
│   │   ├── test_position.py         # 5 tests ✅
│   │   └── test_pieces/
│   │       ├── test_piece_i.py      # 5 tests ✅
│   │       └── test_piece_o.py      # À venir 🔄
│   ├── test_services/               # À venir
│   └── test_objets_valeur/          # À venir
├── test_ports/                      # À venir
└── test_adapters/                   # À venir
```

### Conventions TDD appliquées
- **Fichiers** : `test_[module].py`
- **Classes** : `Test[Entite]` 
- **Méthodes** : `test_[comportement]_[condition]_[resultat]`
- **Languge** : Français pour la lisibilité métier

### Exemples concrets réalisés
```python
# Value Object - Création nouvelle instance
def test_position_peut_se_deplacer(self):
    pos = Position(5, 5)
    nouvelle_pos = pos.deplacer(2, -1)
    # Vérifie immutabilité et nouvelle instance

# Entity - Mutation d'état  
def test_piece_i_peut_se_deplacer(self):
    piece = PieceI.creer(x_spawn=5, y_spawn=0)
    piece.deplacer(1, 2)  # Mute l'instance
    # Vérifie changement d'état sur même objet
```

## 🎯 **Stratégies de test par type**

### 1. Value Objects (immutables)
```python
def test_value_object_deplacer_cree_nouvelle_instance():
    # Arrange
    original = Position(5, 10)
    
    # Act  
    nouveau = original.deplacer(1, 0)
    
    # Assert
    assert nouveau != original  # Nouvelle instance
    assert original == Position(5, 10)  # Original inchangé
```

### 2. Entities (mutables) 
```python
def test_entity_deplacer_mute_instance():
    # Arrange
    piece = PieceI.creer(5, 0)
    positions_initiales = piece.positions.copy()
    
    # Act
    piece.deplacer(1, 0)  # Mutation
    
    # Assert  
    assert piece.positions != positions_initiales  # État changé
```

### 3. Classes abstraites (comportement)
```python
def test_piece_abstraite_deplacer_toutes_positions():
    # Test du comportement commun dans classe abstraite
    # Applicable à toutes les pièces concrètes
    pass
```

## 🔄 **Cycle TDD appliqué**

### 1. RED (Test qui échoue)
```python
def test_piece_i_peut_tourner():
    piece = PieceI.creer(5, 0)
    piece.tourner()  # ❌ Pas encore implémenté
    # Assertions sur nouvelle orientation
```

### 2. GREEN (Implémentation minimale)
```python
def tourner(self) -> None:
    # Code minimal pour faire passer le test
    pass  # ou logique basique
```

### 3. REFACTOR (Amélioration code)
```python
def tourner(self) -> None:
    # Code final optimisé et documenté
    if self._est_horizontal():
        self._devenir_vertical()
    else:
        self._devenir_horizontal()
```

## 🧪 **Isolation et mocking**

### Tests isolés (pas de dépendances)
```python
# Domaine pur - pas de mocking nécessaire
def test_position_dans_limites():
    pos = Position(5, 8)
    assert pos.dans_limites(10, 20) == True
```

### Tests avec dépendances (future)
```python
@unittest.mock.patch('adapters.pygame_adapter')
def test_affichage_piece_sans_pygame(mock_adapter):
    # Test affichage sans dépendance pygame
    pass
```

## 📊 **Métriques qualité actuelles**

### Couverture de code
- **Domaine/entites** : 100% (Position, PieceI)
- **Tests/domaine** : 10 tests, 100% passants
- **Architecture** : Hexagonale respectée

### Types de tests réalisés
- ✅ **Unit tests** : Méthodes individuelles testées
- 🔄 **Integration tests** : À venir (ports + adapters)
- 🔄 **End-to-end tests** : À venir (scénarios complets)

## 🛠️ **Outils et frameworks**

### Framework actuel : unittest ✅
```python
# Assertions utilisées
self.assertEqual(piece.type_piece, TypePiece.I)
self.assertNotEqual(piece.positions, positions_initiales)
self.assertTrue(position.dans_limites(10, 20))
```

### Alternative considérée : pytest
```python
# Syntaxe pytest (si migration future)
assert piece.type_piece == TypePiece.I
assert piece.positions != positions_initiales
assert position.dans_limites(10, 20)
```

## 💡 **Lessons learned TDD**

### ✅ Bonnes pratiques confirmées
1. **Tests d'abord** → Force meilleure conception API
2. **Petits cycles** → Progression constante visible
3. **Nommage explicite** → Tests servent de documentation
4. **Isolation** → Tests domaine sans dépendances externes

### 🔧 Améliorations identifiées
1. **Setup commun** : Fixtures pour création objets test
2. **Tests paramétrés** : Plusieurs cas en un test
3. **Assertions custom** : Messages d'erreur métier
4. **Performance** : Benchmark pour algos complexes

---

**Cette stratégie TDD évolue avec le projet, guidée par l'architecture hexagonale et les besoins métier Tetris ! 🎮**

### Pour unittest
```python
# Assertions courantes
self.assertEqual(a, b)
self.assertTrue(condition)
self.assertRaises(Exception, function)
```

### Pour pytest
```python
# Fixtures
@pytest.fixture
def empty_board():
    return Board()

# Assertions
assert board.width == 10
with pytest.raises(ValueError):
    piece.move_to(-1, 0)
```
