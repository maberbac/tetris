"""
SERVICES - Couche des services du domaine Tetris

Les services encapsulent la logique métier complexe qui ne rentre pas
naturellement dans les entités.

Services disponibles :
- Commandes : Command Pattern pour les actions de jeu
- GestionnaireEvenements : Gestion des inputs et contrôles
- AdaptateurPygame : Bridge vers la bibliothèque Pygame

RÈGLES :
- Services sans état (stateless) ou avec état géré explicitement
- Injection de dépendances via constructeur
- Interface claire et découplée
- Testabilité maximale
"""

from .commandes import (
    Commande, MoteurJeu,
    CommandeDeplacerGauche, CommandeDeplacerDroite, CommandeDescendre,
    CommandeChuteRapide, CommandeTourner, CommandePause
)

from .gestionnaire_evenements import (
    GestionnaireEvenements, TypeEvenement, ToucheClavier,
    ConfigurationControles
)

# Import conditionnel de l'adaptateur Pygame
try:
    from .adaptateur_pygame import AdaptateurPygame
    PYGAME_SUPPORT = True
except ImportError:
    PYGAME_SUPPORT = False
    AdaptateurPygame = None

__all__ = [
    'Commande', 'MoteurJeu',
    'CommandeDeplacerGauche', 'CommandeDeplacerDroite', 'CommandeDescendre',
    'CommandeChuteRapide', 'CommandeTourner', 'CommandePause', 'CommandeAfficherMenu',
    'GestionnaireEvenements', 'TypeEvenement', 'ToucheClavier',
    'ConfigurationControles', 'PYGAME_SUPPORT'
]

if PYGAME_SUPPORT:
    __all__.append('AdaptateurPygame')
