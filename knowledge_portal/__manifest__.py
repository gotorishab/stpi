{
    'name': "Vardhman Knowledge Management Postal",
    'version': '1.0',
    'summary': """Vardhman Portal """,
    'description': """
    Vardhman Homepage
""",
    'category': 'Human Resources',
    'author': '',
    'depends': ['website','hr','board','intranet_home'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/knowledge_assigned_task_cron.xml',
        'views/task.xml',
        'views/assignment.xml',
    ],
    'demo': [],
    'images': [],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
