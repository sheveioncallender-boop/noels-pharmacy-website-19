from odoo import _, api, fields, models


class NoelsContactRequest(models.Model):
    _name = "noels.contact.request"
    _description = "Website Contact Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc, id desc"

    name = fields.Char(
        string="Reference",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("New"),
        index=True,
    )
    state = fields.Selection(
        [("new", "New"), ("in_progress", "In progress"), ("done", "Resolved")],
        default="new",
        required=True,
        tracking=True,
    )
    customer_name = fields.Char(required=True, tracking=True)
    phone = fields.Char(required=True, tracking=True)
    email = fields.Char(tracking=True)
    subject = fields.Char(required=True, tracking=True)
    message = fields.Text(required=True)
    website_id = fields.Many2one("website", required=True, ondelete="restrict")
    company_id = fields.Many2one(
        "res.company",
        related="website_id.company_id",
        store=True,
        readonly=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "noels.contact.request"
                ) or _("New")
        return super().create(vals_list)

    def action_start(self):
        self.write({"state": "in_progress"})

    def action_done(self):
        self.write({"state": "done"})

