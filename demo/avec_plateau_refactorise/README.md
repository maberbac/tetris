# Démonstrations avec Plateau Refactorisé

Ce répertoire contient toutes les démonstrations Tetris utilisant le **vrai plateau refactorisé** au lieu des classes `PlateauDemoX` personnalisées.

## 🎯 Avantages de la refactorisation

### ✅ **Code plus propre**
- Suppression des classes `PlateauDemoI`, `PlateauDemoO`, etc.
- Utilisation directe de `Plateau(6, 6)` 
- Élimination de la duplication de code

### ✅ **Fonctionnalités complètes**
- **Détection automatique des lignes complètes** 🎉
- **Suppression des lignes pleines**
- **Descente automatique des lignes au-dessus**
- Toutes les fonctionnalités du vrai plateau

### ✅ **Intégration architecturale**
- Compatible avec le gestionnaire d'événements
- Utilise les vraies commandes du projet
- Cohérent avec l'architecture globale

## 📁 Structure

```
demo/avec_plateau_refactorise/
├── README.md                    # Ce fichier
├── lanceur_demos.py            # Script de lancement interactif
├── demo_i_avec_plateau.py      # Démo pièce I ✅
├── demo_o_avec_plateau.py      # Démo pièce O ✅  
├── demo_t_avec_plateau.py      # Démo pièce T (à venir)
├── demo_s_avec_plateau.py      # Démo pièce S (à venir)
├── demo_z_avec_plateau.py      # Démo pièce Z (à venir)
├── demo_j_avec_plateau.py      # Démo pièce J (à venir)
└── demo_l_avec_plateau.py      # Démo pièce L (à venir)
```

## 🚀 Utilisation

### Méthode 1 : Lanceur interactif (recommandé)
```bash
cd demo/avec_plateau_refactorise
python lanceur_demos.py
```

### Méthode 2 : Lancement direct
```bash
cd demo/avec_plateau_refactorise
python demo_i_avec_plateau.py  # Pièce I
python demo_o_avec_plateau.py  # Pièce O
```

## 🎮 Contrôles

Toutes les démos utilisent les mêmes contrôles :

- **← →** : Déplacer gauche/droite
- **↑** : Rotation
- **↓** : Descendre
- **Espace** : Chute rapide (jusqu'en bas)
- **Entrée** : Placer la pièce manuellement
- **P** : Pause/Reprendre
- **ESC** : Menu/Quitter

## 💡 Différences avec les anciennes démos

| Aspect | Anciennes démos | Nouvelles démos |  
|--------|----------------|-----------------|
| **Plateau** | `PlateauDemoX` personnalisé | `Plateau(6, 6)` refactorisé |
| **Lignes complètes** | ❌ Non détectées | ✅ Détection automatique |
| **Code** | Duplication importante | Code mutualisé et propre |
| **Architecture** | Isolé | Intégré complètement |

## 🔧 Développement

### Template pour nouvelles pièces

Pour créer une démo pour une nouvelle pièce, copier `demo_i_avec_plateau.py` et :

1. Remplacer `I` par la lettre de la pièce (`T`, `S`, etc.)
2. Changer `TypePiece.I` vers `TypePiece.X`
3. Ajuster la couleur dans la classe d'affichage
4. Tester et ajouter au lanceur

### Points clés d'implémentation

- **Moteur** : Hérite de `MoteurJeu` pour compatibilité
- **Commandes** : Utilisent le pattern Command
- **Gestionnaire** : Étend `GestionnaireEvenements`
- **Plateau** : Utilise `Plateau(6, 6)` directement

## 🎉 Résultats

Grâce à la refactorisation :
- **Moins de code** à maintenir
- **Plus de fonctionnalités** (lignes complètes)
- **Meilleure cohérence** avec l'architecture
- **Expérience utilisateur** plus riche

---

🎯 **Ces démos montrent concrètement les bénéfices de la refactorisation du plateau !**
