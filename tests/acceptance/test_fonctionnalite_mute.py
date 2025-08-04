"""
Tests d'acceptance pour la fonctionnalité mute/unmute avec la touche M.

Ces tests valident le scénario complet utilisateur du contrôle audio
en suivant l'approche TDD et les directives de développement.
"""

import unittest
from unittest.mock import Mock, patch
import time

from src.domaine.services.gestionnaire_evenements import (
    GestionnaireEvenements, TypeEvenement, ToucheClavier
)


class TestAcceptanceMuteUnmute(unittest.TestCase):
    """Tests d'acceptance pour la fonctionnalité mute/unmute."""
    
    def setUp(self):
        """Configuration pour les tests d'acceptance."""
        self.gestionnaire = GestionnaireEvenements()
        self.moteur_mock = Mock()
        self.audio_mock = Mock()
        
        # Configuration du moteur avec système audio
        self.moteur_mock.obtenir_audio.return_value = self.audio_mock
        self.moteur_mock.tourner_piece_active.return_value = True
        
        # Configuration par défaut : audio non mute
        self.audio_mock.basculer_mute_musique.return_value = True  # Premier appel = mute
    
    def test_touche_m_active_mute_audio(self):
        """Scénario : L'utilisateur appuie sur M pour désactiver l'audio."""
        # Given : Le jeu fonctionne avec audio activé
        # When : L'utilisateur appuie sur la touche M
        resultat = self.gestionnaire.traiter_evenement_clavier(
            "m", TypeEvenement.CLAVIER_APPUI, self.moteur_mock
        )
        
        # Then : L'audio est désactivé
        self.assertTrue(resultat)
        self.moteur_mock.obtenir_audio.assert_called_once()
        self.audio_mock.basculer_mute_musique.assert_called_once()
    
    @patch('src.domaine.services.commandes.commandes_base.logger_tetris')
    def test_touche_m_donne_feedback_visuel_mute(self, mock_logger):
        """Scénario : L'utilisateur reçoit un feedback visuel quand il mute."""
        # Given : Audio activé
        self.audio_mock.basculer_mute_musique.return_value = True
        
        # When : Appui sur M pour mute
        self.gestionnaire.traiter_evenement_clavier(
            "m", TypeEvenement.CLAVIER_APPUI, self.moteur_mock
        )
        
        # Then : Message de confirmation via logger
        mock_logger.info.assert_called_with("🔇 Musique désactivée")
    
    @patch('src.domaine.services.commandes.commandes_base.logger_tetris')
    def test_touche_m_donne_feedback_visuel_unmute(self, mock_logger):
        """Scénario : L'utilisateur reçoit un feedback visuel quand il unmute."""
        # Given : Audio désactivé (simule deuxième appui)
        self.audio_mock.basculer_mute_musique.return_value = False
        
        # When : Appui sur M pour unmute
        self.gestionnaire.traiter_evenement_clavier(
            "m", TypeEvenement.CLAVIER_APPUI, self.moteur_mock
        )
        
        # Then : Message de confirmation via logger
        mock_logger.info.assert_called_with("🔊 Musique réactivée")
    
    def test_basculement_mute_unmute_multiple(self):
        """Scénario : L'utilisateur bascule plusieurs fois entre mute/unmute."""
        # Given : Audio disponible
        # Configuration pour simuler le basculement
        effets_basculement = [True, False, True, False]  # mute, unmute, mute, unmute
        self.audio_mock.basculer_mute_musique.side_effect = effets_basculement
        
        resultats = []
        
        # When : Plusieurs appuis sur M
        for i in range(4):
            resultat = self.gestionnaire.traiter_evenement_clavier(
                "m", TypeEvenement.CLAVIER_APPUI, self.moteur_mock
            )
            resultats.append(resultat)
        
        # Then : Tous les appuis sont traités avec succès
        self.assertEqual(resultats, [True, True, True, True])
        self.assertEqual(self.audio_mock.basculer_mute_musique.call_count, 4)
    
    @patch('src.domaine.services.commandes.commandes_base.logger_tetris')
    def test_mute_sans_audio_disponible_informe_utilisateur(self, mock_logger):
        """Scénario : L'utilisateur essaie de mute mais l'audio n'est pas disponible."""
        # Given : Pas de système audio
        self.moteur_mock.obtenir_audio.return_value = None
        
        # When : Appui sur M
        resultat = self.gestionnaire.traiter_evenement_clavier(
            "m", TypeEvenement.CLAVIER_APPUI, self.moteur_mock
        )
        
        # Then : Échec gracieux avec message informatif via logger
        self.assertFalse(resultat)
        mock_logger.warning.assert_called_with("❌ Audio non disponible")
    
    def test_mute_avec_erreur_audio_gere_gracieusement(self):
        """Scénario : Erreur du système audio lors du basculement."""
        # Given : Système audio défaillant
        self.moteur_mock.obtenir_audio.side_effect = Exception("Erreur audio")
        
        # When : Appui sur M
        resultat = self.gestionnaire.traiter_evenement_clavier(
            "m", TypeEvenement.CLAVIER_APPUI, self.moteur_mock
        )
        
        # Then : Échec gracieux sans crash
        self.assertFalse(resultat)
    
    def test_touche_m_ne_repete_pas(self):
        """Scénario : La touche M ne doit pas se répéter automatiquement."""
        # Given : Touche M maintenue
        temps_debut = time.time()
        
        # When : Appui initial puis tentative de répétition
        resultat1 = self.gestionnaire.traiter_evenement_clavier(
            "m", TypeEvenement.CLAVIER_APPUI, self.moteur_mock, temps_debut
        )
        
        # Simuler le temps qui passe (plus que le délai de répétition)
        temps_apres = temps_debut + 0.5  # 500ms plus tard
        
        resultat2 = self.gestionnaire.traiter_evenement_clavier(
            "m", TypeEvenement.CLAVIER_MAINTENU, self.moteur_mock, temps_apres
        )
        
        # Then : Premier appui traité, maintien ignoré (pas de répétition pour mute)
        self.assertTrue(resultat1)
        self.assertFalse(resultat2)  # Mute ne se répète pas
        self.assertEqual(self.audio_mock.basculer_mute_musique.call_count, 1)
    
    def test_integration_mute_avec_autres_controles(self):
        """Scénario : Le mute fonctionne en parallèle des autres contrôles."""
        # Given : Moteur avec pièce active pour les autres contrôles
        piece_mock = Mock()
        plateau_mock = Mock()
        self.moteur_mock.obtenir_piece_active.return_value = piece_mock
        self.moteur_mock.obtenir_plateau.return_value = plateau_mock
        plateau_mock.peut_placer_piece.return_value = True
        
        # When : Utilisation de plusieurs contrôles incluant mute
        resultats = []
        
        # Déplacement gauche
        resultats.append(self.gestionnaire.traiter_evenement_clavier(
            "Left", TypeEvenement.CLAVIER_APPUI, self.moteur_mock
        ))
        
        # Mute
        resultats.append(self.gestionnaire.traiter_evenement_clavier(
            "m", TypeEvenement.CLAVIER_APPUI, self.moteur_mock
        ))
        
        # Rotation
        resultats.append(self.gestionnaire.traiter_evenement_clavier(
            "Up", TypeEvenement.CLAVIER_APPUI, self.moteur_mock
        ))
        
        # Then : Tous les contrôles fonctionnent
        self.assertEqual(resultats, [True, True, True])
        piece_mock.deplacer.assert_called_once_with(-1, 0)
        self.moteur_mock.tourner_piece_active.assert_called_once()
        self.audio_mock.basculer_mute_musique.assert_called_once()


if __name__ == '__main__':
    unittest.main()
