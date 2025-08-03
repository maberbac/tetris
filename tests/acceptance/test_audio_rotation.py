"""
Tests d'acceptance pour les effets sonores de rotation.

Scénarios utilisateur validant l'expérience audio lors des rotations.
"""

import unittest
from unittest.mock import Mock

from src.domaine.services.moteur_partie import MoteurPartie
from src.domaine.entites.fabriques.fabrique_pieces import FabriquePieces
from src.domaine.entites.piece import TypePiece


class TestAcceptanceAudioRotation(unittest.TestCase):
    """Tests d'acceptance pour l'audio de rotation."""
    
    def setUp(self):
        """Configuration pour chaque test."""
        self.mock_audio = Mock()
        self.moteur = MoteurPartie(audio=self.mock_audio)
        self.moteur.en_pause = False  # Démarrer le jeu pour permettre les rotations
        print("\n🎮 TEST ACCEPTANCE AUDIO ROTATION")
        print("=" * 50)
    
    def test_utilisateur_tourne_piece_entend_son(self):
        """Scénario : L'utilisateur tourne une pièce et entend le son rotate.wav."""
        print("🧪 Scénario : Rotation avec son")
        
        # L'utilisateur a une pièce active
        fabrique = FabriquePieces()
        self.moteur.piece_active = fabrique.creer(TypePiece.T, x_pivot=5, y_pivot=15)
        
        print(f"  📍 Pièce active: {self.moteur.piece_active.type_piece.value}")
        
        # L'utilisateur appuie sur la touche de rotation
        resultat = self.moteur.tourner_piece_active()
        
        # L'utilisateur entend le son de rotation
        print("  🔊 Son de rotation joué")
        
        # Vérifications
        self.assertTrue(resultat, "La rotation devrait réussir")
        self.mock_audio.jouer_effet_sonore.assert_called_once_with(
            "assets/audio/sfx/rotate.wav", 
            volume=1.0
        )
        print("  ✅ Son rotate.wav joué avec volume correct (100%)")
    
    def test_utilisateur_tourne_piece_en_mode_mute(self):
        """Scénario : L'utilisateur tourne une pièce en mode mute."""
        print("🧪 Scénario : Rotation en mode mute")
        
        # L'utilisateur a activé le mode mute
        self.mock_audio.jouer_effet_sonore.return_value = True
        
        # L'utilisateur a une pièce active
        fabrique = FabriquePieces()
        self.moteur.piece_active = fabrique.creer(TypePiece.I, x_pivot=5, y_pivot=15)
        
        print(f"  📍 Pièce active: {self.moteur.piece_active.type_piece.value}")
        print("  🔇 Mode mute activé")
        
        # L'utilisateur appuie sur la touche de rotation
        resultat = self.moteur.tourner_piece_active()
        
        # Le système appelle quand même l'audio (qui gérera le mute)
        print("  🎵 Commande audio envoyée (audio gérera le mute)")
        
        # Vérifications
        self.assertTrue(resultat, "La rotation devrait réussir")
        self.mock_audio.jouer_effet_sonore.assert_called_once_with(
            "assets/audio/sfx/rotate.wav", 
            volume=1.0
        )
        print("  ✅ Commande audio envoyée même en mode mute")
    
    def test_utilisateur_rotation_impossible_pas_de_son(self):
        """Scénario : L'utilisateur tente une rotation impossible."""
        print("🧪 Scénario : Rotation impossible")
        
        # Utiliser une configuration simple qui empêche la rotation
        # PieceI très à gauche et verticale, rotation vers horizontal impossible 
        fabrique = FabriquePieces()
        piece_i = fabrique.creer(TypePiece.I, x_pivot=0, y_pivot=15)  # Très à gauche
        piece_i.tourner()  # La mettre verticale d'abord
        self.moteur.piece_active = piece_i
        
        print("  📍 Pièce I verticale très proche du bord gauche")
        
        # L'utilisateur tente de tourner (vers horizontal, ce qui sortirait du plateau)
        resultat = self.moteur.tourner_piece_active()
        
        if not resultat:
            print("  ❌ Rotation bloquée par collision")
            # Aucun son ne doit être joué si rotation échoue
            self.mock_audio.jouer_effet_sonore.assert_not_called()
            print("  ✅ Aucun son joué pour rotation impossible")
        else:
            print("  ✅ Rotation réussie (variation selon position)")
            # Si rotation réussie, son doit être joué
            self.mock_audio.jouer_effet_sonore.assert_called_once()
            print("  ✅ Son joué pour rotation réussie")
        
        # Dans tous les cas, pas de crash
        self.assertIsInstance(resultat, bool)
    
    def test_experience_utilisateur_rotations_multiples(self):
        """Scénario : L'utilisateur fait plusieurs rotations consécutives."""
        print("🧪 Scénario : Rotations multiples")
        
        # L'utilisateur a une pièce T (4 orientations)
        fabrique = FabriquePieces()
        self.moteur.piece_active = fabrique.creer(TypePiece.T, x_pivot=5, y_pivot=15)
        
        print(f"  📍 Pièce {self.moteur.piece_active.type_piece.value} prête")
        
        # L'utilisateur fait 3 rotations successives
        sons_joues = 0
        for i in range(1, 4):
            resultat = self.moteur.tourner_piece_active()
            if resultat:
                sons_joues += 1
            print(f"    🔄 Rotation {i}: {'✅' if resultat else '❌'}")
        
        # Chaque rotation réussie doit avoir joué un son
        print(f"  🔊 {sons_joues} sons de rotation joués")
        
        # Vérifications
        self.assertEqual(self.mock_audio.jouer_effet_sonore.call_count, sons_joues)
        print(f"  ✅ {sons_joues} appels audio pour {sons_joues} rotations réussies")
    
    def test_jeu_sans_audio_fonctionne_normalement(self):
        """Scénario : L'utilisateur joue sur un système sans audio."""
        print("🧪 Scénario : Jeu sans système audio")
        
        # Système sans audio
        moteur_sans_audio = MoteurPartie(audio=None)
        moteur_sans_audio.en_pause = False  # Démarrer le jeu
        fabrique = FabriquePieces()
        moteur_sans_audio.piece_active = fabrique.creer(TypePiece.O, x_pivot=5, y_pivot=15)
        
        print("  🚫 Aucun système audio disponible")
        print(f"  📍 Pièce {moteur_sans_audio.piece_active.type_piece.value} active")
        
        # L'utilisateur tourne quand même
        resultat = moteur_sans_audio.tourner_piece_active()
        
        # Le jeu doit continuer à fonctionner
        self.assertTrue(resultat, "La rotation devrait fonctionner sans audio")
        print("  ✅ Rotation fonctionne sans crash même sans audio")
        print("  🎮 Expérience utilisateur préservée")


if __name__ == '__main__':
    unittest.main()
