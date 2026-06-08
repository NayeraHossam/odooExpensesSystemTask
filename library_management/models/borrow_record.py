from OpenSSL.rand import status
from odoo import models,fields,api
from odoo.exceptions import UserError, ValidationError

class BorrowRecord(models.Model):
    _name = 'borrow.record'
    _description = 'Borrow Record'

    user_id = fields.Many2one('res.partner')
    book_id = fields.Many2one('library.books')
    borrow_date = fields.Datetime()
    return_date = fields.Datetime()
    status = fields.Selection([('borrowed','Borrowed'),('returned','Returned')])


    @api.model
    def create(self, vals):
        book = self.env['library.books'].browse(vals['book_id'])


        if book.available_quantity <= 0:
            raise ValidationError("No copies available.")

        book.available_quantity -= 1

        return super().create(vals)

    def write(self, vals):
        for rec in self:
            if (
                    vals.get('status') == 'returned'
                    and rec.status == 'borrowed'
            ):
                rec.book_id.available_quantity += 1

        return super().write(vals)

    def create_expence(self):
        for rec in self:
            self.env['expense'].create({
                'user_id': rec.user_id.id,
                'amount': rec.book_id.price_borrow,
                'type': 'borrow'
            })



