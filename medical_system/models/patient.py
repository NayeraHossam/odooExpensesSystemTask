from odoo import models, fields,api

class Patient(models.Model):
    _name = 'patient'
    _description = 'Patient'

    name = fields.Char(string='Patient Name')
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ])
    ph_number = fields.Char(string='Phone Number')
    email = fields.Char(string='Email Address')
    next_appointment = fields.Datetime(
        string='Next Appointment',
        compute='_compute_next_appointment',
        store=True
    )

    doctor_id = fields.Many2one('doctor')

    clinic_ids = fields.One2many(
        'appointment',
        'patient_id',
        string='Appointments'
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Contact'
    )



    @api.depends('clinic_ids.appointment')
    def _compute_next_appointment(self):
        for rec in self:
            appointments = rec.clinic_ids.mapped('appointment')
            rec.next_appointment = max(appointments) if appointments else False

    @api.model
    def create(self, vals):
        patient = super().create(vals)

        partner = self.env['res.partner'].create({
            'name': patient.name,
            'email': patient.email,
            'phone': patient.ph_number,
            'budget': 10000,
        })

        patient.partner_id = partner.id

        self.env['expense.user'].create({
            'partner_id': partner.id,
        })

        return patient
