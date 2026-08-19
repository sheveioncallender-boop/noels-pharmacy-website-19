from odoo import fields, models


class NoelsBrand(models.Model):
    _name = "noels.brand"
    _description = "Noel's Product Brand"
    _order = "sequence, name"
    _inherit = ["website.published.mixin"]

    name = fields.Char(required=True, translate=True, index=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    image_1920 = fields.Image(string="Brand logo", max_width=1920, max_height=1920)
    description = fields.Html(translate=True, sanitize=True)
    website_id = fields.Many2one("website", ondelete="cascade")
    product_ids = fields.One2many("product.template", "noels_brand_id", string="Products")

    def _compute_website_url(self):
        for brand in self:
            brand.website_url = f"/brands/{brand.id}"


class ProductTemplate(models.Model):
    _inherit = "product.template"

    noels_brand_id = fields.Many2one(
        "noels.brand",
        string="Website brand",
        ondelete="set null",
        index=True,
    )
