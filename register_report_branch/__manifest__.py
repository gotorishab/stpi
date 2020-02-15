{
    "name": "Register Report Branch",
    "version": "12.0.1.1",
    "description": """
                    Last updated by sangita 24/07/2019 issue
    """,
    "author": "Sangita(Dexciss)",
    'website': "http://www.dexciss.com",
    "depends": ['hr','hr_payroll','base','l10n_in_hr_payroll','employee_dynamic_fields_dex',
                'base_branch_company','hr_contract','report_xlsx'],
    "category": "",
    "demo": [],
    "data": [
            "security/ir.model.access.csv",
            'wizard/contribution_register_report_wizard_view.xml',
            'report/register_report_xls.xml',
            'report/contribution_register_summery_pdf_report_template.xml',
            'report/contribution_register_report_template_view.xml',
            'report/contribution_register_report.xml',
            'view/register_report_view.xml',
            'view/ir_model_field_inherit_view.xml'
            ],

    "installable": True,
    "application": True,
}
