# -*- coding: utf-8 -*-
{
    'name': 'Payroll STPI and Paylevel',
    'version': '12.0.1.0.1',
    'summary': """Payroll.""",
    'description': """Paylevel Master""",
    'category': 'Module for STPI',
    'author': 'Dexciss Technology @RGupta',
    'company': 'Dexciss Technology ',
    'maintainer': 'Dexciss Technology ',
    'website': "https://www.dexciss.com",
    'version': '12.0.4',
    'depends': ['base','hr','hr_contract','hr_payroll','l10n_in_hr_payroll'],
    'data': [
        'views/payment_advices.xml',
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