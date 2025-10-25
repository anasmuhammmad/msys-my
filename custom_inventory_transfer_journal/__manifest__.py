{
    'name': 'Internal Transfer Accounting Entries',
    'version': '17.0.1.0.0',
    'summary': 'Generates journal entries for internal transfers in inventory',
    'category': 'Accounting',
    'author': 'Your Name',
    'license': 'AGPL-3',
    'depends': ['stock', 'account'],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
}
