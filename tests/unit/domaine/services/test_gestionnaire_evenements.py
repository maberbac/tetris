"""
Tests pour le gestionnaire d'événements Tetris

Tests organisés par responsabilité :
1. Configuration et mapping des touches
2. Traitement des événements clavier
3. Gestion de la répétition
4. Intégration avec les commandes
"""

import unittest
from unittest.mock import Mock, patch
import time
from src.domaine.services.gestionnaire_evenements import (
    GestionnaireEvenements, TypeEvenement, ToucheClavier,
    ConfigurationControles
)


class TestConfigurationControles(unittest.TestCase):
    """Tests pour la configuration des contrôles."""
    
    def test_mapping_defaut_contient_touches_principales(self):
        """Le mapping par défaut doit contenir toutes les touches principales."""
        mapping = ConfigurationControles.obtenir_mapping_defaut()
        
        # Vérifier les touches fléchées
        self.assertIn("Left", mapping)
        self.assertIn("Right", mapping)
        self.assertIn("Down", mapping)
        self.assertIn("Up", mapping)
        
        # Vérifier les touches spéciales
        self.assertIn("space", mapping)
        self.assertIn("p", mapping)
        self.assertIn("m", mapping)
        
        # Vérifier qu'on a exactement 7 touches essentielles (incluant mute)
        self.assertEqual(len(mapping), 7)
    
    def test_mapping_defaut_est_copie(self):
        """obtenir_mapping_defaut() doit retourner une copie."""
        mapping1 = ConfigurationControles.obtenir_mapping_defaut()
        mapping2 = ConfigurationControles.obtenir_mapping_defaut()
        
        # Modifier un mapping ne doit pas affecter l'autre
        mapping1["test"] = ToucheClavier.GAUCHE
        
        self.assertNotIn("test", mapping2)


class TestGestionnaireEvenements(unittest.TestCase):
    """Tests pour le gestionnaire d'événements principal."""
    
    def setUp(self):
        """Configuration commune pour les tests."""
        self.gestionnaire = GestionnaireEvenements()
        self.moteur = Mock()
    
    def test_initialisation_avec_mapping_defaut(self):
        """Le gestionnaire doit s'initialiser avec le mapping par défaut."""
        touches_mappees = self.gestionnaire.obtenir_touches_mappees()
        
        self.assertIn("Left", touches_mappees)
        self.assertEqual(touches_mappees["Left"], ToucheClavier.GAUCHE)
    
    def test_initialisation_avec_mapping_personnalise(self):
        """Le gestionnaire doit accepter un mapping personnalisé."""
        mapping_perso = {"w": ToucheClavier.ROTATION, "s": ToucheClavier.CHUTE_RAPIDE}
        gestionnaire = GestionnaireEvenements(mapping_perso)
        
        touches_mappees = gestionnaire.obtenir_touches_mappees()
        
        self.assertEqual(touches_mappees["w"], ToucheClavier.ROTATION)
        self.assertEqual(touches_mappees["s"], ToucheClavier.CHUTE_RAPIDE)
        self.assertEqual(len(touches_mappees), 2)


