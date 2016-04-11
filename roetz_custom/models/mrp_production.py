# coding: utf-8
from openerp import fields, models


class Production(models.Model):
    _inherit = 'mrp.production'

    # Overwrite readonly property
    date_planned = fields.date(readonly=False)
