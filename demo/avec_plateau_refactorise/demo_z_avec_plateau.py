"""
Démonstration Plateau 6x6 avec Pièce Z - Version avec Plateau Refactorisé

Cette version utilise le VRAI plateau refactorisé avec dimensions ajustables,
intégré avec le gestionnaire d'événements complet.

AVANTAGES de cette version :
✅ Utilise le vrai Plateau(6, 6) au lieu de PlateauDemoZ
✅ Bénéficie de la détection des lignes complètes
✅ Code plus propre sans duplication
✅ Intégration complète avec l'architecture

Contrôles :
- ← → : Déplacer gauche/droite
- ↑ : Rotation  
- ↓ : Descendre
- Espace : Chute instantanée
- Entrée : Placer pièce manuellement
- ESC : Menu (quitter)
- P : Pause
"""

import pygame
import sys
import os
import time

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.domaine.entites.fabriques.fabrique_pieces import FabriquePieces
from src.domaine.entites.piece import TypePiece, Piece
from src.domaine.entites.position import Position
from src.domaine.entites.plateau import Plateau  # ← LE VRAI PLATEAU !
from src.domaine.services.gestionnaire_evenements import GestionnaireEvenements, TypeEvenement, ToucheClavier
from src.domaine.services.commandes import MoteurJeu, Commande


class CommandeChuteRapideDemoZ(Commande):
    """Commande de chute rapide pour la démo Z."""
    
    def execute(self, moteur) -> bool:
        """Fait tomber la pièce Z jusqu'en bas."""
        if hasattr(moteur, 'chute_rapide_demo'):
            return moteur.chute_rapide_demo()
        return False


class CommandeDeplacerGaucheDemoZ(Commande):
    """Commande de déplacement gauche pour la démo Z."""
    
    def execute(self, moteur) -> bool:
        """Déplace la pièce Z vers la gauche si possible."""
        piece = moteur.obtenir_piece_active()
        plateau = moteur.obtenir_plateau()
        
        # Sauvegarder l'état actuel
        positions_originales = piece.positions.copy()
        pivot_original = Position(piece.position_pivot.x, piece.position_pivot.y)
        
        # Essayer le déplacement
        piece.deplacer(-1, 0)
        
        # Vérifier si le déplacement est valide
        if plateau.peut_placer_piece(piece):
            print(f"⬅️ Gauche Z → {piece.positions}")
            return True
        else:
            # Annuler le déplacement
            piece.positions = positions_originales
            piece.position_pivot = pivot_original
            return False


class CommandeDeplacerDroiteDemoZ(Commande):
    """Commande de déplacement droite pour la démo Z."""
    
    def execute(self, moteur) -> bool:
        """Déplace la pièce Z vers la droite si possible."""
        piece = moteur.obtenir_piece_active()
        plateau = moteur.obtenir_plateau()
        
        # Sauvegarder l'état actuel
        positions_originales = piece.positions.copy()
        pivot_original = Position(piece.position_pivot.x, piece.position_pivot.y)
        
        # Essayer le déplacement
        piece.deplacer(1, 0)
        
        # Vérifier si le déplacement est valide
        if plateau.peut_placer_piece(piece):
            print(f"➡️ Droite Z → {piece.positions}")
            return True
        else:
            # Annuler le déplacement
            piece.positions = positions_originales
            piece.position_pivot = pivot_original
            return False


class CommandeTournerDemoZ(Commande):
    """Commande de rotation pour la démo Z."""
    
    def execute(self, moteur) -> bool:
        """Fait tourner la pièce Z si possible."""
        piece = moteur.obtenir_piece_active()
        plateau = moteur.obtenir_plateau()
        
        # Sauvegarder l'état actuel
        positions_originales = piece.positions.copy()
        orientation_originale = getattr(piece, '_orientation', None)
        
        # Essayer la rotation
        piece.tourner()
        
        # Vérifier si la rotation est valide
        if plateau.peut_placer_piece(piece):
            print(f"🔄 Rotation Z → {piece.positions}")
            return True
        else:
            # Annuler la rotation
            piece.positions = positions_originales
            if orientation_originale is not None:
                piece._orientation = orientation_originale
            return False


