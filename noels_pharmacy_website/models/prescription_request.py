from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class NoelsPrescriptionRequest(models.Model):
    _name = "noels.prescription.request"
    _description = "Online Prescription Request"
    _inherit = ["mail.thread", "mail.activity.mixin", "portal.mixin"]
    _order = "submitted_at desc, id desc"
    _rec_name = "name"

    name = fields.Char(
        string="Request number",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("New"),
        tracking=True,
        index=True,
    )
    state = fields.Selection(
        [
            ("submitted", "Submitted"),
            ("review", "Under pharmacist review"),
            ("clarification", "Needs clarification"),
            ("approved", "Approved for fulfilment"),
            ("ready", "Ready"),
            ("completed", "Completed"),
            ("declined", "Unable to fulfil"),
            ("cancelled", "Cancelled"),
        ],
        default="submitted",
        required=True,
        tracking=True,
        index=True,
    )
    patient_name = fields.Char(required=True, tracking=True, index=True)
    partner_id = fields.Many2one("res.partner", string="Linked customer", tracking=True)
    date_of_birth = fields.Date(required=True)
    mobile = fields.Char(required=True, tracking=True)
    email = fields.Char(tracking=True)
    doctor_name = fields.Char(tracking=True)
    prescription_date = fields.Date()
    notes = fields.Text(string="Customer notes")
    fulfillment = fields.Selection(
        [("pickup", "Store pickup"), ("delivery", "Delivery")],
        required=True,
        default="pickup",
        tracking=True,
    )
    delivery_address = fields.Text()
    attachment_ids = fields.Many2many(
        "ir.attachment",
        "noels_prescription_attachment_rel",
        "request_id",
        "attachment_id",
        string="Prescription files",
        copy=False,
    )
    consent = fields.Boolean(
        string="Privacy and pharmacist-review consent",
        required=True,
    )
    internal_notes = fields.Html(sanitize=True)
    submitted_at = fields.Datetime(default=fields.Datetime.now, required=True, readonly=True)
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
                    "noels.prescription.request"
                ) or _("New")
        return super().create(vals_list)

    @api.constrains("date_of_birth", "prescription_date")
    def _check_dates(self):
        today = date.today()
        for record in self:
            if record.date_of_birth and record.date_of_birth > today:
                raise ValidationError(_("Date of birth cannot be in the future."))
            if record.prescription_date and record.prescription_date > today:
                raise ValidationError(_("Prescription date cannot be in the future."))

    @api.constrains("consent")
    def _check_consent(self):
        if any(not record.consent for record in self):
            raise ValidationError(_("Consent is required for an online prescription request."))

    def action_review(self):
        self.write({"state": "review"})

    def action_approve(self):
        self.write({"state": "approved"})

    def action_ready(self):
        self.write({"state": "ready"})

    def action_complete(self):
        self.write({"state": "completed"})

    def action_decline(self):
        self.write({"state": "declined"})

    def _compute_access_url(self):
        super()._compute_access_url()
        for record in self:
            record.access_url = f"/my/prescriptions/{record.id}"

