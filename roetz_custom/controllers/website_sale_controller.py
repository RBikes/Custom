from opener.addons.website_sale.controllers.main import website_sale


class SaleController(website_sale):

    def checkout_form_save(self, checkout):
        """  Inject context key honoured in res.partner::write() """
        self.request.context['mail_off'] == True
        res = super(SaleController, self).checkout_form_sale(checkout)
        del self.request.context['mail_off']
        return res

    @http.route('/shop/payment/validate', type='http', auth="public", website=True)
    def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
        """  Inject context key honoured in sale.order::action_quotation_send() """
        self.request.context['mail_off'] == True
        res = super_SaleController, self).payment_validate(
            transaction_id=transaction_id, sale_order_id=sale_order_id, **post)
        del self.request.context['mail_off']
        return res
