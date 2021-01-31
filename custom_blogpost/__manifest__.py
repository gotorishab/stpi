# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website BlogPost Extended',
    'category': 'Website/Website',
    'sequence': 265,
    'summary': 'Create BlogPost in forum',
    'version': '1.0',
    'description': """
Create BlogPost in forum
        """,
    'website': 'https://www.odoo.com/page/community-builder',
    'depends': [
        'website_blog', 'intranet_home'
    ],
    'data': [
        'views/website_blogpost.xml',
    ],
    # 'qweb': [
    #     'static/src/xml/website_blog_templates.xml'
    # ],
    'installable': True,
    'application': False,
}
