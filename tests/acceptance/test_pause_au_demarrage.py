"""
Tests d'acceptance pour la fonctionnalité de pause au démarrage.

Ces tests valident le comportement attendu :
- Le jeu démarre en pause
- ENTER et ESC permettent de basculer pause/jeu
- Les messages d'instruction sont affichés
- Le son est préservé (M pour mute/unmute)
"""

import unittest
import sys
import os

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.domaine.services.moteur_partie import MoteurPartie
from src.domaine.services.gestionnaire_evenements import GestionnaireEvenements, ToucheClavier


class TestPauseAuDemarrage(unittest.TestCase):
    """Tests d'acceptance pour la pause au démarrage."""
    
    def setUp(self):
        """Préparer les tests."""
        self.moteur = MoteurPartie()
        self.gestionnaire = GestionnaireEvenements()
    
    def test_moteur_demarre_en_pause(self):
        """✅ Le moteur démarre en pause pour permettre à l'utilisateur de se préparer."""
        print("🧪 Test : Le moteur démarre en pause")
        print("-" * 50)
        
        # GIVEN : Un nouveau moteur de jeu
        moteur = MoteurPartie()
        
        # THEN : Il doit démarrer en pause
        self.assertTrue(moteur.en_pause, "Le moteur doit démarrer en pause")
        print("✅ Le moteur démarre bien en pause")
    
    def test_basculement_pause_avec_messages(self):
        """✅ Le basculement de pause génère des messages explicatifs."""
        print("🧪 Test : Basculement de pause avec messages")
        print("-" * 50)
        
        # GIVEN : Un moteur en pause au démarrage
        moteur = MoteurPartie()
        self.assertTrue(moteur.en_pause, "Le moteur doit démarrer en pause")
        
        # WHEN : On bascule la pause (reprendre le jeu)
        moteur.basculer_pause()
        
        # THEN : Le jeu n'est plus en pause et un message est généré
        self.assertFalse(moteur.en_pause, "Le jeu ne doit plus être en pause")
        self.assertGreater(len(moteur.messages), 0, "Un message doit être généré")
        self.assertIn("repris", moteur.messages[0].lower(), "Le message doit indiquer que le jeu a repris")
        print("✅ Le basculement fonctionne avec messages explicatifs")
        
        # WHEN : On remet en pause
        moteur.basculer_pause()
        
        # THEN : Le jeu est en pause et un message de pause est généré
        self.assertTrue(moteur.en_pause, "Le jeu doit être en pause")
        self.assertGreater(len(moteur.messages), 1, "Un nouveau message doit être généré")
        message_pause = moteur.messages[-1]
        self.assertIn("pause", message_pause.lower(), "Le message doit mentionner la pause")
        self.assertIn("enter", message_pause.lower(), "Le message doit mentionner ENTER")
        self.assertIn("esc", message_pause.lower(), "Le message doit mentionner ESC")
        print("✅ Le message de pause contient les instructions ENTER/ESC")
    
    def test_touches_enter_et_esc_mappees(self):
        """✅ Les touches ENTER et ESC sont bien mappées pour la pause."""
        print("🧪 Test : Mapping des touches ENTER et ESC") 
        print("-" * 50)
        
        # GIVEN : Un gestionnaire d'événements
        gestionnaire = GestionnaireEvenements()
        
        # WHEN : On vérifie le mapping des touches
        mapping = gestionnaire._mapping_touches
        
        # THEN : ENTER doit être mappé à REPRENDRE
        self.assertIn("Return", mapping, "La touche ENTER (Return) doit être mappée")
        self.assertEqual(mapping["Return"], ToucheClavier.REPRENDRE, 
                        "ENTER doit être mappé à REPRENDRE")
        print("✅ ENTER est mappé à REPRENDRE")
        
        # AND : ESC doit être mappé à MENU (qui fait pause maintenant)
        self.assertIn("Escape", mapping, "La touche ESC (Escape) doit être mappée")
        self.assertEqual(mapping["Escape"], ToucheClavier.MENU,
                        "ESC doit être mappé à MENU")
        print("✅ ESC est mappé à MENU")
        
        # AND : Les commandes REPRENDRE et MENU doivent pointer vers pause
        commandes = gestionnaire._commandes
        self.assertIn(ToucheClavier.REPRENDRE, commandes, "REPRENDRE doit avoir une commande")
        self.assertIn(ToucheClavier.MENU, commandes, "MENU doit avoir une commande")
        
        # Vérifier que les deux sont des CommandePause
        commande_reprendre = commandes[ToucheClavier.REPRENDRE]
        commande_menu = commandes[ToucheClavier.MENU]
        self.assertEqual(type(commande_reprendre).__name__, "CommandePause",
                        "REPRENDRE doit utiliser CommandePause")
        self.assertEqual(type(commande_menu).__name__, "CommandePause", 
                        "MENU doit utiliser CommandePause")
        print("✅ ENTER et ESC utilisent tous deux CommandePause")


def run_tests():
    """Lance les tests d'acceptance de pause au démarrage."""
    print("🎯 TESTS D'ACCEPTANCE - PAUSE AU DÉMARRAGE")
    print("=" * 60)
    print("Validation de la fonctionnalité :")
    print("- Démarrage en pause")
    print("- Contrôles ENTER/ESC")
    print("- Messages explicatifs")
    print("=" * 60)
    
    # Créer la suite de tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPauseAuDemarrage)
    
    # Exécuter les tests avec verbosité
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Résumé
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 TOUS LES TESTS D'ACCEPTANCE RÉUSSIS !")
        print("✅ La fonctionnalité pause au démarrage est validée")
    else:
        print("❌ Certains tests ont échoué")
        print(f"Échecs: {len(result.failures)}")
        print(f"Erreurs: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