class MoteurDemo6x6ZAvecPlateau:
    """
    Moteur pour la démonstration Z utilisant le VRAI plateau refactorisé.
    
    🎯 DIFFÉRENCE CLEF : Utilise Plateau(6, 6) au lieu d'une classe personnalisée !
    """
    
    def __init__(self):
        # LE CHANGEMENT PRINCIPAL : Utiliser le vrai Plateau refactorisé
        self.plateau = Plateau(6, 6)  # ← Directement avec le constructeur !
        
        # Créer la pièce Z au centre
        fabrique = FabriquePieces()
        self.piece_active = fabrique.creer(TypePiece.Z, x_pivot=2, y_pivot=2)
        
        # État du jeu
        self.en_pause = False
        self.afficher_menu = False
        
        print(f"🎮 Moteur démo Z 6x6 avec VRAI plateau initialisé")
        print(f"📍 Plateau: {self.plateau.largeur}x{self.plateau.hauteur}")
        print(f"📍 Pièce Z créée: {self.piece_active.positions}")
    
    def obtenir_piece_active(self) -> Piece:
        """Retourne la pièce actuellement contrôlée."""
        return self.piece_active
    
    def obtenir_plateau(self) -> Plateau:
        """Retourne le vrai plateau refactorisé."""
        return self.plateau
    
    def faire_descendre_piece(self) -> bool:
        """Fait descendre la pièce Z d'une ligne si possible."""
        # Sauvegarder les positions
        positions_orig = self.piece_active.positions.copy()
        pivot_orig = self.piece_active.position_pivot
        
        # Essayer de descendre
        self.piece_active.deplacer(0, 1)
        
        # Vérifier si c'est valide
        if self.plateau.peut_placer_piece(self.piece_active):
            print(f"⬇️ Descente Z → {self.piece_active.positions}")
            return True
        else:
            # Annuler le mouvement
            self.piece_active.positions = positions_orig
            self.piece_active.position_pivot = pivot_orig
            return False
    
    def placer_piece_definitivement(self) -> None:
        """Place la pièce Z définitivement sur le plateau."""
        # Placer la pièce sur le vrai plateau
        self.plateau.placer_piece(self.piece_active)
        print(f"📍 Pièce Z placée définitivement à: {self.piece_active.positions}")
        
        # 🎯 AVANTAGE DU VRAI PLATEAU : Vérifier les lignes complètes !
        lignes_completes = self.plateau.obtenir_lignes_completes()
        if lignes_completes:
            print(f"🎉 LIGNES COMPLÈTES DÉTECTÉES: {lignes_completes}")
            nb_supprimees = self.plateau.supprimer_lignes(lignes_completes)
            print(f"✨ {nb_supprimees} ligne(s) supprimée(s) !")
    
    def generer_nouvelle_piece(self) -> None:
        """Génère une nouvelle pièce Z."""
        fabrique = FabriquePieces()
        self.piece_active = fabrique.creer(TypePiece.Z, x_pivot=2, y_pivot=1)
        print(f"✨ Nouvelle pièce Z générée: {self.piece_active.positions}")
    
    def chute_rapide_demo(self) -> bool:
        """Chute rapide pour la pièce Z."""
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
            print(f"🚀 Chute rapide Z: {nb_lignes_descendues} lignes → {self.piece_active.positions}")
        
        return nb_lignes_descendues > 0
    
    def basculer_pause(self):
        """Bascule l'état de pause."""
        self.en_pause = not self.en_pause
        print(f"⏸️ Pause: {'ON' if self.en_pause else 'OFF'}")
    
    def basculer_menu(self):
        """Bascule l'affichage du menu."""
        self.afficher_menu = not self.afficher_menu
        print(f"📋 Menu: {'OUVERT' if self.afficher_menu else 'FERMÉ'}")


class AffichageAvecPlateauZ:
    """Affichage pour la démo Z avec le vrai plateau."""
    
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
        pygame.display.set_caption("Demo 6x6 - Pièce Z avec Plateau Refactorisé")
        
        # Couleurs
        self.noir = (0, 0, 0)
        self.gris = (64, 64, 64)
        self.blanc = (255, 255, 255)
        self.rouge = (255, 0, 0)       # Rouge pour pièce Z active
        self.gris_place = (180, 180, 180)  # Gris pour pièces placées
        self.rouge_pause = (255, 100, 100)  # Rouge clair pour pause
        self.vert = (0, 255, 0)        # Pour menu
        
        # Police
        self.police = pygame.font.Font(None, 20)
        self.police_titre = pygame.font.Font(None, 24)
    
    def dessiner(self, moteur: MoteurDemo6x6ZAvecPlateau):
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
        
        # Pièces placées sur le VRAI plateau
        for position in moteur.plateau.positions_occupees:
            x = self.marge + position.x * self.taille_cellule
            y = self.marge + position.y * self.taille_cellule
            rect = pygame.Rect(x, y, self.taille_cellule, self.taille_cellule)
            pygame.draw.rect(self.ecran, self.gris_place, rect)
            pygame.draw.rect(self.ecran, self.blanc, rect, 2)
        
        # Pièce active Z
        for pos in moteur.piece_active.positions:
            x = self.marge + pos.x * self.taille_cellule
            y = self.marge + pos.y * self.taille_cellule
            rect = pygame.Rect(x, y, self.taille_cellule, self.taille_cellule)
            pygame.draw.rect(self.ecran, self.rouge, rect)
            pygame.draw.rect(self.ecran, self.blanc, rect, 2)
        
        # Instructions et état
        y_texte = self.marge + self.hauteur_plateau * self.taille_cellule + 10
        
        # Titre
        titre = "Demo 6x6 - Pièce Z avec Plateau Refactorisé"
        texte_titre = self.police_titre.render(titre, True, self.blanc)
        self.ecran.blit(texte_titre, (self.marge, y_texte))
        y_texte += 30
        
        # Contrôles
        instructions = [
            "← → : Déplacer | ↑ : Rotation | ↓ : Descendre",
            "ESPACE : Chute rapide | ENTRÉE : Placer pièce",
            "P : Pause | ESC : Menu/Quitter | DÉTECTION LIGNES ✅",
        ]
        
        for instruction in instructions:
            texte = self.police.render(instruction, True, self.blanc)
            self.ecran.blit(texte, (self.marge, y_texte))
            y_texte += 22
        
        # État du jeu
        couleur_etat = self.rouge_pause if moteur.en_pause else (self.vert if moteur.afficher_menu else self.blanc)
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


