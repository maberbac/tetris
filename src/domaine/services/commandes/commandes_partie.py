"""
Commandes spécifiques à la partie de Tetris.

Services du domaine pour orchestrer les actions de jeu.
"""

from .commandes_base import Commande


class CommandePlacerPiecePartie(Commande):
    """Commande pour placer une pièce définitivement dans la partie."""
    
    def execute(self, moteur) -> bool:
        """Place la pièce active et génère une nouvelle pièce."""
        return moteur.placer_piece_et_generer_nouvelle()


class CommandeChuteRapidePartie(Commande):
    """Commande de chute rapide pour la partie."""
    
    def execute(self, moteur) -> bool:
        """Fait tomber la pièce jusqu'en bas."""
        return moteur.chute_rapide()


class CommandeDeplacerGauchePartie(Commande):
    """Commande de déplacement gauche pour la partie."""
    
    def execute(self, moteur) -> bool:
        """Déplace la pièce vers la gauche si possible."""
        return moteur.deplacer_piece_active(-1, 0)


class CommandeDeplacerDroitePartie(Commande):
    """Commande de déplacement droite pour la partie."""
    
    def execute(self, moteur) -> bool:
        """Déplace la pièce vers la droite si possible."""
        return moteur.deplacer_piece_active(1, 0)


class CommandeTournerPartie(Commande):
    """Commande de rotation pour la partie."""
    
    def execute(self, moteur) -> bool:
        """Fait tourner la pièce si possible."""
        return moteur.tourner_piece_active()
