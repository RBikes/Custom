# coding: utf-8
from openerp import api, models


class AttributeLine(models.Model):
    _inherit = 'product.attribute.line'

    @api.multi
    def write(self, vals):
        if not self.env.context.get('create_product_variant'):
            templates = self.mapped('product_tmpl_id')
        res = super(AttributeLine, self).write(vals)
        if not self.env.context.get('create_product_variant'):
            templates += self.mapped('product_tmpl_id')
            templates.clear_attribute_value_cache()
        return res

    @api.model
    def create(self, vals):
        res = super(AttributeLine, self).create(vals)
        if not self.env.context.get('create_product_variant'):
            res.product_tmpl_id.clear_attribute_value_cache()
        return res

    @api.multi
    def unlink(self):
        if not self.env.context.get('create_product_variant'):
            templates = self.mapped('product_tmpl_id')
        res = super(AttributeLine, self).unlink()
        if not self.env.context.get('create_product_variant'):
            templates.clear_attribute_value_cache()
        return res
