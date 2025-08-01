# 🗺️ Navigation de la documentation Tetris

## 📁 Structure de la documentation organisée

```
tetris/
├── README.md                    # 🎮 Vue d'ensemble du jeu uniquement
├── DOC_TECHNIQUE.md             # 🔧 Documentation technique du jeu
├── docs/                        # 📚 Documentation d'apprentissage
│   ├── learning/               # 🎓 Contenu pédagogique principal
│   │   ├── README.md           # Guide d'apprentissage 
│   │   └── INDEX.md            # Index du contenu éducatif
│   ├── patterns/               # 🔧 Design patterns détaillés
│   │   ├── registry-pattern.md
│   │   └── decorateurs-python.md
│   ├── tdd/                    # 🧪 Stratégies de test
│   ├── INDEX_LECONS.md         # 📋 Chronologie des leçons
│   └── README.md               # Vue d'ensemble de la documentation
├── src/                        # 💻 Code source
└── tests/                      # 🧪 Tests automatisés
```

## 🎯 Points d'entrée selon votre objectif

### 🎮 **Utiliser/comprendre le jeu**
→ Commencez par [../README.md](../README.md) puis [../DOC_TECHNIQUE.md](../DOC_TECHNIQUE.md)

### 🎓 **Apprendre l'architecture**
→ Commencez par [learning/README.md](learning/README.md)

### 📚 **Étudier les patterns**
→ Allez directement à [patterns/](patterns/)

### 🧪 **Comprendre les tests**
→ Consultez [tdd/testing-strategy.md](tdd/testing-strategy.md)

### 📋 **Suivre la progression**
→ Voir [INDEX_LECONS.md](INDEX_LECONS.md) ou [journal-developpement.md](journal-developpement.md)

## 📊 État actuel

- **75 tests** passent (100% ✅) en 0.019s
- **7 pièces** complètement implémentées : I, O, T, S, Z, J, L
- **Registry Pattern** avec auto-enregistrement
- **Architecture hexagonale** respectée
- **Documentation entièrement synchronisée**
- **Projet complètement stable et fonctionnel**

## 🎓 Consignes d'organisation

- **Tout contenu .md d'apprentissage** → `docs/` ou ses sous-répertoires
- **Seules exceptions** :
  - `README.md` (racine) → Présentation du jeu uniquement
  - `DOC_TECHNIQUE.md` (racine) → Documentation technique du jeu
- **Navigation** : Ce fichier pour orienter dans la documentation

---

> Cette organisation sépare clairement le **jeu** de l'**apprentissage** 🎯
