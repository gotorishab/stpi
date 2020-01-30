# -*- coding: utf-8 -*-
{
    'name': "l10n_in_hr_fields",
    'summary': """ """,
    'description': """
    """,
    'author': "Dexciss Technology Pvt Ldt (SMehata, RGupta)",
    'website': "http://www.dexciss.com",
    'description': """
    Updated by Rgupta 27/09/19
    Updated by SMehata 26/08/19
    Last Updated by sangita 21/01/2020""",
    'category': 'hrms',
    'version': '12.0.4',
    'depends': ['base','hr','hr_contract','hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_payroll.xml',
        'views/hr_employee_contracts.xml',
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