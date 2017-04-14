# coding: utf-8
from openerp import api, fields, models


class Value(models.Model):
    _inherit = 'product.attribute.value'

    attribute_id = fields.Many2one(index=True)

    @api.multi
    def write(self, vals):
        if not self.env.context.get('create_product_variant'):
            templates = self.mapped('product_ids.product_tmpl_id')
        res = super(Value, self).write(vals)
        if not self.env.context.get('create_product_variant'):
            templates += self.mapped('product_ids.product_tmpl_id')
            templates.clear_attribute_value_cache()
        return res

    @api.model
    def create(self, vals):
        res = super(Value, self).create(vals)
        if not self.env.context.get('create_product_variant'):
            res.mapped(
                'product_ids.product_tmpl_id').clear_attribute_value_cache()
        return res

    @api.multi
    def unlink(self):
        if not self.env.context.get('create_product_variant'):
            templates = self.mapped('product_ids.product_tmpl_id')
        res = super(Value, self).unlink()
        if not self.env.context.get('create_product_variant'):
            templates.clear_attribute_value_cache()
        return res