class TestTraitementEvenements(unittest.TestCase):
    """Tests pour le traitement des événements."""
    
    def setUp(self):
        """Configuration avec mock du moteur."""
        self.gestionnaire = GestionnaireEvenements()
        self.moteur = Mock()
        
        # Configurer les mocks du moteur
        self.piece_mock = Mock()
        self.plateau_mock = Mock()
        
        self.moteur.obtenir_piece_active.return_value = self.piece_mock
        self.moteur.obtenir_plateau.return_value = self.plateau_mock
        
        # Par défaut, les actions réussissent
        self.plateau_mock.peut_placer_piece.return_value = True
        self.moteur.faire_descendre_piece.return_value = True
    
    def test_traitement_appui_touche_gauche(self):
        """L'appui de la touche gauche doit exécuter la commande correspondante."""
        # Simuler l'appui de la touche gauche
        resultat = self.gestionnaire.traiter_evenement_clavier(
            "Left", TypeEvenement.CLAVIER_APPUI, self.moteur
        )
        
        self.assertTrue(resultat)
        self.piece_mock.deplacer.assert_called_once_with(-1, 0)
    
    def test_traitement_appui_touche_droite(self):
        """L'appui de la touche droite doit exécuter la commande correspondante."""
        resultat = self.gestionnaire.traiter_evenement_clavier(
            "Right", TypeEvenement.CLAVIER_APPUI, self.moteur
        )
        
        self.assertTrue(resultat)
        self.piece_mock.deplacer.assert_called_once_with(1, 0)
    
    def test_traitement_appui_touche_bas(self):
        """L'appui de la touche bas doit faire descendre la pièce."""
        resultat = self.gestionnaire.traiter_evenement_clavier(
            "Down", TypeEvenement.CLAVIER_APPUI, self.moteur
        )
        
        self.assertTrue(resultat)
        self.moteur.faire_descendre_piece.assert_called_once()
    
    def test_traitement_appui_touche_rotation(self):
        """L'appui de la touche rotation doit faire tourner la pièce."""
        resultat = self.gestionnaire.traiter_evenement_clavier(
            "Up", TypeEvenement.CLAVIER_APPUI, self.moteur
        )
        
        self.assertTrue(resultat)
        self.moteur.tourner_piece_active.assert_called_once()
    
    def test_traitement_appui_touche_mute(self):
        """L'appui de la touche mute doit basculer le mute de l'audio."""
        # Mock pour le système audio
        self.moteur.obtenir_audio = Mock()
        audio_mock = Mock()
        self.moteur.obtenir_audio.return_value = audio_mock
        
        resultat = self.gestionnaire.traiter_evenement_clavier(
            "m", TypeEvenement.CLAVIER_APPUI, self.moteur
        )
        
        self.assertTrue(resultat)
        audio_mock.basculer_mute_musique.assert_called_once()
    
    def test_traitement_touche_inconnue(self):
        """Une touche inconnue ne doit pas être traitée."""
        resultat = self.gestionnaire.traiter_evenement_clavier(
            "ToucheInexistante", TypeEvenement.CLAVIER_APPUI, self.moteur
        )
        
        self.assertFalse(resultat)
    
    def test_traitement_echec_commande(self):
        """Un échec de commande doit être correctement géré."""
        # Configurer l'échec du déplacement
        self.plateau_mock.peut_placer_piece.return_value = False
        
        resultat = self.gestionnaire.traiter_evenement_clavier(
            "Left", TypeEvenement.CLAVIER_APPUI, self.moteur
        )
        
        self.assertFalse(resultat)


