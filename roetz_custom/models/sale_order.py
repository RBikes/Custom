# coding: utf-8
from datetime import timedelta
from openerp import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_quotation_send(self):
        if self.env.context.get('mail_off'):
            return False
        return super(SaleOrder, self).action_quotation_send()

    new_commitment_date = fields.Datetime()
    # Overwrite old API function field
    commitment_date = fields.Datetime(
        compute="_compute_commitment_date",
        store=True)

    @api.multi
    @api.depends('date_order', 'order_line', 'order_line.delay')
    def _compute_commitment_date(self):
        """ Take max date instead of min. delivery date """
        for order in self:
            delay = max([line.delay for line in order.order_line] or [0])
            order.commitment_date = fields.Datetime.to_string(
                fields.Datetime.from_string(
                    order.date_order) + timedelta(days=delay))
