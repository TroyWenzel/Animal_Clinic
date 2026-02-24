# 🏥 Animal Clinic — SQLAlchemy Database Project

A backend database management system for a veterinary clinic, built with Python and SQLAlchemy ORM. This project models the relationships between owners, pets, veterinarians, vet technicians, appointments, health charts, and medications using a SQLite database.

---

## 📋 Project Overview

This project demonstrates:
- **Relational database design** with multiple interconnected tables
- **SQLAlchemy ORM** for Python-based database interaction
- **One-to-many and one-to-one relationships** across models
- **Real-world CRUD data modeling** for a veterinary clinic workflow

---

## 🗂️ Database Models

| Model | Description |
|---|---|
| `Owner` | Pet owners with contact information |
| `Pet` | Animals with species, breed, and age — linked to an owner |
| `Veterinarian` | Doctors with specializations (e.g. General Practice, Surgery) |
| `VeterinarianTechnician` | Vet techs who manage appointments |
| `Appointment` | Links a pet to a vet tech, with date, complaint, and status |
| `HealthChart` | Vitals and findings recorded by a vet during an appointment |
| `Medication` | Prescriptions or treatments linked to a health chart |

### Relationships

```
Owner ──< Pet ──< Appointment >── VeterinarianTechnician
                      │
                  HealthChart >── Veterinarian
                      │
                  Medication (one or many per chart)
```

---

## 🛠️ Tech Stack

- **Python 3.13**
- **SQLAlchemy ORM**
- **SQLite** (via `clinic.db`)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/TroyWenzel/Animal_Clinic.git
cd Animal_Clinic
```

### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install sqlalchemy
```

### 4. Run the seed script

This creates the database and populates it with sample data:

```bash
python pet_clinic.py
```

You should see:
```
Database seeded successfully!
Owners: 3
Pets: 6
Appointments: 8
Health Charts: 7
Medications: 11
```

A `clinic.db` file will be created in the project directory.

---

## 🔍 Querying the Database

You can import the models into any Python script to query the data:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pet_clinic import Owner, Pet, Appointment, HealthChart, Medication

engine = create_engine('sqlite:///clinic.db')
Session = sessionmaker(bind=engine)
session = Session()

# Get all owners
owners = session.query(Owner).all()
for owner in owners:
    print(owner.name, owner.phone)

# Get all pets for a specific owner
owner = session.query(Owner).filter_by(name="Sarah Johnson").first()
for pet in owner.pets:
    print(pet.name, pet.species)

# Get all completed appointments
completed = session.query(Appointment).filter_by(status="Completed").all()
for appt in completed:
    print(appt.pet.name, appt.date, appt.presenting_complaints)

# Get a pet's full health history
pet = session.query(Pet).filter_by(name="Max").first()
for appt in pet.appointments:
    if appt.health_chart:
        print(f"Date: {appt.date}")
        print(f"Findings: {appt.health_chart.preliminary_findings}")
        for med in appt.health_chart.medications:
            print(f"  Medication: {med.description}")
```

---

## 🔄 Resetting the Database

If you need to wipe and reseed the database from scratch:

**Windows:**
```bash
del clinic.db
python pet_clinic.py
```

**Mac/Linux:**
```bash
rm clinic.db
python pet_clinic.py
```

---

## 📁 Project Structure

```
Animal_Clinic/
│
├── pet_clinic.py      # Models, table creation, and seed data
├── clinic.db          # SQLite database (auto-generated, not tracked in git)
├── README.md          # This file
└── .venv/             # Virtual environment (not tracked in git)
```

---

## 📝 Sample Data Included

| Category | Count |
|---|---|
| Owners | 3 |
| Pets | 6 (dogs, cats, a bird) |
| Veterinarians | 2 |
| Vet Technicians | 3 |
| Appointments | 8 |
| Health Charts | 7 |
| Medications | 11 |

---

## 👤 Author

**Troy Wenzel** — [github.com/TroyWenzel](https://github.com/TroyWenzel) | [linkedin.com/in/troy-wenzel-0690a760](https://www.linkedin.com/in/troy-wenzel-0690a760/)

*Built as part of the Coding Temple Full-Stack Web Development program — 2025*