# coding: utf-8
from openerp import api, models


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def write(self, vals):
        if self.env.context.get('mail_off') and 'message_follower_ids' in vals:
            del vals['message_follower_ids']
        return super(Partner, self).write(vals)
