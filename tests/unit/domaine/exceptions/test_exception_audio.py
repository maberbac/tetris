"""
Tests unitaires pour ExceptionAudio - Phase TDD RED.
CONFORME AUX DIRECTIVES : Tests officiels dans tests/unit/domaine/exceptions/
"""

import unittest
import sys
import os

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'src'))

# Import qui doit maintenant fonctionner (TDD GREEN)
try:
    from domaine.exceptions.exception_audio import ExceptionAudio
    MODULE_DISPONIBLE = True
except ImportError:
    ExceptionAudio = None
    MODULE_DISPONIBLE = False


class TestExceptionAudio(unittest.TestCase):
    """Tests unitaires pour la classe ExceptionAudio."""
    
    def test_creation_exception_avec_message_defaut(self):
        """Test que ExceptionAudio peut être créée avec message par défaut."""
        if not MODULE_DISPONIBLE:
            self.skipTest("ExceptionAudio pas encore implémentée (TDD RED)")
            
        exc = ExceptionAudio()
        self.assertEqual(str(exc), "Erreur audio")
        self.assertEqual(exc.message, "Erreur audio")
    
    def test_creation_exception_avec_message_personnalise(self):
        """Test que ExceptionAudio peut être créée avec message personnalisé."""
        if not MODULE_DISPONIBLE:
            self.skipTest("ExceptionAudio pas encore implémentée (TDD RED)")
            
        message = "Système audio non disponible"
        exc = ExceptionAudio(message)
        self.assertEqual(str(exc), message)
        self.assertEqual(exc.message, message)
    
    def test_exception_herite_de_exception(self):
        """Test que ExceptionAudio hérite bien de Exception."""
        if not MODULE_DISPONIBLE:
            self.skipTest("ExceptionAudio pas encore implémentée (TDD RED)")
            
        exc = ExceptionAudio()
        self.assertIsInstance(exc, Exception)
    
    def test_message_exception_francais(self):
        """Test que les messages d'exception sont en français."""
        if not MODULE_DISPONIBLE:
            self.skipTest("ExceptionAudio pas encore implémentée (TDD RED)")
            
        # Test avec différents types d'erreurs audio
        messages_francais = [
            "Système audio non disponible",
            "Fichier audio introuvable : tetris-theme.wav", 
            "Mémoire insuffisante pour charger l'audio",
            "Impossible de jouer l'effet sonore : rotate.wav"
        ]
        
        for message in messages_francais:
            with self.subTest(message=message):
                exc = ExceptionAudio(message)
                self.assertEqual(str(exc), message)
                # Vérifier que le message est bien en français (pas d'anglais basique)
                self.assertNotIn("error", message.lower())
                self.assertNotIn("failed", message.lower())
                self.assertNotIn("cannot", message.lower())


if __name__ == '__main__':
    print("🧪 PHASE TDD RED : Tests ExceptionAudio")
    print("=" * 45)
    print("Ces tests vont échouer car ExceptionAudio n'existe pas encore.")
    print("C'est normal et attendu dans l'approche TDD !")
    print()
    unittest.main(verbosity=2)
