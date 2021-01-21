# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Forum Extended',
    'category': 'Website/Website',
    'sequence': 265,
    'summary': 'Create groups in forum',
    'version': '1.0',
    'description': """
Create groups in forum
        """,
    'website': 'https://www.odoo.com/page/community-builder',
    'depends': [
        'website_forum',
    ],
    'data': [
        'views/website_forum.xml',
    ],
    'qweb': [
        'static/src/xml/website_forum_templates.xml'
    ],
    'installable': True,
    'application': False,
}
