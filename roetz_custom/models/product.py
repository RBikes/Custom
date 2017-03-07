# coding: utf-8
from openerp import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def _get_product_variant_count(self):
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

    # Store the default code field to prevent prefetching 3000+ variants for
    # when reading the product code of the first variant.
    default_code = fields.Char(
        related='product_variant_ids.default_code',
        readonly=True, store=True)

    product_variant_count = fields.Integer(
        compute="_get_product_variant_count")
