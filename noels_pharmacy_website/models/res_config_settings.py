from odoo import fields, models
from odoo.exceptions import AccessError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    noels_brand_enabled = fields.Boolean(related='website_id.noels_brand_enabled', readonly=False)
    noels_opening_hours = fields.Text(related='website_id.noels_opening_hours', readonly=False)
    noels_catalogue_notice = fields.Boolean(related='website_id.noels_catalogue_notice', readonly=False)

    def action_noels_unpublish_samples(self):
        self.ensure_one()
        if not self.env.user.has_group('website.group_website_designer'):
            raise AccessError(self.env._('Only website designers may manage the sample catalogue.'))
        products = self.env['product.template'].search([
            ('noels_sample_product', '=', True),
            ('website_id', '=', self.website_id.id),
        ])
        products.write({'is_published': False})
        return {'type': 'ir.actions.client', 'tag': 'display_notification', 'params': {
            'title': self.env._('Sample catalogue unpublished'),
            'message': self.env._('Sample products remain available in the backend. Real products and orders are unchanged.'),
            'type': 'success', 'sticky': False,
        }}
