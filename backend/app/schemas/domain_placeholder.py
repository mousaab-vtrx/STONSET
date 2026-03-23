"""
PLACEHOLDER SCHEMAS FROM DIAGRAMS

This file contains placeholder schemas based on your UML diagrams.
Create individual schema files for each entity.

ENTITIES TO IMPLEMENT (from Figure 7: Diagramme de classes):
============================================================

1. DepartmentCreate / DepartmentResponse
   - nomDepartement: str
   - chefDepartement: FK to User

2. NiveauCreate / NiveauResponse
   - nomNiveau: str
   - archNiveau: str
   - notSemestre: str

3. FiliereCreate / FiliereResponse
   - nomFiliere: str

4. EtatCreate / EtatResponse
   - nomEtat: str

5. ModuleCreate / ModuleResponse
   - codeModule: str
   - nomModule: str
   - semestreModule: str
   - enseignantId: FK to User
   - niveauId: FK to Niveau

6. SectionCreate / SectionResponse
   - nomination: int
   - moduleId: FK to Module

7. ReservationCreate / ReservationResponse
   - dateSeance: date
   - dateDemandeId: datetime
   - dateReponseId: datetime (optional)
   - etat: str
   - accessInternet: bool
   - equipementReseau: bool
   - videoprojecteur: bool
   - typeReservation: str
   - enseignantId: FK to User
   - salleId: FK to SalleTP
   - creneauId: FK to Creneau

8. SalleTPCreate / SalleTPResponse
   - capacite: int
   - accessInternet: bool
   - equipementReseau: bool
   - videoprojecteur: bool
   - departementId: FK to Department

9. SystemeCreate / SystemeResponse
   - nomSysteme: str

10. LogicielCreate / LogicielResponse
    - nomLogiciel: str
    - systemeId: FK to Systeme

11. CreneauCreate / CreneauResponse
    - duree: int
    - heureDebut: int
    - numJour: int
    - numSemaine: int
    - salleId: FK to SalleTP

12. VacancesCreate / VacancesResponse
    - nomVacance: str
    - dateDebut: date
    - dateFin: date
    - numJour: int

13. GroupeTPCreate / GroupeTPResponse
    - numGroupe: int
    - moduleId: FK to Module
    - sectionId: FK to Section

NEXT STEPS:
===========
1. Create app/schemas/<entity_name>.py
2. Define <EntityName>Base, <EntityName>Create, <EntityName>Update, <EntityName>Response
3. Use TodoPlaceholder pattern shown below

TODO SCHEMA TEMPLATE:
====================
```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EntityNameBase(BaseModel):
    \"\"\"Base schema - shared fields.\"\"\"
    # TODO: Add fields from diagrams

class EntityNameCreate(EntityNameBase):
    \"\"\"Create schema - for POST requests.\"\"\"
    pass

class EntityNameUpdate(BaseModel):
    \"\"\"Update schema - for PUT/PATCH requests.\"\"\"
    # TODO: Add optional fields from diagrams
    pass

class EntityNameResponse(EntityNameBase):
    \"\"\"Response schema - for GET requests.\"\"\"
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```
"""

# TODO: Implement all domain schemas here
