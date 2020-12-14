# -*- coding: utf-8 -*-

{
    'name': 'GTS Switcher',
    'category': 'Tools',
    'version': '12.0.0.1',
    'summary': 'Lets switch instances ',
    'description': """ Lets switch instances """,
    'author': 'Geo Technosoft',
    'website': 'https://geotechnosoft.com',
    'sequence': 1,
    'depends': ['base','website'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_user_view.xml',
        'views/config_view.xml',
        'views/website_layout_view.xml',
        'views/res_company_view.xml',
    ],
    'qweb': [],
    'application': True
}
