"""
Démonstration détaillée du décorateur - Step by step.
"""

print("🔍 ANALYSE DÉTAILLÉE DU DÉCORATEUR")
print("=" * 40)

print("\n📝 Voici ce qui se passe quand Python lit :")
print("   @piece_tetris(TypePiece.I)")
print("   class PieceI(Piece):")
print("       ...")

print("\n🔄 ÉTAPES D'EXÉCUTION :")

print("\nÉtape 1: Python appelle piece_tetris(TypePiece.I)")
print("   → Retourne un décorateur spécialisé pour TypePiece.I")

print("\nÉtape 2: Python applique ce décorateur à la classe PieceI")
print("   → decorateur(PieceI) s'exécute")

print("\nÉtape 3: Dans decorateur() :")
print("   → RegistrePieces.enregistrer_piece(TypePiece.I, PieceI)")
print("   → return PieceI  # La classe reste inchangée")

print("\nÉtape 4: Python termine la définition de classe")
print("   → PieceI est maintenant disponible ET enregistrée !")

print("\n🎯 RÉSULTAT :")
print("   ✅ La classe PieceI existe normalement")
print("   ✅ BONUS: Elle est automatiquement dans le registre")
print("   ✅ La fabrique peut la découvrir automatiquement")

print("\n💡 AVANTAGE :")
print("   Plus besoin de modifier FabriquePieces pour ajouter une pièce !")
print("   Il suffit de créer la classe avec @piece_tetris(TypeXXX)")

# Démonstration pratique
from src.domaine.entites.fabriques import FabriquePieces
from src.domaine.entites.piece import TypePiece

print(f"\n🧪 TEST PRATIQUE :")
fabrique = FabriquePieces()
print(f"   Types supportés automatiquement: {[t.value for t in fabrique.obtenir_types_supportes()]}")

piece_i = fabrique.creer(TypePiece.I)
print(f"   Création de PieceI: {piece_i.__class__.__name__} ✅")

piece_aleatoire = fabrique.creer_aleatoire()
print(f"   Création aléatoire: {piece_aleatoire.__class__.__name__} ✅")
