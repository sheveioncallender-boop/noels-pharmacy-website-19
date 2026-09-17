# Noel’s Pharmacy — Odoo 19 Community

Fresh website and ecommerce module, version **19.0.2.0.0**, by **Spxcorp Limited**.

This edition replaces the previous repository implementation at the owner’s request. The earlier code remains available in Git history. **Install this edition on a fresh Odoo 19 database.** It is not an in-place migration of the earlier prescription-intake edition; the migration guard stops that incompatible upgrade before altering its business records.

## Included

- The approved blue/green design, Inter / Inter Tight fonts and supplied Noel’s logo.
- Three rotating photographic hero banners, manual controls, swipe and reduced-motion support.
- Home, Pharmacy Services, Wellness, About Noel’s, and Visit & Contact pages.
- Six circular categories linked to native Odoo ecommerce categories.
- Twelve sample products with photographs, descriptions, categories and test prices, using the requested FCP reference catalogue.
- Homepage product prices calculated by Odoo’s visitor pricelist and tax rules. Unpublished/archived products are excluded; empty categories disappear.
- Odoo’s existing desktop/mobile header, search, customer account, cart, product pages and checkout. This module does not replace their templates or controllers.
- One-time editable pages and sample catalogue records (`noupdate="1"`): later module upgrades preserve content edits, product prices and publication choices.
- Website settings for branding, opening hours, sample notice and bulk unpublishing the sample catalogue.

## Install on Cloudpepper or an Odoo server

1. Connect this repository and the `main` branch to your fresh Odoo **19 Community** instance, or put the `noels_pharmacy_website` folder in your custom addons directory.
2. Restart Odoo, enable developer mode, then choose **Apps → Update Apps List**.
3. Install **Noel’s Pharmacy — Website & Shop**. Odoo installs its standard ecommerce/stock dependencies automatically.
4. Open Website. The module sets the default website’s homepage and logo and adds its page menu entries. The native Shop menu remains in place.
5. Set your company’s real address, phone and email. Set opening hours in **Website → Configuration → Settings → Noel’s Pharmacy**.

CLI alternative:

```sh
odoo-bin -d YOUR_FRESH_DATABASE --addons-path=/path/to/odoo/addons,/path/to/this/repository -i noels_pharmacy_website --without-demo=True --stop-after-init
```

The module targets `website.default_website` on installation. It does not change every website in a multi-website database.

## Manage the shop normally in Odoo

- Edit products, images, prices, variants and publication from Odoo’s normal product screens. Enable **Featured on Noel’s homepage** on products you want in the homepage selection (up to eight, ordered by website sequence).
- Edit ecommerce categories, their image and sequence in Odoo. Enable **Featured on Noel’s homepage** for circle categories (up to twelve). A category needs a published product to appear to visitors.
- Edit the five marketing pages with the Website editor. Product cards and category circles come from the actual catalogue.
- Sample products are saleable Goods with inventory tracking disabled so you can test a cart without creating fictitious stock. For real inventory, enable native Track Inventory and receive the actual quantities in Odoo.
- Currency, taxes, payment providers, delivery methods, checkout policy and automatic invoices use your ordinary Odoo settings. No payment gateway or delivery service is fabricated by this module.
- The sample notice is enabled initially. Review/replace the sample catalogue and test prices, then disable the notice in Website settings. The **Unpublish sample products** button keeps those records and existing orders in the backend.

The fresh edition does not implement prescription uploads or a custom customer portal. Contact enquiries and customer orders use Odoo’s `/contactus` and `/my/orders` flows.

## Validation

`scripts/validate_module.py` checks XML against Odoo 19’s schema, QWeb expressions, Python/JavaScript syntax, SCSS compilation, local assets and the expected catalogue/page structure.

```sh
python -m pip install lxml Pillow libsass tinycss2
python scripts/validate_module.py --odoo-source /path/to/odoo19
```

The GitHub Actions workflow installs a pinned Odoo 19 revision with PostgreSQL, runs the module’s HTTP/cart/publication tests, and checks a subsequent upgrade. It uploads the Odoo logs even on failure. Review the Actions result for runtime test status; static checks alone do not establish successful installation.

Before taking live orders, test a product variant, cart quantity/removal, address entry, your configured delivery method, and a test-mode payment with your own provider. Confirm order and invoice behavior in Odoo.

## Assets and licence

Code: LGPL-3.0-or-later. Photographs are real stock photography; pictured people are not presented as Noel’s employees. Product identities and reference photographs come from the user-requested FCP catalogue for this sample store. Use authorised catalogue imagery and confirmed descriptions/prices for launch. Attribution and source URLs are in `ASSET_CREDITS.json`; font licences are included beside the fonts.
