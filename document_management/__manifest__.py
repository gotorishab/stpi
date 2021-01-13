# -*- coding: utf-8 -*-
# Part of Synconics. See LICENSE file for full copyright and licensing details.

{
    'name': 'Intranet Documents',
    'version': '1.0',
    'category': 'System',
    'depends': ['portal'],
    'description': """ Portal Documents """,
    "data": [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/document_list_view.xml',
        'views/portal_document.xml',
        # /forum/discussion-forum-4/ask
    ],
    'currency': 'EUR',
    'demo': [],
    'installable': True,
}