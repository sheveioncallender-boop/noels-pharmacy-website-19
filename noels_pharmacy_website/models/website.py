from odoo import fields, models
from odoo.fields import Domain


class Website(models.Model):
    _inherit = 'website'

    noels_brand_enabled = fields.Boolean('Use Noel’s branding', default=False)
    noels_opening_hours = fields.Text('Opening hours', translate=True)
    noels_catalogue_notice = fields.Boolean('Show sample catalogue notice', default=False)

    def _noels_categories(self):
        """The same website/publication boundary as Odoo's normal category list."""
        self.ensure_one()
        Category = self.env['product.public.category'].with_context(website_id=self.id)
        if not self.noels_brand_enabled or not self.has_ecommerce_access():
            return Category.browse()
        return Category.search(Domain.AND([
            self.website_domain(),
            [('noels_homepage_featured', '=', True), ('has_published_products', '=', True)],
        ]), order='sequence, name, id', limit=12)

    def _noels_featured_products(self):
        self.ensure_one()
        Product = self.env['product.template'].with_context(website_id=self.id)
        if not self.noels_brand_enabled or not self.has_ecommerce_access():
            return Product.browse()
        # Explicit published/active predicates also apply when an editor previews the page.
        # No sudo: normal product/company/website access rules remain authoritative.
        return Product.search(Domain.AND([
            self.sale_product_domain(),
            [('active', '=', True), ('is_published', '=', True),
             ('noels_homepage_featured', '=', True)],
        ]), order='website_sequence, id', limit=8)

    def _noels_promo_product(self, category_xmlid):
        """Promotional cards disappear when their products are unpublished."""
        self.ensure_one()
        Product = self.env['product.template'].with_context(website_id=self.id)
        category = self.env.ref('noels_pharmacy_website.' + category_xmlid, raise_if_not_found=False)
        if not category or not self.noels_brand_enabled or not self.has_ecommerce_access():
            return Product.browse()
        return Product.search(Domain.AND([
            self.sale_product_domain(),
            [('active', '=', True), ('is_published', '=', True),
             ('public_categ_ids', 'child_of', category.id)],
        ]), order='website_sequence, id', limit=1)
