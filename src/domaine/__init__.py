"""
DOMAINE - Cœur de l'application (Business Logic)

RÈGLE FONDAMENTALE : Ce package ne doit JAMAIS importer quelque chose 
des couches externes (ports, adapters).

Seuls imports autorisés :
- Modules Python standard (typing, dataclasses, abc, etc.)
- Autres modules du domaine

Ce package contient :
- entites/ : Objets métier (Piece, Plateau, Position)
- services/ : Logique métier complexe
- exceptions/ : Exceptions spécifiques au domaine
"""
