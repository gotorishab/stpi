# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrPayslipEmployees(models.TransientModel):
    _name = 'generate.payment.advices'
    _description = 'Generate Payment Advices for all selected employees'

    employee_ids = fields.Many2many('hr.employee', string='Employees')

    @api.multi
    def compute_sheet(self):
        pass
        # """
        #         Advice - Create Advice lines in Payment Advice and
        #         compute Advice lines.
        #         """
        # for advice in self:
        #     old_lines = self.env['hr.payroll.advice.line'].search([('advice_id', '=', advice.id)])
        #     if old_lines:
        #         old_lines.unlink()
        #     payslips = self.env['hr.payslip'].search(
        #         [('date_from', '<=', advice.date), ('date_to', '>=', advice.date), ('state', '=', 'done')])
        #     for slip in payslips:
        #         if not slip.employee_id.bank_account_number:
        #             raise UserError(_('Please define bank account for the %s employee') % (slip.employee_id.name,))
        #         payslip_line = self.env['hr.payslip.line'].search([('slip_id', '=', slip.id), ('code', '=', 'NET')],
        #                                                           limit=1)
        #         if payslip_line:
        #             self.env['hr.payroll.advice.line'].create({
        #                 'advice_id': advice.id,
        #                 'name': slip.employee_id.bank_account_number,
        #                 'ifsc_code': slip.employee_id.ifsc_code or '',
        #                 'employee_id': slip.employee_id.id,
        #                 'bysal': payslip_line.total
        #             })
        #         slip.advice_id = advice.id
