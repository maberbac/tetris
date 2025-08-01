"""
🎯 APPRENTISSAGE DU PATTERN COMMAND - Système Tetris

Ce tutoriel interactif vous enseigne le Pattern Command étape par étape
à travers des exemples concrets du système de contrôles Tetris.
"""

import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

print("📚 APPRENTISSAGE DU PATTERN COMMAND")
print("=" * 50)

# ============================================================================
# 🎯 ÉTAPE 1: COMPRENDRE LE PROBLÈME
# ============================================================================

def etape1_probleme():
    """Étape 1: Comprendre le problème que résout le Pattern Command."""
    print("\n🤔 ÉTAPE 1: QUEL PROBLÈME RÉSOUT LE PATTERN COMMAND ?")
    print("=" * 60)
    
    print("❌ APPROCHE NAÏVE (ce qu'il NE faut PAS faire):")
    print("""
def gerer_clavier(touche, moteur_jeu):
    if touche == "LEFT":
        moteur_jeu.deplacer_piece_gauche()
    elif touche == "RIGHT":
        moteur_jeu.deplacer_piece_droite()
    elif touche == "UP":
        moteur_jeu.faire_tourner_piece()
    elif touche == "DOWN":
        moteur_jeu.deplacer_piece_bas()
    # ... plus de conditions
    """)
    
    print("🚨 PROBLÈMES de cette approche:")
    print("  • Code rigide et difficile à étendre")
    print("  • Impossible d'annuler (Undo) une action")
    print("  • Pas de macro-commandes possibles")
    print("  • Couplage fort entre interface et logique")
    print("  • Difficile de tester individuellement")
    
    input("\nAppuyez sur Entrée pour voir la solution...")
    
    print("\n✅ SOLUTION: PATTERN COMMAND")
    print("  • Encapsuler chaque action dans un objet")
    print("  • Séparer l'invocation de l'exécution")
    print("  • Permettre l'extensibilité")
    print("  • Ajouter des fonctionnalités avancées")


# ============================================================================
# 🏗️ ÉTAPE 2: STRUCTURE DU PATTERN
# ============================================================================

def etape2_structure():
    """Étape 2: Structure théorique du Pattern Command."""
    print("\n🏗️ ÉTAPE 2: STRUCTURE DU PATTERN COMMAND")
    print("=" * 50)
    
    print("📋 COMPOSANTS PRINCIPAUX:")
    print("""
1. 🎯 COMMAND (Interface de commande)
   ┌─────────────────────┐
   │   <<interface>>     │
   │     Command         │
   │                     │
   │ + execute(): bool   │
   └─────────────────────┘

2. 🎮 CONCRETE COMMAND (Commande concrète)
   ┌─────────────────────┐
   │ CommandeDeplacer    │
   │    Gauche           │
   │                     │
   │ - receiver: Moteur  │
   │ + execute(): bool   │
   └─────────────────────┘

3. 🎰 RECEIVER (Récepteur)
   ┌─────────────────────┐
   │    MoteurJeu        │
   │                     │
   │ + deplacer_gauche() │
   │ + deplacer_droite() │
   │ + faire_tourner()   │
   └─────────────────────┘

4. 📞 INVOKER (Invocateur)
   ┌─────────────────────┐
   │ GestionnaireEvents  │
   │                     │
   │ - commandes: dict   │
   │ + executer(cmd)     │
   └─────────────────────┘
    """)
    
    print("🔄 FLUX D'EXÉCUTION:")
    print("  Client → Invoker → Command → Receiver")
    print("  (UI)   → (Gest.) → (Cmd)   → (Moteur)")


# ============================================================================
# 💻 ÉTAPE 3: IMPLÉMENTATION PRATIQUE
# ============================================================================

