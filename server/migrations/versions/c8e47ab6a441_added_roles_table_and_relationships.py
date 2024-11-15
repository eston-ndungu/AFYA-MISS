"""Added roles table and relationships

Revision ID: c8e47ab6a441
Revises: 
Create Date: 2024-11-13 08:49:44.717423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8e47ab6a441'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('medicines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('date_of_birth', sa.DateTime(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('medical_history', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('test_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('test_name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('doctors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name=op.f('fk_doctors_role_id_roles')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('lab_techs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name=op.f('fk_lab_techs_role_id_roles')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receptionists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name=op.f('fk_receptionists_role_id_roles')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('appointments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.Column('appointment_time', sa.DateTime(), nullable=False),
    sa.Column('appointment_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], name=op.f('fk_appointments_doctor_id_doctors')),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], name=op.f('fk_appointments_patient_id_patients')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('consultations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.Column('consultation_date', sa.DateTime(), nullable=False),
    sa.Column('consultation_notes', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], name=op.f('fk_consultations_doctor_id_doctors')),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], name=op.f('fk_consultations_patient_id_patients')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('diagnoses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.Column('diagnosis_description', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('diagnosis_notes', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], name=op.f('fk_diagnoses_doctor_id_doctors')),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], name=op.f('fk_diagnoses_patient_id_patients')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('receptionist_id', sa.Integer(), nullable=False),
    sa.Column('service', sa.String(), nullable=False),
    sa.Column('amount', sa.Numeric(), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], name=op.f('fk_payments_patient_id_patients')),
    sa.ForeignKeyConstraint(['receptionist_id'], ['receptionists.id'], name=op.f('fk_payments_receptionist_id_receptionists')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.Column('lab_tech_id', sa.Integer(), nullable=False),
    sa.Column('test_types_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('pending', 'completed', name='test_status'), server_default='pending', nullable=False),
    sa.Column('test_results', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], name=op.f('fk_tests_doctor_id_doctors')),
    sa.ForeignKeyConstraint(['lab_tech_id'], ['lab_techs.id'], name=op.f('fk_tests_lab_tech_id_lab_techs')),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], name=op.f('fk_tests_patient_id_patients')),
    sa.ForeignKeyConstraint(['test_types_id'], ['test_types.id'], name=op.f('fk_tests_test_types_id_test_types')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prescriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('appointment_id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.Column('medicine_id', sa.Integer(), nullable=False),
    sa.Column('dosage', sa.String(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('prescription_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['appointment_id'], ['appointments.id'], name=op.f('fk_prescriptions_appointment_id_appointments')),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], name=op.f('fk_prescriptions_doctor_id_doctors')),
    sa.ForeignKeyConstraint(['medicine_id'], ['medicines.id'], name=op.f('fk_prescriptions_medicine_id_medicines')),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], name=op.f('fk_prescriptions_patient_id_patients')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prescriptions')
    op.drop_table('tests')
    op.drop_table('payments')
    op.drop_table('diagnoses')
    op.drop_table('consultations')
    op.drop_table('appointments')
    op.drop_table('receptionists')
    op.drop_table('lab_techs')
    op.drop_table('doctors')
    op.drop_table('test_types')
    op.drop_table('roles')
    op.drop_table('patients')
    op.drop_table('medicines')
    # ### end Alembic commands ###
