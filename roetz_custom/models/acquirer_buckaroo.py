# coding: utf-8
from hashlib import sha1
import urllib
import urlparse
from openerp import models


class AcquirerBuckaroo(models.Model):
    _inherit = 'payment.acquirer'

    def _buckaroo_generate_digital_sign(self, acquirer, inout, values):
        """ Overwrite this method so that we can apply our own keys list """
        assert inout in ('in', 'out')
        assert acquirer.provider == 'buckaroo'

        # keys = "add_returndata Brq_amount Brq_culture Brq_currency
        # Brq_invoicenumber Brq_return Brq_returncancel Brq_returnerror
        # Brq_returnreject brq_test Brq_websitekey".split()
        keys = ("Brq_amount Brq_culture Brq_currency Brq_invoicenumber "
                "brq_test Brq_websitekey").split()

        def get_value(key):
            if values.get(key):
                return values[key]
            return ''

        values = dict(values or {})

        if inout == 'out':
            for key in values.keys():
                # case insensitive keys
                if key.upper() == 'BRQ_SIGNATURE':
                    del values[key]
                    break

            items = sorted(values.items(), key=lambda (x, y): x.lower())
            sign = ''.join('%s=%s' % (
                k, urllib.unquote_plus(v)) for k, v in items)
        else:
            sign = ''.join('%s=%s' % (k, get_value(k)) for k in keys)
        #Add the pre-shared secret key at the end of the signature
        sign = sign + acquirer.brq_secretkey
        if isinstance(sign, str):
            # TODO: remove me? should not be used
            sign = urlparse.parse_qsl(sign)
        shasign = sha1(sign.encode('utf-8')).hexdigest()
        return shasign
