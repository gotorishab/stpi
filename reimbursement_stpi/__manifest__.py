# -*- coding: utf-8 -*-
{
	'name': 'Reimbursement Stpi',
	'version': '12.0.1.0.0',
	'summary': 'Reimbursement Stpi',
	'category': 'Tools',
	'author': 'Dexciss Technologies Pvt Ltd(@ RGupta)',
	'maintainer': 'dexciss Techno Solutions',
	'company': 'dexciss Techno Solutions',
	'website': 'https://www.dexciss.com',
	'depends': ['base','hr','hr_applicant'],
	'data': [
		'security/ir.model.access.csv',
		'security/security.xml',
		'security/reimbursement.xml',
        # 'views/reimbursement.xml',
        'views/reimbursement_main.xml',
        'views/reimbursement_attendence.xml',
		'wizard/multi_approve.xml'
	],
	'images': [],
	'license': 'AGPL-3',
	'installable': True,
	'application': False,
	'auto_install': False,
}