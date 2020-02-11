{
    'name': 'STPI Leave Management',
    'version': '12.0.1.0',
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
        'hr_holidays','hr','sandwich_rule','hr_branch_company','hr_payroll','hr_employee_stpi'
    ],
    'data': [
        'data/hr_leave_type_data.xml',
        'data/holidays_type_data.xml',
        'data/allocate_leave_cron_job.xml',
        'data/expire_leave_cron_job.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/hr_leave_type_extended.xml',
        'views/leave_type_view.xml',
        'views/employee_stages.xml',
        'views/leave_employee_type_view.xml',
        'views/hr_employee_view.xml',
        'views/hr_leave_view.xml',
        'views/hr_payslip_view.xml'
    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
