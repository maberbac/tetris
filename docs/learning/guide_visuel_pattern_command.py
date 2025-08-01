"""
🎨 GUIDE VISUEL DU PATTERN COMMAND - Diagrammes et Exemples

Ce guide complément le tutoriel principal avec des diagrammes visuels
et des exemples de code progressifs pour mieux comprendre le Pattern Command.
"""

def afficher_diagramme_avant_apres():
    """Comparaison visuelle avant/après Pattern Command."""
    print("📊 AVANT vs APRÈS - PATTERN COMMAND")
    print("=" * 50)
    
    print("❌ AVANT (Code couplé):")
    print("""
    ┌─────────────────────┐
    │    Interface UI     │
    │                     │
    │ if touche == "LEFT": │
    │   moteur.gauche()   │
    │ elif touche == "UP": │
    │   moteur.rotation() │
    │ elif ...            │
    │                     │
    │ ┌─────────────────┐ │
    │ │   MoteurJeu     │ │
    │ │  (directement   │ │
    │ │   couplé)       │ │
    │ └─────────────────┘ │
    └─────────────────────┘
    
    PROBLÈMES:
    • Code rigide
    • Difficile à tester
    • Impossible d'étendre
    • Couplage fort
    """)
    
    input("Appuyez sur Entrée pour voir la solution...")
    
    print("\n✅ APRÈS (Pattern Command):")
    print("""
    ┌─────────────────────┐    ┌─────────────────────┐
    │   Interface UI      │    │    Gestionnaire     │
    │                     │───▶│   d'Événements      │
    │ traiter_touche()    │    │                     │
    └─────────────────────┘    │ Map<Touche,Command> │
                               └──────────┬──────────┘
                                         │
                            ┌────────────▼────────────┐
                            │     <<interface>>       │
                            │       Command           │
                            │                         │ 
                            │    + execute(): bool    │
                            └────────────┬────────────┘
                                        ▲
                         ┌──────────────┼──────────────┐
                         │              │              │
            ┌────────────▼───┐ ┌────────▼───┐ ┌───────▼────┐
            │CommandeGauche  │ │CommandeDroite│ │CommandeRotation│
            │                │ │              │ │                │
            │+ execute()     │ │+ execute()   │ │+ execute()     │
            └────────┬───────┘ └──────┬───────┘ └────────┬───────┘
                     │                │                  │
                     └────────────────┼──────────────────┘
                                      │
                            ┌─────────▼─────────┐
                            │    MoteurJeu      │
                            │                   │
                            │ + deplacer_gauche │
                            │ + deplacer_droite │
                            │ + faire_tourner   │
                            └───────────────────┘
    
    AVANTAGES:
    • ✅ Extensible facilement
    • ✅ Tests unitaires simples
    • ✅ Découplage complet
    • ✅ Fonctionnalités avancées possibles
    """)


def afficher_flux_execution():
    """Diagramme de séquence du Pattern Command."""
    print("\n🔄 FLUX D'EXÉCUTION - DIAGRAMME DE SÉQUENCE")
    print("=" * 55)
    
    print("""
    Client       Gestionnaire    Command         MoteurJeu
    (UI)         (Invoker)      (ConcreteCmd)   (Receiver)
     │               │               │               │
     │──touche────▶│               │               │
     │               │               │               │
     │               │──getCommand──▶│               │
     │               │               │               │ 
     │               │◀──command─────│               │
     │               │               │               │
     │               │──execute()───▶│               │
     │               │               │               │
     │               │               │──action()───▶│
     │               │               │               │
     │               │               │◀──result─────│
     │               │               │               │
     │               │◀──success────│               │
     │               │               │               │
     │◀──résultat───│               │               │
     │               │               │               │
    
    ÉTAPES:
    1. 🖱️ L'utilisateur appuie sur une touche
    2. 📞 Le gestionnaire trouve la commande associée
    3. ⚡ La commande s'exécute
    4. 🎮 La commande appelle le moteur de jeu
    5. ✅ Le résultat remonte jusqu'au client
    """)


