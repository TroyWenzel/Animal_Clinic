from sqlalchemy import create_engine, Integer, String, ForeignKey, DateTime, Table, Column, Text, Numeric
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Mapped, mapped_column
from datetime import datetime

engine = create_engine('sqlite:///clinic.db')

Session = sessionmaker(bind=engine)
session = Session() #Create Sessions

Base = declarative_base()
#====================================================
#               Setting up Models
#====================================================
# Owner Model
class Owner(Base):
    __tablename__ = 'owners'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True)
    
    # Relationships
    pets = relationship('Pet', back_populates='owner')


# Pet Model
class Pet(Base):
    __tablename__ = 'pets'
    
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('owners.id'), nullable=False)
    name = Column(String(100), nullable=False)
    species = Column(String(50), nullable=False)  # e.g., "Dog", "Cat", "Bird"
    breed = Column(String(100))
    age = Column(Integer)
    
    # Relationships
    owner = relationship('Owner', back_populates='pets')
    appointments = relationship('Appointment', back_populates='pet')


# Veterinarian Model
class Veterinarian(Base):
    __tablename__ = 'veterinarians'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100))  # e.g., "General", "Surgery", "Dermatology"
    
    # Relationships
    health_charts = relationship('HealthChart', back_populates='veterinarian')


# Veterinarian Technician Model
class VeterinarianTechnician(Base):
    __tablename__ = 'veterinarian_technicians'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(100), unique=True)
    
    # Relationships
    appointments = relationship('Appointment', back_populates='vet_tech')


