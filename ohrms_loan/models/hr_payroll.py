# -*- coding: utf-8 -*-
import time
import babel
from odoo import models, fields, api, tools, _
from datetime import datetime


class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.input'

    loan_line_id = fields.Many2one('hr.loan.line', string="Loan Installment")


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    @api.one
    def compute_total_paid(self):
        """This compute the total paid amount of Loan.
            """
        total = 0.0
        for line in self.loan_ids:
            if line.paid:
                total += line.amount
        self.total_paid = total

    loan_ids = fields.One2many('hr.loan.line', 'payslip_id', string="Loans")
    total_paid = fields.Float(string="Total Loan Amount", compute='compute_total_paid')
    #added by sangita
    refund_id = fields.Many2one('hr.payslip',string="Refund ID")

    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee(self):
        if (not self.employee_id) or (not self.date_from) or (not self.date_to):
            return

        employee = self.employee_id
        date_from = self.date_from
        date_to = self.date_to
        contract_ids = []

        ttyme = datetime.fromtimestamp(time.mktime(time.strptime(str(date_from), "%Y-%m-%d")))
        locale = self.env.context.get('lang') or 'en_US'
        self.name = _('Salary Slip of %s for %s') % (
        employee.name, tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale)))
        self.company_id = employee.company_id

        if not self.env.context.get('contract') or not self.contract_id:
            contract_ids = self.get_contract(employee, date_from, date_to)
            if not contract_ids:
                return
            self.contract_id = self.env['hr.contract'].browse(contract_ids[0])

        if not self.contract_id.struct_id:
            return
        self.struct_id = self.contract_id.struct_id

        # computation of the salary input
        contracts = self.env['hr.contract'].browse(contract_ids)
        worked_days_line_ids = self.get_worked_day_lines(contracts, date_from, date_to)
        worked_days_lines = self.worked_days_line_ids.browse([])
        for r in worked_days_line_ids:
            worked_days_lines += worked_days_lines.new(r)
        self.worked_days_line_ids = worked_days_lines
        if contracts:
            input_line_ids = self.get_inputs(contracts, date_from, date_to)
            input_lines = self.input_line_ids.browse([])
            for r in input_line_ids:
                input_lines += input_lines.new(r)
            self.input_line_ids = input_lines
        return

    def get_inputs(self, contract_ids, date_from, date_to):
        """This Compute the other inputs to employee payslip.
                           """
        res = super(HrPayslip, self).get_inputs(contract_ids, date_from, date_to)
        contract_obj = self.env['hr.contract']
        emp_id = contract_obj.browse(contract_ids[0].id).employee_id
        lon_obj = self.env['hr.loan'].search([('employee_id', '=', emp_id.id), ('state', '=', 'approve')])
        for loan in lon_obj:
            for loan_line in loan.loan_lines:
                if date_from <= loan_line.date <= date_to and not loan_line.paid:
                    for result in res:
                        if result.get('code') == 'LO':
                            result['amount'] = loan_line.amount
                            result['loan_line_id'] = loan_line.id
        return res

    @api.multi
    def get_loan(self):
        """This gives the installment lines of an employee where the state is not in paid.
            """
        self.loan_ids.unlink()
        loan_list = []
        loan_ids = self.env['hr.loan.line'].search([('employee_id', '=', self.employee_id.id), ('paid', '=', False)])
        for loan in loan_ids:
            print("--------------------------loan",loan.id)
            if loan.loan_id.state == 'approve':
                # loan_list.append(loan.id)
                loan_list.append((0, 0, {
                    "loan_payslip_id": loan.loan_id.id,
                    "date":loan.date,
                    "amount":loan.amount,
                    "paid":loan.paid
                }))
        self.loan_ids = loan_list
        for s in self:
            for loan in s.loan_ids:
                if loan.date <= s.date_to:
                    loan.paid = True
        return True

    #added by sangita
    @api.multi
    def compute_sheet(self):
        for s in self:
            s.get_loan()
            return super(HrPayslip,s).compute_sheet()
       
    @api.multi
    def refund_sheet(self):
        res =  super(HrPayslip,self).refund_sheet()
        self.state = 'cancel'
        for s in self:
            for loan in s.loan_ids:
                if loan.date <= s.date_to:
                    loan.paid = False
        self.refund_id = self.copy({'credit_note': True, 'name': _('Refund: ') + self.name})
        return True
         
#     @api.multi
#     def refund_sheet(self):
#         for payslip in self:
#             print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
#             copied_payslip = payslip.copy({'credit_note': True, 'name': _('Refund: ') + payslip.name})
#             print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;",copied_payslip)
#             copied_payslip.action_payslip_done()
#             print("=============================",copied_payslip.action_payslip_done())
#             payslip.state = 'cancel'
#             print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",payslip.state)
#             for loan in payslip.loan_ids:
#                 print(">>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<",loan)
#                 if loan.date <= payslip.date_to:
#                     print("'''''''''''''''''''''''''''''''''",loan.date)
#                     loan.paid = False
#                     print(";8888888888888888888888888",loan.paid)
# #         copied_payslip = self.copy({'credit_note': True, 'name': _('Refund: ') + s.name})
#             payslip.refund_id = copied_payslip
#             print("[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[",payslip.refund_id)
#         formview_ref = self.env.ref('hr_payroll.view_hr_payslip_form', False)
#         treeview_ref = self.env.ref('hr_payroll.view_hr_payslip_tree', False)
# #         print"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,",copied_payslip.ids
#         return {
#             'name': ("Refund Payslip"),
#             'view_mode': 'tree, form',
#             'view_id': False,
#             'view_type': 'form',
#             'res_model': 'hr.payslip',
#             'type': 'ir.actions.do_nothing',
#             'target': 'current',
#             'domain': "[('id', 'in', %s)]" % copied_payslip.ids,
#             'views': [(treeview_ref and treeview_ref.id or False, 'tree'), (formview_ref and formview_ref.id or False, 'form')],
#             'context': {}
#         }


    @api.multi
    def action_payslip_done(self):
        loan_list = []
        for line in self.loan_ids:
            if line.paid:
                loan_ids = self.env['hr.loan.line'].search(
                    [('employee_id', '=', self.employee_id.id),('loan_id','=',line.loan_payslip_id.id), ('paid', '=', False), ('date', '=', line.date)])
                for loans in loan_ids:
                    loans.paid = True
                    loans.loan_payslip_ref_id = self.id
                # loan_list.append(line.id)
            else:
                line.payslip_id = False
        # self.loan_ids = loan_list
        return super(HrPayslip, self).action_payslip_done()