# coding: utf-8
from openerp import api, models


class Quant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def _account_entry_move(self, quants, move):
        if not move:
            return False
        return super(Quant, self)._account_entry_move(quants, move)
