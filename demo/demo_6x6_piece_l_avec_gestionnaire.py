"""
Démonstration Plateau 6x6 avec Pièce L - Version avec Gestionnaire d'Événements

Cette version utilise le vrai système de commandes et gestionnaire d'événements
du projet Tetris, montrant l'intégration complète de l'architecture.

Contrôles (selon le gestionnaire) :
- ← → : Déplacer gauche/droite
- ↑ : Rotation  
- ↓ : Descendre
- Espace : Chute instantanée (pas implémentée ici)
- ESC : Menu (quitter pour cette démo)
- P : Pause
"""

import pygame
import sys
import os
import time

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.domaine.entites.fabriques.fabrique_pieces import FabriquePieces
from src.domaine.entites.piece import TypePiece, Piece
from src.domaine.entites.position import Position
from src.domaine.services.gestionnaire_evenements import GestionnaireEvenements, TypeEvenement, ToucheClavier
from src.domaine.services.commandes import MoteurJeu, Commande


class CommandeChuteRapideDemo(Commande):
    """Commande de chute rapide modifiée pour la démo - sans génération de nouvelle pièce."""
    
    def execute(self, moteur) -> bool:
        """Fait tomber la pièce jusqu'en bas sans la remplacer."""
        if hasattr(moteur, 'chute_rapide_demo'):
            return moteur.chute_rapide_demo()
        return False


class CommandePlacerPieceDemo(Commande):
    """Commande pour placer une pièce définitivement sur le plateau."""
    
    def execute(self, moteur) -> bool:
        """Place la pièce sur le plateau et génère une nouvelle pièce."""
        moteur.placer_piece_definitivement()
        moteur.generer_nouvelle_piece()
        return True


class CommandeDeplacerGaucheDemo(Commande):
    """Commande de déplacement gauche corrigée pour la démo."""
    
    def execute(self, moteur) -> bool:
        """Déplace la pièce vers la gauche si possible."""
        piece = moteur.obtenir_piece_active()
        plateau = moteur.obtenir_plateau()
        
        # Sauvegarder l'état actuel (positions ET pivot)
        positions_originales = piece.positions.copy()
        pivot_original = Position(piece.position_pivot.x, piece.position_pivot.y)
        
        # Essayer le déplacement
        piece.deplacer(-1, 0)
        
        # Vérifier si le déplacement est valide
        if plateau.peut_placer_piece(piece):
            print(f"⬅️ Gauche → {piece.positions}")
            return True
        else:
            # Annuler le déplacement (positions ET pivot)
            piece.positions = positions_originales
            piece.position_pivot = pivot_original
            return False


class CommandeDeplacerDroiteDemo(Commande):
    """Commande de déplacement droite corrigée pour la démo."""
    
    def execute(self, moteur) -> bool:
        """Déplace la pièce vers la droite si possible."""
        piece = moteur.obtenir_piece_active()
        plateau = moteur.obtenir_plateau()
        
        # Sauvegarder l'état actuel (positions ET pivot)
        positions_originales = piece.positions.copy()
        pivot_original = Position(piece.position_pivot.x, piece.position_pivot.y)
        
        # Essayer le déplacement
        piece.deplacer(1, 0)
        
        # Vérifier si le déplacement est valide
        if plateau.peut_placer_piece(piece):
            print(f"➡️ Droite → {piece.positions}")
            return True
        else:
            # Annuler le déplacement (positions ET pivot)
            piece.positions = positions_originales
            piece.position_pivot = pivot_original
            return False


class CommandeTournerDemo(Commande):
    """Commande de rotation corrigée pour la démo."""
    
    def execute(self, moteur) -> bool:
        """Fait tourner la pièce si possible."""
        piece = moteur.obtenir_piece_active()
        plateau = moteur.obtenir_plateau()
        
        # Sauvegarder l'état actuel (positions ET orientation si elle existe)
        positions_originales = piece.positions.copy()
        orientation_originale = getattr(piece, '_orientation', None)
        
        # Essayer la rotation
        piece.tourner()
        
        # Vérifier si la rotation est valide
        if plateau.peut_placer_piece(piece):
            print(f"🔄 Rotation → {piece.positions}")
            return True
        else:
            # Annuler la rotation
            piece.positions = positions_originales
            if orientation_originale is not None:
                piece._orientation = orientation_originale
            return False


