# -*- coding: utf-8 -*-
{
    'name': "Job Application Form",

    'summary': """
            Job Application Form
             """,

    'description': """
        Job Application Form
    """,

    'author': "Dexciss Technology",
    'website': "https://dexciss.com/",
    'category': 'Job Application Form',
    'version': '0.1',

    'depends': ['hr_applicant', 'website_hr_recruitment'],

    'data': [
        'views/website_hr_recruitment_templates.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': True,
    'application': True,
}
