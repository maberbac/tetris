"""
Module d'affichage pour le jeu Tetris.
Gère la fenêtre de jeu et le rendu de la grille.
"""

import pygame

class Affichage:
    """
    Classe responsable de l'affichage du jeu Tetris.
    
    Attributs:
        ecran: Surface principale de pygame
        largeur_ecran: Largeur de l'écran
        hauteur_ecran: Hauteur de l'écran
        position_grille_x: Position X de la grille (centrée)
        position_grille_y: Position Y de la grille (centrée)
    """
    
    # Constantes de couleur
    COULEUR_NOIR = (0, 0, 0)        # #000000 - Arrière-plan
    COULEUR_GRIS = (192, 192, 192)  # #C0C0C0 - Fond des cellules
    COULEUR_BLANC = (255, 255, 255) # #FFFFFF - Contours des cellules
    
    # Constantes de dimensions
    LARGEUR_GRILLE = 10    # Nombre de colonnes
    HAUTEUR_GRILLE = 20    # Nombre de lignes
    TAILLE_CELLULE = 30    # Taille d'une cellule en pixels
    
    def __init__(self):
        """
        Initialise le système d'affichage.
        Crée une fenêtre plein écran et calcule la position de la grille.
        """
        pygame.init()
        
        # Créer une fenêtre plein écran
        self.ecran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Tetris")
        
        # Obtenir les dimensions de l'écran
        self.largeur_ecran = self.ecran.get_width()
        self.hauteur_ecran = self.ecran.get_height()
        
        # Calculer la position pour centrer la grille
        largeur_grille_pixels = self.LARGEUR_GRILLE * self.TAILLE_CELLULE   # 300px
        hauteur_grille_pixels = self.HAUTEUR_GRILLE * self.TAILLE_CELLULE   # 600px
        
        self.position_grille_x = (self.largeur_ecran - largeur_grille_pixels) // 2
        self.position_grille_y = (self.hauteur_ecran - hauteur_grille_pixels) // 2
    
    def dessiner_grille(self):
        """
        Dessine la grille de jeu vide.
        """
        # Remplir l'arrière-plan en noir
        self.ecran.fill(self.COULEUR_NOIR)
        
        # Dessiner chaque cellule de la grille
        for ligne in range(self.HAUTEUR_GRILLE):
            for colonne in range(self.LARGEUR_GRILLE):
                # Calculer la position de la cellule
                position_cellule_x = self.position_grille_x + colonne * self.TAILLE_CELLULE
                position_cellule_y = self.position_grille_y + ligne * self.TAILLE_CELLULE
                
                # Créer le rectangle de la cellule
                rectangle_cellule = pygame.Rect(position_cellule_x, position_cellule_y, 
                                               self.TAILLE_CELLULE, self.TAILLE_CELLULE)
                
                # Remplir la cellule en gris
                pygame.draw.rect(self.ecran, self.COULEUR_GRIS, rectangle_cellule)
                
                # Dessiner le contour blanc
                pygame.draw.rect(self.ecran, self.COULEUR_BLANC, rectangle_cellule, 1)
    
    def mettre_a_jour(self):
        """
        Met à jour l'affichage.
        """
        pygame.display.flip()
    
    def nettoyer(self):
        """
        Nettoie les ressources pygame.
        """
        pygame.quit()
