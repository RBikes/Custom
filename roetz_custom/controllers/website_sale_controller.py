from openerp import http
from openerp.addons.website_sale.controllers.main import website_sale


class SaleController(website_sale):

    def checkout_form_save(self, checkout):
        """  Inject context key honoured in res.partner::write() """
        http.request.context['mail_off'] = True
        res = super(SaleController, self).checkout_form_sale(checkout)
        del http.request.context['mail_off']
        return res

    @http.route('/shop/payment/validate', type='http', auth="public",
                website=True)
    def payment_validate(
            self, transaction_id=None, sale_order_id=None, **post):
        """  Inject context key honoured in sale.order::action_quotation_send()
        """
        http.request.context['mail_off'] = True
        res = super(SaleController, self).payment_validate(
            transaction_id=transaction_id, sale_order_id=sale_order_id, **post)
        del http.request.context['mail_off']
        return res
