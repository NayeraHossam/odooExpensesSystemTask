from odoo import models,fields,api
from odoo.exceptions import UserError, ValidationError


class Expense(models.Model):
    _name = 'expense'
    _description = 'Expense'

    name = fields.Char(required=True)
    amount = fields.Float()
    date = fields.Date()
    type= fields.Selection([('borrow','Borrow'),('buy','Buy'),('manual','Manual')],required=True)

    user_id = fields.Many2one('res.partner')

    @api.model
    def create(self,vals):
        partner = self.env['res.partner'].browse(vals['user_id'])
        amount = vals.get('amount',0)

        if amount<=0:
            raise ValidationError(
                "Amount must be greater than 0"
            )
        if amount>partner.budget:
            raise ValidationError(
                "Expenses exceed the budget"
            )

        partner.budget -= amount

        return super().create(vals)








