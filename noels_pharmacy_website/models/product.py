from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    noels_homepage_featured = fields.Boolean(
        'Prioritise on Noel’s homepage', copy=False,
        help='Optional: show this product first. Published products appear automatically.')
    noels_sample_product = fields.Boolean('Noel’s sample product', copy=False)
    noels_sample_source_url = fields.Char('Sample reference', copy=False)


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    noels_homepage_featured = fields.Boolean(
        'Prioritise in homepage categories', copy=False,
        help='Optional: show this category first. Categories with published products appear automatically.')
