from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    noels_store_phone = fields.Char(
        related="website_id.noels_store_phone",
        readonly=False,
    )
    noels_whatsapp_number = fields.Char(
        related="website_id.noels_whatsapp_number",
        readonly=False,
    )
    noels_whatsapp_display = fields.Char(
        related="website_id.noels_whatsapp_display",
        readonly=False,
    )
    noels_store_address = fields.Char(
        related="website_id.noels_store_address",
        readonly=False,
    )
    noels_opening_hours = fields.Char(
        related="website_id.noels_opening_hours",
        readonly=False,
    )
    noels_public_email = fields.Char(
        related="website_id.noels_public_email",
        readonly=False,
    )
    noels_notification_email = fields.Char(
        related="website_id.noels_notification_email",
        readonly=False,
    )
    noels_delivery_threshold = fields.Monetary(
        related="website_id.noels_delivery_threshold",
        readonly=False,
        currency_field="company_currency_id",
    )

