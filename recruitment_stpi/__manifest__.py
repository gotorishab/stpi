# -*- coding: utf-8 -*-
{
    'name': "Job Application Form - STPI",

    'summary': """
            Job Application Form for STPI 
            Last Updated by Sangita 16/01/2020 by task TASK-2020-00027
             """,

    'description': """
        Job Application Form for STPI
    """,

    'author': "Rishab Gupta",
    'website': "https://dexciss.com/",
    'category': 'Job Application Form',
    'version': '0.2',

    'depends': ['hr_applicant', 'website_hr_recruitment'],

    'data': [
        'views/website_hr_recruitment_templates.xml',
        'views/hr_applicant.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': True,
    'application': True,
}
