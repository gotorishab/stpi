# -*- coding: utf-8 -*-
{
	'name': 'Recruitment Roster',
	'version': '12.0.1.0.0',
	'summary': 'Recruitment Roster',
	'category': 'Tools',
	'author': 'Dexciss Technologies Pvt Ltd(@ RGupta)',
	'maintainer': 'dexciss Techno Solutions',
	'company': 'dexciss Techno Solutions',
	'website': 'https://www.dexciss.com',
	'depends': ['base','mail'],
	'data': [
		'security/ir.model.access.csv',
		'security/security.xml',
		'views/roster_rec.xml',
		'views/job_opening.xml',
	],
	'images': [],
	'license': 'AGPL-3',
	'installable': True,
	'application': False,
	'auto_install': False,
}