def etape3_implementation():
    """Étape 3: Implémentation concrète avec exemples."""
    print("\n💻 ÉTAPE 3: IMPLÉMENTATION DANS TETRIS")
    print("=" * 45)
    
    # Simuler un moteur simple
    class MoteurJeuSimple:
        def __init__(self):
            self.position_x = 5
            self.position_y = 2
            self.historique = []
        
        def deplacer_gauche(self):
            ancien_x = self.position_x
            self.position_x -= 1
            self.historique.append(f"Déplacement: {ancien_x} → {self.position_x}")
            print(f"  🎮 Moteur: Position X = {self.position_x}")
            return True
        
        def deplacer_droite(self):
            ancien_x = self.position_x
            self.position_x += 1
            self.historique.append(f"Déplacement: {ancien_x} → {self.position_x}")
            print(f"  🎮 Moteur: Position X = {self.position_x}")
            return True
        
        def afficher_etat(self):
            print(f"  📍 Position actuelle: ({self.position_x}, {self.position_y})")
            if self.historique:
                print(f"  📝 Dernière action: {self.historique[-1]}")
    
    print("1️⃣ CRÉATION DU RECEIVER (MoteurJeu)")
    moteur = MoteurJeuSimple()
    moteur.afficher_etat()
    
    input("\nAppuyez sur Entrée pour créer les commandes...")
    
    # Interface Command
    from abc import ABC, abstractmethod
    
    class Command(ABC):
        """Interface de base pour toutes les commandes."""
        
        @abstractmethod
        def execute(self) -> bool:
            """Exécute la commande. Retourne True si succès."""
            pass
    
    print("\n2️⃣ CRÉATION DES CONCRETE COMMANDS")
    
    # Commandes concrètes
    class CommandeDeplacerGauche(Command):
        def __init__(self, moteur: MoteurJeuSimple):
            self.moteur = moteur
        
        def execute(self) -> bool:
            print("  🔧 CommandeDeplacerGauche.execute() appelée")
            return self.moteur.deplacer_gauche()
    
    class CommandeDeplacerDroite(Command):
        def __init__(self, moteur: MoteurJeuSimple):
            self.moteur = moteur
        
        def execute(self) -> bool:
            print("  🔧 CommandeDeplacerDroite.execute() appelée")
            return self.moteur.deplacer_droite()
    
    # Créer les commandes
    cmd_gauche = CommandeDeplacerGauche(moteur)
    cmd_droite = CommandeDeplacerDroite(moteur)
    
    print("  ✅ CommandeDeplacerGauche créée")
    print("  ✅ CommandeDeplacerDroite créée")
    
    input("\nAppuyez sur Entrée pour créer l'invoker...")
    
    print("\n3️⃣ CRÉATION DE L'INVOKER (Gestionnaire)")
    
    class GestionnaireSimple:
        def __init__(self):
            self.commandes = {}
        
        def associer_commande(self, touche: str, commande: Command):
            self.commandes[touche] = commande
            print(f"  🔗 Touche '{touche}' associée à {commande.__class__.__name__}")
        
        def executer_commande(self, touche: str):
            if touche in self.commandes:
                print(f"  📞 Exécution de la commande pour '{touche}'")
                return self.commandes[touche].execute()
            else:
                print(f"  ❌ Aucune commande pour '{touche}'")
                return False
    
    gestionnaire = GestionnaireSimple()
    gestionnaire.associer_commande("LEFT", cmd_gauche)
    gestionnaire.associer_commande("RIGHT", cmd_droite)
    
    input("\nAppuyez sur Entrée pour tester le système...")
    
    print("\n4️⃣ TEST DU SYSTÈME COMPLET")
    print("-" * 30)
    
    # Simuler des appuis de touches
    touches_test = ["LEFT", "LEFT", "RIGHT", "LEFT", "RIGHT", "RIGHT"]
    
    for i, touche in enumerate(touches_test):
        print(f"\n🎯 Test {i+1}: Appui sur '{touche}'")
        moteur.afficher_etat()
        
        succes = gestionnaire.executer_commande(touche)
        print(f"  Résultat: {'✅ Succès' if succes else '❌ Échec'}")
        
        moteur.afficher_etat()
        
        if i < len(touches_test) - 1:
            input("  Appuyez sur Entrée pour continuer...")


# ============================================================================
# 🚀 ÉTAPE 4: AVANTAGES DU PATTERN
# ============================================================================

