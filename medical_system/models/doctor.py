from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError



class Doctor(models.Model):
    _name = 'doctor'
    _description = 'Doctor'

    name = fields.Char(string='Doctor Name')
    email = fields.Char(string='Email Address')
    #clinic_name = fields.Char(related = 'clinic_ids.name')

    clinic_ids = fields.One2many(
        'appointment',
        'doctor_id',
        string='Reservations'
    )

    appointment_ids = fields.One2many(
        'available.appointments',
        'doctor_app_id',
        string='Available Appointments'
    )
    patient_ids = fields.One2many('patient', 'doctor_id', string='Patients')

