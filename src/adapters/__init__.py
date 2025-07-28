"""
ADAPTERS - Implémentations concrètes

Les adapters implémentent les interfaces définies dans les ports.
Ils contiennent tous les détails techniques.

adapters/entree/ : Drivers - Qui UTILISE l'application (UI, API, Tests)
adapters/sortie/ : Driven - UTILISÉ par l'application (DB, Affichage, etc.)

RÈGLES :
- Implémentent les interfaces des ports
- Contiennent les détails techniques (pygame, fichiers, etc.)
- Interchangeables sans affecter le domaine
"""
