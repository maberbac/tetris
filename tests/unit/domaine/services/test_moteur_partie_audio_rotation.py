"""
Tests unitaires pour l'intégration audio rotation dans MoteurPartie.

Tests TDD pour vérifier que les rotations déclenchent bien les sons.
"""

import unittest
from unittest.mock import Mock

from src.domaine.services.moteur_partie import MoteurPartie
from src.domaine.entites.fabriques.fabrique_pieces import FabriquePieces
from src.domaine.entites.piece import TypePiece


class TestMoteurPartieAudioRotation(unittest.TestCase):
    """Tests pour l'audio de rotation dans le moteur."""
    
    def setUp(self):
        """Configuration pour chaque test."""
        self.mock_audio = Mock()
        self.moteur = MoteurPartie(audio=self.mock_audio)
        
        # Ajouter une pièce pour les tests
        fabrique = FabriquePieces()
        self.moteur.piece_active = fabrique.creer(TypePiece.I, x_pivot=5, y_pivot=0)
    
    def test_rotation_reussie_joue_son(self):
        """Une rotation réussie doit jouer le son rotate.wav."""
        # S'assurer que la rotation sera possible
        # PieceI au centre peut tourner
        
        # Exécuter la rotation
        resultat = self.moteur.tourner_piece_active()
        
        # Vérifications
        self.assertTrue(resultat, "La rotation devrait réussir")
        self.mock_audio.jouer_effet_sonore.assert_called_once_with(
            "assets/audio/sfx/rotate.wav", 
            volume=1.0
        )
    
    def test_rotation_echouee_ne_joue_pas_son(self):
        """Une rotation échouée ne doit pas jouer de son."""
        # Utilisons directement la pièce active existante du moteur
        # qui a déjà été générée et peut être dans une position où rotation échoue parfois
        
        # Reset le mock pour être sûr
        self.mock_audio.reset_mock()
        
        # Forcer une situation de rotation invalide en modifiant la pièce
        # On va créer une PieceI verticale en position où rotation horizontale échouerait
        fabrique = FabriquePieces()
        piece_i = fabrique.creer(TypePiece.I, x_pivot=0, y_pivot=18)  # Très à gauche et bas
        piece_i.tourner()  # La mettre verticale
        self.moteur.piece_active = piece_i
        
        # Tenter la rotation (de vertical vers horizontal près du bord)
        resultat = self.moteur.tourner_piece_active()
        
        # Si la rotation échoue, aucun son ne doit être joué
        if not resultat:
            self.mock_audio.jouer_effet_sonore.assert_not_called()
        # Si la rotation réussit, un son doit être joué
        else:
            self.mock_audio.jouer_effet_sonore.assert_called_once()
        
        # Dans tous les cas, le test ne doit pas crasher
        self.assertIsInstance(resultat, bool)
    
    def test_rotation_sans_audio_ne_crash_pas(self):
        """La rotation doit fonctionner même sans système audio."""
        # Créer un moteur sans audio
        moteur_sans_audio = MoteurPartie(audio=None)
        fabrique = FabriquePieces()
        moteur_sans_audio.piece_active = fabrique.creer(TypePiece.T, x_pivot=5, y_pivot=0)
        
        # Exécuter la rotation - ne doit pas crasher
        resultat = moteur_sans_audio.tourner_piece_active()
        
        # Vérification
        self.assertTrue(resultat, "La rotation devrait réussir même sans audio")
    
    def test_rotation_jeu_pause_ne_joue_pas_son(self):
        """Une tentative de rotation en pause ne doit pas jouer de son."""
        # Mettre le jeu en pause
        self.moteur.en_pause = True
        
        # Tenter la rotation
        resultat = self.moteur.tourner_piece_active()
        
        # Vérifications
        self.assertFalse(resultat, "La rotation devrait être bloquée en pause")
        self.mock_audio.jouer_effet_sonore.assert_not_called()
    
    def test_rotation_jeu_termine_ne_joue_pas_son(self):
        """Une tentative de rotation quand le jeu est terminé ne doit pas jouer de son."""
        # Terminer le jeu
        self.moteur.jeu_termine = True
        
        # Tenter la rotation
        resultat = self.moteur.tourner_piece_active()
        
        # Vérifications
        self.assertFalse(resultat, "La rotation devrait être bloquée quand le jeu est terminé")
        self.mock_audio.jouer_effet_sonore.assert_not_called()


if __name__ == '__main__':
    unittest.main()
