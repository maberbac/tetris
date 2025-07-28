"""
Démonstration du fonctionnement du décorateur @piece_tetris.

Ce script montre étape par étape comment l'auto-enregistrement fonctionne.
"""

# Simulons le processus step-by-step
print("🎯 DÉMONSTRATION DU DÉCORATEUR @piece_tetris")
print("=" * 50)

# 1. Avant l'importation de PieceI
from src.domaine.entites.fabriques.registre_pieces import RegistrePieces
from src.domaine.entites.piece import TypePiece

print("1️⃣ État initial du registre :")
print(f"   Pièces enregistrées: {len(RegistrePieces.obtenir_types_supportes())}")
print(f"   Types: {[t.value for t in RegistrePieces.obtenir_types_supportes()]}")

print("\n2️⃣ Importation de PieceI (décorateur s'exécute) :")
print("   @piece_tetris(TypePiece.I) s'exécute automatiquement...")

# 2. L'importation déclenche l'auto-enregistrement
from src.domaine.entites.pieces.piece_i import PieceI

print(f"   ✅ PieceI maintenant enregistrée !")

print("\n3️⃣ État après importation :")
print(f"   Pièces enregistrées: {len(RegistrePieces.obtenir_types_supportes())}")
print(f"   Types: {[t.value for t in RegistrePieces.obtenir_types_supportes()]}")

print("\n4️⃣ Vérification du mapping :")
classe_obtenue = RegistrePieces.obtenir_classe_piece(TypePiece.I)
print(f"   TypePiece.I → {classe_obtenue.__name__}")
print(f"   C'est bien PieceI ? {classe_obtenue == PieceI}")

print("\n🎉 MAGIE ACCOMPLIE !")
print("   La pièce s'est enregistrée automatiquement lors de l'importation !")
