# coding: utf-8
import logging
from openerp import models


class AccountMoveReconcile(models.Model):
    _inherit = 'account.move.reconcile'

    def _register_hook(self, cr):
        """ Remove constraint _check_same_partner so that customer invoices
        can be reconciled with moves from the payment provider """
        res = super(AccountMoveReconcile, self)._register_hook(cr)
        index = 0
        for _fun, msg, _names in self._constraints[:]:
            if '_check_same_partner' in str(_fun):
                logging.getLogger(__name__).debug(
                    "Removing constraint that limits reconcilations to move "
                    "lines that have the same partner.")
                del self._constraints[index]
            index += 1
        return res
