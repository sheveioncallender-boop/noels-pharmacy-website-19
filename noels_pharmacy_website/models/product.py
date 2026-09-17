from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    noels_homepage_featured = fields.Boolean('Feature on Noel’s homepage', copy=False)
    noels_sample_product = fields.Boolean('Noel’s sample product', copy=False)
    noels_sample_source_url = fields.Char('Sample reference', copy=False)


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    noels_homepage_featured = fields.Boolean('Show in Noel’s category circles', copy=False)
