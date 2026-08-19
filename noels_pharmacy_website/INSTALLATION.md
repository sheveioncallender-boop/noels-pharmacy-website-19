# Installation and Launch Checklist

## 1. Install the addon

1. Deploy the `noels_pharmacy_website` folder through Cloudpepper.
2. Restart Odoo if prompted.
3. Enable Developer Mode.
4. Open **Apps → Update Apps List**.
5. Search for **Noel's Pharmacy Website & eCommerce** and click **Install**.

## 2. Configure staff access

Assign the appropriate user group to pharmacy staff:

- **Noel's Online User** — review and update online requests.
- **Noel's Online Manager** — user access plus configuration and deletion rights.

## 3. Complete store settings

Open **Noel's Online → Configuration → Website Settings** and set:

- opening hours;
- public and notification email addresses;
- store phone and WhatsApp details;
- store address;
- free-delivery threshold, if used.

The international WhatsApp value should use digits only, such as `18687506635`.

The menu opens Odoo's standard Settings screen. Noel's options appear under the **Website** app section, while General Settings, Users, Sales, Accounting and other installed-app settings remain available normally.

## 4. Publish products

Use Odoo's normal eCommerce product workflow. Add the product, images, price, variants, eCommerce categories and stock rules, then publish it on the website. Published products automatically become searchable in `/shop` and available to Noel's homepage product sections.

## 5. Configure eCommerce

Set the TTD pricelist and taxes, warehouse rules, payment providers, pickup/delivery methods, checkout policies, company details, domain and outgoing mail server through standard Odoo settings.

## 6. Test prescription intake

1. Set the staff notification email.
2. Submit a harmless PDF or image through `/prescriptions`.
3. Confirm the request appears under **Noel's Online → Prescription Requests**.
4. Confirm its sequential reference, attachments and acknowledgement email.
5. Test status changes and the signed-in customer route `/my/prescriptions`.

The form creates a review request; it does not promise approval, availability or dispensing.

## 7. Pre-launch review

- Confirm opening hours and contact email.
- Add official social profile links when available.
- Review the draft Privacy Policy and Terms & Conditions with Noel's advisers.
- Verify delivery areas, charges and return policy.
- Test payment, checkout, email and mobile layouts on the production domain.