class PlateauDemo:
    """Plateau simple pour la démonstration 6x6."""
    
    def __init__(self, largeur: int, hauteur: int):
        self.largeur = largeur
        self.hauteur = hauteur
        self._positions_occupees = set()
    
    def peut_placer_piece(self, piece: Piece) -> bool:
        """Vérifie si une pièce peut être placée."""
        for position in piece.positions:
            # Vérifier les limites
            if (position.x < 0 or position.x >= self.largeur or
                position.y < 0 or position.y >= self.hauteur):
                # Debug seulement pour les cas problématiques
                #print(f"🚫 Collision limite: position {position} hors plateau ({self.largeur}x{self.hauteur})")
                return False
            # Vérifier les collisions avec pièces placées
            if position in self._positions_occupees:
                # Debug seulement pour les cas problématiques  
                #print(f"🚫 Collision pièce: position {position} déjà occupée")
                return False
        return True
    
    def placer_piece(self, piece: Piece):
        """Place une pièce définitivement."""
        for position in piece.positions:
            self._positions_occupees.add(position)
    
    def obtenir_positions_occupees(self):
        """Retourne les positions occupées."""
        return self._positions_occupees.copy()


class MoteurDemo6x6:
    """
    Moteur simple pour la démonstration 6x6.
    Implémente le protocole MoteurJeu pour fonctionner avec les commandes.
    """
    
    def __init__(self):
        # Plateau 6x6 pour la démo
        self.plateau = PlateauDemo(largeur=6, hauteur=6)
        
        # Créer la pièce L au centre
        fabrique = FabriquePieces()
        self.piece_active = fabrique.creer(TypePiece.L, x_pivot=2, y_pivot=2)
        
        # État du jeu
        self.en_pause = False
        self.afficher_menu = False
        
        print(f"🎮 Moteur démo 6x6 initialisé")
        print(f"📍 Pièce L créée: {self.piece_active.positions}")
    
    def obtenir_piece_active(self) -> Piece:
        """Retourne la pièce actuellement contrôlée."""
        return self.piece_active
    
    def obtenir_plateau(self) -> PlateauDemo:
        """Retourne le plateau de jeu."""
        return self.plateau
    
    def faire_descendre_piece(self) -> bool:
        """Fait descendre la pièce d'une ligne si possible."""
        # Sauvegarder les positions
        positions_orig = self.piece_active.positions.copy()
        pivot_orig = self.piece_active.position_pivot
        
        # Essayer de descendre
        self.piece_active.deplacer(0, 1)
        
        # Vérifier si c'est valide
        if self.plateau.peut_placer_piece(self.piece_active):
            print(f"⬇️ Descente → {self.piece_active.positions}")
            return True
        else:
            # Annuler le mouvement
            self.piece_active.positions = positions_orig
            self.piece_active.position_pivot = pivot_orig
            return False
    
    def placer_piece_definitivement(self) -> None:
        """Place la pièce définitivement sur le plateau."""
        # Placer la pièce sur le plateau
        self.plateau.placer_piece(self.piece_active)
        print(f"📍 Pièce placée définitivement à: {self.piece_active.positions}")
    
    def generer_nouvelle_piece(self) -> None:
        """Génère une nouvelle pièce (pour cette démo, on recrée une L)."""
        fabrique = FabriquePieces()
        self.piece_active = fabrique.creer(TypePiece.L, x_pivot=2, y_pivot=1)
        print(f"✨ Nouvelle pièce L générée: {self.piece_active.positions}")
    
    def chute_rapide_demo(self) -> bool:
        """Chute rapide modifiée pour la démo - sans génération de nouvelle pièce."""
        nb_lignes_descendues = 0
        
        while True:
            # Sauvegarder la position actuelle
            positions_orig = self.piece_active.positions.copy()
            pivot_orig = self.piece_active.position_pivot
            
            # Essayer de descendre
            self.piece_active.deplacer(0, 1)
            
            # Vérifier si le déplacement est valide
            if self.plateau.peut_placer_piece(self.piece_active):
                nb_lignes_descendues += 1
            else:
                # Annuler le dernier déplacement et arrêter
                self.piece_active.positions = positions_orig
                self.piece_active.position_pivot = pivot_orig
                break
        
        if nb_lignes_descendues > 0:
            print(f"🚀 Chute rapide: {nb_lignes_descendues} lignes → {self.piece_active.positions}")
        
        return nb_lignes_descendues > 0
    
    def basculer_pause(self):
        """Bascule l'état de pause."""
        self.en_pause = not self.en_pause
        print(f"⏸️ Pause: {'ON' if self.en_pause else 'OFF'}")
    
    def basculer_menu(self):
        """Bascule l'affichage du menu."""
        self.afficher_menu = not self.afficher_menu
        print(f"📋 Menu: {'OUVERT' if self.afficher_menu else 'FERMÉ'}")


