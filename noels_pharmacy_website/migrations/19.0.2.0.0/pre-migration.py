def migrate(cr, version):
    # This fresh storefront deliberately replaces the old repository implementation.
    # Its old prescription/contact models require a separate data migration, not
    # automatic removal as a side effect of a website redesign.
    cr.execute("""
        SELECT 1 FROM ir_model_data
        WHERE module = 'noels_pharmacy_website'
          AND name = 'page_wellness' AND model = 'ir.ui.view'
        LIMIT 1
    """)
    if cr.fetchone():
        raise RuntimeError(
            'Noel’s 2.0 is a fresh-install storefront. This database contains the '
            'earlier prescription-intake edition. Install the new storefront on '
            'a fresh staging database; migrate existing business records separately. '
            'The upgrade has been stopped before replacing those records.'
        )
