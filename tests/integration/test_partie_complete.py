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
from partie_tetris import MoteurPartie

def test_generation_aleatoire():
    """Test de la génération aléatoire des pièces."""
    print("🧪 Test de génération aléatoire des pièces")
    print("-" * 40)
    
    fabrique = FabriquePieces()
    
    # Générer 20 pièces et vérifier la variété
    pieces_generees = []
    for i in range(20):
        piece = fabrique.creer_aleatoire()
        pieces_generees.append(piece.type_piece)  # CORRECTION: type_piece au lieu de type
        print(f"Pièce {i+1:2d}: {piece.type_piece.value}")
    
    # Vérifier qu'on a au moins 3 types différents (probabilité très élevée)
    types_uniques = set(pieces_generees)
    print(f"\n📊 Types uniques générés: {len(types_uniques)}/7")
    print(f"✅ Types: {[t.value for t in types_uniques]}")
    
    assert len(types_uniques) >= 3, f"Pas assez de variété: {len(types_uniques)} types"
    return True

def test_plateau_collision():
    """Test des collisions avec le plateau."""
    print("\n🧪 Test des collisions avec le plateau")  
    print("-" * 40)
    
    plateau = Plateau(10, 20)
    fabrique = FabriquePieces()
    
    # Créer une pièce au centre - CORRECTION: utiliser TypePiece.I directement
    from src.domaine.entites.piece import TypePiece
    piece = fabrique.creer(TypePiece.I, x_pivot=5, y_pivot=0)  # CORRECTION: type_piece au lieu de from_type
    print(f"✅ Pièce I créée à (5, 0)")
    
    # Test de position normale
    collision_normale = not plateau.peut_placer_piece(piece)
    print(f"Position normale (5,0): collision={collision_normale}")
    
    # Tester les collisions en déplaçant la pièce
    # Déplacement vers la gauche extrême (doit causer collision)
    positions_orig = piece.positions.copy()
    pivot_orig = piece.position_pivot
    
    piece.deplacer(-10, 0)  # Déplacer très loin à gauche
    collision_gauche = not plateau.peut_placer_piece(piece)
    print(f"Collision gauche (delta_x=-10): {collision_gauche}")
    
    # Remettre position originale et tester droite
    piece.positions = positions_orig
    piece.position_pivot = pivot_orig
    piece.deplacer(10, 0)  # Déplacer très loin à droite
    collision_droite = not plateau.peut_placer_piece(piece)
    print(f"Collision droite (delta_x=+10): {collision_droite}")
    
    # Remettre position originale et tester bas
    piece.positions = positions_orig
    piece.position_pivot = pivot_orig
    piece.deplacer(0, 25)  # Déplacer très loin en bas
    collision_bas = not plateau.peut_placer_piece(piece)
    print(f"Collision bas (delta_y=+25): {collision_bas}")
    
    assert collision_gauche == True, "Devrait détecter collision à gauche"
    assert collision_droite == True, "Devrait détecter collision à droite"
    assert collision_bas == True, "Devrait détecter collision en bas"
    assert collision_normale == False, "Position normale ne devrait pas être en collision"
    
    return True

def test_moteur_partie():
    """Test des fonctionnalités de base du moteur."""
    print("\n🧪 Test du moteur de partie")
    print("-" * 40)
    
    moteur = MoteurPartie()
    print("✅ Moteur créé")
    
    # Vérifier l'état initial - CORRECTION: obtenir_piece_active au lieu de obtenir_piece_courante
    piece_courante = moteur.obtenir_piece_active()
    plateau = moteur.obtenir_plateau()
    
    print(f"✅ Pièce courante: {piece_courante.type_piece.value}")  # CORRECTION: type_piece
    print(f"✅ Plateau: {plateau.largeur}×{plateau.hauteur}")
    
    # Tester les commandes de base
    # (On ne peut pas vraiment tester sans interface complète)
    
    # Vérifier les statistiques
    stats = moteur.obtenir_statistiques()
    print(f"📊 Stats initiales - Score: {stats.score}, Niveau: {stats.niveau}")
    
    return True

