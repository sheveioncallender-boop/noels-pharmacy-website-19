from lxml import html

from odoo.tests import HttpCase, tagged
from odoo.addons.website_sale.tests.common import MockRequest
from ..hooks import post_init_hook
from ..cleanup import retire_sample_catalogue
from ..upgrade import apply_storefront_redesign, REDESIGN_MARKER


@tagged('post_install', '-at_install', 'noels_pharmacy')
class TestNoelsWebsite(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref('website.default_website')
        cls.website.write({'domain': False, 'ecommerce_access': 'everyone'})
        cls.category = cls.env.ref('noels_pharmacy_website.category_1')
        # Test-only products are rolled back by HttpCase, never installed as data.
        cls.products = cls.env['product.template'].create([
            {'name': 'Test catalogue product %s' % number, 'type': 'consu',
             'list_price': 25.0, 'sale_ok': True, 'is_storable': False,
             'is_published': True, 'website_id': cls.website.id,
             'public_categ_ids': [(6, 0, [cls.env.ref('noels_pharmacy_website.category_%s' % number).id])],
             'noels_homepage_featured': True}
            for number in range(1, 7)
        ])
        cls.product = cls.products[0]

    def test_seed_records_and_idempotent_setup(self):
        samples = self.env['product.template'].search([('noels_sample_product', '=', True)])
        self.assertEqual(len(samples), 0)
        self.assertFalse(self.website.noels_catalogue_notice)
        self.assertEqual(self.website.homepage_url, '/noels-home')
        menu_count = self.env['website.menu'].search_count([('website_id', '=', self.website.id)])
        self.product.list_price = 72.50
        post_init_hook(self.env)
        self.assertEqual(self.product.list_price, 72.50)
        self.assertEqual(self.env['website.menu'].search_count([('website_id', '=', self.website.id)]), menu_count)

    def test_publishing_and_website_isolation(self):
        public = self.website.with_user(self.website.user_id).with_context(website_id=self.website.id)
        with MockRequest(public.env, website=public):
            self.assertIn(self.product.id, public._noels_featured_products().ids)
            self.product.is_published = False
            self.assertNotIn(self.product.id, public._noels_featured_products().ids)
            self.product.is_published = True
            self.product.active = False
            self.assertNotIn(self.product.id, public._noels_featured_products().ids)
        other = self.env['website'].create({'name': 'Another store', 'company_id': self.website.company_id.id, 'noels_brand_enabled': True})
        other_public = other.with_user(other.user_id).with_context(website_id=other.id)
        with MockRequest(other_public.env, website=other_public):
            self.assertNotIn(self.category.id, other_public._noels_categories().ids)
            self.assertNotIn(self.product.id, other_public._noels_featured_products().ids)

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
        for path in ['/', '/pharmacy-services', '/wellness', '/about-noels', '/visit-noels', '/shop', self.product.website_url]:
            with self.subTest(path=path):
                response = self.url_open(path, timeout=60)
                self.assertEqual(response.status_code, 200, response.text[:1000])
                document = html.fromstring(response.content)
                self.assertEqual(len(document.xpath('//header[@id="top"]')), 1)
                self.assertTrue(document.xpath('//header//a[@href="/shop/cart"]'))
                self.assertFalse(document.xpath('//header//button[contains(@class,"menu-toggle")]'))
                self.assertTrue(document.xpath('//header//*[contains(concat(" ", @class, " "), " noels-topbar ")]'))
        home = html.fromstring(self.url_open('/').content)
        self.assertFalse(home.xpath('//*[contains(@class,"noels-catalogue-notice") or contains(@class,"noels-sample-badge")]'))
        self.assertEqual(len(home.xpath('//a[contains(@class,"noels-category")]')), 6)
        self.assertEqual(len(home.xpath('//div[contains(concat(" ",@class," ")," banner-slide ")]')), 3)

    def test_native_cart_and_checkout(self):
        self.url_open('/')  # Establish the standard Odoo visitor/session.
        result = self.make_jsonrpc_request('/shop/cart/add', {
            'product_template_id': self.product.id,
            'product_id': self.product.product_variant_id.id,
            'quantity': 2,
        }, timeout=60)
        self.assertEqual(result['quantity'], 2)
        cart = self.url_open('/shop/cart', timeout=60)
        self.assertEqual(cart.status_code, 200)
        self.assertIn(self.product.name, html.fromstring(cart.content).text_content())
        checkout = self.url_open('/shop/checkout', timeout=60)
        self.assertEqual(checkout.status_code, 200)
        self.assertNotIn('Traceback', checkout.text)

    def test_live_merchandising_empty_publish_and_unpublish(self):
        self.env['product.template'].search([('is_published', '=', True)]).write({'is_published': False})
        self.products.noels_homepage_featured = False
        self.category.noels_homepage_featured = False

        def home():
            response = self.url_open('/', timeout=60)
            self.assertEqual(response.status_code, 200)
            return html.fromstring(response.content)

        def by_class(document, name):
            return document.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " %s ")]' % name)

        empty = home()
        self.assertEqual(len(by_class(empty, 'noels-featured-section')), 1)
        self.assertEqual(len(by_class(empty, 'noels-product-placeholder')), 4)
        self.assertEqual(len(by_class(empty, 'noels-promo-card')), 2)
        self.assertEqual(len(by_class(empty, 'noels-promo-lifestyle')), 2)
        self.assertFalse(by_class(empty, 'noels-product-card'))
        self.assertFalse(by_class(empty, 'noels-product-price'))

        # Normal Odoo publication is enough: no extra homepage checkbox required.
        self.product.is_published = True
        published = home()
        cards = by_class(published, 'noels-product-card')
        self.assertEqual(len(cards), 1)
        self.assertIn(self.product.name, cards[0].text_content())
        self.assertFalse(by_class(published, 'noels-product-placeholder'))
        self.assertEqual(len(by_class(published, 'noels-category')), 1)
        promos = by_class(published, 'noels-promo-card')
        self.assertEqual(len(promos), 2)
        self.assertEqual(promos[0].get('href'), self.product.website_url)
        self.assertEqual(len(by_class(published, 'noels-promo-lifestyle')), 1)

        self.product.is_published = False
        unpublished = home()
        self.assertEqual(len(by_class(unpublished, 'noels-product-placeholder')), 4)
        self.assertEqual(len(by_class(unpublished, 'noels-promo-card')), 2)
        self.assertNotIn(self.product.name, unpublished.text_content())

        self.website.ecommerce_access = 'logged_in'
        private = home()
        self.assertFalse(by_class(private, 'noels-featured-section'))
        self.assertFalse(by_class(private, 'noels-promo-card'))

    def test_company_phone_and_desktop_cart_order(self):
        self.website.company_id.phone = '+1 868 555 0199'
        page = html.fromstring(self.url_open('/').content)
        self.assertTrue(page.xpath('//header//a[@href="tel:+1 868 555 0199"]'))
        self.assertNotIn('555-555-5556', page.xpath('//header')[0].text_content())
        desktop_cart = page.xpath('//*[@id="o_main_nav"]//*[contains(concat(" ", @class, " "), " o_wsale_my_cart ")]')
        self.assertEqual(len(desktop_cart), 1)
        self.assertTrue(desktop_cart[0].xpath('preceding-sibling::*'))
        self.assertEqual(page.xpath('//*[contains(concat(" ", @class, " "), " noels-home ")]')[0].get('id'), 'wrap')

    def test_redesign_upgrade_preserves_catalogue_and_other_pages(self):
        home = self.env.ref('noels_pharmacy_website.page_home').view_id.with_context(lang='en_US')
        about = self.env.ref('noels_pharmacy_website.page_about').view_id.with_context(lang='en_US')
        old = '<t t-name="noels_pharmacy_website.page_home"><t t-call="website.layout"><div id="wrap">Existing homepage edit</div></t></t>'
        home.arch_db = old
        about_before = about.arch_db
        self.product.list_price = 72.50
        self.product.is_published = False
        self.env['ir.config_parameter'].sudo().set_param(REDESIGN_MARKER, False)
        apply_storefront_redesign(self.env)
        self.assertIn('noels-home', home.arch_db)
        backup = self.env['ir.ui.view'].with_context(active_test=False).search([
            ('key', '=', 'noels_pharmacy_website.home_before_2_1'),
        ], limit=1)
        self.assertTrue(backup)
        self.assertFalse(backup.active)
        self.assertIn('Existing homepage edit', backup.arch_db)
        self.assertEqual(about.arch_db, about_before)
        self.assertEqual(self.product.list_price, 72.50)
        self.assertFalse(self.product.is_published)
        home.arch_db = old
        apply_storefront_redesign(self.env)
        self.assertIn('Existing homepage edit', home.arch_db)

    def test_frontend_asset_compilation(self):
        page = html.fromstring(self.url_open('/').content)
        assets = [href for href in page.xpath('//link[@rel="stylesheet"]/@href')
                  if '/web/assets/' in href]
        self.assertTrue(assets)
        for href in assets:
            response = self.url_open(href, timeout=120)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('style compilation failed', response.text.lower())
            self.assertNotIn('sass.compileerror', response.text.lower())


    def test_retire_samples_preserves_real_products_and_order_lines(self):
        sample = self.product.copy({'name': 'Old module sample', 'noels_sample_product': True,
                                    'noels_homepage_featured': True, 'is_published': True})
        self.env['ir.model.data'].create({'module': 'noels_pharmacy_website',
            'name': 'sample_vanicream_daily', 'model': 'product.template',
            'res_id': sample.id, 'noupdate': True})
        # An unrelated record marked as a sample is outside this module's ownership.
        unrelated = self.product.copy({'noels_sample_product': True, 'is_published': True})
        order = self.env['sale.order'].create({'partner_id': self.env.user.partner_id.id,
            'order_line': [(0, 0, {'product_id': sample.product_variant_id.id,
                                  'product_uom_qty': 1, 'price_unit': 25})]})
        self.website.noels_catalogue_notice = True
        retire_sample_catalogue(self.env)
        retire_sample_catalogue(self.env)  # Safe to repeat.
        self.assertFalse(sample.active or sample.is_published or sample.noels_homepage_featured)
        self.assertTrue(self.product.active and self.product.is_published)
        self.assertTrue(unrelated.active and unrelated.is_published)
        self.assertEqual(order.order_line.product_id, sample.with_context(active_test=False).product_variant_ids)
        self.assertFalse(self.website.noels_catalogue_notice)