class GestionnaireDemoZAvecPlateau(GestionnaireEvenements):
    """Gestionnaire d'événements pour la démo Z avec vrai plateau."""
    
    def _creer_commandes(self):
        """Crée le mapping avec nos commandes pour la pièce Z."""
        from src.domaine.services.commandes import (
            CommandeDescendre, CommandePause, CommandeAfficherMenu
        )
        
        return {
            ToucheClavier.GAUCHE: CommandeDeplacerGaucheDemoZ(),
            ToucheClavier.DROITE: CommandeDeplacerDroiteDemoZ(),
            ToucheClavier.ROTATION: CommandeTournerDemoZ(),
            ToucheClavier.CHUTE_RAPIDE: CommandeDescendre(),
            ToucheClavier.CHUTE_INSTANTANEE: CommandeChuteRapideDemoZ(),
            ToucheClavier.MENU: CommandeAfficherMenu(),
            ToucheClavier.PAUSE: CommandePause(),
        }


class DemoZAvecPlateauRefactorise:
    """Démonstration Z utilisant le vrai plateau refactorisé."""
    
    def __init__(self):
        self.moteur = MoteurDemo6x6ZAvecPlateau()
        self.affichage = AffichageAvecPlateauZ()
        self.gestionnaire = GestionnaireDemoZAvecPlateau()
        
        # Configuration des délais
        self.gestionnaire.configurer_delais_repetition(
            delai_initial=0.3,
            delai_repetition=0.15
        )
        
        print("🚀 Démonstration Z avec plateau REFACTORISÉ initialisée !")
        print("🎯 Cette version montre les bénéfices concrets de la refactorisation !")
    
    def executer(self):
        """Boucle principale de la démonstration."""
        horloge = pygame.time.Clock()
        actif = True
        
        print("\n=== DEMO Z AVEC PLATEAU REFACTORISÉ ===")
        print("✨ AVANTAGES de cette version:")
        print("  🎯 Utilise Plateau(6, 6) - pas de code dupliqué")
        print("  🎉 Détection automatique des lignes complètes")
        print("  🧹 Code plus propre et maintenable")
        print("  ⚡ Intégration complète avec l'architecture")
        print()
        print("Contrôles:")
        print("  ← → : Déplacer | ↑ : Rotation | ↓ : Descendre")
        print("  ESPACE : Chute rapide | ENTRÉE : Placer")
        print("  P : Pause | ESC : Menu/Quitter")
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
                                actif = False
                            else:
                                self.moteur.basculer_menu()
                        elif nom_touche == "p":
                            self.moteur.basculer_pause()
                
                    # Touche spéciale pour placer manuellement
                    if event.key == pygame.K_RETURN:
                        self.moteur.placer_piece_definitivement()
                        self.moteur.generer_nouvelle_piece()
                        print("⏎ Pièce Z placée manuellement")
                
                elif event.type == pygame.KEYUP:
                    nom_touche = convertir_touche_pygame(event.key)
                    if nom_touche:
                        self.gestionnaire.traiter_evenement_clavier(
                            nom_touche,
                            TypeEvenement.CLAVIER_RELACHE,
                            self.moteur,
                            temps_actuel
                        )
            
            # Mettre à jour la répétition des touches
            if not self.moteur.en_pause:
                self.gestionnaire.mettre_a_jour_repetition(self.moteur, temps_actuel)
            
            # Dessiner
            self.affichage.dessiner(self.moteur)
            horloge.tick(60)
        
        pygame.quit()
        print("\n✨ Démonstration Z avec plateau refactorisé terminée.")
        print("🎯 Vous avez vu les bénéfices de la refactorisation en action !")


if __name__ == "__main__":
    print("🚀 Démarrage de la démonstration Z avec plateau REFACTORISÉ...")
    print("🎯 Cette version montre les bénéfices concrets de la refactorisation !")
    
    demo = DemoZAvecPlateauRefactorise()
    demo.executer()
