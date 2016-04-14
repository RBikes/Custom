# coding: utf-8
from openerp import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_quotation_send(self):
        if self.env.context.get('mail_off'):
            return False
        return super(SaleOrder, self).action_quotation_send()
