# coding: utf-8
from openerp import models


class AcquirerBuckaroo(models.Model):
    _inherit = 'aqcuirer.buckaroo'

    keys = ("Brq_amount Brq_culture Brq_currency Brq_invoicenumber "
            "brq_test Brq_websitekey").split()
