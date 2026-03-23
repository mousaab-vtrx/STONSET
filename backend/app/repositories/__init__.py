"""
Repositories package.
All data access layer repositories.
"""

from app.repositories.user_repo import UserRepository
from app.repositories.department_repo import DepartmentRepository
from app.repositories.niveau_repo import NiveauRepository
from app.repositories.filiere_repo import FiliereRepository
from app.repositories.module_repo import ModuleRepository
from app.repositories.section_repo import SectionRepository
from app.repositories.groupe_tp_repo import GroupeTPRepository
from app.repositories.etat_repo import EtatRepository
from app.repositories.creneau_repo import CreneauRepository
from app.repositories.vacances_repo import VacancesRepository
from app.repositories.systeme_repo import SystemeRepository
from app.repositories.logiciel_repo import LogicielRepository
from app.repositories.salle_tp_repo import SalleTPRepository
from app.repositories.reservation_repo import ReservationRepository

__all__ = [
    "UserRepository",
    "DepartmentRepository",
    "NiveauRepository",
    "FiliereRepository",
    "ModuleRepository",
    "SectionRepository",
    "GroupeTPRepository",
    "EtatRepository",
    "CreneauRepository",
    "VacancesRepository",
    "SystemeRepository",
    "LogicielRepository",
    "SalleTPRepository",
    "ReservationRepository",
]
