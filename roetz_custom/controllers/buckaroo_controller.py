# coding: utf-8
import logging
import pprint
import werkzeug
from openerp import http, SUPERUSER_ID
from opener.addons.payment_buckaroo.controllers.main import BuckarooController
from openerp import models

_logger = logging.getLogger(__name__)


class PatchBuckaroo(models.AbstractModel):
    _name = 'patch.buckaroo'

    def _register_hook(self, cr):
        res = super(PatchBuckaroo, self)._register_hook(cr)
        BuckarooController._return_url = (
            'https://www.roetz-bikes.com/payment/buckaroo/return')
        BuckarooController._cancel_url = (
            'https://www.roetz-bikes.com/payment/buckaroo/cancel')
        BuckarooController._exception_url = (
            'https://www.roetz-bikes.com/payment/buckaroo/error')
        BuckarooController._exception_url = (
            'https://www.roetz-bikes.com/payment/buckaroo/error')
        return res


class RoetzBuckaroo(BuckarooController):

    @http.route([
        '/payment/buckaroo/return',
        '/payment/buckaroo/cancel',
        '/payment/buckaroo/error',
        '/payment/buckaroo/reject',
    ], type='http', auth='none')
    def buckaroo_return(self, **post):
        """ Override this method to return url based on status code """
        _logger.info('Buckaroo: entering form_feedback with post data %s',
                     pprint.pformat(post))  # debug
        http.request.registry['payment.transaction'].form_feedback(
            http.request.cr, SUPERUSER_ID, post, 'buckaroo',
            context=http.request.context)
        if post.get('brq_statuscode') in ('190', '790', '791', '792', '793'):
            return_url = '/shop/payment/validate'
        else:
            return_url = '/page/payment-failed'
        return werkzeug.utils.redirect(return_url)
