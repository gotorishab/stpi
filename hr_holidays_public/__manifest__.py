# Copyright 2015 2011,2013 Michael Telahun Makonnen <mmakonnen@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'STPI Leave Management',
    'version': '12.0.1.0',
    'summary': 'Manage Leave Requests',
    'description': """
        Helps you to Public Holiday Requests of your company's staff.
        """,
    'category': 'Human Resources',
    'author': "Sangita(Dexciss Technology Pvt. Ltd,Pune)",
    'company': 'Dexciss Technology Pvt. Ltd,Pune',
    'maintainer': 'Dexciss Technology Pvt. Ltd,Pune',
    'website': "https://www.dexciss.com",
    'depends': [
        'hr_holidays','base_branch_company'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_holidays_public_view.xml',
    ],
    'installable': True,
}
