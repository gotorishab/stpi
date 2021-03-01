# -*- coding: utf-8 -*-
{
    'name': "Exit / Transfer Management",
    'summary': """ Manage employee exit transfer data""",
    'description': "Group Category 'Exit or Transfer'",
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Hrms',
    'version': '12.0.1',
    'depends': ['base',"mail",],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/mail_template.xml',
        'views/exit_transfer_views.xml',
        'views/print_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}