from odoo import api, models


class WebsitePage(models.Model):
    _inherit = 'website.page'

    @api.model
    def _allow_to_use_cache(self, request):
        # Odoo's full-page public cache lasts an hour and does not vary by
        # catalogue publication or visitor pricelist. Render this commerce
        # homepage live; leave normal caching on the other marketing pages.
        page_info = self._get_page_info(request)
        if page_info:
            view = self.env['ir.ui.view'].browse(page_info['view_id'])
            if view.key == 'noels_pharmacy_website.page_home':
                return False
        return super()._allow_to_use_cache(request)
