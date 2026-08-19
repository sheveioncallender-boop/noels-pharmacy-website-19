from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    noels_store_phone = fields.Char(
        string="Store phone",
        default="610-6635",
    )
    noels_whatsapp_number = fields.Char(
        string="WhatsApp number",
        default="18687506635",
        help="Use the full international number without spaces or punctuation.",
    )
    noels_whatsapp_display = fields.Char(
        string="WhatsApp display number",
        default="750-6635",
    )
    noels_store_address = fields.Char(
        string="Store address",
        default="55 Rodney Road, Endeavour, Chaguanas",
    )
    noels_opening_hours = fields.Char(
        string="Opening hours",
        default="Opening hours coming soon",
    )
    noels_public_email = fields.Char(string="Public email")
    noels_notification_email = fields.Char(
        string="Prescription notification email",
        help="New prescription and contact requests are sent here. If empty, the company email is used.",
    )
    noels_delivery_threshold = fields.Monetary(
        string="Free delivery threshold",
        currency_field="noels_company_currency_id",
        default=300.0,
    )
    noels_company_currency_id = fields.Many2one(
        related="company_id.currency_id",
        readonly=True,
    )
