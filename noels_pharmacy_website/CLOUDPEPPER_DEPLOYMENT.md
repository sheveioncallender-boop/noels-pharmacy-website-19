# GitHub and Cloudpepper Deployment

## Required repository layout

Your GitHub repository root should contain this folder directly:

```text
noels_pharmacy_website/
  __manifest__.py
  controllers/
  data/
  models/
  security/
  static/
  views/
```

The README and deployment documents inside the addon are safe for Odoo and should remain in the folder.

## First deployment

1. Extract the delivery ZIP. It produces one folder named `noels_pharmacy_website`.
2. Drag that folder into the root of the GitHub repository and commit it.
3. In Cloudpepper, connect the repository and intended branch.
4. Pull/deploy the latest commit.
5. Restart the Odoo service if Cloudpepper requests it.
6. In Odoo Developer Mode, open **Apps → Update Apps List**.
7. Install **Noel's Pharmacy Website & eCommerce**.
8. Hard-refresh the website with `Ctrl + F5`.

## Updating later

Keep the same repository and technical folder name. Replace or update the files in `noels_pharmacy_website`, commit, deploy through Cloudpepper, restart Odoo, update the Apps List and click **Upgrade** on the installed module.

Do not install a second copy under another folder name.

## Rollback

Keep a current database and filestore backup before production changes. To roll back, deploy the last known-good Git commit, restart Odoo and upgrade the same installed module.
