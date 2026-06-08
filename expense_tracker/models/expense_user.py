from odoo import models,fields,api
from odoo.exceptions import UserError, ValidationError

class ExpenseUser(models.Model):
    _name = 'expense.user'
    _description = 'Expense User'

    partner_id = fields.Many2one(
        'res.partner',
        string="User",
        required=True,
        readonly=0


    )

    email = fields.Char(
        related='partner_id.email',
        string="Email",
        readonly=0
    )

    budget = fields.Float(
        related='partner_id.budget',
        string="Budget",
        readonly=0
    )
    is_budget_low = fields.Boolean(
        compute = '_compute_budget_warning',
        string="Budget low",
        store = True
    )



    @api.depends('budget')
    def _compute_budget_warning(self):
        for rec in self:
            rec.is_budget_low = rec.budget < 50

