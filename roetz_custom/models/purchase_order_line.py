# coding: utf-8
from openerp import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_id = fields.Many2one(index=True)
