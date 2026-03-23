"""
PLACEHOLDER MODELS FROM DIAGRAMS

This file contains placeholder models based on your UML diagrams.
Replace each TODO model with actual implementation from Figure 7.

ENTITIES TO IMPLEMENT (from Figure 7: Diagramme de classes):
============================================================

1. Department (Département)
   - idDepartement: int (primary key)
   - nomDepartement: varchar
   - chefDepartement: FK to User

2. Niveau (Level/Year)
   - idNiveau: int (primary key)
   - nomNiveau: varchar
   - archNiveau: varchar
   - notSemestre: varchar

3. Filière (Program/Major)
   - idFiliere: int (primary key)
   - nomFiliere: varchar

4. État (Status)
   - idEtat: int (primary key)
   - nomEtat: varchar

5. Module (Course/Subject)
   - idModule: int (primary key)
   - codeModule: varchar
   - nomModule: varchar
   - semestreModule: varchar

6. Section (Group/Class)
   - idSection: int (primary key)
   - nomination: int

7. Réservation (Reservation)
   - idReservation: int (primary key)
   - dateSeance: date
   - dateDemandeId: dateTime
   - dateReponseId: dateTime
   - etat: varchar
   - accessInternet: boolean
   - equipementReseau: boolean
   - videoprojecteur: boolean
   - typeReservation: varchar

8. SalleTP (TP Room/Lab Room)
   - idSalle: int (primary key)
   - capacite: int
   - accessInternet: boolean
   - equipementReseau: boolean
   - videoprojecteur: boolean

9. Système (System/OS)
   - idSysteme: int (primary key)
   - nomSysteme: varchar

10. Logiciel (Software/Application)
    - idLogiciel: int (primary key)
    - nomLogiciel: varchar

11. Créneau (Time Slot)
    - duree: int
    - heureDebut: int
    - numJour: int
    - numSemaine: int

12. Vacances (Vacation/Break)
    - idVacance: int (primary key)
    - nomVacance: int
    - dateDebut: date
    - dateFin: date
    - numJour: int

13. GroupeTP (TP Group)
    - numGroupe: int

RELATIONSHIPS (from Figure 7):
=============================
- User (Enseignant) 1..* ----> 0..* Réservation
- Réservation 0..* <---- 1..* SalleTP
- Département 1..* ---> 0..* Niveau
- Niveau 1..* ---> 1..* Filière
- Filière 1..* ---> 1..* Module
- Module 1..* ---> 1..* Section
- Module 1..* ---> 1..* GroupeTP
- Section 1..* ---> 1..* GroupeTP
- SalleTP 1..* ---> 0..* Créneau
- Réservation 0..* ---> 1..* Créneau
- SalleTP 1..* ---> 1..* Système
- Système 1..* <---- 0..* Logiciel
- Réservation 0..* ---> 0..* Vacances

USE CASES TO IMPLEMENT (from Figures 1, 2, 3):
==============================================

ENSEIGNANT (Figure 1):
- Authentication
- Demande de réservation (Request Reservation)
- Consulter son planning des réservations (View Reservation Schedule)
- Visualiser ses informations personnelles (View Personal Info)
- Mise à jour des informations (Update Info)

CHEF DE DÉPARTEMENT (Figure 2):
- Gestion des enseignants (Manage Teachers)
  - Ajout d'un enseignant (Add Teacher)
  - Suppression d'un enseignant (Remove Teacher)
- Demande de réservation (Request Reservation)

RESPONSABLE DU SERVICE (Figure 3):
- Authentication
- Gestion des demandes de réservation (Manage Reservation Requests)
  - Listage des demandes traitées (List Processed Requests)
  - Traitement des demandes en cours (Process Pending Requests)
  - Affectation de la salle après validation (Assign Room After Validation)
- Gestion des salles (Room Management)
  - Ajout d'une salle (Add Room)
  - Modification d'une salle (Modify Room)
  - Visualisation des salles existantes (View Existing Rooms)
  - Suppression d'une salle (Delete Room)
- Consultation du planning des réservations (Consult Reservation Schedule)
- Visualiser ses informations personnelles (View Personal Info)
- Mise à jour des informations (Update Info)

NEXT STEPS:
===========
1. Copy one TODO model template below
2. Create app/models/<entity_name>.py
3. Implement the model with all fields from Figure 7
4. Add relationships using SQLModel Relationship
5. Update app/models/__init__.py to import new models
6. Create corresponding schema in app/schemas/<entity_name>.py
7. Create repository in app/repositories/<entity_name>_repo.py
8. Create service in app/services/<entity_name>_service.py
9. Create API router in app/api/v1/<entity_name>.py

TODO MODEL TEMPLATE:
====================
```python
# TODO: Implement from diagrams
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class EntityName(SQLModel, table=True):
    \"\"\"
    Entity description.
    From diagrams: Figure 7
    \"\"\"
    id: Optional[int] = Field(default=None, primary_key=True)
    # TODO: Add all fields from diagrams
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # TODO: Add foreign keys
    # TODO: Add relationships
```
"""

# TODO: Implement all domain models here
# See template above and UML diagram Figure 7
