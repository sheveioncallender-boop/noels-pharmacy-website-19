"""Run in odoo-bin shell after installing 2.0, and again after upgrading to 2.1."""
import os

home = env.ref('noels_pharmacy_website.page_home').view_id.with_context(lang='en_US')
product = env.ref('noels_pharmacy_website.sample_vanicream_daily')
about = env.ref('noels_pharmacy_website.page_about').view_id.with_context(lang='en_US')
params = env['ir.config_parameter'].sudo()
phase = os.environ['NOELS_UPGRADE_PHASE']
if phase == 'before':
    home.arch_db = home.arch_db.replace('For a healthier you.', 'Saved before the redesign.')
    product.write({'list_price': 72.50, 'is_published': False})
    params.set_param('noels_test.about_before', about.arch_db)
    params.set_param('noels_test.product_count', env['product.template'].search_count([]))
    env.cr.commit()
elif phase == 'after':
    assert 'noels-home' in home.arch_db
    assert 'Care you trust.' in home.arch_db
    backups = env['ir.ui.view'].with_context(active_test=False).search([
        ('key', '=', 'noels_pharmacy_website.home_before_2_1'),
    ])
    assert len(backups) == 1 and not backups.active
    assert 'Saved before the redesign.' in backups.arch_db
    assert product.list_price == 72.50 and not product.is_published
    assert about.arch_db == params.get_param('noels_test.about_before')
    assert env['product.template'].search_count([]) == int(params.get_param('noels_test.product_count'))
    print('PASS: actual 2.0-to-2.1 migration, homepage backup, catalogue and other pages preserved.')
else:
    raise ValueError(phase)
