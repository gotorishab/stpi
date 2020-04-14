# -*- coding: utf-8 -*-
{
	'name': 'Appraisal - STPI',
	'version': '12.0.1.0.0',
	'summary': 'Appraisal Stpi',
	'category': 'Tools',
	'author': 'Dexciss Technologies Pvt Ltd(@ RGupta)',
	'maintainer': 'dexciss Techno Solutions',
	'company': 'Dexciss Techno Solutions',
	'website': 'https://www.dexciss.com',
	'depends': ['base','hr','hr_payroll','date_range','stpi_contract_pr'],
	'data': [
		'security/ir.model.access.csv',
		'security/security.xml',
        'views/appraisal_forms.xml',
        'views/appraisal_template.xml',
	],
	'images': [],
	'license': 'AGPL-3',
	'installable': True,
	'application': False,
	'auto_install': False,
}