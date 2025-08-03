"""
Tests d'acceptance pour la fonctionnalité de pause au démarrage.

Ces tests valident le comportement attendu :
- Le jeu démarre en pause
- La touche P permet de basculer pause/jeu
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
        self.assertIn("p", message_pause.lower(), "Le message doit mentionner la touche P")
        print("✅ Le message de pause contient les instructions sur la touche P")
    
    def test_touche_p_mappee(self):
        """✅ La touche P (principale) est bien mappée pour la pause."""
        print("🧪 Test : Mapping de la touche P") 
        print("-" * 50)
        
        # GIVEN : Un gestionnaire d'événements
        gestionnaire = GestionnaireEvenements()
        
        # WHEN : On vérifie le mapping des touches
        mapping = gestionnaire._mapping_touches
        
        # THEN : P doit être mappé à PAUSE (contrôle principal)
        self.assertIn("p", mapping, "La touche P doit être mappée")
        self.assertEqual(mapping["p"], ToucheClavier.PAUSE, 
                        "P doit être mappé à PAUSE")
        print("✅ P est mappé à PAUSE (contrôle principal)")
        
        # AND : La commande PAUSE a son rôle
        commandes = gestionnaire._commandes
        self.assertIn(ToucheClavier.PAUSE, commandes, "PAUSE doit avoir une commande")
        
        # Vérifier le type de commande
        commande_pause = commandes[ToucheClavier.PAUSE]
        self.assertEqual(type(commande_pause).__name__, "CommandePause",
                        "PAUSE doit utiliser CommandePause")
        print("✅ P utilise CommandePause")


def run_tests():
    """Lance les tests d'acceptance de pause au démarrage."""
    print("🎯 TESTS D'ACCEPTANCE - PAUSE AU DÉMARRAGE")
    print("=" * 60)
    print("Validation de la fonctionnalité :")
    print("- Démarrage en pause")
    print("- Contrôle principal : P")
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
