{
    'name': "Noel's Pharmacy — Website & Shop",
    'version': '19.0.2.0.0',
    'summary': 'Noel’s design, native Odoo eCommerce, circular categories and a sample catalogue',
    'category': 'Website/eCommerce',
    'author': 'Spxcorp Limited',
    'website': 'https://spxcorp.net',
    'license': 'LGPL-3',
    'depends': ['website_sale_stock'],
    'data': [
        'views/backend_views.xml',
        'views/layout.xml',
        'views/commerce_blocks.xml',
        'data/catalog.xml',
        'data/pages.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'noels_pharmacy_website/static/src/css/fonts.css',
            'noels_pharmacy_website/static/src/css/pages.scss',
            'noels_pharmacy_website/static/src/css/brand.scss',
            'noels_pharmacy_website/static/src/js/banner.js',
        ],
    },
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'installable': True,
    'application': True,
}
