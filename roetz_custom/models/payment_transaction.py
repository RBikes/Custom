# coding: utf-8
from openerp import api, models


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def form_feedback(self, data, acquirer_name):
        return super(PaymentTransaction, self).with_context(
            mail_off=True).form_feedback(data, aquirer_name)
