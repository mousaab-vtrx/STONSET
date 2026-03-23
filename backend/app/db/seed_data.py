"""
Seed database with test data.
Run from project root: cd backend && python -m app.db.seed_data
"""
import asyncio
from datetime import time, date
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.security import get_password_hash
from app.models import (
    User,
    Department,
    Niveau,
    Filiere,
    Module,
    Section,
    GroupeTP,
    Etat,
    Creneau,
    Vacances,
    Systeme,
    Logiciel,
    SalleTP,
)


async def seed_data():
    """Add test data to database."""
    engine = create_async_engine(
        settings.DATABASE_URL.replace("mysql+pymysql", "mysql+aiomysql"),
        echo=False,
        future=True,
    )

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        # 1. Users (for testing - password: test1234)
        hashed = get_password_hash("test1234")
        users = [
            # Department heads
            User(
                email="chef@test.com",
                nom_user="Martin",
                prenom_user="Marie",
                hashed_password=hashed,
                user_type="chef_dept",
            ),
            # Service responsible
            User(
                email="responsable@test.com",
                nom_user="Bernard",
                prenom_user="Pierre",
                hashed_password=hashed,
                user_type="responsable_service",
            ),
            # Teachers - Software Engineering
            User(
                email="prof.alami@test.com",
                nom_user="Alami",
                prenom_user="Ahmed",
                hashed_password=hashed,
                user_type="enseignant",
            ),
            User(
                email="prof.laroui@test.com",
                nom_user="Laroui",
                prenom_user="Fatima",
                hashed_password=hashed,
                user_type="enseignant",
            ),
            User(
                email="prof.oussama@test.com",
                nom_user="Oussama",
                prenom_user="Hassan",
                hashed_password=hashed,
                user_type="enseignant",
            ),
            # Teachers - Networks
            User(
                email="prof.chen@test.com",
                nom_user="Chen",
                prenom_user="Li",
                hashed_password=hashed,
                user_type="enseignant",
            ),
            User(
                email="prof.dupuis@test.com",
                nom_user="Dupuis",
                prenom_user="Luc",
                hashed_password=hashed,
                user_type="enseignant",
            ),
            # Teachers - Security
            User(
                email="prof.richard@test.com",
                nom_user="Richard",
                prenom_user="Sophie",
                hashed_password=hashed,
                user_type="enseignant",
            ),
            User(
                email="prof.blanc@test.com",
                nom_user="Blanc",
                prenom_user="Marc",
                hashed_password=hashed,
                user_type="enseignant",
            ),
            # Additional teachers
            User(
                email="prof.dupont@test.com",
                nom_user="Dupont",
                prenom_user="Jean",
                hashed_password=hashed,
                user_type="enseignant",
            ),
            User(
                email="prof.robin@test.com",
                nom_user="Robin",
                prenom_user="Anne",
                hashed_password=hashed,
                user_type="enseignant",
            ),
        ]
        for u in users:
            session.add(u)
        await session.flush()
        print(f"✓ Created {len(users)} users")

        # 2. Department
        dept = Department(
            nom_department="Informatique",
            description="Computer Science Department",
            chef_department_id=users[1].id,
        )
        session.add(dept)
        await session.flush()
        print("✓ Created 1 department")

        # 3. Niveau
        niveaux = [
            Niveau(nom_niveau="1ère année", department_id=dept.id),
            Niveau(nom_niveau="2ème année", department_id=dept.id),
            Niveau(nom_niveau="3ème année", department_id=dept.id),
        ]
        for n in niveaux:
            session.add(n)
        await session.flush()
        print(f"✓ Created {len(niveaux)} niveaux")

        # 4. Filiere
        filieres = [
            Filiere(nom_filiere="Génie Logiciel", niveau_id=niveaux[0].id),
            Filiere(nom_filiere="Développement Web", niveau_id=niveaux[0].id),
            Filiere(nom_filiere="Réseaux", niveau_id=niveaux[1].id),
            Filiere(nom_filiere="Administration Systèmes", niveau_id=niveaux[1].id),
            Filiere(nom_filiere="Sécurité Informatique", niveau_id=niveaux[2].id),
            Filiere(nom_filiere="Cloud Computing", niveau_id=niveaux[2].id),
        ]
        for f in filieres:
            session.add(f)
        await session.flush()
        print(f"✓ Created {len(filieres)} filières")

        # 5. Modules
        modules = [
            # Software Engineering Modules (1st year)
            Module(
                code_module="CS101",
                nom_module="Introduction to Programming",
                filiere_id=filieres[0].id,
                description="Basics of programming in Python and Java",
            ),
            Module(
                code_module="CS102",
                nom_module="Object-Oriented Programming",
                filiere_id=filieres[0].id,
                description="OOP concepts, design patterns, and best practices",
            ),
            Module(
                code_module="CS103",
                nom_module="Data Structures",
                filiere_id=filieres[0].id,
                description="Arrays, linked lists, trees, graphs, and sorting algorithms",
            ),
            # Web Development Modules (1st year)
            Module(
                code_module="WEB101",
                nom_module="Web Fundamentals",
                filiere_id=filieres[1].id,
                description="HTML, CSS, JavaScript basics",
            ),
            Module(
                code_module="WEB102",
                nom_module="Frontend Frameworks",
                filiere_id=filieres[1].id,
                description="React, Vue.js, Angular fundamentals",
            ),
            Module(
                code_module="WEB103",
                nom_module="Backend Development",
                filiere_id=filieres[1].id,
                description="Node.js, FastAPI, and database integration",
            ),
            # Networks Modules (2nd year)
            Module(
                code_module="NET101",
                nom_module="Network Fundamentals",
                filiere_id=filieres[2].id,
                description="TCP/IP, OSI model, and networking protocols",
            ),
            Module(
                code_module="NET102",
                nom_module="Routing and Switching",
                filiere_id=filieres[2].id,
                description="Router configuration, switching, and VLANs",
            ),
            Module(
                code_module="NET103",
                nom_module="Network Security",
                filiere_id=filieres[2].id,
                description="Firewalls, VPN, and packet filtering",
            ),
            # System Administration (2nd year)
            Module(
                code_module="SYS101",
                nom_module="Linux Administration",
                filiere_id=filieres[3].id,
                description="Linux OS, shell scripting, and system management",
            ),
            Module(
                code_module="SYS102",
                nom_module="Windows Server Administration",
                filiere_id=filieres[3].id,
                description="Active Directory, Group Policy, and server roles",
            ),
            Module(
                code_module="SYS103",
                nom_module="Virtual Infrastructure",
                filiere_id=filieres[3].id,
                description="Virtualization with KVM, VMware, and Hyper-V",
            ),
            # Security Modules (3rd year)
            Module(
                code_module="SEC101",
                nom_module="Cybersecurity Basics",
                filiere_id=filieres[4].id,
                description="Introduction to security concepts and threats",
            ),
            Module(
                code_module="SEC102",
                nom_module="Cryptography",
                filiere_id=filieres[4].id,
                description="Encryption, hashing, digital signatures, and PKI",
            ),
            Module(
                code_module="SEC103",
                nom_module="Penetration Testing",
                filiere_id=filieres[4].id,
                description="Vulnerability scanning, exploitation, and reporting",
            ),
            # Cloud Computing (3rd year)
            Module(
                code_module="CLOUD101",
                nom_module="Cloud Architecture",
                filiere_id=filieres[5].id,
                description="AWS, Azure, GCP fundamentals and IaaS/PaaS/SaaS",
            ),
            Module(
                code_module="CLOUD102",
                nom_module="Containerization & Orchestration",
                filiere_id=filieres[5].id,
                description="Docker, Kubernetes, and container management",
            ),
            Module(
                code_module="CLOUD103",
                nom_module="Cloud DevOps",
                filiere_id=filieres[5].id,
                description="CI/CD pipelines, automation, and infrastructure as code",
            ),
        ]
        for m in modules:
            session.add(m)
        await session.flush()
        print(f"✓ Created {len(modules)} modules")

        # 6. Sections
        sections = [
            # Introduction to Programming
            Section(nom_section="Section A", numero_section=1, module_id=modules[0].id, capacity=30),
            Section(nom_section="Section B", numero_section=2, module_id=modules[0].id, capacity=28),
            Section(nom_section="Section C", numero_section=3, module_id=modules[0].id, capacity=32),
            # OOP
            Section(nom_section="Section A", numero_section=1, module_id=modules[1].id, capacity=30),
            Section(nom_section="Section B", numero_section=2, module_id=modules[1].id, capacity=28),
            # Data Structures
            Section(nom_section="Section A", numero_section=1, module_id=modules[2].id, capacity=25),
            # Web Fundamentals
            Section(nom_section="Section A", numero_section=1, module_id=modules[3].id, capacity=30),
            Section(nom_section="Section B", numero_section=2, module_id=modules[3].id, capacity=29),
            # Frontend Frameworks
            Section(nom_section="Section A", numero_section=1, module_id=modules[4].id, capacity=25),
            # Backend Development
            Section(nom_section="Section A", numero_section=1, module_id=modules[5].id, capacity=24),
            # Network Fundamentals
            Section(nom_section="Section A", numero_section=1, module_id=modules[6].id, capacity=28),
            Section(nom_section="Section B", numero_section=2, module_id=modules[6].id, capacity=26),
            # Routing and Switching
            Section(nom_section="Section A", numero_section=1, module_id=modules[7].id, capacity=20),
            # Network Security
            Section(nom_section="Section A", numero_section=1, module_id=modules[8].id, capacity=22),
            # Linux Administration
            Section(nom_section="Section A", numero_section=1, module_id=modules[9].id, capacity=24),
            # Windows Server Administration
            Section(nom_section="Section A", numero_section=1, module_id=modules[10].id, capacity=20),
            # Virtual Infrastructure
            Section(nom_section="Section A", numero_section=1, module_id=modules[11].id, capacity=18),
            # Cybersecurity Basics
            Section(nom_section="Section A", numero_section=1, module_id=modules[12].id, capacity=26),
            # Cryptography
            Section(nom_section="Section A", numero_section=1, module_id=modules[13].id, capacity=22),
            # Penetration Testing
            Section(nom_section="Section A", numero_section=1, module_id=modules[14].id, capacity=20),
            # Cloud Architecture
            Section(nom_section="Section A", numero_section=1, module_id=modules[15].id, capacity=28),
            # Containerization & Orchestration
            Section(nom_section="Section A", numero_section=1, module_id=modules[16].id, capacity=25),
            # Cloud DevOps
            Section(nom_section="Section A", numero_section=1, module_id=modules[17].id, capacity=22),
        ]
        for s in sections:
            session.add(s)
        await session.flush()
        print(f"✓ Created {len(sections)} sections")

        # 7. Groupes TP (with session types)
        groupes = [
            # Introduction to Programming - Section A
            GroupeTP(num_groupe=1, nom_groupe="TP-CS101-A1", type="TP", module_id=modules[0].id, section_id=sections[0].id, capacity=15),
            GroupeTP(num_groupe=2, nom_groupe="TP-CS101-A2", type="TP", module_id=modules[0].id, section_id=sections[0].id, capacity=15),
            # Introduction to Programming - Section B
            GroupeTP(num_groupe=3, nom_groupe="TP-CS101-B1", type="TP", module_id=modules[0].id, section_id=sections[1].id, capacity=14),
            GroupeTP(num_groupe=4, nom_groupe="TP-CS101-B2", type="TP", module_id=modules[0].id, section_id=sections[1].id, capacity=14),
            # Introduction to Programming - Section C
            GroupeTP(num_groupe=5, nom_groupe="TP-CS101-C1", type="TP", module_id=modules[0].id, section_id=sections[2].id, capacity=16),
            GroupeTP(num_groupe=6, nom_groupe="TP-CS101-C2", type="TP", module_id=modules[0].id, section_id=sections[2].id, capacity=16),
            # OOP - Section A
            GroupeTP(num_groupe=1, nom_groupe="TP-CS102-A1", type="TP", module_id=modules[1].id, section_id=sections[3].id, capacity=15),
            GroupeTP(num_groupe=2, nom_groupe="TP-CS102-A2", type="TP", module_id=modules[1].id, section_id=sections[3].id, capacity=15),
            # OOP - Section B
            GroupeTP(num_groupe=3, nom_groupe="TP-CS102-B1", type="TP", module_id=modules[1].id, section_id=sections[4].id, capacity=14),
            GroupeTP(num_groupe=4, nom_groupe="TP-CS102-B2", type="TP", module_id=modules[1].id, section_id=sections[4].id, capacity=14),
            # Data Structures
            GroupeTP(num_groupe=1, nom_groupe="TP-CS103-A1", type="TP", module_id=modules[2].id, section_id=sections[5].id, capacity=13),
            GroupeTP(num_groupe=2, nom_groupe="TP-CS103-A2", type="TP", module_id=modules[2].id, section_id=sections[5].id, capacity=12),
            # Web Fundamentals - Section A
            GroupeTP(num_groupe=1, nom_groupe="TP-WEB101-A1", type="TP", module_id=modules[3].id, section_id=sections[6].id, capacity=15),
            GroupeTP(num_groupe=2, nom_groupe="TP-WEB101-A2", type="TP", module_id=modules[3].id, section_id=sections[6].id, capacity=15),
            # Web Fundamentals - Section B
            GroupeTP(num_groupe=3, nom_groupe="TP-WEB101-B1", type="TP", module_id=modules[3].id, section_id=sections[7].id, capacity=15),
            GroupeTP(num_groupe=4, nom_groupe="TP-WEB101-B2", type="TP", module_id=modules[3].id, section_id=sections[7].id, capacity=14),
            # Frontend Frameworks
            GroupeTP(num_groupe=1, nom_groupe="TP-WEB102-A1", type="TP", module_id=modules[4].id, section_id=sections[8].id, capacity=13),
            GroupeTP(num_groupe=2, nom_groupe="TP-WEB102-A2", type="TP", module_id=modules[4].id, section_id=sections[8].id, capacity=12),
            # Backend Development
            GroupeTP(num_groupe=1, nom_groupe="TP-WEB103-A1", type="TP", module_id=modules[5].id, section_id=sections[9].id, capacity=12),
            GroupeTP(num_groupe=2, nom_groupe="TP-WEB103-A2", type="TP", module_id=modules[5].id, section_id=sections[9].id, capacity=12),
            # Network Fundamentals - Section A
            GroupeTP(num_groupe=1, nom_groupe="TP-NET101-A1", type="TP", module_id=modules[6].id, section_id=sections[10].id, capacity=14),
            GroupeTP(num_groupe=2, nom_groupe="TP-NET101-A2", type="TP", module_id=modules[6].id, section_id=sections[10].id, capacity=14),
            # Network Fundamentals - Section B
            GroupeTP(num_groupe=3, nom_groupe="TP-NET101-B1", type="TP", module_id=modules[6].id, section_id=sections[11].id, capacity=13),
            GroupeTP(num_groupe=4, nom_groupe="TP-NET101-B2", type="TP", module_id=modules[6].id, section_id=sections[11].id, capacity=13),
            # Routing and Switching
            GroupeTP(num_groupe=1, nom_groupe="TP-NET102-A1", type="TP", module_id=modules[7].id, section_id=sections[12].id, capacity=10),
            GroupeTP(num_groupe=2, nom_groupe="TP-NET102-A2", type="TP", module_id=modules[7].id, section_id=sections[12].id, capacity=10),
            # Network Security
            GroupeTP(num_groupe=1, nom_groupe="TP-NET103-A1", type="TP", module_id=modules[8].id, section_id=sections[13].id, capacity=11),
            GroupeTP(num_groupe=2, nom_groupe="TP-NET103-A2", type="TP", module_id=modules[8].id, section_id=sections[13].id, capacity=11),
            # Linux Administration
            GroupeTP(num_groupe=1, nom_groupe="TP-SYS101-A1", type="TP", module_id=modules[9].id, section_id=sections[14].id, capacity=12),
            GroupeTP(num_groupe=2, nom_groupe="TP-SYS101-A2", type="TP", module_id=modules[9].id, section_id=sections[14].id, capacity=12),
            # Windows Server Administration
            GroupeTP(num_groupe=1, nom_groupe="TP-SYS102-A1", type="TP", module_id=modules[10].id, section_id=sections[15].id, capacity=10),
            GroupeTP(num_groupe=2, nom_groupe="TP-SYS102-A2", type="TP", module_id=modules[10].id, section_id=sections[15].id, capacity=10),
            # Virtual Infrastructure
            GroupeTP(num_groupe=1, nom_groupe="TP-SYS103-A1", type="TP", module_id=modules[11].id, section_id=sections[16].id, capacity=9),
            GroupeTP(num_groupe=2, nom_groupe="TP-SYS103-A2", type="TP", module_id=modules[11].id, section_id=sections[16].id, capacity=9),
            # Cybersecurity Basics
            GroupeTP(num_groupe=1, nom_groupe="TP-SEC101-A1", type="TP", module_id=modules[12].id, section_id=sections[17].id, capacity=13),
            GroupeTP(num_groupe=2, nom_groupe="TP-SEC101-A2", type="TP", module_id=modules[12].id, section_id=sections[17].id, capacity=13),
            # Cryptography
            GroupeTP(num_groupe=1, nom_groupe="TP-SEC102-A1", type="TP", module_id=modules[13].id, section_id=sections[18].id, capacity=11),
            GroupeTP(num_groupe=2, nom_groupe="TP-SEC102-A2", type="TP", module_id=modules[13].id, section_id=sections[18].id, capacity=11),
            # Penetration Testing
            GroupeTP(num_groupe=1, nom_groupe="TP-SEC103-A1", type="TP", module_id=modules[14].id, section_id=sections[19].id, capacity=10),
            GroupeTP(num_groupe=2, nom_groupe="TP-SEC103-A2", type="TP", module_id=modules[14].id, section_id=sections[19].id, capacity=10),
            # Cloud Architecture
            GroupeTP(num_groupe=1, nom_groupe="TP-CLOUD101-A1", type="TP", module_id=modules[15].id, section_id=sections[20].id, capacity=14),
            GroupeTP(num_groupe=2, nom_groupe="TP-CLOUD101-A2", type="TP", module_id=modules[15].id, section_id=sections[20].id, capacity=14),
            # Containerization & Orchestration
            GroupeTP(num_groupe=1, nom_groupe="TP-CLOUD102-A1", type="TP", module_id=modules[16].id, section_id=sections[21].id, capacity=13),
            GroupeTP(num_groupe=2, nom_groupe="TP-CLOUD102-A2", type="TP", module_id=modules[16].id, section_id=sections[21].id, capacity=12),
            # Cloud DevOps
            GroupeTP(num_groupe=1, nom_groupe="TP-CLOUD103-A1", type="TP", module_id=modules[17].id, section_id=sections[22].id, capacity=11),
            GroupeTP(num_groupe=2, nom_groupe="TP-CLOUD103-A2", type="TP", module_id=modules[17].id, section_id=sections[22].id, capacity=11),
        ]
        for g in groupes:
            session.add(g)
        await session.flush()
        print(f"✓ Created {len(groupes)} groupes TP")

        # 8. Etats
        etats = [
            Etat(nom_etat="En attente", description="Pending approval"),
            Etat(nom_etat="Approuvée", description="Approved"),
            Etat(nom_etat="Rejetée", description="Rejected"),
        ]
        for e in etats:
            session.add(e)
        await session.flush()
        print(f"✓ Created {len(etats)} états")

        # 9. Creneaux (expanded with more time slots)
        creneaux = [
            Creneau(heure_debut=time(8, 0), duree=90, num_jour=1, num_semaine=1, jour_nom="Monday"),
            Creneau(heure_debut=time(10, 0), duree=90, num_jour=1, num_semaine=1, jour_nom="Monday"),
            Creneau(heure_debut=time(13, 30), duree=90, num_jour=1, num_semaine=1, jour_nom="Monday"),
            Creneau(heure_debut=time(15, 30), duree=90, num_jour=1, num_semaine=1, jour_nom="Monday"),
            Creneau(heure_debut=time(8, 0), duree=90, num_jour=2, num_semaine=1, jour_nom="Tuesday"),
            Creneau(heure_debut=time(10, 0), duree=90, num_jour=2, num_semaine=1, jour_nom="Tuesday"),
            Creneau(heure_debut=time(13, 30), duree=90, num_jour=2, num_semaine=1, jour_nom="Tuesday"),
            Creneau(heure_debut=time(8, 0), duree=90, num_jour=3, num_semaine=1, jour_nom="Wednesday"),
            Creneau(heure_debut=time(10, 0), duree=90, num_jour=3, num_semaine=1, jour_nom="Wednesday"),
            Creneau(heure_debut=time(13, 30), duree=90, num_jour=3, num_semaine=1, jour_nom="Wednesday"),
            Creneau(heure_debut=time(15, 30), duree=90, num_jour=3, num_semaine=1, jour_nom="Wednesday"),
            Creneau(heure_debut=time(8, 0), duree=90, num_jour=4, num_semaine=1, jour_nom="Thursday"),
            Creneau(heure_debut=time(10, 0), duree=90, num_jour=4, num_semaine=1, jour_nom="Thursday"),
            Creneau(heure_debut=time(13, 30), duree=90, num_jour=4, num_semaine=1, jour_nom="Thursday"),
            Creneau(heure_debut=time(8, 0), duree=90, num_jour=5, num_semaine=1, jour_nom="Friday"),
            Creneau(heure_debut=time(10, 0), duree=90, num_jour=5, num_semaine=1, jour_nom="Friday"),
        ]
        for c in creneaux:
            session.add(c)
        await session.flush()
        print(f"✓ Created {len(creneaux)} créneaux")

        # 10. Vacances
        vacances = [
            Vacances(nom_vacances="Été 2025", date_debut=date(2025, 7, 1), date_fin=date(2025, 8, 31)),
            Vacances(nom_vacances="Noël 2024-2025", date_debut=date(2024, 12, 20), date_fin=date(2025, 1, 5)),
        ]
        for v in vacances:
            session.add(v)
        await session.flush()
        print(f"✓ Created {len(vacances)} vacances")

        # 11. Systemes
        systemes = [
            Systeme(nom_systeme="Windows 10", version="10.0"),
            Systeme(nom_systeme="Linux Ubuntu", version="22.04 LTS"),
            Systeme(nom_systeme="macOS", version="13"),
        ]
        for s in systemes:
            session.add(s)
        await session.flush()
        print(f"✓ Created {len(systemes)} systems")

        # 12. Salles TP (expanded with more rooms)
        salles = [
            # Building A - Ground Floor
            SalleTP(
                nom_salle="Lab-101 (A-GF)",
                code="L101",
                capacite=30,
                access_internet=True,
                equipement_reseau=True,
                videoprojecteur=True,
                description="Main Lab - Windows (Building A, Ground Floor)",
                systeme_id=systemes[0].id,
            ),
            SalleTP(
                nom_salle="Lab-102 (A-GF)",
                code="L102",
                capacite=25,
                access_internet=True,
                equipement_reseau=True,
                videoprojecteur=False,
                description="Linux Lab (Building A, Ground Floor)",
                systeme_id=systemes[1].id,
            ),
            SalleTP(
                nom_salle="Lab-103 (A-GF)",
                code="L103",
                capacite=20,
                access_internet=True,
                equipement_reseau=False,
                videoprojecteur=True,
                description="Development Lab - Mobile (Building A, Ground Floor)",
                systeme_id=systemes[0].id,
            ),
            # Building A - First Floor
            SalleTP(
                nom_salle="Lab-201 (A-F1)",
                code="L201",
                capacite=28,
                access_internet=True,
                equipement_reseau=True,
                videoprojecteur=True,
                description="Network Lab (Building A, First Floor)",
                systeme_id=systemes[1].id,
            ),
            SalleTP(
                nom_salle="Lab-202 (A-F1)",
                code="L202",
                capacite=24,
                access_internet=True,
                equipement_reseau=True,
                videoprojecteur=True,
                description="Web Development Lab (Building A, First Floor)",
                systeme_id=systemes[0].id,
            ),
            SalleTP(
                nom_salle="Lab-203 (A-F1)",
                code="L203",
                capacite=22,
                access_internet=True,
                equipement_reseau=False,
                videoprojecteur=True,
                description="Database Lab (Building A, First Floor)",
                systeme_id=systemes[0].id,
            ),
            # Building B - Ground Floor
            SalleTP(
                nom_salle="Lab-104 (B-GF)",
                code="L104",
                capacite=32,
                access_internet=True,
                equipement_reseau=True,
                videoprojecteur=True,
                description="Large Lab - Advanced Systems (Building B, Ground Floor)",
                systeme_id=systemes[1].id,
            ),
            SalleTP(
                nom_salle="Lab-105 (B-GF)",
                code="L105",
                capacite=15,
                access_internet=False,
                equipement_reseau=False,
                videoprojecteur=False,
                description="Isolated Lab - Secure Testing (Building B, Ground Floor)",
                systeme_id=systemes[1].id,
            ),
            # Building B - First Floor
            SalleTP(
                nom_salle="Lab-301 (B-F1)",
                code="L301",
                capacite=26,
                access_internet=True,
                equipement_reseau=True,
                videoprojecteur=True,
                description="Security Lab - Penetration Testing (Building B, First Floor)",
                systeme_id=systemes[1].id,
            ),
            SalleTP(
                nom_salle="Lab-302 (B-F1)",
                code="L302",
                capacite=28,
                access_internet=True,
                equipement_reseau=True,
                videoprojecteur=True,
                description="Cloud Lab - Docker & Kubernetes (Building B, First Floor)",
                systeme_id=systemes[1].id,
            ),
            # Building C
            SalleTP(
                nom_salle="Lab-401 (C-F1)",
                code="L401",
                capacite=20,
                access_internet=True,
                equipement_reseau=True,
                videoprojecteur=True,
                description="System Admin Lab (Building C, First Floor)",
                systeme_id=systemes[0].id,
            ),
            SalleTP(
                nom_salle="Lab-402 (C-F1)",
                code="L402",
                capacite=18,
                access_internet=True,
                equipement_reseau=False,
                videoprojecteur=False,
                description="Cryptography Lab (Building C, First Floor)",
                systeme_id=systemes[1].id,
            ),
        ]
        for s in salles:
            session.add(s)
        await session.flush()
        print(f"✓ Created {len(salles)} lab rooms")

        # 13. Logiciels (software)
        logiciels = [
            # Development Tools
            Logiciel(nom_logiciel="VSCode", version="1.85", systeme_id=systemes[0].id),
            Logiciel(nom_logiciel="PyCharm", version="2023.3", systeme_id=systemes[1].id),
            Logiciel(nom_logiciel="IntelliJ IDEA", version="2023.3", systeme_id=systemes[0].id),
            Logiciel(nom_logiciel="Visual Studio", version="2022", systeme_id=systemes[0].id),
            
            # Programming Languages & Runtime
            Logiciel(nom_logiciel="Python", version="3.11", systeme_id=systemes[1].id),
            Logiciel(nom_logiciel="Java JDK", version="21", systeme_id=systemes[0].id),
            Logiciel(nom_logiciel="Node.js", version="20", systeme_id=systemes[0].id),
            Logiciel(nom_logiciel="Go", version="1.21", systeme_id=systemes[1].id),
            
            # Version Control & CI/CD
            Logiciel(nom_logiciel="Git", version="2.42", systeme_id=systemes[1].id),
            Logiciel(nom_logiciel="GitHub Desktop", version="3.3", systeme_id=systemes[0].id),
            Logiciel(nom_logiciel="GitLab Runner", version="16.4", systeme_id=systemes[1].id),
            Logiciel(nom_logiciel="Jenkins", version="2.414", systeme_id=systemes[1].id),
            
            # Containerization & Virtualization
            Logiciel(nom_logiciel="Docker", version="24.0", systeme_id=systemes[1].id),
            Logiciel(nom_logiciel="Docker Desktop", version="4.25", systeme_id=systemes[0].id),
            Logiciel(nom_logiciel="Kubernetes", version="1.28", systeme_id=systemes[1].id),
            Logiciel(nom_logiciel="VirtualBox", version="7.0", systeme_id=systemes[0].id),
            Logiciel(nom_logiciel="VMware Workstation", version="17", systeme_id=systemes[0].id),
            
            # Database & Data Tools
            Logiciel(nom_logiciel="MySQL", version="8.0", systeme_id=systemes[0].id),
            Logiciel(nom_logiciel="PostgreSQL", version="15", systeme_id=systemes[1].id),
            Logiciel(nom_logiciel="MongoDB", version="6.0", systeme_id=systemes[1].id),
            Logiciel(nom_logiciel="DBeaver", version="23.2", systeme_id=systemes[0].id),
            
            # Web Services & APIs
            Logiciel(nom_logiciel="Nginx", version="1.24", systeme_id=systemes[1].id),
            Logiciel(nom_logiciel="Apache", version="2.4", systeme_id=systemes[1].id),
            Logiciel(nom_logiciel="Postman", version="11.0", systeme_id=systemes[0].id),
            Logiciel(nom_logiciel="FastAPI", version="0.104", systeme_id=systemes[1].id),
            
            # Security & Network Tools
            Logiciel(nom_logiciel="Wireshark", version="4.0", systeme_id=systemes[0].id),
            Logiciel(nom_logiciel="Burp Suite", version="2023.11", systeme_id=systemes[1].id),
            Logiciel(nom_logiciel="OpenVPN", version="2.6", systeme_id=systemes[1].id),
            Logiciel(nom_logiciel="Nmap", version="7.94", systeme_id=systemes[1].id),
            
            # Automation & Testing
            Logiciel(nom_logiciel="Ansible", version="2.10", systeme_id=systemes[1].id),
            Logiciel(nom_logiciel="Terraform", version="1.6", systeme_id=systemes[1].id),
            Logiciel(nom_logiciel="Selenium", version="4.14", systeme_id=systemes[0].id),
            Logiciel(nom_logiciel="JUnit", version="5", systeme_id=systemes[0].id),
        ]
        for l in logiciels:
            session.add(l)
        await session.flush()
        print(f"✓ Created {len(logiciels)} logiciels")

        await session.commit()
        print("\n✓ All test data seeded successfully!")
        print("\n" + "="*60)
        print("TEST ACCOUNTS (password: test1234)")
        print("="*60)
        print("\nDepartment Head:")
        print("  - chef@test.com")
        print("\nService Responsible:")
        print("  - responsable@test.com")
        print("\nTeachers (Enseignants):")
        print("  - prof.alami@test.com (Ahmed Alami)")
        print("  - prof.laroui@test.com (Fatima Laroui)")
        print("  - prof.oussama@test.com (Hassan Oussama)")
        print("  - prof.chen@test.com (Li Chen)")
        print("  - prof.dupuis@test.com (Luc Dupuis)")
        print("  - prof.richard@test.com (Sophie Richard)")
        print("  - prof.blanc@test.com (Marc Blanc)")
        print("  - prof.dupont@test.com (Jean Dupont)")
        print("  - prof.robin@test.com (Anne Robin)")
        print("\n" + "="*60)
        print("DATA SUMMARY")
        print("="*60)
        print(f"  ✓ {len(users)} users")
        print(f"  ✓ {len(niveaux)} education levels (1st, 2nd, 3rd year)")
        print(f"  ✓ {len(filieres)} programs/filières")
        print(f"  ✓ {len(modules)} modules/courses")
        print(f"  ✓ {len(sections)} sections")
        print(f"  ✓ {len(groupes)} groupe TP (practical work groups)")
        print(f"  ✓ {len(salles)} laboratory rooms")
        print(f"  ✓ {len(creneaux)} time slots")
        print(f"  ✓ {len(logiciels)} software packages")
        print("="*60)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_data())
