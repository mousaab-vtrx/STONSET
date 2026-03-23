"""
API v1 package.
All API routers for version 1.
"""

from app.api.v1 import (
    auth,
    users,
    departments,
    niveaux,
    filieres,
    modules,
    sections,
    groupes_tp,
    etats,
    creneaux,
    vacances,
    systemes,
    logiciels,
    salles_tp,
    reservations,
)

__all__ = [
    "auth",
    "users",
    "departments",
    "niveaux",
    "filieres",
    "modules",
    "sections",
    "groupes_tp",
    "etats",
    "creneaux",
    "vacances",
    "systemes",
    "logiciels",
    "salles_tp",
    "reservations",
]
