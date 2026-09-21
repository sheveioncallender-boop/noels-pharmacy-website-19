from odoo import SUPERUSER_ID, api
from odoo.addons.noels_pharmacy_website.upgrade import apply_storefront_redesign


def migrate(cr, version):
    apply_storefront_redesign(api.Environment(cr, SUPERUSER_ID, {}))
