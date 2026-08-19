import base64
import mimetypes
import os
import re
import logging

from werkzeug.utils import secure_filename

from odoo import _, fields, http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
ALLOWED_UPLOADS = {
    ".pdf": ("application/pdf", b"%PDF-"),
    ".png": ("image/png", b"\x89PNG\r\n\x1a\n"),
    ".jpg": ("image/jpeg", b"\xff\xd8\xff"),
    ".jpeg": ("image/jpeg", b"\xff\xd8\xff"),
}
MAX_FILE_BYTES = 10 * 1024 * 1024
_logger = logging.getLogger(__name__)


class NoelsWebsite(http.Controller):
    def _base_values(self, **extra):
        website = request.website.sudo()
        values = {
            "noels_website": website,
            "noels_phone": website.noels_store_phone or "610-6635",
            "noels_whatsapp": website.noels_whatsapp_number or "18687506635",
            "noels_whatsapp_display": website.noels_whatsapp_display or "750-6635",
            "noels_address": website.noels_store_address
            or "55 Rodney Road, Endeavour, Chaguanas",
            "noels_hours": website.noels_opening_hours or _("Opening hours coming soon"),
            "noels_email": website.noels_public_email,
            "form_error": None,
            "contact_error": None,
            "form_data": {},
        }
        values.update(extra)
        return values

    @http.route("/wellness", type="http", auth="public", website=True, sitemap=True)
    def wellness(self, **kwargs):
        return request.render(
            "noels_pharmacy_website.page_wellness",
            self._base_values(),
        )

    @http.route("/pharmacy-services", type="http", auth="public", website=True, sitemap=True)
    def pharmacy_services(self, **kwargs):
        return request.render(
            "noels_pharmacy_website.page_pharmacy_services",
            self._base_values(),
        )

    @http.route("/about-us", type="http", auth="public", website=True, sitemap=True)
    def about(self, **kwargs):
        return request.render(
            "noels_pharmacy_website.page_about",
            self._base_values(),
        )

    @http.route("/faq", type="http", auth="public", website=True, sitemap=True)
    def faq(self, **kwargs):
        return request.render(
            "noels_pharmacy_website.page_faq",
            self._base_values(),
        )

    @http.route("/delivery-returns", type="http", auth="public", website=True, sitemap=True)
    def delivery_returns(self, **kwargs):
        return request.render(
            "noels_pharmacy_website.page_delivery_returns",
            self._base_values(),
        )

    @http.route("/privacy-policy", type="http", auth="public", website=True, sitemap=True)
    def privacy(self, **kwargs):
        return request.render(
            "noels_pharmacy_website.page_privacy",
            self._base_values(),
        )

    @http.route("/terms-conditions", type="http", auth="public", website=True, sitemap=True)
    def terms(self, **kwargs):
        return request.render(
            "noels_pharmacy_website.page_terms",
            self._base_values(),
        )

    @http.route("/brands", type="http", auth="public", website=True, sitemap=True)
    def brands(self, **kwargs):
        domain = [
            ("is_published", "=", True),
            "|",
            ("website_id", "=", False),
            ("website_id", "=", request.website.id),
        ]
        brands = request.env["noels.brand"].sudo().search(domain)
        return request.render(
            "noels_pharmacy_website.page_brands",
            self._base_values(brands=brands),
        )

    @http.route(
        "/brands/<model('noels.brand'):brand>",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def brand_detail(self, brand, **kwargs):
        brand = brand.sudo()
        if not brand.is_published or (
            brand.website_id and brand.website_id != request.website
        ):
            return request.not_found()
        products = request.env["product.template"].sudo().search(
            [
                ("noels_brand_id", "=", brand.id),
                ("is_published", "=", True),
                ("sale_ok", "=", True),
                "|",
                ("website_id", "=", False),
                ("website_id", "=", request.website.id),
            ],
            order="website_sequence asc, id desc",
        )
        return request.render(
            "noels_pharmacy_website.page_brand_detail",
            self._base_values(brand=brand, products=products),
        )

    @http.route(
        "/prescriptions",
        type="http",
        auth="public",
        website=True,
        methods=["GET", "POST"],
        sitemap=True,
    )
    def prescriptions(self, **post):
        if request.httprequest.method == "GET":
            return request.render(
                "noels_pharmacy_website.page_prescriptions",
                self._base_values(),
            )

        if post.get("website"):
            return request.redirect("/prescriptions")

        values, error = self._validate_prescription(post)
        if error:
            return request.render(
                "noels_pharmacy_website.page_prescriptions",
                self._base_values(form_error=error, form_data=post),
            )

        uploads = request.httprequest.files.getlist("prescription_files")
        upload_values, error = self._prepare_uploads(uploads)
        if error:
            return request.render(
                "noels_pharmacy_website.page_prescriptions",
                self._base_values(form_error=error, form_data=post),
            )

        public_user = request.website.user_id
        if request.env.user != public_user:
            values["partner_id"] = request.env.user.partner_id.id

        record = request.env["noels.prescription.request"].sudo().create(values)
        attachment_ids = []
        for upload in upload_values:
            attachment = request.env["ir.attachment"].sudo().create(
                {
                    "name": upload["name"],
                    "datas": base64.b64encode(upload["data"]),
                    "mimetype": upload["mimetype"],
                    "res_model": "noels.prescription.request",
                    "res_id": record.id,
                    "type": "binary",
                }
            )
            attachment_ids.append(attachment.id)
        record.sudo().write({"attachment_ids": [(6, 0, attachment_ids)]})
        self._queue_prescription_emails(record)

        return request.render(
            "noels_pharmacy_website.prescription_thank_you",
            self._base_values(prescription_request=record),
        )

    def _validate_prescription(self, post):
        required = {
            "patient_name": _("Patient name"),
            "date_of_birth": _("Date of birth"),
            "mobile": _("Mobile number"),
            "fulfillment": _("Fulfilment method"),
        }
        for key, label in required.items():
            if not (post.get(key) or "").strip():
                return {}, _("%s is required.") % label
        if post.get("fulfillment") not in {"pickup", "delivery"}:
            return {}, _("Select a valid fulfilment method.")
        if post.get("fulfillment") == "delivery" and not (
            post.get("delivery_address") or ""
        ).strip():
            return {}, _("A delivery address is required for delivery requests.")
        if not post.get("consent"):
            return {}, _("Please accept the privacy and pharmacist-review consent.")
        email = (post.get("email") or "").strip()
        if email and not EMAIL_RE.match(email):
            return {}, _("Enter a valid email address.")
        try:
            date_of_birth = fields.Date.to_date(post["date_of_birth"])
            prescription_date = fields.Date.to_date(post.get("prescription_date"))
        except (TypeError, ValueError):
            return {}, _("Enter valid dates.")
        values = {
            "patient_name": post["patient_name"].strip(),
            "date_of_birth": date_of_birth,
            "mobile": post["mobile"].strip(),
            "email": email,
            "doctor_name": (post.get("doctor_name") or "").strip(),
            "prescription_date": prescription_date,
            "notes": (post.get("notes") or "").strip(),
            "fulfillment": post["fulfillment"],
            "delivery_address": (post.get("delivery_address") or "").strip(),
            "consent": True,
            "website_id": request.website.id,
        }
        return values, None

    def _prepare_uploads(self, uploads):
        usable_uploads = [item for item in uploads if item and item.filename]
        if not usable_uploads:
            return [], _("Attach at least one prescription image or PDF.")
        if len(usable_uploads) > 5:
            return [], _("You can attach up to five files per request.")
        prepared = []
        for item in usable_uploads:
            filename = secure_filename(os.path.basename(item.filename))
            extension = os.path.splitext(filename)[1].lower()
            if extension not in ALLOWED_UPLOADS:
                return [], _("Only PDF, PNG, JPG and JPEG files are accepted.")
            data = item.read(MAX_FILE_BYTES + 1)
            if len(data) > MAX_FILE_BYTES:
                return [], _("Each prescription file must be 10 MB or smaller.")
            mimetype, magic = ALLOWED_UPLOADS[extension]
            if not data.startswith(magic):
                return [], _("One of the files does not match its file type.")
            prepared.append(
                {
                    "name": filename,
                    "data": data,
                    "mimetype": mimetypes.guess_type(filename)[0] or mimetype,
                }
            )
        return prepared, None

    def _queue_prescription_emails(self, record):
        try:
            if record.email:
                template = request.env.ref(
                    "noels_pharmacy_website.mail_template_prescription_customer",
                    raise_if_not_found=False,
                )
                if template:
                    template.sudo().send_mail(record.id, force_send=False)
            notify_email = (
                record.website_id.noels_notification_email or record.company_id.email
            )
            if notify_email:
                template = request.env.ref(
                    "noels_pharmacy_website.mail_template_prescription_staff",
                    raise_if_not_found=False,
                )
                if template:
                    template.sudo().with_context(
                        noels_notification_email=notify_email
                    ).send_mail(record.id, force_send=False)
        except Exception:
            _logger.exception("Could not queue email for prescription request %s", record.name)

    @http.route(
        "/contact-us",
        type="http",
        auth="public",
        website=True,
        methods=["GET", "POST"],
        sitemap=True,
    )
    def contact(self, **post):
        if request.httprequest.method == "GET":
            return request.render(
                "noels_pharmacy_website.page_contact",
                self._base_values(),
            )
        if post.get("website"):
            return request.redirect("/contact-us?sent=1")
        for key in ("customer_name", "phone", "subject", "message"):
            if not (post.get(key) or "").strip():
                return request.render(
                    "noels_pharmacy_website.page_contact",
                    self._base_values(
                        contact_error=_("Complete all required fields."),
                        form_data=post,
                    ),
                )
        email = (post.get("email") or "").strip()
        if email and not EMAIL_RE.match(email):
            return request.render(
                "noels_pharmacy_website.page_contact",
                self._base_values(
                    contact_error=_("Enter a valid email address."),
                    form_data=post,
                ),
            )
        record = request.env["noels.contact.request"].sudo().create(
            {
                "customer_name": post["customer_name"].strip(),
                "phone": post["phone"].strip(),
                "email": email,
                "subject": post["subject"].strip(),
                "message": post["message"].strip(),
                "website_id": request.website.id,
            }
        )
        notify_email = (
            record.website_id.noels_notification_email or record.company_id.email
        )
        if notify_email:
            try:
                template = request.env.ref(
                    "noels_pharmacy_website.mail_template_contact_staff",
                    raise_if_not_found=False,
                )
                if template:
                    template.sudo().with_context(
                        noels_notification_email=notify_email
                    ).send_mail(record.id, force_send=False)
            except Exception:
                _logger.exception("Could not queue email for website enquiry %s", record.name)
        return request.render(
            "noels_pharmacy_website.contact_thank_you",
            self._base_values(contact_request=record),
        )


class NoelsCustomerPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "noels_prescription_count" in counters:
            partner = request.env.user.partner_id.commercial_partner_id
            values["noels_prescription_count"] = (
                request.env["noels.prescription.request"]
                .sudo()
                .search_count(
                    [
                        ("partner_id.commercial_partner_id", "=", partner.id),
                        ("website_id", "=", request.website.id),
                    ]
                )
            )
        return values

    @http.route(
        ["/my/prescriptions", "/my/prescriptions/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_prescriptions(self, page=1, **kwargs):
        partner = request.env.user.partner_id.commercial_partner_id
        domain = [
            ("partner_id.commercial_partner_id", "=", partner.id),
            ("website_id", "=", request.website.id),
        ]
        model = request.env["noels.prescription.request"].sudo()
        total = model.search_count(domain)
        pager = portal_pager(
            url="/my/prescriptions",
            total=total,
            page=page,
            step=20,
        )
        prescriptions = model.search(
            domain,
            order="submitted_at desc, id desc",
            limit=20,
            offset=pager["offset"],
        )
        values = self._prepare_portal_layout_values()
        values.update(
            {
                "prescriptions": prescriptions,
                "page_name": "noels_prescriptions",
                "pager": pager,
            }
        )
        return request.render(
            "noels_pharmacy_website.portal_my_prescriptions",
            values,
        )

    @http.route(
        "/my/prescriptions/<int:request_id>",
        type="http",
        auth="user",
        website=True,
    )
    def portal_prescription_detail(self, request_id, **kwargs):
        record = request.env["noels.prescription.request"].sudo().browse(request_id)
        partner = request.env.user.partner_id.commercial_partner_id
        if (
            not record.exists()
            or record.partner_id.commercial_partner_id != partner
            or record.website_id != request.website
        ):
            return request.not_found()
        values = self._prepare_portal_layout_values()
        values.update(
            {
                "prescription": record,
                "page_name": "noels_prescription_detail",
            }
        )
        return request.render(
            "noels_pharmacy_website.portal_prescription_detail",
            values,
        )
