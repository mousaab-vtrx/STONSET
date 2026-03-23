"""
Pydantic Schemas package.
All request/response validation schemas.
"""

from app.schemas.user import UserBase, UserCreate, UserUpdate, UserResponse, TokenResponse
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.schemas.niveau import NiveauCreate, NiveauUpdate, NiveauResponse
from app.schemas.filiere import FiliereCreate, FiliereUpdate, FiliereResponse
from app.schemas.module import ModuleCreate, ModuleUpdate, ModuleResponse
from app.schemas.section import SectionCreate, SectionUpdate, SectionResponse
from app.schemas.groupe_tp import GroupeTPCreate, GroupeTPUpdate, GroupeTPResponse
from app.schemas.etat import EtatCreate, EtatUpdate, EtatResponse
from app.schemas.creneau import CreneauCreate, CreneauUpdate, CreneauResponse
from app.schemas.vacances import VacancesCreate, VacancesUpdate, VacancesResponse
from app.schemas.systeme import SystemeCreate, SystemeUpdate, SystemeResponse
from app.schemas.logiciel import LogicielCreate, LogicielUpdate, LogicielResponse
from app.schemas.salle_tp import SalleTPCreate, SalleTPUpdate, SalleTPResponse
from app.schemas.reservation import ReservationCreate, ReservationUpdate, ReservationResponse

__all__ = [
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "TokenResponse",
    # Domain entities
    "DepartmentCreate",
    "DepartmentUpdate",
    "DepartmentResponse",
    "NiveauCreate",
    "NiveauUpdate",
    "NiveauResponse",
    "FiliereCreate",
    "FiliereUpdate",
    "FiliereResponse",
    "ModuleCreate",
    "ModuleUpdate",
    "ModuleResponse",
    "SectionCreate",
    "SectionUpdate",
    "SectionResponse",
    "GroupeTPCreate",
    "GroupeTPUpdate",
    "GroupeTPResponse",
    "EtatCreate",
    "EtatUpdate",
    "EtatResponse",
    "CreneauCreate",
    "CreneauUpdate",
    "CreneauResponse",
    "VacancesCreate",
    "VacancesUpdate",
    "VacancesResponse",
    "SystemeCreate",
    "SystemeUpdate",
    "SystemeResponse",
    "LogicielCreate",
    "LogicielUpdate",
    "LogicielResponse",
    "SalleTPCreate",
    "SalleTPUpdate",
    "SalleTPResponse",
    "ReservationCreate",
    "ReservationUpdate",
    "ReservationResponse",
]
