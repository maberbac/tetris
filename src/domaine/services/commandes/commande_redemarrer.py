"""
Commande pour redémarrer une nouvelle partie (touche R)
Respecte le Command Pattern et les directives TDD
"""

from .commandes_base import Commande, MoteurJeu


class CommandeRedemarrer(Commande):
    """
    Commande pour redémarrer une nouvelle partie avec la touche R.
    Ne fonctionne que si le jeu est en état game over.
    
    Architecture : Command Pattern
    Responsabilité : Gérer le redémarrage d'une nouvelle partie
    """

    def execute(self, moteur: MoteurJeu) -> bool:
        """
        Exécute la commande de redémarrage.
        
        Args:
            moteur: Le moteur de jeu à redémarrer
            
        Returns:
            True si redémarrage effectué, False si ignoré
        """
        if not moteur.est_game_over():
            # Ne redémarre que si game over
            return False
            
        # Redémarrage complet de la partie
        moteur.redemarrer_partie()
        return True
