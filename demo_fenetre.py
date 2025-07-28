"""
Démonstration de la grille en mode fenêtré.
"""

import pygame
import sys
from affichage_test import AffichageTest

def main():
    """
    Fonction principale pour tester l'affichage en mode fenêtré.
    """
    # Créer l'affichage en mode test
    affichage = AffichageTest()
    
    # Variables pour la boucle de jeu
    horloge = pygame.time.Clock()
    jeu_actif = True
    
    print("Grille Tetris affichée en mode fenêtré. Fermez la fenêtre pour quitter.")
    
    # Boucle de jeu principale
    while jeu_actif:
        # Gérer les événements
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                jeu_actif = False
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    jeu_actif = False
        
        # Dessiner la grille
        affichage.dessiner_grille()
        
        # Mettre à jour l'affichage
        affichage.mettre_a_jour()
        
        # Contrôler le framerate
        horloge.tick(60)
    
    # Nettoyer et quitter
    affichage.nettoyer()
    print("Démonstration terminée.")

if __name__ == "__main__":
    main()
