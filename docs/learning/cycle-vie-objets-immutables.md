# Gestion des instances immutables - Cycle de vie des objets Position

## Date : 27 juillet 2025

## 🎯 **Que devient l'ancienne instance après déplacement ?**

### **Réponse courte :**
L'ancienne instance **reste intacte** et sera **automatiquement supprimée** par le Garbage Collector de Python quand plus rien ne la référence.

## 🔍 **Démonstration détaillée**

### **1. Création et déplacement - Étape par étape**

```python
# Étape 1 : Création de la position originale
pos_originale = Position(5, 10)
print(f"Position originale : {pos_originale}")
print(f"ID mémoire : {id(pos_originale)}")

# Étape 2 : "Déplacement" (création d'une nouvelle instance)
pos_deplacee = pos_originale.deplacer(2, -1)
print(f"Position déplacée : {pos_deplacee}")
print(f"ID mémoire : {id(pos_deplacee)}")

# Étape 3 : Vérification que l'originale existe toujours
print(f"Position originale après déplacement : {pos_originale}")
print(f"Les deux objets sont différents : {id(pos_originale) != id(pos_deplacee)}")
```

**Résultat :**
```
Position originale : Position(x=5, y=10)
ID mémoire : 140234567890123
Position déplacée : Position(x=7, y=9)
ID mémoire : 140234567890456
Position originale après déplacement : Position(x=5, y=10)
Les deux objets sont différents : True
```

### **2. Cycle de vie des références**

```python
def demontrer_cycle_vie():
    # 1. Création - 1 référence vers Position(5, 10)
    pos1 = Position(5, 10)
    print(f"Référence 1 créée : {pos1}")
    
    # 2. Deuxième référence vers le MÊME objet
    pos2 = pos1
    print(f"Référence 2 créée : {pos2}")
    print(f"Même objet ? {pos1 is pos2}")  # True
    
    # 3. Déplacement - création d'un NOUVEL objet
    pos3 = pos1.deplacer(1, 0)
    print(f"Nouvel objet créé : {pos3}")
    print(f"Ancien objet toujours là : {pos1}")
    
    # 4. Suppression d'une référence
    del pos1  # pos2 existe encore, Position(5, 10) reste en mémoire
    print(f"pos1 supprimée, pos2 existe : {pos2}")
    
    # 5. Suppression dernière référence
    del pos2  # Plus aucune référence, Position(5, 10) sera supprimée par GC
    print(f"Nouvel objet seul survivant : {pos3}")
    
    # Position(5, 10) est maintenant éligible pour le Garbage Collection
```

### **3. Comparaison avec les objets mutables**

```python
# MUTABLE (liste) - Modification en place
liste = [1, 2, 3]
id_original = id(liste)
liste.append(4)  # Modifie l'objet existant
print(f"Même objet après modification : {id(liste) == id_original}")  # True

# IMMUTABLE (Position) - Création de nouveaux objets
pos = Position(5, 10)
id_original = id(pos)
nouvelle_pos = pos.deplacer(1, 0)  # Crée un NOUVEL objet
print(f"Même objet après déplacement : {id(pos) == id_original}")  # True
print(f"Nouvel objet créé : {id(nouvelle_pos) != id_original}")  # True
```

## 🧠 **Gestion automatique de la mémoire**

### **Garbage Collection Python**

```python
import gc

def observer_garbage_collection():
    # Créer plusieurs positions
    positions = []
    for i in range(5):
        pos = Position(i, i * 2)
        positions.append(pos)
    
    print(f"5 positions créées : {len(positions)}")
    
    # Créer de nouvelles positions par déplacement
    nouvelles_positions = []
    for pos in positions:
        nouvelle_pos = pos.deplacer(10, 10)
        nouvelles_positions.append(nouvelle_pos)
    
    # Maintenant on a 10 objets Position en mémoire
    print("10 objets Position existent maintenant")
    
    # Supprimer les références aux anciennes positions
    del positions  # Les 5 premières positions deviennent éligibles au GC
    
    # Forcer le garbage collection
    objets_collectes = gc.collect()
    print(f"Objets supprimés par GC : {objets_collectes}")
    
    return nouvelles_positions  # Seules les nouvelles restent
```

### **Optimisations Python automatiques**

```python
# Python optimise certains cas
pos1 = Position(0, 0)
pos2 = Position(0, 0)

# Pour les petites valeurs, Python PEUT réutiliser les objets
# (mais ce n'est pas garanti avec nos objets personnalisés)
print(f"Même objet ? {pos1 is pos2}")  # Probablement False

# Mais l'égalité fonctionne toujours
print(f"Valeurs égales ? {pos1 == pos2}")  # True
```

## 🎮 **Impact sur Tetris**

### **1. Avantage : Sécurité totale**

```python
def deplacer_piece_securise(positions_piece: List[Position]) -> List[Position]:
    # Les positions originales ne peuvent PAS être modifiées
    nouvelles_positions = []
    for pos in positions_piece:
        nouvelle_pos = pos.deplacer(0, 1)  # Chute d'une ligne
        nouvelles_positions.append(nouvelle_pos)
    
    # positions_piece reste intacte !
    return nouvelles_positions

# Usage
piece_positions = [Position(5, 0), Position(6, 0), Position(7, 0)]
piece_apres_chute = deplacer_piece_securise(piece_positions)

# GARANTIE : piece_positions n'a pas changé
print(f"Positions originales intactes : {piece_positions}")
print(f"Nouvelles positions : {piece_apres_chute}")
```

### **2. Gestion des états précédents**

