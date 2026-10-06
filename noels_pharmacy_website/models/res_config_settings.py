from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    noels_brand_enabled = fields.Boolean(related='website_id.noels_brand_enabled', readonly=False)
    noels_opening_hours = fields.Text(related='website_id.noels_opening_hours', readonly=False)
