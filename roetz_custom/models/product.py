# coding: utf-8
import logging
from openerp import api, fields, models
from openerp.tools import ormcache
from openerp.addons.stock.product import product_product as StockProduct


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @ormcache()
    @api.multi
    def get_attribute_value_ids(self, pricelist_id, currency_id):
        self.ensure_one()
        product = self.with_context(active_id=self.id)
        attribute_value_ids = []
        visible_attrs = set(
            l.attribute_id.id
            for l in product.attribute_line_ids
            if len(l.value_ids) > 1)
        if pricelist_id != self.env.context['pricelist']:
            website_currency_id = currency_id
            to_currency_id = self.env['product.pricelist'].browse(
                self.env.context['pricelist']).currency_id.id
            for p in product.product_variant_ids:
                price = self.env['res.currency'].browse(
                    website_currency_id).compute(
                        p.lst_price, to_currency_id)
                attribute_value_ids.append([
                    p.id,
                    [v.id for v in p.attribute_value_ids
                     if v.attribute_id.id in visible_attrs],
                    p.price, price])
        else:
            attribute_value_ids = [
                [
                    p.id, [
                        v.id for v in p.attribute_value_ids
                        if v.attribute_id.id in visible_attrs
                    ],
                    p.price, p.lst_price,
                ] for p in product.product_variant_ids]
        return attribute_value_ids

    @api.multi
    def _compute_product_variant_count(self):
        """ Much quicker in SQL """
        if not self:
            return
        self.env.cr.execute(
            """ SELECT product_tmpl_id, COUNT(*) FROM product_product
                WHERE active AND product_tmpl_id IN %s GROUP BY product_tmpl_id
            """, (tuple(self.ids),))
        res = dict([(row[0], row[1]) for row in self.env.cr.fetchall()])
        for template in self:
            template.product_variant_count = res.get(template.id, 0)

    @api.multi
    def _compute_purchase_count(self):
        if not self:
            return
        self.env.cr.execute(
            """
            SELECT pp.product_tmpl_id, COUNT(pol.id)
            FROM product_product pp, purchase_order_line pol
            WHERE pol.product_id = pp.id AND product_tmpl_id IN %s
            GROUP BY pp.product_tmpl_id;
            """, (tuple(self.ids),))
        res = dict([(row[0], row[1]) for row in self.env.cr.fetchall()])
        for template in self:
            template.purchase_count = res.get(template.id, 0)

    @api.multi
    def _compute_sales_count(self):
        if not self:
            return
        self.env.cr.execute(
            """
            SELECT pp.product_tmpl_id, COUNT(sol.id)
            FROM product_product pp, sale_order_line sol
            WHERE sol.product_id = pp.id AND product_tmpl_id IN %s
            GROUP BY pp.product_tmpl_id;
            """, (tuple(self.ids),))
        res = dict([(row[0], row[1]) for row in self.env.cr.fetchall()])
        for template in self:
            template.sale_count = res.get(template.id, 0)

    @api.multi
    def _compute_mo_count(self):
        if not self:
            return
        self.env.cr.execute(
            """
            SELECT pp.product_tmpl_id, COUNT(mp.id)
            FROM product_product pp, mrp_production mp
            WHERE mp.product_id = pp.id AND product_tmpl_id IN %s
            GROUP BY pp.product_tmpl_id;
            """, (tuple(self.ids),))
        res = dict([(row[0], row[1]) for row in self.env.cr.fetchall()])
        for template in self:
            template.mo_count = res.get(template.id, 0)

    # Store the default code field to prevent prefetching 3000+ variants for
    # when reading the product code of the first variant.
    default_code = fields.Char(
        related='product_variant_ids.default_code',
        readonly=True, store=True)

    mo_count = fields.Integer(compute="_compute_mo_count")
    product_variant_count = fields.Integer(
        compute="_compute_product_variant_count")
    purchase_count = fields.Integer(compute="_compute_purchase_count")
    sales_count = fields.Integer(compute="_compute_sales_count")


class Product(models.Model):
    _inherit = 'product.product'

    def _register_hook(self, cr):
        """ Monkeypatch a wrapper around _product_available """

        def _product_available(
                self, cr, uid, ids, field_names=None, arg=False, context=None):
            """ Set prefetch_max to length of ids """
            context = dict(context, prefetch_max_product_product=len(ids))
            return self._roetz_product_available(
                cr, uid, ids, field_names=field_names, arg=arg,
                context=context)

        if not hasattr(StockProduct, '_roetz_custom_product_available'):
            logging.getLogger(__name__).info(
                'Installing monkeypatch on product.product::_product_available'
            )
            StockProduct._roetz_product_available = \
                StockProduct._product_available
            StockProduct._product_available = _product_available
        return super(Product, self)._register_hook(cr)
