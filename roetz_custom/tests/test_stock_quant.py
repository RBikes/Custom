# coding: utf-8
from openerp.tests.common import TransactionCase


class TestStockQuant(TransactionCase):
    def test_stock_quant(self):
        """ I can call _account_entry_move without an actual move """
        self.env['stock.quant']._account_entry_move(
            self.env['stock.quant'], self.env['account.move'])
