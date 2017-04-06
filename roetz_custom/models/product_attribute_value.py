# coding: utf-8
from openerp import fields, models


class Value(models.Model):
    _inherit = 'product.attribute.value'

    attribute_id = fields.Many2one(index=True)
