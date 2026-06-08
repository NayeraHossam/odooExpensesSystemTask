from odoo import models, fields

class Clinic(models.Model):
    _name = 'clinic'
    _description = 'Clinic'

    name = fields.Char(string='Clinic Name')
    address = fields.Char(string='Address')
    doctor_ids = fields.Many2many(
        'doctor',
        string='Doctors'
    )