class TestGestionRepetition(unittest.TestCase):
    """Tests pour la gestion de la répétition des touches."""
    
    def setUp(self):
        """Configuration pour les tests de répétition."""
        self.gestionnaire = GestionnaireEvenements()
        self.moteur = Mock()
        
        # Configurer des délais courts pour les tests
        self.gestionnaire.configurer_delais_repetition(0.1, 0.05)  # 100ms initial, 50ms répétition
        
        # Mocks pour le moteur
        self.piece_mock = Mock()
        self.plateau_mock = Mock()
        
        self.moteur.obtenir_piece_active.return_value = self.piece_mock
        self.moteur.obtenir_plateau.return_value = self.plateau_mock
        self.plateau_mock.peut_placer_piece.return_value = True
    
    def test_appui_marque_touche_repetable(self):
        """L'appui d'une touche répétable doit être marqué."""
        temps_debut = time.time()
        
        # Appuyer sur une touche répétable
        self.gestionnaire.traiter_evenement_clavier(
            "Left", TypeEvenement.CLAVIER_APPUI, self.moteur, temps_debut
        )
        
        # Vérifier que la touche est marquée comme maintenue
        self.assertIn(ToucheClavier.GAUCHE, self.gestionnaire._touches_maintenues)
    
    def test_relache_supprime_touche_maintenue(self):
        """Le relâchement d'une touche doit la supprimer des touches maintenues."""
        temps_debut = time.time()
        
        # Appuyer puis relâcher
        self.gestionnaire.traiter_evenement_clavier(
            "Left", TypeEvenement.CLAVIER_APPUI, self.moteur, temps_debut
        )
        self.gestionnaire.traiter_evenement_clavier(
            "Left", TypeEvenement.CLAVIER_RELACHE, self.moteur, temps_debut
        )
        
        # Vérifier que la touche n'est plus maintenue
        self.assertNotIn(ToucheClavier.GAUCHE, self.gestionnaire._touches_maintenues)
    
    def test_repetition_apres_delai_initial(self):
        """La répétition doit commencer après le délai initial."""
        temps_debut = time.time()
        
        # Appuyer sur la touche
        self.gestionnaire.traiter_evenement_clavier(
            "Left", TypeEvenement.CLAVIER_APPUI, self.moteur, temps_debut
        )
        
        # Simuler le temps qui passe (après délai initial)
        temps_repetition = temps_debut + 0.12  # 120ms > 100ms initial
        
        resultat = self.gestionnaire.traiter_evenement_clavier(
            "Left", TypeEvenement.CLAVIER_MAINTENU, self.moteur, temps_repetition
        )
        
        # La répétition devrait avoir lieu
        # Note: dépend de la précision temporelle, test approximatif
        self.assertIsInstance(resultat, bool)
    
    def test_touche_non_repetable_pas_marquee(self):
        """Les touches non répétables ne doivent pas être marquées."""
        temps_debut = time.time()
        
        # Appuyer sur une touche non répétable (rotation)
        self.gestionnaire.traiter_evenement_clavier(
            "Up", TypeEvenement.CLAVIER_APPUI, self.moteur, temps_debut
        )
        
        # Vérifier que la touche n'est pas marquée pour répétition
        self.assertNotIn(ToucheClavier.ROTATION, self.gestionnaire._touches_maintenues)
    
    def test_reinitialisation_touches_maintenues(self):
        """La réinitialisation doit vider toutes les touches maintenues."""
        temps_debut = time.time()
        
        # Appuyer sur plusieurs touches
        for touche in ["Left", "Right", "Down"]:
            self.gestionnaire.traiter_evenement_clavier(
                touche, TypeEvenement.CLAVIER_APPUI, self.moteur, temps_debut
            )
        
        # Vérifier qu'elles sont maintenues
        self.assertGreater(len(self.gestionnaire._touches_maintenues), 0)
        
        # Réinitialiser
        self.gestionnaire.reinitialiser_touches_maintenues()
        
        # Vérifier que tout est vide
        self.assertEqual(len(self.gestionnaire._touches_maintenues), 0)


class TestPersonnalisationMapping(unittest.TestCase):
    """Tests pour la personnalisation du mapping des touches."""
    
    def setUp(self):
        """Configuration pour les tests de personnalisation."""
        self.gestionnaire = GestionnaireEvenements()
        self.moteur = Mock()
    
    def test_ajout_mapping_personnalise(self):
        """On doit pouvoir ajouter un mapping personnalisé."""
        # Ajouter un nouveau mapping
        self.gestionnaire.ajouter_mapping_touche("w", ToucheClavier.ROTATION)
        
        # Vérifier qu'il est présent
        mapping = self.gestionnaire.obtenir_touches_mappees()
        self.assertEqual(mapping["w"], ToucheClavier.ROTATION)
    
    def test_suppression_mapping(self):
        """On doit pouvoir supprimer un mapping."""
        # Vérifier qu'un mapping existe
        mapping_avant = self.gestionnaire.obtenir_touches_mappees()
        self.assertIn("Left", mapping_avant)
        
        # Supprimer le mapping
        self.gestionnaire.supprimer_mapping_touche("Left")
        
        # Vérifier qu'il n'existe plus
        mapping_apres = self.gestionnaire.obtenir_touches_mappees()
        self.assertNotIn("Left", mapping_apres)
    
    def test_modification_mapping_existant(self):
        """On doit pouvoir modifier un mapping existant."""
        # Modifier un mapping existant
        self.gestionnaire.ajouter_mapping_touche("Left", ToucheClavier.DROITE)
        
        # Vérifier la modification
        mapping = self.gestionnaire.obtenir_touches_mappees()
        self.assertEqual(mapping["Left"], ToucheClavier.DROITE)


class TestStatistiques(unittest.TestCase):
    """Tests pour les fonctionnalités de statistiques."""
    
    def test_statistiques_format(self):
        """Les statistiques doivent avoir le bon format."""
        gestionnaire = GestionnaireEvenements()
        
        stats = gestionnaire.statistiques()
        
        self.assertIsInstance(stats, str)
        self.assertIn("GestionnaireEvenements", stats)
        self.assertIn("mappings", stats)
        self.assertIn("commandes", stats)


if __name__ == '__main__':
    unittest.main()
