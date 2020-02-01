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
    'depends': ['base','hr','hr_applicant','hr_skills','hr_recruitment','oh_employee_documents_expiry','hr_holidays','stpi_contract_pr','employee_stages','category_religion'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_main.xml',
        'views/employee_family_view.xml',
        'wizard/hr_employee_transfer_approve.xml',
        'views/hr_employee_transfer_view.xml',
        'views/employee_previous_occupation.xml',
        'views/employee_training_view.xml',
        'views/employee_stages_inherit.xml',
        'views/hr_leave_inherit.xml',
        'report/employee_service_book.xml',
        'data/previous_occupation_organisation_type_demo.xml',
        'data/relative_type_demo.xml',
        'data/hr_leave_cron.xml',
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