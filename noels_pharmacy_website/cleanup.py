"""Retire only module-owned sample products, keeping order references valid."""
SAMPLE_XMLIDS = ('sample_vanicream_daily', 'sample_vanicream_cream', 'sample_olay_body', 'sample_eos_lotion', 'sample_ogx_mist', 'sample_ogx_shampoo', 'sample_olly_softgels', 'sample_olly_gummies', 'sample_johnsons_shampoo', 'sample_venus_razor', 'sample_dove_spray', 'sample_burts_lip')


def retire_sample_catalogue(env):
    products = env['product.template'].with_context(active_test=False).browse()
    for name in SAMPLE_XMLIDS:
        product = env.ref('noels_pharmacy_website.' + name, raise_if_not_found=False)
        if product and product.exists() and product.noels_sample_product:
            products |= product
    products.write({'is_published': False, 'active': False, 'noels_homepage_featured': False})
    env['website'].search([('noels_catalogue_notice', '=', True)]).write({'noels_catalogue_notice': False})