def exemple_evolution_code():
    """Montre l'évolution du code étape par étape."""
    print("\n📈 ÉVOLUTION DU CODE - ÉTAPE PAR ÉTAPE")
    print("=" * 50)
    
    print("🎯 ÉTAPE 1: Code naïf (à éviter)")
    print("""
def gerer_input(touche, moteur):
    if touche == "LEFT":
        moteur.x -= 1
    elif touche == "RIGHT":
        moteur.x += 1
    # Pas extensible, pas testable
    """)
    
    input("Évolution: Appuyez sur Entrée...")
    
    print("\n🎯 ÉTAPE 2: Extraction en méthodes")
    print("""
class GestionnaireInput:
    def gerer_gauche(self, moteur):
        moteur.x -= 1
    
    def gerer_droite(self, moteur):
        moteur.x += 1
    
    def gerer_input(self, touche, moteur):
        if touche == "LEFT":
            self.gerer_gauche(moteur)
        elif touche == "RIGHT":
            self.gerer_droite(moteur)
    # Mieux, mais encore couplé
    """)
    
    input("Évolution: Appuyez sur Entrée...")
    
    print("\n🎯 ÉTAPE 3: Introduction des objets Command")
    print("""
class Command:
    def execute(self): pass

class CommandeGauche(Command):
    def __init__(self, moteur):
        self.moteur = moteur
    
    def execute(self):
        self.moteur.x -= 1

class Gestionnaire:
    def __init__(self):
        self.commandes = {}
    
    def associer(self, touche, commande):
        self.commandes[touche] = commande
    
    def executer(self, touche):
        if touche in self.commandes:
            self.commandes[touche].execute()
    # Découplé et extensible !
    """)
    
    input("Finalisation: Appuyez sur Entrée...")
    
    print("\n🎯 ÉTAPE 4: Version finale avec gestion d'erreurs")
    print("""
class CommandeAvecValidation(Command):
    def execute(self) -> bool:
        try:
            # Sauvegarder l'état
            etat_precedent = self.moteur.sauvegarder()
            
            # Tenter l'action
            resultat = self.executer_action()
            
            # Valider
            if self.est_valide():
                return True
            else:
                # Annuler en cas d'échec
                self.moteur.restaurer(etat_precedent)
                return False
        except Exception:
            return False
    
    @abstractmethod
    def executer_action(self): pass
    
    @abstractmethod  
    def est_valide(self) -> bool: pass
    # Robuste avec rollback automatique !
    """)


def patterns_associes():
    """Montre les patterns qui se combinent bien avec Command."""
    print("\n🔗 PATTERNS COMPLÉMENTAIRES AU COMMAND")
    print("=" * 45)
    
    print("1️⃣ COMMAND + STRATEGY")
    print("""
    Différentes façons d'exécuter la même commande:
    
    class CommandeDeplacer:
        def __init__(self, moteur, strategie):
            self.moteur = moteur
            self.strategie = strategie  # Strategy pattern
        
        def execute(self):
            return self.strategie.deplacer(self.moteur)
    
    # Différentes stratégies:
    # - DeplacementNormal()
    # - DeplacementAvecAnimation()
    # - DeplacementInstantane()
    """)
    
    print("\n2️⃣ COMMAND + COMPOSITE")
    print("""
    Macro-commandes (combinaison de commandes):
    
    class MacroCommande(Command):
        def __init__(self):
            self.commandes = []
        
        def ajouter(self, commande):
            self.commandes.append(commande)
        
        def execute(self):
            for cmd in self.commandes:
                if not cmd.execute():
                    return False
            return True
    
    # Exemple: "Super Move" = Gauche + Rotation + Chute
    super_move = MacroCommande()
    super_move.ajouter(CommandeGauche(moteur))
    super_move.ajouter(CommandeRotation(moteur))
    super_move.ajouter(CommandeChute(moteur))
    """)
    
    print("\n3️⃣ COMMAND + MEMENTO (pour UNDO)")
    print("""
    Commandes réversibles avec sauvegarde d'état:
    
    class CommandeAvecUndo(Command):
        def __init__(self, moteur):
            self.moteur = moteur
            self.memento = None  # Memento pattern
        
        def execute(self):
            # Sauvegarder l'état
            self.memento = self.moteur.creer_memento()
            # Exécuter
            return self.executer_action()
        
        def undo(self):
            if self.memento:
                self.moteur.restaurer_memento(self.memento)
    """)


