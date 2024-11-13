from app import app, db
from models import Role, Doctor, Receptionist, LabTech, Patient, Appointment, Test, Consultation, Diagnosis, Prescription, Payment, TestType, Medicine

# Import random, Faker, datetime, and timedelta
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Helper function to drop all tables (clear the database)
def drop_all_tables():
    with app.app_context():
        db.drop_all()  # Drops all tables in the database
        print("All tables dropped successfully.")

# Helper function to create roles
def create_roles():
    roles = ['Doctor', 'Receptionist', 'LabTech']
    specialties = ['Cardiologist', 'Dermatologist', 'Orthopedist', 'Neurologist', 'Pediatrician', 'General Physician']

    for role_name in roles:
        existing_role = Role.query.filter_by(name=role_name).first()
        if not existing_role:
            role = Role(name=role_name)
            db.session.add(role)

    for specialty in specialties:
        existing_role = Role.query.filter_by(name=specialty).first()
        if not existing_role:
            role = Role(name=specialty)
            db.session.add(role)

    db.session.commit()
    print("Roles created successfully.")

# Helper function to create doctors
def create_doctors():
    roles = Role.query.all()
    for i in range(10):  # Create 10 doctors
        role = random.choice(roles)
        doctor = Doctor(
            name=fake.name(),
            email=fake.email(),
            password=fake.password(),
            role_id=role.id,
        )
        db.session.add(doctor)
    db.session.commit()
    print("Doctors created successfully.")

# Helper function to create receptionists
def create_receptionists():
    roles = Role.query.filter(Role.name == 'Receptionist').all()
    for i in range(5):  # Create 5 receptionists
        role = random.choice(roles)
        receptionist = Receptionist(
            name=fake.name(),
            email=fake.email(),
            password=fake.password(),
            role_id=role.id,
        )
        db.session.add(receptionist)
    db.session.commit()
    print("Receptionists created successfully.")

# Helper function to create lab techs
def create_lab_techs():
    roles = Role.query.filter(Role.name == 'LabTech').all()
    for i in range(5):  # Create 5 lab techs
        role = random.choice(roles)
        lab_tech = LabTech(
            name=fake.name(),
            role_id=role.id,
        )
        db.session.add(lab_tech)
    db.session.commit()
    print("LabTechs created successfully.")

# Helper function to create patients
def create_patients():
    conditions = [
        'Hypertension', 'Diabetes', 'Asthma', 'Chronic Back Pain', 'Migraine', 'Anemia', 'Arthritis', 'Allergies'
    ]
    for i in range(20):  # Create 20 patients
        patient = Patient(
            name=fake.name(),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=80),
            phone_number=fake.phone_number(),
            email=fake.email(),
            address=fake.address(),
            gender=random.choice(['Male', 'Female']),
            medical_history=random.choice(conditions)
        )
        db.session.add(patient)
    db.session.commit()
    print("Patients created successfully.")

# Helper function to create medicines
def create_medicines():
    medicines = [
        ('Paracetamol', 'Used to relieve pain and reduce fever'),
        ('Ibuprofen', 'Used to reduce fever, pain, and inflammation'),
        ('Amoxicillin', 'An antibiotic used to treat bacterial infections'),
        ('Cetirizine', 'An antihistamine used to relieve allergy symptoms'),
        ('Metformin', 'Used to control high blood sugar in type 2 diabetes'),
        ('Aspirin', 'Used to reduce pain, fever, and inflammation'),
        ('Lisinopril', 'Used to treat high blood pressure and heart failure')
    ]

    for name, description in medicines:
        existing_medicine = Medicine.query.filter_by(name=name).first()
        if not existing_medicine:
            medicine = Medicine(
                name=name,
                description=description
            )
            db.session.add(medicine)
    db.session.commit()
    print("Medicines created successfully.")

# Helper function to create appointments
def create_appointments():
    patients = Patient.query.all()
    doctors = Doctor.query.all()

    for i in range(10):  # Create 10 appointments
        appointment = Appointment(
            patient_id=random.choice(patients).id,
            doctor_id=random.choice(doctors).id,
            appointment_time=fake.date_this_year(),
            appointment_date=fake.date_this_year()
        )
        db.session.add(appointment)
    db.session.commit()
    print("Appointments created successfully.")

# Helper function to create consultations
def create_consultations():
    patients = Patient.query.all()
    doctors = Doctor.query.all()

    consultation_notes = [
        "Patient presents with a headache and dizziness. Recommended further tests.",
        "Patient shows signs of chronic back pain. Suggested physical therapy.",
        "Patient reports feeling fatigued. Blood tests suggested for anemia.",
        "Patient complains of joint pain and swelling. Arthritis suspected, medication prescribed.",
        "Patient has a persistent cough. Possible asthma attack. Medication prescribed."
    ]

    for i in range(5):  # Create 5 consultations
        consultation = Consultation(
            patient_id=random.choice(patients).id,
            doctor_id=random.choice(doctors).id,
            consultation_date=fake.date_this_year(),
            consultation_notes=random.choice(consultation_notes)
        )
        db.session.add(consultation)
    db.session.commit()
    print("Consultations created successfully.")

# Helper function to create diagnoses
def create_diagnoses():
    conditions = [
        'Hypertension', 'Diabetes', 'Asthma', 'Chronic Back Pain', 'Migraine', 'Anemia', 'Arthritis', 'Allergies'
    ]
    patients = Patient.query.all()
    doctors = Doctor.query.all()

    for i in range(5):  # Create 5 diagnoses
        diagnosis = Diagnosis(
            patient_id=random.choice(patients).id,
            doctor_id=random.choice(doctors).id,
            diagnosis_description=random.choice(conditions),
            created_at=fake.date_this_year(),
            diagnosis_notes=fake.text(max_nb_chars=100)
        )
        db.session.add(diagnosis)
    db.session.commit()
    print("Diagnoses created successfully.")

# Helper function to create prescriptions
def create_prescriptions():
    medicines = Medicine.query.all()
    appointments = Appointment.query.all()
    patients = Patient.query.all()
    doctors = Doctor.query.all()

    for i in range(5):  # Create 5 prescriptions
        prescription = Prescription(
            appointment_id=random.choice(appointments).id,
            patient_id=random.choice(patients).id,
            doctor_id=random.choice(doctors).id,
            medicine_id=random.choice(medicines).id,
            dosage=fake.word(),
            quantity=random.randint(1, 5),
            duration=random.randint(1, 10),
            prescription_date=fake.date_this_year()
        )
        db.session.add(prescription)
    db.session.commit()
    print("Prescriptions created successfully.")

# Helper function to create payments
def create_payments():
    patients = Patient.query.all()
    receptionists = Receptionist.query.all()

    for i in range(5):  # Create 5 payments
        payment = Payment(
            patient_id=random.choice(patients).id,
            receptionist_id=random.choice(receptionists).id,
            service=random.choice(['Consultation', 'Lab Test', 'X-Ray', 'Blood Test']),
            amount=random.randint(100, 500)
        )
        db.session.add(payment)
    db.session.commit()
    print("Payments created successfully.")

# Main function to seed the database
def seed_data():
    drop_all_tables()  # Drop all tables before reseeding
    db.create_all()    # Recreate all tables
    create_roles()
    create_doctors()
    create_receptionists()
    create_lab_techs()
    create_patients()
    create_medicines()  # New function to add medicines
    create_appointments()
    create_consultations()
    create_diagnoses()
    create_prescriptions()
    create_payments()

if __name__ == "__main__":
    with app.app_context():
        seed_data()
