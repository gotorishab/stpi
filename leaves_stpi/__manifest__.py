{
    'name': 'STPI Leave Management',
    'version': '12.0.0.0',
    'summary': 'Manage Leave Requests',
    'description': """
        Helps you to manage Leave Requests of your company's staff.
        """,
    'category': 'Human Resources',
    'author': "Sangita(Dexciss Technology Pvt. Ltd,Pune)",
    'company': 'Dexciss Technology Pvt. Ltd,Pune',
    'maintainer': 'Dexciss Technology Pvt. Ltd,Pune',
    'website': "https://www.dexciss.com",
    'depends': [
        'hr_holidays','hr','sandwich_rule','hr_branch_company'
    ],
    'data': [
        'data/hr_leave_type_data.xml',
        'data/leave_employee_type.xml',
        'data/leave_employee_stages.xml',
        'data/holidays_type_data.xml',
        'security/ir.model.access.csv',
        'views/hr_leave_type_extended.xml',
        'views/leave_type_view.xml',
        'views/employee_stages.xml',
        'views/leave_employee_type_view.xml',
        'views/hr_employee_view.xml',
        'views/hr_leave_view.xml'
    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
