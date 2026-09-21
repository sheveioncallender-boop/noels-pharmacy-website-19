# Noel’s Pharmacy — Odoo 19 Community

Fresh website and ecommerce module, version **19.0.2.1.0**, by **Spxcorp Limited**.

This edition replaces the previous repository implementation at the owner’s request. The earlier code remains available in Git history. **Use a fresh Odoo 19 database when coming from the old prescription-intake edition. The 2.0 native storefront can be upgraded to 2.1 using the steps below.** It is not an in-place migration of the earlier prescription-intake edition; the migration guard stops that incompatible upgrade before altering its business records.

## Included

- The approved blue/green design, Inter / Inter Tight fonts and supplied Noel’s logo.
- Three rotating photographic hero banners, manual controls, swipe and reduced-motion support.
- Home, Pharmacy Services, Wellness, About Noel’s, and Visit & Contact pages.
- Six rounded category cards linked to native Odoo ecommerce categories.
- Twelve sample products with photographs, descriptions, categories and test prices, using the requested FCP reference catalogue.
- Homepage product prices calculated by Odoo’s visitor pricelist and tax rules. Unpublished/archived products are excluded; empty categories disappear.
- Odoo’s existing desktop/mobile header, search, customer account, cart, product pages and checkout. This module does not replace their templates or controllers.
- One-time editable pages and sample catalogue records (`noupdate="1"`). This 2.1 redesign updates the homepage once, with an inactive backup of its previous content; subsequent upgrades preserve editor changes. Product prices and publication choices remain unchanged.
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
- Edit ecommerce categories, their image and sequence in Odoo. Enable **Featured on Noel’s homepage** for category cards (up to twelve). A category needs a published product to appear to visitors.
- Edit the five marketing pages with the Website editor. Product cards and category cards come from the actual catalogue.
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

## Version 2.1 — Value Seekers design approach for Noel’s

- A blue announcement strip, white native Odoo header, and desktop order of logo,
  menu, search, sign-in/account and cart. Native mobile navigation is retained.
- Phone and opening hours come from Noel’s company/website settings. No Value
  Seekers number, invented contact details or default Odoo phone is inserted.
- Three HD photo banners use a white-to-photo layout, bold blue/green headlines
  and rounded buttons. The homepage has category cards, two product promotions,
  native-priced featured products and an about section. All five pages share
  the refreshed typography, rounded surfaces and spacing.
- Native shop, product options, cart, checkout, account and contact flows remain
  under Odoo. Product/category selections still honour website access and publication.
- Shared Community brand variables make the backend/editor toolbar blue as well.
  Page/header styling and header ordering are conditional on Noel’s branding;
  the shared backend brand colour applies database-wide.
- Original Noel’s logo, HD marketing photographs and sample catalogue are retained.
  Product images use Odoo’s image_1024 endpoint; larger uploads improve source quality.

### Upgrade an existing 2.0 storefront

1. Pull/redeploy the latest `main` branch and restart Odoo.
2. In Apps, Upgrade **Noel’s Pharmacy — Website & Shop**. Updating the Apps List
   alone does not apply the redesign.
3. Hard-refresh the website. The homepage route remains `/noels-home`.
4. The migration saves the previous homepage architecture as the inactive view
   **Noel’s homepage — backup before 2.1 redesign**, before installing the new layout.
   Product data, prices, publication, orders, menus and other page content are retained
   (apart from correcting the original Wellness contact button’s destination).
5. Check the company phone and website opening hours. Saved website-specific header
   customizations may override module views and should be reviewed individually.

The old prescription-intake edition remains protected by its existing migration
block. These steps apply to the 2.0 native storefront, not that earlier edition.

Validation covers real Odoo template inheritance, SCSS compilation and HTTP/cart
checks in CI. CI also installs the previous 2.0 release, changes a product and the
homepage, then verifies the 2.1 migration keeps those business settings and a
recoverable copy of the old homepage. The local visual preview could not be opened
in the available browser; no live customer instance has been changed or tested.
