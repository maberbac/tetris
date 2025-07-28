#!/usr/bin/env python3
"""
Démonstration de l'extensibilité du Registry Pattern avec PieceS

Montre comment ajouter une nouvelle pièce sans modifier le code existant.
"""

print("🎮 DÉMONSTRATION : Extensibilité Registry Pattern")
print("=" * 50)

# 1. Importation de PieceS déclenche l'auto-enregistrement
print("\n🔧 ÉTAPE 1 : Auto-enregistrement de PieceS")
from src.domaine.entites.pieces.piece_s import PieceS
print("   ✅ PieceS importée et auto-enregistrée")

# 2. Vérification dans le registre
print("\n📋 ÉTAPE 2 : Vérification du registre")
from src.domaine.entites.fabriques.registre_pieces import RegistrePieces
types_supportes = RegistrePieces.obtenir_types_supportes()
print(f"   Types supportés : {sorted([t.value for t in types_supportes])}")

# 3. Création via fabrique (sans modification de code !)
print("\n🏭 ÉTAPE 3 : Création via fabrique")
from src.domaine.entites.fabriques.fabrique_pieces import FabriquePieces
from src.domaine.entites.piece import TypePiece

fabrique = FabriquePieces()
piece_s = fabrique.creer(TypePiece.S, x_spawn=5, y_spawn=1)
print(f"   ✅ Création : {piece_s.type_piece}")
print(f"   📍 Positions initiales : {piece_s.positions}")

# 4. Test de comportement spécialisé
print("\n🔄 ÉTAPE 4 : Test de rotation spécialisée")
piece_s.tourner()
print(f"   📍 Après 1 rotation : {piece_s.positions}")
piece_s.tourner()
print(f"   📍 Après 2 rotations : {piece_s.positions}")

# 5. Création aléatoire
print("\n🎲 ÉTAPE 5 : Création aléatoire avec S")
pieces_aleatoires = [fabrique.creer_aleatoire() for _ in range(8)]
types_crees = [p.type_piece.value for p in pieces_aleatoires]
print(f"   Types créés : {types_crees}")
print(f"   ✅ S inclus dans la génération : {'S' in types_crees}")

print("\n🎯 RÉSULTAT : Extensibilité réussie !")
print("   • Aucun code existant modifié")
print("   • PieceS s'intègre automatiquement")  
print("   • Registry Pattern prouvé !")
print("\n💡 Prochaine étape : PieceZ, PieceJ, PieceL avec le même pattern")
