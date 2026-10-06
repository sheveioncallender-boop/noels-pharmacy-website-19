from odoo import api, SUPERUSER_ID
from odoo.addons.noels_pharmacy_website.cleanup import retire_sample_catalogue


def migrate(cr, version):
    retire_sample_catalogue(api.Environment(cr, SUPERUSER_ID, {}))
