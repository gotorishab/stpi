# -*- coding: utf-8 -*-
{
    'name': 'Employee Customisation - STPI',
    'version': '12.0.1.0.0',
    'summary': """Employee Customisation - STPI""",
    'description': """Employee Customisation - STPI""",
    'category': 'Module for STPI',
    'author': 'Dexciss Technology @RGupta',
    'company': 'Dexciss Technology ',
    'maintainer': 'Dexciss Technology ',
    'website': "https://www.dexciss.com",
    'version': '12.0.4',
    'depends': ['base','hr','employee_stages'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/hr_employee_transfer_approve.xml',
        'views/hr_employee_transfer_view.xml',
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