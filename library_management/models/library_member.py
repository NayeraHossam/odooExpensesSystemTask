from odoo import models,fields,api
from odoo.exceptions import UserError, ValidationError

class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'

    library_id = fields.Many2one('res.partner')


    @api.model
    def create(self, vals):
        member = super().create(vals)

        self.env['expense.user'].create({
            'partner_id': member.library_id.id,
            'budget': 1000,
        })

        return member