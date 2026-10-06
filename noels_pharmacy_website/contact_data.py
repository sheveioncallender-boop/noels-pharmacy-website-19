"""Public store details supplied in the owner's Google listing screenshot."""


def apply_listing_details(env):
    website = env.ref('website.default_website')
    marker = 'noels_pharmacy_website.google_contact_2_1_3'
    params = env['ir.config_parameter'].sudo()
    if not website.noels_brand_enabled or params.get_param(marker):
        return
    # Keep public storefront details separate from the company's billing address.
    defaults = {
        'noels_public_phone': '+1 868 750-6635',
        'noels_public_address': '38, Chaguanas\nTrinidad & Tobago',
    }
    website.write({name: value for name, value in defaults.items() if not website[name]})
    params.set_param(marker, '1')
