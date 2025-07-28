"""
PORTS - Interfaces et contrats

Les ports définissent les contrats entre le domaine et l'extérieur.
Le domaine définit CE DONT il a besoin, pas COMMENT c'est implémenté.

ports/entree/ : Use Cases - Ce que l'application FAIT
ports/sortie/ : Services externes - Ce dont l'application a BESOIN

RÈGLES :
- Que des interfaces abstraites (ABC)
- Définies par le domaine, pour le domaine
- Implémentées dans les adapters
"""
