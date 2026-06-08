from odoo import models, fields
from odoo.exceptions import ValidationError


class BorrowBookWizard(models.TransientModel):
    _name = 'borrow.book.wizard'
    _description = 'Borrow Book Wizard'

    user_id = fields.Many2one(
        'res.partner',
        string='Member',
        required=True
    )

    book_id = fields.Many2one(
        'library.books',
        string='Book',
        required=True
    )

    borrow_date = fields.Datetime(
        default=fields.Datetime.now,
        required=True
    )

    def action_borrow(self):

        expense_user = self.env['expense.user'].search([
            ('partner_id', '=', self.user_id.id)
        ], limit=1)

        if not expense_user:
            raise ValidationError("Expense user not found.")

        if self.book_id.available_quantity <= 0:
            raise ValidationError("No copies available.")

        if expense_user.budget < self.book_id.price_borrow:
            raise ValidationError("Insufficient budget.")

        self.env['borrow.record'].create({
            'user_id': self.user_id.id,
            'book_id': self.book_id.id,
            'borrow_date': self.borrow_date,
            'status': 'borrowed',
        })

        self.book_id.available_quantity -= 1

        expense_user.budget -= self.book_id.price_borrow

        self.env['expense'].create({
            'name': f'Borrow {self.book_id.name}',
            'user_id': self.user_id.id,
            'amount': self.book_id.price_borrow,
            'type': 'borrow',
        })

        return {'type': 'ir.actions.act_window_close'}