```python
class HistoriqueMouvements:
    def __init__(self):
        self.historique: List[List[Position]] = []
    
    def sauvegarder_etat(self, positions: List[Position]):
        # Sécurisé : les positions ne peuvent pas changer
        self.historique.append(positions.copy())
    
    def annuler_dernier_mouvement(self) -> List[Position]:
        if self.historique:
            return self.historique.pop()
        return []

# Les anciennes positions restent intactes dans l'historique !
```

### **3. Cache et optimisations**

```python
# Cache des calculs de collision
cache_collisions = {}

def calculer_collision(position: Position, plateau) -> bool:
    # Grâce à l'immutabilité, on peut utiliser position comme clé
    if position in cache_collisions:
        return cache_collisions[position]
    
    resultat = # ... calcul complexe ...
    cache_collisions[position] = resultat
    return resultat

# La position ne changera JAMAIS, le cache est sûr !
```

## ⚡ **Performance et mémoire**

### **Questions légitimes :**

**Q : "Créer de nouveaux objets, ce n'est pas lent ?"**
- **R :** Pour des objets simples comme Position, c'est très rapide
- Position contient juste 2 entiers, presque gratuit à créer
- Python optimise la création d'objets

**Q : "Ça consomme plus de mémoire ?"**
- **R :** Momentanément oui, mais le GC nettoie automatiquement
- Pour un jeu Tetris, négligeable (quelques dizaines de positions max)
- Le gain en sécurité compense largement

**Q : "Et si j'ai des millions de positions ?"**
- **R :** Alors là, il faudrait considérer d'autres approches
- Mais pour Tetris : total overkill de s'inquiéter

### **🚨 QUESTION CRUCIALE : Fuite mémoire sans `del` ?**

**Q : "Risque de fuite mémoire si j'oublie de faire `del` ?"**
- **R : NON ! Aucun risque de fuite mémoire !** 🎯

#### **Démonstration pratique :**

```python
def demonstration_sans_del():
    # Scénario typique dans Tetris
    position_piece = Position(5, 10)
    
    # Déplacement sans del explicite
    position_piece = position_piece.deplacer(1, 0)  # Gauche
    position_piece = position_piece.deplacer(0, 1)  # Bas
    position_piece = position_piece.deplacer(-1, 0) # Droite
    position_piece = position_piece.deplacer(0, 1)  # Bas
    
    # À chaque ligne, l'ancienne position est AUTOMATIQUEMENT
    # marquée pour suppression par le GC !
    
    return position_piece  # Position finale : (5, 12)

# Toutes les positions intermédiaires sont automatiquement nettoyées !
```

#### **Pourquoi PAS de fuite mémoire :**

**1. Réassignation automatique :**
```python
pos = Position(5, 10)        # pos référence Position(5, 10)
pos = pos.deplacer(1, 0)     # pos référence maintenant Position(6, 10)
                             # Position(5, 10) n'a plus AUCUNE référence
                             # → Éligible au GC AUTOMATIQUEMENT
```

**2. Variables locales dans les fonctions :**
```python
def deplacer_piece():
    pos = Position(5, 10)
    pos = pos.deplacer(1, 0)
    return pos
    # Quand la fonction se termine, toutes les variables locales
    # sont automatiquement supprimées → GC automatique !

nouvelle_pos = deplacer_piece()  # Aucune fuite !
```

**3. Boucles et itérations :**
```python
positions_historique = []
pos = Position(5, 10)

for i in range(100):
    pos = pos.deplacer(0, 1)  # Chute de 100 lignes
    if i % 10 == 0:  # Sauvegarder tous les 10 mouvements
        positions_historique.append(pos)

# Seules 10 positions sont gardées en mémoire
# Les 90 autres sont automatiquement supprimées !
```

#### **Vraies fuites mémoire (à éviter) :**

```python
# ❌ MAUVAIS : Accumulation inutile
toutes_positions = []  # Liste qui grandit sans limite
pos = Position(5, 10)

for i in range(1000000):
    pos = pos.deplacer(0, 1)
    toutes_positions.append(pos)  # Garde TOUTES les positions !
    
# Ici oui, fuite mémoire car on accumule volontairement

# ✅ BON : Usage normal
pos = Position(5, 10)
for i in range(1000000):
    pos = pos.deplacer(0, 1)  # Seule la dernière position reste !
```

#### **Le `del` explicite : quand l'utiliser :**

```python
# Dans 99% des cas : PAS BESOIN de del
pos = Position(5, 10)
pos = pos.deplacer(1, 0)  # L'ancienne est automatiquement nettoyée

# del explicite : SEULEMENT dans des cas très spécifiques
grande_structure = {
    'positions': [Position(x, y) for x in range(1000) for y in range(1000)],
    'cache': {...},  # Beaucoup de données
    'historique': [...]
}

# Si vous voulez libérer immédiatement cette grosse structure :
del grande_structure  # Optionnel, mais peut être utile

# Mais pour des objets simples comme Position : INUTILE !
```

## 💡 **Résumé**

### **Ce qui arrive à l'ancienne instance :**

1. **Elle reste intacte** tant qu'une variable la référence
2. **Elle devient éligible au GC** quand plus rien ne la référence
3. **Python la supprime automatiquement** pour libérer la mémoire
4. **Vous n'avez rien à faire** - tout est automatique !

### **Avantages pour Tetris :**
- ✅ **Sécurité** : Aucun effet de bord possible
- ✅ **Simplicité** : Pas de gestion manuelle de la mémoire
- ✅ **Prédictibilité** : Le comportement est toujours le même
- ✅ **Cache** : Objets utilisables comme clés de dictionnaire

**L'immutabilité est un choix architectural qui privilégie la sécurité et la simplicité sur une micro-optimisation prématurée !** 🎯
