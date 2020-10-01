# -*- coding: utf-8 -*-
{
	'name': 'TDS',
	'version': '12.0.1.0.0',
	'summary': 'TDS Stpi',
	'category': 'Tools',
	'author': 'Dexciss Technologies Pvt Ltd(@ RGupta)',
	'maintainer': 'dexciss Techno Solutions',
	'company': 'dexciss Techno Solutions',
	'website': 'https://www.dexciss.com',
	'depends': ['base','hr','hr_payroll','date_range'],
	'data': [
		'security/ir.model.access.csv',
		'security/security.xml',
		'data/Income_tax_rule.xml',
		'data/income_tax_slab.xml',
		'data/email_template.xml',
		'data/hr_declaration_cron.xml',
		'report/employee_service_book.xml',
		'wizard/reason_wizard.xml',
		'wizard/non_documents.xml',
        'views/date_range.xml',
        'views/hr_payslip.xml',
        'views/tds.xml',
        'views/hr_declaration.xml',
        'views/hr_payroll.xml',
        'views/non_documents_report.xml',
		'wizard/send_reminders.xml',
	],
	'images': [],
	'license': 'AGPL-3',
	'installable': True,
	'application': False,
	'auto_install': False,
}