from odoo import models,fields,api
from odoo.exceptions import UserError, ValidationError

class Books(models.Model):
    _name = 'library.books'
    _description = 'Books'


    name = fields.Char(required=True)
    author = fields.Char()
    date = fields.Date()
    category= fields.Selection([('fiction','Fiction'),('thriller','Thriller'),('romance','Romance')],required=True)
    price_borrow = fields.Float()
    price_buy = fields.Float()
    available_quantity= fields.Integer()
    sale_ids = fields.One2many(
        'sale.record',
        'book_id'
    )


    order_count = fields.Integer(
        compute='_compute_order_count',
        store=True
    )
    related_product=fields.Many2one('product.template')

    @api.model_create_multi
    def create(self, vals_list):
        books = super().create(vals_list)

        for book in books:
            product = self.env['product.template'].create({
                'name': book.name,
                'list_price': book.price_buy,
            })

            book.related_product = product.id

        return books

    @api.depends('sale_ids')
    def _compute_order_count(self):
        for book in self:
            book.order_count = len(book.sale_ids)