class AffichageAvecGestionnaire:
    """Affichage pour la démo avec gestionnaire d'événements."""
    
    def __init__(self):
        pygame.init()
        
        # Configuration d'affichage
        self.taille_cellule = 60
        self.largeur_plateau = 6
        self.hauteur_plateau = 6
        self.marge = 40
        
        # Fenêtre
        largeur_fenetre = self.largeur_plateau * self.taille_cellule + 2 * self.marge
        hauteur_fenetre = self.hauteur_plateau * self.taille_cellule + 2 * self.marge + 120
        
        self.ecran = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
        pygame.display.set_caption("Demo 6x6 - Avec Gestionnaire d'Événements")
        
        # Couleurs
        self.noir = (0, 0, 0)
        self.gris = (64, 64, 64)
        self.blanc = (255, 255, 255)
        self.orange = (255, 165, 0)
        self.rouge = (255, 0, 0)      # Pour pause
        self.vert = (0, 255, 0)       # Pour menu
        
        # Police
        self.police = pygame.font.Font(None, 20)
        self.police_titre = pygame.font.Font(None, 24)
    
    def dessiner(self, moteur: MoteurDemo6x6):
        """Dessine tout l'affichage."""
        # Fond
        self.ecran.fill(self.noir)
        
        # Grille de base
        for ligne in range(self.hauteur_plateau):
            for colonne in range(self.largeur_plateau):
                x = self.marge + colonne * self.taille_cellule
                y = self.marge + ligne * self.taille_cellule
                
                rect = pygame.Rect(x, y, self.taille_cellule, self.taille_cellule)
                pygame.draw.rect(self.ecran, self.gris, rect)
                pygame.draw.rect(self.ecran, self.blanc, rect, 1)
        
        # Pièces du plateau (si il y en a)
        for position in moteur.plateau.obtenir_positions_occupees():
            x = self.marge + position.x * self.taille_cellule
            y = self.marge + position.y * self.taille_cellule
            rect = pygame.Rect(x, y, self.taille_cellule, self.taille_cellule)
            pygame.draw.rect(self.ecran, self.rouge, rect)
            pygame.draw.rect(self.ecran, self.blanc, rect, 2)
        
        # Pièce active
        for pos in moteur.piece_active.positions:
            x = self.marge + pos.x * self.taille_cellule
            y = self.marge + pos.y * self.taille_cellule
            rect = pygame.Rect(x, y, self.taille_cellule, self.taille_cellule)
            pygame.draw.rect(self.ecran, self.orange, rect)
            pygame.draw.rect(self.ecran, self.blanc, rect, 2)
        
        # Instructions et état
        y_texte = self.marge + self.hauteur_plateau * self.taille_cellule + 10
        
        # Titre
        titre = "Demo 6x6 - Gestionnaire d'Événements"
        texte_titre = self.police_titre.render(titre, True, self.blanc)
        self.ecran.blit(texte_titre, (self.marge, y_texte))
        y_texte += 30
        
        # Contrôles
        instructions = [
            "← → : Déplacer | ↑ : Rotation | ↓ : Descendre",
            "ESPACE : Chute rapide | ENTRÉE : Placer pièce",
            "P : Pause | ESC : Menu/Quitter",
        ]
        
        for instruction in instructions:
            texte = self.police.render(instruction, True, self.blanc)
            self.ecran.blit(texte, (self.marge, y_texte))
            y_texte += 22
        
        # État du jeu
        couleur_etat = self.rouge if moteur.en_pause else (self.vert if moteur.afficher_menu else self.blanc)
        etat = "PAUSE" if moteur.en_pause else ("MENU" if moteur.afficher_menu else "JEU")
        texte_etat = self.police.render(f"État: {etat}", True, couleur_etat)
        self.ecran.blit(texte_etat, (self.marge, y_texte))
        
        pygame.display.flip()


def convertir_touche_pygame(touche_pygame: int) -> str:
    """Convertit une touche pygame en nom de touche pour le gestionnaire."""
    mapping_pygame = {
        pygame.K_LEFT: "Left",
        pygame.K_RIGHT: "Right",
        pygame.K_UP: "Up",
        pygame.K_DOWN: "Down",
        pygame.K_SPACE: "space",
        pygame.K_ESCAPE: "Escape",
        pygame.K_p: "p",
    }
    return mapping_pygame.get(touche_pygame, "")


