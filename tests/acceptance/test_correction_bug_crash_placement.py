"""
Tests d'acceptance pour la correction du bug de crash lors du placement de pièces.

BUG DÉTECTÉ : ValueError lancée quand on essaie de placer une pièce 
dans une position invalide via placer_piece_et_supprimer_lignes.

COMPORTEMENT ATTENDU : Le jeu ne doit jamais crasher, mais gérer 
gracieusement les tentatives de placement invalides.

SCÉNARIOS UTILISATEUR :
- Que se passe-t-il quand le plateau est plein et qu'une pièce ne peut plus descendre ?
- Comment le jeu réagit-il à une situation de Game Over inévitable ?
- L'utilisateur voit-il un message de fin de partie approprié ?
"""

import pytest
from src.domaine.entites.plateau import Plateau
from src.domaine.entites.fabriques.fabrique_pieces import FabriquePieces
from src.domaine.entites.piece import TypePiece
from src.domaine.services.moteur_partie import MoteurPartie


class TestAcceptanceCorrectionBugCrashPlacement:
    """Tests d'acceptance pour valider les scénarios utilisateur lors des crashes de placement."""
    
    def test_placement_piece_position_invalide_ne_crash_pas(self):
        """
        SCÉNARIO : L'utilisateur joue et le plateau devient très plein.
        QUAND : Une pièce essaie d'être placée dans une position invalide
        ALORS : Le jeu ne crash pas et retourne un indicateur d'échec
        """
        # Arrange : Plateau presque plein (situation de jeu réelle)
        plateau = Plateau(4, 5)
        fabrique = FabriquePieces()
        
        # Remplir tout le plateau sauf la ligne du haut
        for y in range(1, 5):
            for x in range(4):
                from src.domaine.entites.position import Position
                plateau._positions_occupees.add(Position(x, y))
        
        # Créer une pièce qui ne peut pas être placée
        piece_impossible = fabrique.creer(TypePiece.I, x_pivot=0, y_pivot=0)
        
        # Act : Ne doit PAS crasher, retourner -1
        resultat = plateau.placer_piece_et_supprimer_lignes(piece_impossible)
        
        # Assert : Échec gracieux
        assert resultat == -1
    
    def test_moteur_partie_placement_invalide_declenche_game_over(self):
        """
        SCÉNARIO : L'utilisateur joue et arrive dans une situation de Game Over
        QUAND : Le moteur essaie de placer une pièce qui ne peut pas être placée
        ALORS : Le jeu déclenche gracieusement un Game Over au lieu de crasher
        """
        # Arrange : Moteur avec plateau presque plein
        moteur = MoteurPartie()
        
        # Forcer une pièce dans une position où elle ne peut pas être placée
        fabrique = FabriquePieces()
        piece_bloquee = fabrique.creer(TypePiece.I, x_pivot=0, y_pivot=0)
        
        # CORRECTION : Créer une collision RÉELLE avec les positions de la pièce I
        # Pièce I à (0,0) a des positions : (-2,-1), (-1,-1), (0,-1), (1,-1)
        # On occupe exactement CES positions pour forcer la collision
        from src.domaine.entites.position import Position
        for pos in piece_bloquee.positions:
            moteur.plateau._positions_occupees.add(pos)
        
        # Forcer cette pièce comme pièce active
        moteur.piece_active = piece_bloquee
        
        # CORRECTION : Désactiver la pause pour permettre le placement
        moteur.en_pause = False
        
        # Vérification : s'assurer qu'il y a bien collision
        assert not moteur.plateau.peut_placer_piece(piece_bloquee), "La pièce devrait être en collision"
        
        # Act : Ne doit PAS crasher, retourner False et déclencher Game Over
        resultat = moteur.placer_piece_et_generer_nouvelle()
        
        # Assert : Échec gracieux avec Game Over
        assert resultat == False
        assert moteur.jeu_termine == True
    
    def test_coherence_verification_placement(self):
        """
        SCÉNARIO : L'utilisateur fait des mouvements et le jeu vérifie la validité
        QUAND : Le système vérifie si une pièce peut être placée
        ALORS : La vérification et le placement donnent des résultats cohérents
        """
        plateau = Plateau(3, 3)
        fabrique = FabriquePieces()
        
        # Remplir partiellement le plateau
        from src.domaine.entites.position import Position
        plateau._positions_occupees.add(Position(1, 1))
        
        # Tester une pièce qui chevauche
        piece_chevauchante = fabrique.creer(TypePiece.O, x_pivot=1, y_pivot=1)
        
        # peut_placer_piece doit retourner False
        assert not plateau.peut_placer_piece(piece_chevauchante)
        
        # placer_piece_et_supprimer_lignes doit être cohérent (retour -1)
        resultat = plateau.placer_piece_et_supprimer_lignes(piece_chevauchante)
        assert resultat == -1
    
    def test_scenario_reel_chute_automatique_plateau_plein(self):
        """
        SCÉNARIO : L'utilisateur joue normalement et le plateau se remplit progressivement
        QUAND : Une pièce tombe automatiquement mais ne peut plus être placée
        ALORS : Le jeu gère gracieusement la situation et déclenche un Game Over
        """
        moteur = MoteurPartie()
        
        # Forcer une pièce en position spécifique
        fabrique = FabriquePieces()
        piece_en_zone_invisible = fabrique.creer(TypePiece.I, x_pivot=4, y_pivot=0)
        moteur.piece_active = piece_en_zone_invisible
        
        # Créer une collision directe : occuper les MÊMES positions que la pièce
        from src.domaine.entites.position import Position
        for pos in piece_en_zone_invisible.positions:
            moteur.plateau._positions_occupees.add(pos)
        
        # CORRECTION : Désactiver la pause pour permettre le placement
        moteur.en_pause = False
        
        # Vérification : la pièce ne peut effectivement pas être placée (collision)
        assert not moteur.plateau.peut_placer_piece(piece_en_zone_invisible)
        
        # APRÈS CORRECTION : Placement impossible déclenche Game Over gracieusement
        resultat = moteur.placer_piece_et_generer_nouvelle()
        assert resultat == False
        assert moteur.jeu_termine == True
    
    def test_experience_utilisateur_game_over_sans_crash(self):
        """
        SCÉNARIO : L'utilisateur arrive en fin de partie naturellement
        QUAND : Le jeu ne peut plus placer de nouvelles pièces
        ALORS : L'utilisateur voit un Game Over propre sans message d'erreur technique
        """
        moteur = MoteurPartie()
        
        # Pièce qui ne peut absolument pas être placée (collision directe)
        fabrique = FabriquePieces()
        piece_impossible = fabrique.creer(TypePiece.I, x_pivot=4, y_pivot=0)
        moteur.piece_active = piece_impossible
        
        # Créer une collision : occuper exactement les mêmes positions
        from src.domaine.entites.position import Position
        for pos in piece_impossible.positions:
            moteur.plateau._positions_occupees.add(pos)
        
        # CORRECTION : Désactiver la pause pour permettre le placement
        moteur.en_pause = False
        
        # Vérification : la pièce ne peut effectivement pas être placée
        assert not moteur.plateau.peut_placer_piece(piece_impossible)
        
        # APRÈS CORRECTION : L'utilisateur voit un Game Over propre
        # Le moteur détecte l'impossibilité et déclenche Game Over
        resultat = moteur.placer_piece_et_generer_nouvelle()
        assert resultat == False  # Échec gracieux
        assert moteur.jeu_termine == True  # Game Over déclenché proprement
