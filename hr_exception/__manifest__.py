# -*- coding: utf-8 -*-
# © 2011 Raphaël Valyi, Renato Lima, Guewen Baconnier, Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{'name': 'Hr Exception',
 'summary': 'Custom exceptions on Hr',
 'version': '12.0.3',
 'category': 'Generic Modules/Purchase',

'author': "Dexciss Technology Pvt Ltd(SMehata)",
 'website': 'http://www.Dexciss.com',
 'depends': ['hr_employee_requisition', 'base_exception_and_approval', 'ohrms_loan', 'tour_request'],
 'license': 'AGPL-3',
'description':"""
                updated by smehata 23/08/19 add Loan Exception
                updated by smehata 20/08/19 
                Last Updated by sangita 21/01/2020
                 """,
 'data': [
          'security/ir.model.access.csv',
          'security/approval_security.xml',
            'wizard/reason_wizard.xml',
            'view/hr_loan_view.xml',
            'view/tour_request.xml',
            'wizard/hr_loan_wizard_view.xml',
            'wizard/employee_requisition_wizard_view.xml',
            'wizard/tour_request_wizard_view.xml',
     # 'view/hr_job_view.xml',
          # 'view/employee_requisition_view.xml',
          # 'wizard/hr_job_exception_wizard_view.xml',


 ],
 'images': [],
 'installable': True,
 }
