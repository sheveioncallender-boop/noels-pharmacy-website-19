"""Exercise a real 2.1.0 database upgrade to the sample-free storefront."""
import os

home = env.ref('noels_pharmacy_website.page_home').view_id.with_context(lang='en_US')
product = env.ref('noels_pharmacy_website.sample_vanicream_daily')
about = env.ref('noels_pharmacy_website.page_about').view_id.with_context(lang='en_US')
website = env.ref('website.default_website')
params = env['ir.config_parameter'].sudo()
phase = os.environ['NOELS_UPGRADE_PHASE']
if phase == 'before':
    home.arch_db = home.arch_db.replace('Care you trust.', 'Keep this homepage edit.')
    product.write({'list_price': 72.50, 'is_published': True})
    real = env['product.template'].create({'name': 'Real catalogue item', 'type': 'consu',
        'list_price': 99, 'sale_ok': True, 'is_published': True, 'website_id': website.id,
        'noels_homepage_featured': True})
    order = env['sale.order'].create({'partner_id': env.user.partner_id.id,
        'order_line': [(0, 0, {'product_id': product.product_variant_id.id,
                              'product_uom_qty': 1, 'price_unit': 72.50})]})
    website.noels_catalogue_notice = True
    params.set_param('noels_test.home_before', home.arch_db)
    params.set_param('noels_test.about_before', about.arch_db)
    params.set_param('noels_test.real_id', real.id)
    params.set_param('noels_test.order_id', order.id)
    params.set_param('noels_test.product_count', env['product.template'].with_context(active_test=False).search_count([]))
    env.cr.commit()
elif phase == 'after':
    assert home.arch_db == params.get_param('noels_test.home_before')
    assert about.arch_db == params.get_param('noels_test.about_before')
    assert product.list_price == 72.50 and not product.is_published and not product.active
    samples = env['product.template'].with_context(active_test=False).search([('noels_sample_product', '=', True)])
    assert len(samples) == 12 and not any(p.active or p.is_published for p in samples)
    real = env['product.template'].browse(int(params.get_param('noels_test.real_id')))
    assert real.active and real.is_published and real.list_price == 99
    order = env['sale.order'].browse(int(params.get_param('noels_test.order_id')))
    assert order.order_line.product_id.product_tmpl_id == product
    assert env['product.template'].with_context(active_test=False).search_count([]) == int(params.get_param('noels_test.product_count'))
    assert not website.noels_catalogue_notice
    assert website.noels_public_phone == '+1 868 750-6635'
    assert website.noels_public_address == '38, Chaguanas\nTrinidad & Tobago'
    layout = env.ref('noels_pharmacy_website.layout_brand').arch_db
    assert 'noels-catalogue-notice' not in layout
    print('PASS: 2.1.0 upgrade archives all 12 samples, removes notice, preserves real products, orders and edited pages.')
else:
    raise ValueError(phase)
