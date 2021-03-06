# -*- coding: utf-8 -*-
{
	'name': 'Birthday Check',
	'version': '12.0.1.0.0',
	'summary': 'Birthday Check',
	'category': 'Tools',
	'author': 'Dexciss Technologies Pvt Ltd(@ RGupta)',
	'maintainer': 'dexciss Techno Solutions',
	'company': 'dexciss Techno Solutions',
	'website': 'https://www.dexciss.com',
	'depends': ['base','hr','hr_employee_stpi','category_religion','groups_inherit'],
	'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
		'data/birthday_check_cron.xml',
        'views/birthday_check.xml',
        'views/cheque_requests.xml',
        'views/menuitems.xml',
        'wizard/cheque_request_wizard.xml',
        'wizard/cheque_request_action_wizard.xml',
        'wizard/birthday_cheque.xml',
	],
	'images': [],
	'license': 'AGPL-3',
	'installable': True,
	'application': False,
	'auto_install': False,
}