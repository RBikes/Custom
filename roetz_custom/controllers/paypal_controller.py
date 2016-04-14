# coding: utf-8
from opener.addons.payment_paypal.controllers.main import PaypalController
from openerp import models


class PatchPaypal(models.AbstractModel):
    _name = 'patch.paypal'

    def _register_hook(self, cr):
        res = super(PatchPaypal, self)._register_hook(cr)
        PaypalController._notify_url = (
            'https://www.roetz-bikes.com/payment/paypal/ipn/')
        PaypalController._return_url = (
            'https://www.roetz-bikes.com/payment/paypal/dpn/')
        PaypalController._cancel_url = (
            'https://www.roetz-bikes.com/payment/paypal/cancel/')
        return res
