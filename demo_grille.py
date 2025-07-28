"""
Fichier principal pour tester l'affichage de la grille Tetris.
"""

import pygame
import sys
from affichage import Affichage

def main():
    """
    Fonction principale pour tester l'affichage.
    """
    # Créer l'affichage
    affichage = Affichage()
    
    # Variables pour la boucle de jeu
    horloge = pygame.time.Clock()
    jeu_actif = True
    
    print("Grille Tetris affichée. Appuyez sur ECHAP pour quitter.")
    
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
    sys.exit()

if __name__ == "__main__":
    main()
