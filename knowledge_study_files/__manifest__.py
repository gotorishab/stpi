# -*- coding: utf-8 -*-
# Part of Synconics. See LICENSE file for full copyright and licensing details.

{
    'name': 'Portal Documents',
    'version': '1.0',
    'category': 'System',
    'depends': ['portal'],
    'description': """ Portal Documents """,
    "data": [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/maintenance.xml',
        'views/portal_document.xml',
    ],
    'currency': 'EUR',
    'demo': [],
    'installable': True,
}