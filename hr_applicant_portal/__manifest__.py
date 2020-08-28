{
    'name': "HR Applicant Portal",
    'version': '1.0',
    'summary': """HR Applicant Portal """,
    'description': """
    HR Applicant Portal
""",
    'category': 'Human Resources',
    'author': '',
    'depends': ['hr_applicant','website'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/portal_hr_applicant_templates.xml',
    ],
    'demo': [],
    'images': [],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
