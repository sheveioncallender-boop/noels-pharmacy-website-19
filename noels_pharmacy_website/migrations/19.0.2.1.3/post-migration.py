from odoo import api, SUPERUSER_ID
from odoo.addons.noels_pharmacy_website.contact_data import apply_listing_details


def migrate(cr, version):
    apply_listing_details(api.Environment(cr, SUPERUSER_ID, {}))