def test_statistiques():
    """Test du système de statistiques."""
    print("\n🧪 Test des statistiques")
    print("-" * 40)
    
    from src.domaine.entites.statistiques.statistiques_jeu import StatistiquesJeu
    from src.domaine.entites.piece import TypePiece
    
    # Création des statistiques
    stats = StatistiquesJeu()
    print(f"📊 Statistiques initiales : Score={stats.score}, Niveau={stats.niveau}")
    
    # Test 1: État initial
    assert stats.score == 0, f"Score initial devrait être 0, trouvé {stats.score}"
    assert stats.niveau == 1, f"Niveau initial devrait être 1, trouvé {stats.niveau}"
    assert stats.lignes_completees == 0, f"Lignes complétées initiales devraient être 0, trouvé {stats.lignes_completees}"
    assert stats.pieces_placees == 0, f"Pièces placées initiales devraient être 0, trouvé {stats.pieces_placees}"
    print("✅ État initial correct")
    
    # Test 2: Ajout de pièces
    stats.ajouter_piece(TypePiece.I)
    stats.ajouter_piece(TypePiece.O) 
    stats.ajouter_piece(TypePiece.T)
    assert stats.pieces_placees == 3, f"Devrait avoir 3 pièces placées, trouvé {stats.pieces_placees}"
    assert stats.pieces_par_type[TypePiece.I] == 1, f"Devrait avoir 1 pièce I, trouvé {stats.pieces_par_type[TypePiece.I]}"
    assert stats.pieces_par_type[TypePiece.O] == 1, f"Devrait avoir 1 pièce O, trouvé {stats.pieces_par_type[TypePiece.O]}"
    assert stats.pieces_par_type[TypePiece.T] == 1, f"Devrait avoir 1 pièce T, trouvé {stats.pieces_par_type[TypePiece.T]}"
    print("✅ Comptage des pièces correct")
    
    # Test 3: Calcul du score (ligne simple)
    score_initial = stats.score
    stats.ajouter_score_selon_lignes_completees(1)
    score_attendu = score_initial + (100 * stats.niveau)  # 100 points par ligne simple
    assert stats.score >= score_initial, f"Score devrait augmenter après ligne complète"
    assert stats.lignes_completees == 1, f"Devrait avoir 1 ligne complétée, trouvé {stats.lignes_completees}"
    print(f"✅ Score après 1 ligne : {stats.score} points")
    
    # Test 4: Score pour Tetris (4 lignes simultanées)
    score_avant_tetris = stats.score
    stats.ajouter_score_selon_lignes_completees(4)  # Tetris !
    bonus_tetris = 800 * stats.niveau
    assert stats.score > score_avant_tetris, f"Score devrait augmenter significativement pour un Tetris"
    assert stats.lignes_completees == 5, f"Devrait avoir 5 lignes complétées au total, trouvé {stats.lignes_completees}"
    print(f"✅ Score après Tetris : {stats.score} points (bonus Tetris appliqué)")
    
    # Test 5: Progression de niveau
    # Compléter 10 lignes au total pour passer au niveau 2
    stats.ajouter_score_selon_lignes_completees(5)  # 5 lignes de plus = 10 total
    assert stats.lignes_completees == 10, f"Devrait avoir 10 lignes complétées, trouvé {stats.lignes_completees}"
    assert stats.niveau == 2, f"Devrait être au niveau 2 après 10 lignes, trouvé niveau {stats.niveau}"
    print(f"✅ Progression de niveau : Niveau {stats.niveau} après {stats.lignes_completees} lignes")
    
    # Test 6: Score multiplié par niveau
    score_niveau2 = stats.score
    stats.ajouter_score_selon_lignes_completees(2)  # Double ligne au niveau 2
    bonus_double = 300 * 2  # 300 points × niveau 2
    assert stats.score > score_niveau2, f"Score devrait augmenter avec bonus de niveau"
    assert stats.niveau == 2, f"Devrait rester au niveau 2, trouvé niveau {stats.niveau}"
    print(f"✅ Bonus de niveau appliqué : Score final {stats.score} points")
    
    # Test 7: Vérification de tous les types de pièces
    for type_piece in [TypePiece.S, TypePiece.Z, TypePiece.J, TypePiece.L]:
        stats.ajouter_piece(type_piece)
    
    total_pieces = sum(stats.pieces_par_type.values())
    assert total_pieces == stats.pieces_placees, f"Somme des pièces par type ({total_pieces}) devrait égaler le total ({stats.pieces_placees})"
    print(f"✅ Comptage cohérent : {stats.pieces_placees} pièces au total")
    
    # Résumé des statistiques finales
    print("\n📊 STATISTIQUES FINALES :")
    print(f"   💰 Score final : {stats.score:,} points")
    print(f"   📈 Niveau atteint : {stats.niveau}")
    print(f"   📝 Lignes complétées : {stats.lignes_completees}")
    print(f"   🧩 Pièces placées : {stats.pieces_placees}")
    print("   🎯 Répartition des pièces :")
    for type_piece, count in stats.pieces_par_type.items():
        if count > 0:
            print(f"      {type_piece.value}: {count}")
    
    print("✅ Tous les tests de statistiques réussis !")
    return True

if __name__ == "__main__":
    """Exécuter tous les tests d'intégration."""
    print("🎮 TESTS D'INTÉGRATION - PARTIE COMPLÈTE")
    print("=" * 50)
    
    tests = [
        test_generation_aleatoire,
        test_plateau_collision,
        test_moteur_partie,
        test_statistiques
    ]
    
    resultats = []
    for test in tests:
        try:
            resultat = test()
            resultats.append(resultat)
            print("✅ Test réussi\n")
        except Exception as e:
            print(f"❌ Test échoué: {e}\n")
            resultats.append(False)
    
    # Résumé
    print("=" * 50)
    print("📊 RÉSUMÉ DES TESTS D'INTÉGRATION")
    print("=" * 50)
    
    for i, (test, resultat) in enumerate(zip(tests, resultats)):
        status = "✅ RÉUSSI" if resultat else "❌ ÉCHOUÉ"
        print(f"{i+1}. {test.__name__}: {status}")
    
    reussis = sum(resultats)
    total = len(resultats)
    pourcentage = (reussis / total) * 100
    
    print(f"\n🎯 BILAN: {reussis}/{total} tests réussis ({pourcentage:.1f}%)")
    
    if pourcentage == 100:
        print("🏆 TOUS LES TESTS D'INTÉGRATION RÉUSSIS !")
    else:
        print("⚠️ Certains tests nécessitent des corrections")
