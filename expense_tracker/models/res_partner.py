from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    budget = fields.Float(
        string="Budget",
        default=100.0
    )
