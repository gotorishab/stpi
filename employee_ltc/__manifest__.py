# -*- coding: utf-8 -*-
{
    'name': "LTC - STPI",
    'summary': """ LTC - STPI""",
    'description': """
    """,
    'author': "Dexciss Technology Pvt Ldt (RGupta)",
    'website': "http://www.dexciss.com",
    'description': """

    """,
    'category': 'hrms',
    'version': '12.0.1',
    'depends': ['base','hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_ltc.xml',
        'report/ltc_report.xml',


    ],

    # 'demo': [
    #     'data/previous_occupation_organisation_type_demo.xml',
    #
    # ],


    'installable': True,
    'application': True,
    'auto_install': False,
    'demo': True

}