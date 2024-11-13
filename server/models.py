from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Enum
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

# Define metadata for naming conventions (including foreign key names)
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

# Initialize the SQLAlchemy object
db = SQLAlchemy(metadata=metadata)


# Role Model (for roles table)
class Role(db.Model, SerializerMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Relationships
    doctors = db.relationship('Doctor', back_populates='role')
    receptionists = db.relationship('Receptionist', back_populates='role')
    lab_techs = db.relationship('LabTech', back_populates='role')

    serialize_only = ('id', 'name')


# Doctors Model
class Doctor(db.Model, SerializerMixin):  # Table: 'doctors'
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    # Relationships
    role = db.relationship('Role', back_populates='doctors')
    appointments = db.relationship('Appointment', back_populates='doctor')
    diagnoses = db.relationship('Diagnosis', back_populates='doctor')
    prescriptions = db.relationship('Prescription', back_populates='doctor')

    serialize_rules = ('-role.doctors', '-appointments.doctor', '-diagnoses.doctor', '-prescriptions.doctor')


# Receptionist Model
class Receptionist(db.Model, SerializerMixin):  # Table: 'receptionists'
    __tablename__ = 'receptionists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    # Relationships
    role = db.relationship('Role', back_populates='receptionists')
    payments = db.relationship('Payment', back_populates='receptionist')

    serialize_rules = ('-role.receptionists', '-payments.receptionist')


# LabTech Model
class LabTech(db.Model, SerializerMixin):  # Table: 'lab_techs'
    __tablename__ = 'lab_techs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    # Relationships
    role = db.relationship('Role', back_populates='lab_techs')
    tests = db.relationship('Test', back_populates='lab_tech')

    serialize_rules = ('-role.lab_techs', '-tests.lab_tech')


# Patient Model
class Patient(db.Model, SerializerMixin):  # Table: 'patients'
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    phone_number = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    medical_history = db.Column(db.String)

    # Relationships
    appointments = db.relationship('Appointment', back_populates='patient')
    tests = db.relationship('Test', back_populates='patient')
    diagnoses = db.relationship('Diagnosis', back_populates='patient')
    prescriptions = db.relationship('Prescription', back_populates='patient')
    payments = db.relationship('Payment', back_populates='patient')
    consultations = db.relationship('Consultation', back_populates='patient')  # Add this line

    serialize_rules = ('-appointments.patient', '-tests.patient', '-diagnoses.patient', '-prescriptions.patient', '-payments.patient', '-consultations.patient')  # Update serialize rules if necessary



# Appointment Model
class Appointment(db.Model, SerializerMixin):  # Table: 'appointments'
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)

    # Relationships
    patient = db.relationship('Patient', back_populates='appointments')
    doctor = db.relationship('Doctor', back_populates='appointments')

    serialize_rules = ('-patient.appointments', '-doctor.appointments')


# Test Model
class Test(db.Model, SerializerMixin):  # Table: 'tests'
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    lab_tech_id = db.Column(db.Integer, db.ForeignKey('lab_techs.id'), nullable=False)
    test_types_id = db.Column(db.Integer, db.ForeignKey('test_types.id'), nullable=False)
    status = db.Column(Enum('pending', 'completed', name='test_status'), nullable=False, server_default='pending')
    test_results = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)

    # Relationships
    patient = db.relationship('Patient', back_populates='tests')
    lab_tech = db.relationship('LabTech', back_populates='tests')
    test_types = db.relationship('TestType', back_populates='tests')

    serialize_only = ('id', 'patient_id', 'doctor_id', 'lab_tech_id', 'test_types_id', 'status', 'created_at')


# TestTypes Model
class TestType(db.Model, SerializerMixin):  # Table: 'test_types'
    __tablename__ = 'test_types'

    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric, nullable=False)

    # Relationships
    tests = db.relationship('Test', back_populates='test_types')

    serialize_only = ('id', 'test_name', 'description', 'price', 'tests.id')


# Consultation Model
class Consultation(db.Model, SerializerMixin):  # Table: 'consultations'
    __tablename__ = 'consultations'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    consultation_date = db.Column(db.DateTime, nullable=False)
    consultation_notes = db.Column(db.String)

    # Relationships
    patient = db.relationship('Patient', back_populates='consultations')  # Reverse relationship to Patient

    serialize_only = (
        'id', 'patient_id', 'doctor_id', 'consultation_date',
        'consultation_notes', 'patient.name'
    )


# Diagnosis Model
class Diagnosis(db.Model, SerializerMixin):  # Table: 'diagnoses'
    __tablename__ = 'diagnoses'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    diagnosis_description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    diagnosis_notes = db.Column(db.String)

    # Relationships
    patient = db.relationship('Patient', back_populates='diagnoses')
    doctor = db.relationship('Doctor', back_populates='diagnoses')

    serialize_only = (
        'id', 'patient_id', 'doctor_id', 'diagnosis_description',
        'created_at', 'diagnosis_notes'
    )


# Prescription Model
class Prescription(db.Model, SerializerMixin):  # Table: 'prescriptions'
    __tablename__ = 'prescriptions'

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    dosage = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    prescription_date = db.Column(db.DateTime, nullable=False)

    # Relationships
    patient = db.relationship('Patient', back_populates='prescriptions')
    doctor = db.relationship('Doctor', back_populates='prescriptions')
    medicine = db.relationship('Medicine', back_populates='prescriptions')

    serialize_only = (
        'id', 'appointment_id', 'patient_id', 'doctor_id', 'medicine_id',
        'dosage', 'quantity', 'duration', 'prescription_date'
    )


# Medicine Model
class Medicine(db.Model, SerializerMixin):  # Table: 'medicines'
    __tablename__ = 'medicines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    # Relationships
    prescriptions = db.relationship('Prescription', back_populates='medicine')

    serialize_only = ('id', 'name', 'description')


# Payments Model
class Payment(db.Model, SerializerMixin):  # Table: 'payments'
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    receptionist_id = db.Column(db.Integer, db.ForeignKey('receptionists.id'), nullable=False)
    service = db.Column(db.String, nullable=False)
    amount = db.Column(db.Numeric, nullable=False)

    # Relationships
    patient = db.relationship('Patient', back_populates='payments')
    receptionist = db.relationship('Receptionist', back_populates='payments')

    serialize_rules = ('-patient.payments', '-receptionist.payments')
