# -*- coding: utf-8 -*-
# © 2011 Raphaël Valyi, Renato Lima, Guewen Baconnier, Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{'name': 'Hr Exception',
 'summary': 'Custom exceptions on Hr',
 'version': '12.0.4',
 'category': 'Generic Modules/Purchase',

'author': "Dexciss Technology Pvt Ltd(SMehata)",
 'website': 'http://www.Dexciss.com',
 'depends': ['hr_employee_requisition', 'base_exception_and_approval', 'ohrms_loan', 'tour_request','birthday_check',
             'hr_employee_transfer','employee_vehicle_request','reimbursement_stpi','hr_holidays'],
 'license': 'AGPL-3',
'description':"""
                updated by smehata 23/08/19 add Loan Exception
                updated by smehata 20/08/19 
                Last Updated by sangita 21/01/2020
                Last Updated by sangita 04/02/2020 added vehicle request exception
                 """,
 'data': [
          'security/ir.model.access.csv',
          'security/approval_security.xml',
            'wizard/reason_wizard.xml',
            'view/hr_loan_view.xml',
            'view/tour_request.xml',
            'view/tour_claim.xml',
            'view/hr_employee_transfer.xml',
            'view/employee_vehicle_request.xml',
            'view/reimbursement.xml',
            'view/hr_leave_view.xml',
            'wizard/hr_loan_wizard_view.xml',
            'wizard/employee_requisition_wizard_view.xml',
            'wizard/tour_request_wizard_view.xml',
            'wizard/tour_claim_wizard_view.xml',
            'wizard/cheque_requests_wizard_view.xml',
            'wizard/hr_employee_transfer_wizard_view.xml',
            'wizard/employee_vehicle_wizard_view.xml',
            'wizard/reimbursement_wizard_view.xml'
            'wizard/hr_leave_wizard_view.xml'

 ],
 'images': [],
 'installable': True,
 }
