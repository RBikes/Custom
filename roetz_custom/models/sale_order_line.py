# coding: utf-8
from openerp import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_id = fields.Many2one(index=True)