class GestionnaireDemoPersonnalise(GestionnaireEvenements):
    """Gestionnaire d'événements personnalisé pour la démo."""
    
    def _creer_commandes(self):
        """Crée le mapping avec nos commandes personnalisées."""
        from src.domaine.services.commandes import (
            CommandeDescendre, CommandePause, CommandeAfficherMenu
        )
        
        return {
            ToucheClavier.GAUCHE: CommandeDeplacerGaucheDemo(),           # Notre version corrigée
            ToucheClavier.DROITE: CommandeDeplacerDroiteDemo(),          # Notre version corrigée
            ToucheClavier.ROTATION: CommandeTournerDemo(),               # Notre version corrigée
            ToucheClavier.CHUTE_RAPIDE: CommandeDescendre(),
            ToucheClavier.CHUTE_INSTANTANEE: CommandeChuteRapideDemo(),  # Notre version modifiée
            ToucheClavier.MENU: CommandeAfficherMenu(),
            ToucheClavier.PAUSE: CommandePause(),
        }


class DemoAvecGestionnaire:
    """Démonstration principale utilisant le gestionnaire d'événements."""
    
    def __init__(self):
        self.moteur = MoteurDemo6x6()
        self.affichage = AffichageAvecGestionnaire()
        self.gestionnaire = GestionnaireDemoPersonnalise()  # Notre gestionnaire personnalisé
        
        # Configuration des délais (plus courts pour la démo)
        self.gestionnaire.configurer_delais_repetition(
            delai_initial=0.3,      # 300ms avant répétition
            delai_repetition=0.15   # 150ms entre répétitions
        )
        
        print("🎮 Démonstration avec gestionnaire d'événements initialisée")
        print("📋 Mapping des touches:", self.gestionnaire.obtenir_touches_mappees())
    
    def executer(self):
        """Boucle principale de la démonstration."""
        horloge = pygame.time.Clock()
        actif = True
        
        print("\n=== DEMO 6x6 AVEC GESTIONNAIRE D'ÉVÉNEMENTS ===")
        print("Contrôles via gestionnaire:")
        print("  ← → : Déplacer (avec répétition)")
        print("  ↑ : Rotation")
        print("  ↓ : Descendre (avec répétition)")
        print("  ESPACE : Chute rapide (jusqu'en bas)")
        print("  ENTRÉE : Placer pièce manuellement")
        print("  P : Pause/Reprendre")
        print("  ESC : Menu/Quitter")
        print()
        print(self.gestionnaire.statistiques())
        print()
        
        while actif:
            temps_actuel = time.time()
            
            # Traiter les événements pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    actif = False
                
                elif event.type == pygame.KEYDOWN:
                    nom_touche = convertir_touche_pygame(event.key)
                    if nom_touche:
                        resultat = self.gestionnaire.traiter_evenement_clavier(
                            nom_touche, 
                            TypeEvenement.CLAVIER_APPUI, 
                            self.moteur, 
                            temps_actuel
                        )
                        
                        # Gestion spéciale pour ESC et P
                        if nom_touche == "Escape":
                            if self.moteur.afficher_menu:
                                actif = False  # Quitter si menu ouvert
                            else:
                                self.moteur.basculer_menu()
                        elif nom_touche == "p":
                            self.moteur.basculer_pause()
                
                # Touches spéciales pour la démo
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Entrée pour placer la pièce
                        self.moteur.placer_piece_definitivement()
                        self.moteur.generer_nouvelle_piece()
                        print("⏎ Pièce placée manuellement avec Entrée")
                
                elif event.type == pygame.KEYUP:
                    nom_touche = convertir_touche_pygame(event.key)
                    if nom_touche:
                        self.gestionnaire.traiter_evenement_clavier(
                            nom_touche,
                            TypeEvenement.CLAVIER_RELACHE,
                            self.moteur,
                            temps_actuel
                        )
            
            # Mettre à jour la répétition des touches si pas en pause
            if not self.moteur.en_pause:
                self.gestionnaire.mettre_a_jour_repetition(self.moteur, temps_actuel)
            
            # Dessiner
            self.affichage.dessiner(self.moteur)
            horloge.tick(60)
        
        pygame.quit()
        print("\n" + self.gestionnaire.statistiques())
        print("Démonstration terminée.")


if __name__ == "__main__":
    demo = DemoAvecGestionnaire()
    demo.executer()