def antipatterns_command():
    """Montre les erreurs courantes avec le Pattern Command."""
    print("\n⚠️ ANTI-PATTERNS À ÉVITER")
    print("=" * 35)
    
    print("❌ ANTI-PATTERN 1: Commande trop grosse")
    print("""
class CommandeGiantesque(Command):
    def execute(self):
        # 500 lignes de code ici
        # Fait tout: validation, action, logging, etc.
        pass
    
    PROBLÈME: Viole le principe de responsabilité unique
    SOLUTION: Décomposer en plus petites commandes
    """)
    
    print("\n❌ ANTI-PATTERN 2: Logique dans l'invoker")
    print("""
class MauvaisGestionnaire:
    def executer(self, touche):
        commande = self.commandes[touche]
        
        # ❌ Logique métier dans l'invoker !
        if self.jeu_en_pause:
            return False
        if not self.piece_active:
            self.generer_piece()
        
        return commande.execute()
    
    PROBLÈME: L'invoker connaît trop la logique métier
    SOLUTION: Déplacer la logique dans les commandes
    """)
    
    print("\n❌ ANTI-PATTERN 3: Commandes avec effets de bord")
    print("""
class CommandeAvecEffetsDeBord(Command):
    def execute(self):
        # Action principale
        self.moteur.deplacer_gauche()
        
        # ❌ Effets de bord cachés
        self.moteur.mettre_a_jour_score()
        self.moteur.verifier_lignes_completes()
        self.moteur.generer_particules()
        
    PROBLÈME: La commande fait trop de choses
    SOLUTION: Une commande = une action atomique
    """)
    
    print("\n✅ BONNES PRATIQUES:")
    print("  • Une commande = une responsabilité")
    print("  • Commandes idempotentes si possible")
    print("  • Gestion d'erreurs systématique")
    print("  • Noms explicites (CommandeDeplacerGauche vs Cmd1)")
    print("  • Tests unitaires pour chaque commande")


def quiz_interactif():
    """Quiz interactif pour tester la compréhension."""
    print("\n🧠 QUIZ - TESTEZ VOS CONNAISSANCES")
    print("=" * 40)
    
    questions = [
        {
            "question": "Quel est le principal avantage du Pattern Command ?",
            "options": [
                "A) Améliorer les performances",
                "B) Découpler l'invocation de l'exécution", 
                "C) Réduire la mémoire utilisée",
                "D) Simplifier le code"
            ],
            "reponse": "B",
            "explication": "Le Pattern Command découple celui qui demande une action de celui qui l'exécute."
        },
        {
            "question": "Dans le Pattern Command, qui est le 'Receiver' ?",
            "options": [
                "A) L'objet Command",
                "B) L'interface utilisateur", 
                "C) L'objet qui exécute réellement l'action",
                "D) Le gestionnaire d'événements"
            ],
            "reponse": "C",
            "explication": "Le Receiver (MoteurJeu dans Tetris) est l'objet qui effectue réellement l'action."
        },
        {
            "question": "Pour implémenter UNDO, que doit faire une commande ?",
            "options": [
                "A) Rien de spécial",
                "B) Sauvegarder l'état avant modification", 
                "C) Demander à l'utilisateur",
                "D) Relancer l'application"
            ],
            "reponse": "B",
            "explication": "Pour permettre l'annulation, il faut sauvegarder l'état avant la modification."
        }
    ]
    
    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\n❓ QUESTION {i}:")
        print(q["question"])
        for option in q["options"]:
            print(f"   {option}")
        
        reponse = input("\nVotre réponse (A/B/C/D): ").strip().upper()
        
        if reponse == q["reponse"]:
            print("✅ Correct !")
            score += 1
        else:
            print(f"❌ Incorrect. La bonne réponse était {q['reponse']}")
        
        print(f"💡 Explication: {q['explication']}")
        input("Appuyez sur Entrée pour continuer...")
    
    print(f"\n🏆 RÉSULTAT: {score}/{len(questions)}")
    if score == len(questions):
        print("🎉 Parfait ! Vous maîtrisez le Pattern Command !")
    elif score >= len(questions) // 2:
        print("👍 Bien ! Continuez à pratiquer !")
    else:
        print("📚 Révisez le tutoriel et réessayez !")


def menu_guide_visuel():
    """Menu du guide visuel."""
    while True:
        print("\n" + "=" * 60)
        print("🎨 GUIDE VISUEL - PATTERN COMMAND")
        print("=" * 60)
        print("1. 📊 Avant/Après - Comparaison visuelle")
        print("2. 🔄 Flux d'exécution - Diagramme de séquence")
        print("3. 📈 Évolution du code étape par étape")
        print("4. 🔗 Patterns complémentaires")
        print("5. ⚠️ Anti-patterns à éviter")
        print("6. 🧠 Quiz interactif")
        print("7. 🔙 Retour au tutoriel principal")
        
        choix = input("\nChoisissez une section (1-7): ").strip()
        
        if choix == "1":
            afficher_diagramme_avant_apres()
        elif choix == "2":
            afficher_flux_execution()
        elif choix == "3":
            exemple_evolution_code()
        elif choix == "4":
            patterns_associes()
        elif choix == "5":
            antipatterns_command()
        elif choix == "6":
            quiz_interactif()
        elif choix == "7":
            break
        else:
            print("❌ Choix invalide. Essayez 1-7.")


if __name__ == "__main__":
    menu_guide_visuel()
