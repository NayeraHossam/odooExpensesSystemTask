from odoo import models, fields,api
from odoo.exceptions import UserError, ValidationError


class Appointment(models.Model):
    _name = 'appointment'
    _description = 'Appointment'

    reason = fields.Char(string='Reason')
    appointment = fields.Datetime(string='Appointment')
    clinic_name = fields.Char(string='Clinic Name')

    patient_id = fields.Many2one(
        'patient',
        string='Patient',
        required=True
    )

    doctor_id = fields.Many2one(
        'doctor',
        string='Doctor',
        required=True
    )
    available_slot_id = fields.Many2one(
        'available.appointments',
        domain="[('doctor_app_id', '=', doctor_id)]"
    )
    available_appointment_ids = fields.One2many(
        related='doctor_id.appointment_ids',
        readonly=True,
    )
    partner_id = fields.Many2one('res.partner')

    @api.constrains('doctor_id', 'appointment')
    def _check_appointment_availability(self):
        for rec in self:
            available_slots = rec.doctor_id.appointment_ids.mapped('appointment_datetime')

            if rec.appointment not in available_slots:
                raise ValidationError(
                    'Appointment is not available for this doctor.'
                )

    @api.model
    def create(self, vals):
        record = super().create(vals)

        # find matching available slot
        slot = self.env['available.appointments'].search([
            ('doctor_app_id', '=', record.doctor_id.id),
            ('appointment_datetime', '=', record.appointment)
        ], limit=1)

        if slot:
            slot.unlink()

        record.create_expense()

        return record

    def create_expense(self):
        for rec in self:
            partner = self.env['res.partner'].search([
                ('name', '=', rec.patient_id.name)
            ], limit=1)

            if not partner:
                raise ValidationError(
                    f"No partner found for patient {rec.patient_id.name}"
                )

            self.env['expense'].create({
                'name': f'Appointment Expense - {rec.patient_id.name}',
                'user_id': rec.patient_id.partner_id.id,
                'amount': 100,
                'date': rec.appointment.date(),
                'type': 'manual',
            })