def etape4_avantages():
    """Étape 4: Démonstration des avantages du Pattern Command."""
    print("\n🚀 ÉTAPE 4: AVANTAGES DU PATTERN COMMAND")
    print("=" * 50)
    
    print("✅ AVANTAGE 1: EXTENSIBILITÉ")
    print("  • Ajouter une nouvelle commande = créer une nouvelle classe")
    print("  • Pas besoin de modifier le code existant")
    
    input("Démonstration: Appuyez sur Entrée pour ajouter une commande de rotation...")
    
    # Ajouter dynamiquement une nouvelle commande
    class MoteurAvecRotation:
        def __init__(self):
            self.position_x = 5
            self.rotation = 0
        
        def faire_tourner(self):
            self.rotation = (self.rotation + 90) % 360
            print(f"  🔄 Rotation: {self.rotation}°")
            return True
        
        def afficher_etat(self):
            print(f"  📍 Position: {self.position_x}, Rotation: {self.rotation}°")
    
    class CommandeRotation:
        def __init__(self, moteur):
            self.moteur = moteur
        
        def execute(self):
            print("  🔧 CommandeRotation.execute() appelée")
            return self.moteur.faire_tourner()
    
    moteur_rot = MoteurAvecRotation()
    cmd_rotation = CommandeRotation(moteur_rot)
    
    print("  ✅ Nouvelle commande 'CommandeRotation' ajoutée !")
    print("  ✅ Système étendu sans modifier le code existant")
    
    input("\nAvantage 2: Appuyez sur Entrée pour voir l'UNDO/REDO...")
    
    print("\n✅ AVANTAGE 2: UNDO/REDO")
    
    class CommandeAvecUndo:
        def __init__(self, moteur):
            self.moteur = moteur
            self.ancienne_position = None
        
        def execute(self):
            self.ancienne_position = self.moteur.position_x
            self.moteur.position_x -= 1
            print(f"  ⬅️ Déplacement: {self.ancienne_position} → {self.moteur.position_x}")
            return True
        
        def undo(self):
            if self.ancienne_position is not None:
                print(f"  ↩️ Annulation: {self.moteur.position_x} → {self.ancienne_position}")
                self.moteur.position_x = self.ancienne_position
                return True
            return False
    
    class GestionnaireAvecUndo:
        def __init__(self):
            self.historique = []
        
        def executer_commande(self, commande):
            if commande.execute():
                self.historique.append(commande)
                return True
            return False
        
        def annuler_derniere(self):
            if self.historique:
                derniere_cmd = self.historique.pop()
                return derniere_cmd.undo()
            return False
    
    moteur_undo = MoteurAvecRotation()
    gestionnaire_undo = GestionnaireAvecUndo()
    
    print("  🎮 Test UNDO/REDO:")
    moteur_undo.afficher_etat()
    
    # Exécuter une commande
    cmd_undo = CommandeAvecUndo(moteur_undo)
    gestionnaire_undo.executer_commande(cmd_undo)
    moteur_undo.afficher_etat()
    
    input("  Appuyez sur Entrée pour annuler...")
    
    # Annuler
    gestionnaire_undo.annuler_derniere()
    moteur_undo.afficher_etat()
    
    print("\n✅ AUTRES AVANTAGES:")
    print("  • 📊 Logging automatique des actions")
    print("  • 🔄 Macro-commandes (séquences)")
    print("  • ⚡ Exécution différée")
    print("  • 🧪 Tests unitaires faciles")
    print("  • 🔌 Découplage interface/logique")


# ============================================================================
# 🎮 ÉTAPE 5: APPLICATION DANS TETRIS
# ============================================================================

def etape5_tetris():
    """Étape 5: Application concrète dans le système Tetris."""
    print("\n🎮 ÉTAPE 5: APPLICATION DANS LE SYSTÈME TETRIS")
    print("=" * 55)
    
    print("📁 STRUCTURE DES FICHIERS:")
    print("""
src/interface/commandes/
├── __init__.py
├── commande_base.py          # Interface Command
├── commande_deplacer_gauche.py
├── commande_deplacer_droite.py
├── commande_faire_tourner.py
├── commande_deplacer_bas.py
├── commande_faire_chuter.py
├── commande_basculer_pause.py
└── commande_afficher_menu.py
    """)
    
    print("🔗 INTÉGRATION AVEC LE GESTIONNAIRE:")
    print("""
gestionnaire_evenements.py:
┌─────────────────────────────────┐
│ class GestionnaireEvenements:   │
│                                 │
│   def __init__(self, moteur):   │
│     self.commandes = {          │
│       ToucheClavier.GAUCHE:     │
│         CommandeDeplacerGauche  │
│       ToucheClavier.DROITE:     │
│         CommandeDeplacerDroite  │
│       # ... autres commandes    │
│     }                           │
│                                 │
│   def traiter_touche(touche):   │
│     cmd = self.commandes[touche]│
│     return cmd.executer()       │
└─────────────────────────────────┘
    """)
    
    print("🎯 EXEMPLE CONCRET - CommandeDeplacerGauche:")
    print("""
class CommandeDeplacerGauche(CommandeBase):
    def __init__(self, moteur: MoteurJeu):
        self.moteur = moteur
    
    def executer(self) -> bool:
        piece = self.moteur.obtenir_piece_active()
        plateau = self.moteur.obtenir_plateau()
        
        if not piece:
            return False
        
        # Sauvegarder l'état actuel
        positions_originales = piece.positions.copy()
        
        # Tenter le déplacement
        piece.deplacer(-1, 0)
        
        # Vérifier si c'est valide
        if plateau.peut_placer_piece(piece):
            return True  # Succès
        else:
            # Restaurer l'état original
            piece._positions = positions_originales
            return False  # Échec
    """)
    
    print("⚡ AVANTAGES DANS TETRIS:")
    print("  • Chaque touche = une commande indépendante")
    print("  • Facile d'ajouter de nouvelles touches")
    print("  • Validation automatique avec rollback")
    print("  • Configuration des touches flexible")
    print("  • Tests unitaires par commande")


# ============================================================================
# 🎓 ÉTAPE 6: EXERCICES PRATIQUES
# ============================================================================

