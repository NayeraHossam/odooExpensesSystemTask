from odoo import models,fields,api
from odoo.exceptions import UserError, ValidationError

class SaleRecord(models.Model):
    _name = 'sale.record'
    _description = 'Sale Record'

    user_id = fields.Many2one('res.partner')
    book_id = fields.Many2one('library.books')
    quantity = fields.Integer(default=1)
    price = fields.Float(related='book_id.price_buy')
    total_price = fields.Float(compute='_compute_total_price', store=True)
    confirm = fields.Boolean(default=False)

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')



    @api.model
    def create(self, vals):
        record = super().create(vals)

        self.env['expense'].create({
            'name':'Book Purchase',
            'user_id': record.user_id.id,
            'amount': record.book_id.price_buy,
            'type': 'buy',
        })
        return record

    @api.depends('book_id.price_buy', 'quantity')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.book_id.price_buy * record.quantity
        return record.total_price

    def action_confirm(self):
        SaleOrder = self.env['sale.order']

        for record in self:

            if record.book_id.available_quantity <= 0:
                raise ValidationError("No copies available.")

            sale_order = self.env['sale.order'].create({
                'partner_id': record.user_id.id,
                'date_order': record.book_id.date,
            })

            self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': record.book_id.related_product.id,
                'product_uom_qty': record.quantity,
                'price_unit': record.price,
            })

            record.sale_order_id = sale_order.id
            record.book_id.available_quantity -= record.quantity
            record.confirm = True

        return True

    def action_view_sale_order(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.sale_order_id.id,
            'target': 'new',
        }






