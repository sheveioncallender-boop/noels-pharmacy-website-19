from lxml import html

from odoo.tests import HttpCase, tagged
from odoo.addons.website_sale.tests.common import MockRequest
from ..hooks import post_init_hook


@tagged('post_install', '-at_install', 'noels_pharmacy')
class TestNoelsWebsite(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref('website.default_website')
        cls.website.write({'domain': False, 'ecommerce_access': 'everyone'})
        cls.sample = cls.env.ref('noels_pharmacy_website.sample_vanicream_daily')
        cls.category = cls.env.ref('noels_pharmacy_website.category_1')

    def test_seed_records_and_idempotent_setup(self):
        samples = self.env['product.template'].search([('noels_sample_product', '=', True)])
        self.assertEqual(len(samples), 12)
        self.assertTrue(all(p.image_1920 and p.website_description and p.public_categ_ids for p in samples))
        self.assertEqual(self.website.homepage_url, '/noels-home')
        menu_count = self.env['website.menu'].search_count([('website_id', '=', self.website.id)])
        self.sample.list_price = 72.50
        post_init_hook(self.env)
        self.assertEqual(self.sample.list_price, 72.50)
        self.assertEqual(self.env['website.menu'].search_count([('website_id', '=', self.website.id)]), menu_count)

    def test_publishing_and_website_isolation(self):
        public = self.website.with_user(self.website.user_id).with_context(website_id=self.website.id)
        with MockRequest(public.env, website=public):
            self.assertIn(self.sample.id, public._noels_featured_products().ids)
            self.sample.is_published = False
            self.assertNotIn(self.sample.id, public._noels_featured_products().ids)
            self.sample.is_published = True
            self.sample.active = False
            self.assertNotIn(self.sample.id, public._noels_featured_products().ids)
        other = self.env['website'].create({'name': 'Another store', 'company_id': self.website.company_id.id, 'noels_brand_enabled': True})
        other_public = other.with_user(other.user_id).with_context(website_id=other.id)
        with MockRequest(other_public.env, website=other_public):
            self.assertNotIn(self.category.id, other_public._noels_categories().ids)
            self.assertNotIn(self.sample.id, other_public._noels_featured_products().ids)

    def test_empty_categories_and_private_shop(self):
        public = self.website.with_user(self.website.user_id).with_context(website_id=self.website.id)
        self.category.product_tmpl_ids.write({'is_published': False})
        with MockRequest(public.env, website=public):
            self.assertNotIn(self.category.id, public._noels_categories().ids)
            self.assertFalse(public._noels_promo_product('category_1'))
        self.website.ecommerce_access = 'logged_in'
        with MockRequest(public.env, website=public):
            self.assertFalse(public._noels_featured_products())
            self.assertFalse(public._noels_categories())

    def test_pages_header_and_native_shop(self):
        for path in ['/', '/pharmacy-services', '/wellness', '/about-noels', '/visit-noels', '/shop', self.sample.website_url]:
            with self.subTest(path=path):
                response = self.url_open(path, timeout=60)
                self.assertEqual(response.status_code, 200, response.text[:1000])
                document = html.fromstring(response.content)
                self.assertEqual(len(document.xpath('//header[@id="top"]')), 1)
                self.assertTrue(document.xpath('//header//a[@href="/shop/cart"]'))
                self.assertFalse(document.xpath('//header//button[contains(@class,"menu-toggle")]'))
        home = html.fromstring(self.url_open('/').content)
        self.assertEqual(len(home.xpath('//a[contains(@class,"noels-category")]')), 6)
        self.assertEqual(len(home.xpath('//div[contains(concat(" ",@class," ")," banner-slide ")]')), 3)

    def test_native_cart_and_checkout(self):
        self.url_open('/')  # Establish the standard Odoo visitor/session.
        result = self.make_jsonrpc_request('/shop/cart/add', {
            'product_template_id': self.sample.id,
            'product_id': self.sample.product_variant_id.id,
            'quantity': 2,
        }, timeout=60)
        self.assertEqual(result['quantity'], 2)
        cart = self.url_open('/shop/cart', timeout=60)
        self.assertEqual(cart.status_code, 200)
        self.assertIn(self.sample.name, html.fromstring(cart.content).text_content())
        checkout = self.url_open('/shop/checkout', timeout=60)
        self.assertEqual(checkout.status_code, 200)
        self.assertNotIn('Traceback', checkout.text)
