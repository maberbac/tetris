"""
Tests d'intégration pour vérifier la génération aléatoire et les fonctionnalités
de base de la partie de Tetris.
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from src.domaine.entites.fabriques.fabrique_pieces import FabriquePieces
from src.domaine.entites.plateau import Plateau
from partie_tetris import MoteurPartie, StatistiquesJeu

def test_generation_aleatoire():
    """Test de la génération aléatoire des pièces."""
    print("🧪 Test de génération aléatoire des pièces")
    print("-" * 40)
    
    fabrique = FabriquePieces()
    
    # Générer 20 pièces aléatoires
    pieces = [fabrique.creer_aleatoire() for _ in range(20)]
    
    # Compter les types
    compteur = {}
    for piece in pieces:
        type_piece = piece.type_piece.value
        compteur[type_piece] = compteur.get(type_piece, 0) + 1
    
    print(f"📊 Répartition sur 20 pièces générées :")
    for type_piece, count in sorted(compteur.items()):
        pourcentage = (count / 20) * 100
        print(f"   {type_piece}: {count} pièces ({pourcentage:.1f}%)")
    
    # Vérifier qu'on a bien de la variété
    types_uniques = len(compteur)
    print(f"✅ {types_uniques} types différents générés (sur 7 possibles)")
    
    return types_uniques >= 5  # Au moins 5 types différents sur 20 générations


def test_plateau_refactorise():
    """Test du plateau refactorisé."""
    print("\n🧪 Test du plateau refactorisé")
    print("-" * 40)
    
    # Créer un plateau personnalisé
    plateau = Plateau(6, 8)  # Plus petit pour le test
    print(f"📍 Plateau créé: {plateau.largeur}x{plateau.hauteur}")
    
    # Créer une pièce I horizontale sur ligne 6
    fabrique = FabriquePieces()
    from src.domaine.entites.piece import TypePiece
    piece_i = fabrique.creer(TypePiece.I, x_pivot=2, y_pivot=6)
    
    # Tester le placement
    if plateau.peut_placer_piece(piece_i):
        plateau.placer_piece(piece_i)
        print(f"✅ Pièce I placée: {piece_i.positions}")
        print(f"📍 {len(plateau.positions_occupees)} positions occupées")
    else:
        print("❌ Impossible de placer la pièce I")
        return False
    
    # Simuler une ligne complète (remplir la ligne 7 complètement)  
    from src.domaine.entites.position import Position
    positions_ligne_7 = [Position(x, 7) for x in range(6)]
    for pos in positions_ligne_7:
        plateau._positions_occupees.add(pos)  # Accès direct pour le test
    
    print(f"🔧 Ligne 7 remplie complètement (6 positions)")
    print(f"📍 Total: {len(plateau.positions_occupees)} positions occupées")
    
    # Tester la détection de lignes complètes
    lignes_completes = plateau.obtenir_lignes_completes()
    print(f"🎯 Lignes complètes détectées: {lignes_completes}")
    
    if lignes_completes:
        nb_supprimees = plateau.supprimer_lignes(lignes_completes)
        print(f"✨ {nb_supprimees} ligne(s) supprimée(s)")
        print(f"📍 {len(plateau.positions_occupees)} positions restantes")
        return True
    else:
        print("❌ Aucune ligne complète détectée")
        return False


def test_moteur_partie():
    """Test du moteur de partie."""
    print("\n🧪 Test du moteur de partie")
    print("-" * 40)
    
    moteur = MoteurPartie()
    
    # Vérifier l'initialisation
    print(f"📍 Plateau: {moteur.plateau.largeur}x{moteur.plateau.hauteur}")
    print(f"🎲 Pièce active: {moteur.piece_active.type_piece.value if moteur.piece_active else 'Aucune'}")
    print(f"🎯 Pièce suivante: {moteur.piece_suivante.type_piece.value if moteur.piece_suivante else 'Aucune'}")
    
    # Test de mouvement  
    if moteur.piece_active:
        print(f"📍 Position initiale: {moteur.piece_active.positions}")
        
        # Tester déplacement gauche
        if moteur.deplacer_piece_active(-1, 0):
            print("✅ Déplacement gauche réussi")
        
        # Tester rotation
        if moteur.tourner_piece_active():
            print("✅ Rotation réussie")
        
        # Tester chute rapide
        lignes_descendues = moteur.chute_rapide()
        if lignes_descendues:
            print(f"✅ Chute rapide: descendu de {lignes_descendues} lignes")
    
    # Vérifier les statistiques
    stats = moteur.obtenir_statistiques()
    print(f"📊 Stats initiales - Score: {stats.score}, Niveau: {stats.niveau}")
    
    return True


def test_statistiques():
    """Test du système de statistiques."""
    print("\n🧪 Test des statistiques")
    print("-" * 40)
    
    stats = StatistiquesJeu()
    
    # Test ajout de pièces
    from src.domaine.entites.piece import TypePiece
    stats.ajouter_piece(TypePiece.I)
    stats.ajouter_piece(TypePiece.T)
    stats.ajouter_piece(TypePiece.O)
    
    print(f"✅ 3 pièces ajoutées: {stats.pieces_placees}")
    print(f"📊 I: {stats.pieces_par_type[TypePiece.I]}, T: {stats.pieces_par_type[TypePiece.T]}, O: {stats.pieces_par_type[TypePiece.O]}")
    
    # Test ajout de lignes
    score_avant = stats.score
    stats.ajouter_lignes(2)  # Double ligne
    print(f"✅ 2 lignes ajoutées - Score: {score_avant} → {stats.score} (+{stats.score - score_avant})")
    
    # Test Tetris
    score_avant = stats.score
    stats.ajouter_lignes(4)  # Tetris !
    print(f"🎉 TETRIS ! - Score: {score_avant} → {stats.score} (+{stats.score - score_avant})")
    print(f"📈 Niveau: {stats.niveau}")
    
    return True


def main():
    """Lance tous les tests d'intégration."""
    print("🧪 TESTS D'INTÉGRATION - PARTIE TETRIS")
    print("=" * 50)
    
    tests = [
        ("Génération aléatoire", test_generation_aleatoire),
        ("Plateau refactorisé", test_plateau_refactorise),
        ("Moteur de partie", test_moteur_partie),
        ("Statistiques", test_statistiques)
    ]
    
    resultats = []
    
    for nom_test, fonction_test in tests:
        try:
            resultat = fonction_test()
            resultats.append((nom_test, resultat))
            status = "✅ RÉUSSI" if resultat else "❌ ÉCHEC"
            print(f"\n{status}")
        except Exception as e:
            print(f"\n❌ ERREUR: {e}")
            resultats.append((nom_test, False))
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS D'INTÉGRATION")
    print("=" * 50)
    
    reussites = 0
    for nom_test, resultat in resultats:
        status = "✅" if resultat else "❌"
        print(f"{status} {nom_test}")
        if resultat:
            reussites += 1
    
    print(f"\n🎯 {reussites}/{len(tests)} tests réussis")
    
    if reussites == len(tests):
        print("🎉 Tous les tests d'intégration sont passés ! La partie est prête à jouer.")
        print("\nPour jouer, utilisez: python jouer.py")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")


if __name__ == "__main__":
    main()
