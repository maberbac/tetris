"""
Adaptateur d'affichage pygame pour la partie de Tetris.

Implémentation concrète utilisant pygame pour l'affichage.
"""

import pygame
from typing import TYPE_CHECKING

from src.domaine.entites.piece import TypePiece
from src.ports.sortie.affichage_jeu import AffichageJeu

if TYPE_CHECKING:
    from src.domaine.services.moteur_partie import MoteurPartie


class AffichagePartie(AffichageJeu):
    """Affichage complet pour la partie de Tetris utilisant pygame."""
    
    def __init__(self):
        self.initialise = False
        
    def initialiser(self) -> None:
        """Initialise l'affichage pygame."""
        if self.initialise:
            return
            
        pygame.init()
        
        # Configuration d'affichage
        self.taille_cellule = 30
        self.largeur_plateau = 10
        self.hauteur_plateau = 20
        self.marge = 20
        
        # Zone de jeu
        self.largeur_jeu = self.largeur_plateau * self.taille_cellule
        self.hauteur_jeu = self.hauteur_plateau * self.taille_cellule
        
        # Interface complète avec panneaux latéraux
        self.largeur_interface = 200  # Panel droit pour stats/preview
        largeur_totale = self.largeur_jeu + self.largeur_interface + 3 * self.marge
        hauteur_totale = self.hauteur_jeu + 2 * self.marge + 60  # Space pour titre
        
        self.ecran = pygame.display.set_mode((largeur_totale, hauteur_totale))
        pygame.display.set_caption("Tetris - Partie Complète avec Génération Aléatoire")
        
        # Couleurs
        self.noir = (0, 0, 0)
        self.gris_fonce = (40, 40, 40)
        self.gris = (128, 128, 128) 
        self.blanc = (255, 255, 255)
        self.gris_place = (180, 180, 180)
        self.rouge = (255, 0, 0)
        self.vert = (0, 255, 0)
        self.bleu = (0, 0, 255)
        self.jaune = (255, 255, 0)
        self.cyan = (0, 255, 255)
        self.violet = (128, 0, 128)
        self.orange = (255, 165, 0)
        
        # Couleurs par type de pièce
        self.couleurs_pieces = {
            TypePiece.I: self.cyan,
            TypePiece.O: self.jaune,
            TypePiece.T: self.violet,
            TypePiece.S: self.vert,
            TypePiece.Z: self.rouge,
            TypePiece.J: self.bleu,
            TypePiece.L: self.orange
        }
        
        # Polices
        self.police_titre = pygame.font.Font(None, 32)
        self.police_normale = pygame.font.Font(None, 24)
        self.police_petite = pygame.font.Font(None, 18)
        
        # Zones de rendu
        self.zone_jeu_x = self.marge
        self.zone_jeu_y = self.marge + 40
        self.zone_interface_x = self.zone_jeu_x + self.largeur_jeu + self.marge
        
        self.initialise = True
        print("🖥️ Interface graphique initialisée")
    
    def dessiner(self, moteur: 'MoteurPartie') -> None:
        """Dessine l'interface complète du jeu."""
        if not self.initialise:
            self.initialiser()
            
        # Fond
        self.ecran.fill(self.noir)
        
        # Titre
        titre = "TETRIS - Partie Complète"
        texte_titre = self.police_titre.render(titre, True, self.blanc)
        self.ecran.blit(texte_titre, (self.marge, 5))
        
        # Zone de jeu principale
        self._dessiner_plateau(moteur)
        self._dessiner_piece_active(moteur)
        
        # Interface latérale
        self._dessiner_statistiques(moteur)
        self._dessiner_piece_suivante(moteur)
        self._dessiner_controles()
        
        # Messages et état
        self._dessiner_messages(moteur)
        self._dessiner_etat_jeu(moteur)
        
        pygame.display.flip()
    
    def nettoyer(self) -> None:
        """Nettoie les ressources pygame."""
        if self.initialise:
            pygame.quit()
            self.initialise = False
    
    def _dessiner_plateau(self, moteur: 'MoteurPartie') -> None:
        """Dessine la grille et les pièces placées."""
        # Grille de base
        for ligne in range(self.hauteur_plateau):
            for colonne in range(self.largeur_plateau):
                x = self.zone_jeu_x + colonne * self.taille_cellule
                y = self.zone_jeu_y + ligne * self.taille_cellule
                
                rect = pygame.Rect(x, y, self.taille_cellule, self.taille_cellule)
                pygame.draw.rect(self.ecran, self.gris_fonce, rect)
                pygame.draw.rect(self.ecran, self.gris, rect, 1)
        
        # Pièces placées (masquer la zone invisible)
        for position in moteur.plateau.positions_occupees:
            if position.y >= 0:  # Masquage de la zone invisible pour les pièces placées
                x = self.zone_jeu_x + position.x * self.taille_cellule
                y = self.zone_jeu_y + position.y * self.taille_cellule
                rect = pygame.Rect(x, y, self.taille_cellule, self.taille_cellule)
                pygame.draw.rect(self.ecran, self.gris_place, rect)
                pygame.draw.rect(self.ecran, self.blanc, rect, 2)
    
    def _dessiner_piece_active(self, moteur: 'MoteurPartie') -> None:
        """Dessine la pièce actuellement contrôlée."""
        if not moteur.piece_active:
            return
        
        couleur = self.couleurs_pieces.get(moteur.piece_active.type_piece, self.blanc)
        
        # Ne dessiner que les positions visibles (y >= 0) pour masquer la zone invisible
        for pos in moteur.piece_active.positions:
            if pos.y >= 0:  # Masquage de la zone invisible
                x = self.zone_jeu_x + pos.x * self.taille_cellule
                y = self.zone_jeu_y + pos.y * self.taille_cellule
                rect = pygame.Rect(x, y, self.taille_cellule, self.taille_cellule)
                pygame.draw.rect(self.ecran, couleur, rect)
                pygame.draw.rect(self.ecran, self.blanc, rect, 2)
    
    def _dessiner_statistiques(self, moteur: 'MoteurPartie') -> None:
        """Dessine les statistiques de la partie."""
        x = self.zone_interface_x
        y = self.zone_jeu_y
        
        # Titre
        titre = self.police_normale.render("STATISTIQUES", True, self.blanc)
        self.ecran.blit(titre, (x, y))
        y += 35
        
        # Score et niveau
        stats = moteur.stats
        textes_stats = [
            f"Score: {stats.score:,}",
            f"Niveau: {stats.niveau}",
            f"Lignes: {stats.lignes_completees}",
            f"Pièces: {stats.pieces_placees}",
            "",
            "Pièces utilisées:"
        ]
        
        for texte in textes_stats:
            if texte:
                rendu = self.police_petite.render(texte, True, self.blanc)
                self.ecran.blit(rendu, (x, y))
            y += 20
        
        # Statistiques par pièce
        for type_piece, count in stats.pieces_par_type.items():
            couleur = self.couleurs_pieces.get(type_piece, self.blanc)
            texte = f"{type_piece.value}: {count}"
            rendu = self.police_petite.render(texte, True, couleur)
            self.ecran.blit(rendu, (x + 10, y))
            y += 18
    
    def _dessiner_piece_suivante(self, moteur: 'MoteurPartie') -> None:
        """Dessine la preview de la pièce suivante."""
        if not moteur.piece_suivante:
            return
        
        x = self.zone_interface_x
        y = self.zone_jeu_y + 280
        
        # Titre
        titre = self.police_normale.render("SUIVANTE", True, self.blanc)
        self.ecran.blit(titre, (x, y))
        y += 30
        
        # Dessiner la pièce (centrée dans une petite zone)
        couleur = self.couleurs_pieces.get(moteur.piece_suivante.type_piece, self.blanc)
        taille_preview = 20
        
        # Calculer le centre de la preview
        min_x = min(pos.x for pos in moteur.piece_suivante.positions)
        max_x = max(pos.x for pos in moteur.piece_suivante.positions)
        min_y = min(pos.y for pos in moteur.piece_suivante.positions)
        max_y = max(pos.y for pos in moteur.piece_suivante.positions)
        
        offset_x = x + 30 - (min_x + max_x) * taille_preview // 2
        offset_y = y + 20 - (min_y + max_y) * taille_preview // 2
        
        for pos in moteur.piece_suivante.positions:
            rect_x = offset_x + pos.x * taille_preview
            rect_y = offset_y + pos.y * taille_preview
            rect = pygame.Rect(rect_x, rect_y, taille_preview, taille_preview)
            pygame.draw.rect(self.ecran, couleur, rect)
            pygame.draw.rect(self.ecran, self.blanc, rect, 1)
    
    def _dessiner_controles(self) -> None:
        """Dessine l'aide des contrôles."""
        x = self.zone_interface_x
        y = self.zone_jeu_y + 380
        
        titre = self.police_normale.render("CONTRÔLES", True, self.blanc)
        self.ecran.blit(titre, (x, y))
        y += 25
        
        controles = [
            "← → : Déplacer",
            "↑ : Rotation",
            "↓ : Chute rapide",
            "Space : Chute instant.",
            "P : Pause",
            "ESC : Menu/Quitter"
        ]
        
        for controle in controles:
            rendu = self.police_petite.render(controle, True, self.blanc)
            self.ecran.blit(rendu, (x, y))
            y += 16
    
    def _dessiner_messages(self, moteur: 'MoteurPartie') -> None:
        """Dessine les messages temporaires."""
        messages = moteur.obtenir_messages()
        
        if messages:
            y = self.zone_jeu_y + self.hauteur_jeu // 2
            for message in messages[-3:]:  # Maximum 3 messages
                rendu = self.police_normale.render(message, True, self.jaune)
                largeur_texte = rendu.get_width()
                x = self.zone_jeu_x + (self.largeur_jeu - largeur_texte) // 2
                
                # Fond semi-transparent
                rect_fond = pygame.Rect(x - 10, y - 5, largeur_texte + 20, 30)
                surface_fond = pygame.Surface((largeur_texte + 20, 30))
                surface_fond.set_alpha(128)
                surface_fond.fill(self.noir)
                self.ecran.blit(surface_fond, (x - 10, y - 5))
                
                self.ecran.blit(rendu, (x, y))
                y += 35
    
    def _dessiner_etat_jeu(self, moteur: 'MoteurPartie') -> None:
        """Dessine l'état actuel du jeu."""
        if moteur.jeu_termine:
            texte = "GAME OVER"
            couleur = self.rouge
        elif moteur.en_pause:
            texte = "PAUSE"
            couleur = self.jaune
        elif moteur.afficher_menu:
            texte = "MENU"
            couleur = self.vert
        else:
            return
        
        rendu = self.police_titre.render(texte, True, couleur)
        largeur_texte = rendu.get_width()
        x = self.zone_jeu_x + (self.largeur_jeu - largeur_texte) // 2
        y = self.zone_jeu_y + self.hauteur_jeu // 2 - 50
        
        # Fond semi-transparent
        rect_fond = pygame.Rect(x - 15, y - 10, largeur_texte + 30, 40)
        surface_fond = pygame.Surface((largeur_texte + 30, 40))
        surface_fond.set_alpha(180)
        surface_fond.fill(self.noir)
        self.ecran.blit(surface_fond, (x - 15, y - 10))
        
        self.ecran.blit(rendu, (x, y))
