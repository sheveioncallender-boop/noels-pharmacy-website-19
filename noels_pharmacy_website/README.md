# Noel's Pharmacy Website & eCommerce — Odoo 19

This single folder is the complete installable Odoo addon for **Noel's Pharmacy & Wellness Center Ltd.** It is ready to place directly in a GitHub repository connected to Cloudpepper.

## What is included

- Premium responsive website, photographic homepage carousel, header and footer
- Official Noel's logo, favicon and Odoo app icon
- Odoo-native product publishing, catalogue search, product pages, cart and checkout
- Homepage product/category sections populated from published Odoo products
- Prescription request form with secure PDF/JPG/PNG uploads and staff workflow
- Customer portal prescription history
- Contact requests, brand directory and configurable website details
- Wellness, services, About, Contact, FAQ, delivery, privacy and terms pages
- Responsive styling for desktop, tablet and mobile

## GitHub: drag-and-drop setup

1. Extract the supplied ZIP.
2. Open your GitHub repository and choose **Add file → Upload files**.
3. Drag this entire `noels_pharmacy_website` folder into the repository root.
4. Commit the upload.

The folder name must remain exactly `noels_pharmacy_website`. Do not upload only the ZIP and do not put this addon inside a second wrapper folder.

## Cloudpepper deployment

1. Connect the GitHub repository and branch in Cloudpepper.
2. Pull or deploy the latest commit, then restart Odoo if requested.
3. Enable Developer Mode in Odoo.
4. Open **Apps → Update Apps List**.
5. Search for **Noel's Pharmacy Website & eCommerce** and install it.
6. Hard-refresh the browser with `Ctrl + F5`.

See `CLOUDPEPPER_DEPLOYMENT.md` and `INSTALLATION.md` in this folder for the full setup checklist.

## Business details included

- 55 Rodney Road, Endeavour, Chaguanas
- Landline: 610-NOEL / 610-6635
- WhatsApp: 750-NOEL / 750-6635

Opening hours, public email, staff notification email and delivery settings are configurable after installation from **Noel's Online → Configuration → Website Settings**. This opens Odoo's normal Settings screen; Noel's options are integrated into the **Website** section without hiding the other Odoo settings.

## Technical notes

- Odoo version: 19.0
- Addon version: 19.0.1.2.0
- License: LGPL-3.0-or-later
- Required standard apps: Website, eCommerce, Portal, Discuss/Mail and Contacts

Odoo remains the source of truth for products, categories, prices, variants, stock rules, cart, checkout, payments and customer orders. Publishing a product in Odoo makes it available to the website automatically.
