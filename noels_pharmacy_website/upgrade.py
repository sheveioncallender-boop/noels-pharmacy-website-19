"""One-time, recoverable homepage redesign for the existing 2.0 storefront."""
from lxml import etree

from odoo.tools import file_open


REDESIGN_MARKER = 'noels_pharmacy_website.storefront_2_1_applied'


def apply_storefront_redesign(env):
    params = env['ir.config_parameter'].sudo()
    if params.get_param(REDESIGN_MARKER):
        return
    page = env.ref('noels_pharmacy_website.page_home', raise_if_not_found=False)
    if not page:
        return
    view = page.view_id.with_context(lang='en_US')
    # Keep the actual pre-upgrade architecture, including any editor changes.
    env['ir.ui.view'].create({
        'name': 'Noel’s homepage — backup before 2.1 redesign',
        'key': 'noels_pharmacy_website.home_before_2_1',
        'type': 'qweb', 'arch_db': view.arch_db,
        'website_id': view.website_id.id, 'active': False,
    })
    with file_open('noels_pharmacy_website/data/pages.xml', 'rb') as source:
        document = etree.parse(source)
    architecture = document.xpath('//record[@id="page_home"]/field[@name="arch"]/*')[0]
    view.write({'arch_db': etree.tostring(architecture, encoding='unicode')})
    # Correct only the original mismatched Wellness CTA. Preserve other page edits.
    wellness = env.ref('noels_pharmacy_website.page_wellness', raise_if_not_found=False)
    if wellness:
        wellness_view = wellness.view_id.with_context(lang='en_US')
        arch = etree.fromstring(wellness_view.arch_db.encode())
        links = arch.xpath('//section[contains(@class,"cta-section")]//a[@href="/shop"]')
        changed = False
        for link in links:
            if 'Visit & contact' in ''.join(link.itertext()):
                link.set('href', '/visit-noels')
                changed = True
        if changed:
            wellness_view.write({'arch_db': etree.tostring(arch, encoding='unicode')})
    params.set_param(REDESIGN_MARKER, True)
