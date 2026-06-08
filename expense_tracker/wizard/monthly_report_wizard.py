from odoo import models, fields
from datetime import date

class MonthlyReportWizard(models.TransientModel):
    _name = 'monthly.report.wizard'
    _description = 'Monthly Expense Report Wizard'

    month = fields.Selection([
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ], required=True)

    year = fields.Integer(
        default=date.today().year,
        required=True
    )

    def action_generate_report(self):
        expenses = self.env['expense'].search([])

        monthly_expenses = expenses.filtered(
            lambda e:
                e.date and
                e.date.month == int(self.month) and
                e.date.year == int(self.year)
        )

        total = sum(monthly_expenses.mapped('amount'))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Monthly Expenses',
            'res_model': 'expense',
            'view_mode': 'tree,form',
            'domain': [
                ('id', 'in', monthly_expenses.ids)
            ],
            'context': {
                'default_total_amount': total
            }
        }