def etape6_exercices():
    """Étape 6: Exercices pour pratiquer le Pattern Command."""
    print("\n🎓 ÉTAPE 6: EXERCICES PRATIQUES")
    print("=" * 40)
    
    print("💪 EXERCICE 1: Créer une CommandeRotationInverse")
    print("  • Fait tourner la pièce dans l'autre sens")
    print("  • Associer à la touche 'Q'")
    
    print("\n💪 EXERCICE 2: Implémenter un système d'historique")
    print("  • Garder les 10 dernières commandes")
    print("  • Permettre l'annulation multiple")
    
    print("\n💪 EXERCICE 3: Créer une macro-commande")
    print("  • 'Tetris Move': Gauche + Rotation + Chute")
    print("  • Exécute 3 commandes d'un coup")
    
    print("\n💪 EXERCICE 4: Ajouter du logging")
    print("  • Chaque commande log son exécution")
    print("  • Mesurer le temps d'exécution")
    
    print("\n💪 EXERCICE 5: Configuration dynamique")
    print("  • Permettre de changer les touches en cours de jeu")
    print("  • Sauvegarder/charger la configuration")


def menu_apprentissage():
    """Menu principal du tutoriel Pattern Command."""
    while True:
        print("\n" + "=" * 60)
        print("📚 TUTORIEL PATTERN COMMAND - SYSTÈME TETRIS")
        print("=" * 60)
        print("1. 🤔 Le problème à résoudre")
        print("2. 🏗️ Structure du pattern")
        print("3. 💻 Implémentation pratique")
        print("4. 🚀 Avantages démontrés")
        print("5. 🎮 Application dans Tetris")
        print("6. 🎓 Exercices pratiques")
        print("7. 📖 Voir le code source des commandes")
        print("8. 🚪 Quitter")
        
        choix = input("\nChoisissez une étape (1-8): ").strip()
        
        try:
            if choix == "1":
                etape1_probleme()
            elif choix == "2":
                etape2_structure()
            elif choix == "3":
                etape3_implementation()
            elif choix == "4":
                etape4_avantages()
            elif choix == "5":
                etape5_tetris()
            elif choix == "6":
                etape6_exercices()
            elif choix == "7":
                voir_code_source()
            elif choix == "8":
                print("🎉 Félicitations ! Vous maîtrisez maintenant le Pattern Command !")
                print("💡 N'oubliez pas: 'Encapsuler une requête en tant qu'objet'")
                break
            else:
                print("❌ Choix invalide. Essayez 1-8.")
        except KeyboardInterrupt:
            print("\n👋 Apprentissage interrompu.")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")
            import traceback
            traceback.print_exc()


def voir_code_source():
    """Affiche le code source des commandes Tetris."""
    print("\n📖 CODE SOURCE DES COMMANDES TETRIS")
    print("=" * 45)
    
    print("🔧 Interface de base:")
    print("""
# commande_base.py
from abc import ABC, abstractmethod
from typing import Protocol

class MoteurJeu(Protocol):
    '''Interface que doit implémenter le moteur de jeu.'''
    def obtenir_piece_active(self): ...
    def obtenir_plateau(self): ...

class CommandeBase(ABC):
    '''Interface de base pour toutes les commandes.'''
    
    def __init__(self, moteur: MoteurJeu):
        self.moteur = moteur
    
    @abstractmethod
    def executer(self) -> bool:
        '''Exécute la commande. Retourne True si succès.'''
        pass
    """)
    
    input("\nAppuyez sur Entrée pour voir une commande concrète...")
    
    print("\n🔧 Commande concrète:")
    print("""
# commande_deplacer_gauche.py
class CommandeDeplacerGauche(CommandeBase):
    '''Commande pour déplacer la pièce active vers la gauche.'''
    
    def executer(self) -> bool:
        piece = self.moteur.obtenir_piece_active()
        plateau = self.moteur.obtenir_plateau()
        
        if not piece:
            return False
        
        # Sauvegarder l'état pour rollback
        positions_originales = piece.positions.copy()
        
        try:
            # Tenter le déplacement
            piece.deplacer(-1, 0)
            
            # Valider avec le plateau
            if plateau.peut_placer_piece(piece):
                return True
            else:
                # Rollback en cas d'échec
                piece._positions = positions_originales
                return False
                
        except Exception:
            # Rollback en cas d'erreur
            piece._positions = positions_originales
            return False
    """)
    
    print("\n🎯 Points clés du code:")
    print("  • 🛡️ Validation avant exécution")
    print("  • 🔄 Rollback automatique en cas d'échec")
    print("  • 🧪 Gestion d'erreurs robuste")
    print("  • 📏 Responsabilité unique (Single Responsibility)")
    print("  • 🔌 Découplage total du moteur de jeu")


if __name__ == "__main__":
    try:
        menu_apprentissage()
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