# Appointment Model (Junction between Pet and Vet Tech)
class Appointment(Base):
    __tablename__ = 'appointments'
    
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey('pets.id'), nullable=False)
    vet_tech_id = Column(Integer, ForeignKey('veterinarian_technicians.id'), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    presenting_complaints = Column(String(200))
    status = Column(String(20), default='Scheduled')  # "Scheduled", "Completed", "Cancelled"
    
    # Relationships
    pet = relationship('Pet', back_populates='appointments')
    vet_tech = relationship('VeterinarianTechnician', back_populates='appointments')
    health_chart = relationship('HealthChart', back_populates='appointment', useList=False)


# Health Chart Model
class HealthChart(Base):
    __tablename__ = 'health_charts'
    
    id = Column(Integer, primary_key=True)
    vet_id = Column(Integer, ForeignKey('veterinarians.id'), nullable=False)
    appointment_id = Column(Integer, ForeignKey('appointments.id'), nullable=False, unique=True)
    pets_weight = Column(Numeric(6, 2))  # e.g., 25.50 kg
    weight_unit = Column(String(5), default='kg')
    pets_vitals_temp = Column(Numeric(4, 1))  # Temperature
    temp_unit = Column(String(5), default="°F")
    pets_vitals_pulse = Column(Integer)            # beats per minute
    pets_vitals_respiration = Column(Integer)      # breaths per minute
    preliminary_findings = Column(String(200))
    
    # Relationships
    veterinarian = relationship('Veterinarian', back_populates='health_charts')
    appointment = relationship('Appointment', back_populates='health_chart')
    medications = relationship('Medication', back_populates='health_chart')


# Medication Model
class Medication(Base):
    __tablename__ = 'medications'
    
    id = Column(Integer, primary_key=True)
    health_chart_id = Column(Integer, ForeignKey('health_charts.id'), nullable=False)
    description = Column(String(200), nullable=False)
    notes = Column(Text)
    
    # Relationships
    health_chart = relationship('HealthChart', back_populates='medications')
    
#================================================================
#                       Importing Data
#================================================================
# adding owners
owner1 = Owner(
    name="Sarah Johnson",
    phone="555-0101",
    email="sarah.johnson@email.com"
)
owner2 = Owner(
    name="Michael Chen",
    phone="555-0202",
    email="michael.chen@email.com"
)
owner3 = Owner(
    name="Emily Rodriguez",
    phone="555-0303",
    email="emily.rodriguez@email.com"
)

session.add_all([owner1, owner2, owner3])
session.flush()

# Create 6 Pets (2 belong to owner1, demonstrating many-to-one)
pet1 = Pet(
    name="Max",
    species="Dog",
    breed="Golden Retriever",
    age=5,
    owner_id=owner1.id
)
pet2 = Pet(
    name="Luna",
    species="Dog",
    breed="German Shepherd",
    age=3,
    owner_id=owner1.id  # Second pet for owner1 (many-to-one relationship)
)
pet3 = Pet(
    name="Whiskers",
    species="Cat",
    breed="Siamese",
    age=4,
    owner_id=owner2.id
)
pet4 = Pet(
    name="Shadow",
    species="Cat",
    breed="Maine Coon",
    age=2,
    owner_id=owner3.id
)
pet5 = Pet(
    name="Tweety",
    species="Bird",
    breed="Canary",
    age=1,
    owner_id=owner3.id
)
pet6 = Pet(
    name="Charlie",
    species="Dog",
    breed="Beagle",
    age=6,
    owner_id=owner2.id
)

session.add_all([pet1, pet2, pet3, pet4, pet5, pet6])
session.flush()

# 3. Create 3 Veterinarian Technicians
vet_tech1 = VeterinarianTechnician(
    name="Jessica Martinez",
    phone="555-1001",
    email="jessica.martinez@vetclinic.com"
)
vet_tech2 = VeterinarianTechnician(
    name="David Thompson",
    phone="555-1002",
    email="david.thompson@vetclinic.com"
)
vet_tech3 = VeterinarianTechnician(
    name="Amanda Lee",
    phone="555-1003",
    email="amanda.lee@vetclinic.com"
)

session.add_all([vet_tech1, vet_tech2, vet_tech3])
session.flush()

# 4. Create 2 Veterinarians with different specializations
vet1 = Veterinarian(
    name="Dr. Robert Williams",
    specialization="General Practice"
)
vet2 = Veterinarian(
    name="Dr. Lisa Anderson",
    specialization="Surgery"
)

session.add_all([vet1, vet2])
session.flush()

# 5. Create 8 Appointments
appointments = [
    Appointment(
        pet_id=pet1.id,
        vet_tech_id=vet_tech1.id,
        date=datetime(2025, 1, 5),
        presenting_complaints="Annual checkup and vaccinations",
        status="Completed"
    ),
    Appointment(
        pet_id=pet2.id,
        vet_tech_id=vet_tech2.id,
        date=datetime(2025, 1, 20),
        presenting_complaints="Limping on right front leg",
        status="Completed"
    ),
    Appointment(
        pet_id=pet3.id,
        vet_tech_id=vet_tech1.id,
        date=datetime(2025, 2, 10),
        presenting_complaints="Not eating, lethargic",
        status="Completed"
    ),
    Appointment(
        pet_id=pet4.id,
        vet_tech_id=vet_tech3.id,
        date=datetime(2025, 2, 25),
        presenting_complaints="Skin irritation and scratching",
        status="Completed"
    ),
    Appointment(
        pet_id=pet5.id,
        vet_tech_id=vet_tech2.id,
        date=datetime(2025, 3, 15),
        presenting_complaints="Routine wellness exam",
        status="Completed"
    ),
    Appointment(
        pet_id=pet6.id,
        vet_tech_id=vet_tech3.id,
        date=datetime(2025, 4, 5),
        presenting_complaints="Coughing and wheezing",
        status="Completed"
    ),
    Appointment(
        pet_id=pet1.id,  # Max's second appointment
        vet_tech_id=vet_tech1.id,
        date=datetime(2025, 4, 25),
        presenting_complaints="Follow-up checkup",
        status="Completed"
    ),
    Appointment(
        pet_id=pet3.id,  # Whiskers' second appointment
        vet_tech_id=vet_tech2.id,
        date=datetime(2025, 11, 25),
        presenting_complaints="Scheduled dental cleaning",
        status="Scheduled"
    )
]

session.add_all(appointments)
session.flush()

health_charts = [
    HealthChart(
        vet_id=vet1.id,
        appointment_id=appointments[0].id,
        pets_weight=32.5,
        weight_unit='kg',
        pets_vitals_temp=101.2,
        temp_unit='°F',
        pets_vitals_pulse=85,
        pets_vitals_respiration=22,
        preliminary_findings="Healthy, good body condition"
    ),
    HealthChart(
        vet_id=vet2.id,  # Surgery specialist for injury
        appointment_id=appointments[1].id,
        pets_weight=28.0,
        weight_unit='kg',
        pets_vitals_temp=101.8,
        temp_unit='°F',
        pets_vitals_pulse=90,
        pets_vitals_respiration=24,
        preliminary_findings="Swelling in right front paw, possible sprain"
    ),
    HealthChart(
        vet_id=vet1.id,
        appointment_id=appointments[2].id,
        pets_weight=4.5,
        weight_unit='kg',
        pets_vitals_temp=103.5,
        temp_unit='°F',
        pets_vitals_pulse=180,
        pets_vitals_respiration=35,
        preliminary_findings="Dehydrated, elevated temperature, possible infection"
    ),
    HealthChart(
        vet_id=vet1.id,
        appointment_id=appointments[3].id,
        pets_weight=5.8,
        weight_unit='kg',
        pets_vitals_temp=102.0,
        temp_unit='°F',
        pets_vitals_pulse=160,
        pets_vitals_respiration=30,
        preliminary_findings="Flea infestation, skin inflammation"
    ),
    HealthChart(
        vet_id=vet1.id,
        appointment_id=appointments[4].id,
        pets_weight=0.12,
        weight_unit='kg',
        pets_vitals_temp=105.0,
        temp_unit='°F',
        pets_vitals_pulse=600,
        pets_vitals_respiration=60,
        preliminary_findings="Healthy bird, normal avian vitals"
    ),
    HealthChart(
        vet_id=vet1.id,
        appointment_id=appointments[5].id,
        pets_weight=11.2,
        weight_unit='kg',
        pets_vitals_temp=102.5,
        temp_unit='°F',
        pets_vitals_pulse=95,
        pets_vitals_respiration=28,
        preliminary_findings="Respiratory congestion, kennel cough suspected"
    ),
    HealthChart(
        vet_id=vet1.id,
        appointment_id=appointments[6].id,
        pets_weight=33.0,
        weight_unit='kg',
        pets_vitals_temp=101.0,
        temp_unit='°F',
        pets_vitals_pulse=82,
        pets_vitals_respiration=20,
        preliminary_findings="Recovering well, no concerns"
    )
]

session.add_all(health_charts)
session.flush()

# 7. Create medications (demonstrating that multiple pets can receive same type of medication)
medications = [
    # Max's first visit - vaccinations
    Medication(
        health_chart_id=health_charts[0].id,
        description="Rabies vaccine",
        notes="Annual vaccination, next due in 1 year"
    ),
    Medication(
        health_chart_id=health_charts[0].id,
        description="DHPP vaccine",
        notes="Distemper, hepatitis, parvovirus, parainfluenza combination"
    ),
    
    # Luna's injury visit
    Medication(
        health_chart_id=health_charts[1].id,
        description="Carprofen 75mg tablets",
        notes="Give 1 tablet twice daily with food for 10 days for pain and inflammation"
    ),
    
    # Whiskers' illness
    Medication(
        health_chart_id=health_charts[2].id,
        description="Amoxicillin 50mg",
        notes="Give 1 capsule twice daily for 14 days. Complete full course even if symptoms improve"
    ),
    Medication(
        health_chart_id=health_charts[2].id,
        description="Subcutaneous fluids",
        notes="Administered 100ml in clinic for rehydration"
    ),
    
    # Shadow's skin condition
    Medication(
        health_chart_id=health_charts[3].id,
        description="Flea treatment - Advantage II",
        notes="Applied topically, repeat monthly"
    ),
    Medication(
        health_chart_id=health_charts[3].id,
        description="Prednisolone 5mg tablets",
        notes="Give half tablet once daily for 7 days to reduce inflammation"
    ),
    
    # Tweety's wellness (no medication needed, but adding vitamin supplement)
    Medication(
        health_chart_id=health_charts[4].id,
        description="Avian vitamin supplement",
        notes="Add to water 2-3 times per week"
    ),
    
    # Charlie's kennel cough
    Medication(
        health_chart_id=health_charts[5].id,
        description="Doxycycline 100mg",
        notes="Give 1 tablet twice daily for 10 days"
    ),
    Medication(
        health_chart_id=health_charts[5].id,
        description="Hydrocodone cough suppressant",
        notes="Give 5ml every 8 hours as needed for cough"
    ),
    
    # Max's follow-up (preventative)
    Medication(
        health_chart_id=health_charts[6].id,
        description="Heartgard Plus",
        notes="Monthly heartworm prevention, administer with food"
    )
]

session.add_all(medications)
session.commit()

Base.metadata.create_all(bind=engine) #Add to the bottom of page