from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class AvailableAppointments(models.Model):
    _name = 'available.appointments'
    _description = 'Available Appointments'

    appointment_datetime = fields.Datetime(string="Appointment Time", required=True)
    type_of_appointment = fields.Selection([('doctor','Doctor'),('clinic','Clinic')],string="Type of Appointment")

    doctor_app_id = fields.Many2one('doctor', required=True, ondelete='cascade')