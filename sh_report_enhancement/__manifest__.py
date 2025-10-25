# -*- coding: utf-8 -*-
# Part of Softhealer Technologies
{
    "name": "Report Enhancement",

    "author": "Softhealer Technologies",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "0.0.2",

    "category": "Document Management",

    "license": "OPL-1",

    "summary": "Manage Reports Manage Report With Header Manage Report With Footer Report Custom Header Report Custom Footer Document Management Report Template Manage Report With Header Footer Odoo ",

    "description": """This module enhances the documents/reports by adding a custom header and footer image in all odoo pdf reports. """,
    'depends': [
        'base',
        'base_setup',
        'web',
        'l10n_din5008'
    ],
    'data': [
        'views/report_base_layout.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "images": ["static/description/background.png", ],
    "price": 15,
    "currency": "EUR"
}
