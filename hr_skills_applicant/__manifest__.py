# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Skills Management',
    'category': 'Hidden',
    'version': '1.3',
    'summary': 'Manage skills, knowledge and resumé of your employees',
    'description':
        """
Skills and Resumé for HR
========================
Last Updated by RGupta 06/09/2019 -> Type -> Required

This module introduces skills and resumé management for employees.
    Last Updated by sangits 02/04/2019
        """,
    'depends': ['hr','hr_recruitment','hr_skills'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_views.xml',
    ],
    # 'demo': [],
    # 'qweb': [
    #     'static/src/xml/resume_templates.xml',
    #     'static/src/xml/skills_templates.xml',
    # ],
    'installable': True,
    'application': True,
}
