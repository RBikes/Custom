# coding: utf-8
from openerp import fields, models


class Production(models.Model):
    _inherit = 'mrp.production'

    # Overwrite readonly property
    date_planned = fields.Date(readonly=False)
    product_id = fields.Many2one(index=True)
