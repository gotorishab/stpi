from odoo import models, fields, api,_
from odoo.exceptions import UserError


class HrPayrollAdvices(models.Model):
    _name='hr.payroll.advice'


    @api.multi
    def generate_wiz(self):
        pass

    @api.multi
    def compute_advice(self):
        """
        Advice - Create Advice lines in Payment Advice and
        compute Advice lines.
        """
        for advice in self:
            old_lines = self.env['hr.payroll.advice.line'].search([('advice_id', '=', advice.id)])
            if old_lines:
                old_lines.unlink()
            payslips = self.env['hr.payslip'].search([('date_from', '<=', advice.date), ('date_to', '>=', advice.date), ('state', '=', 'done')])
            for slip in payslips:
                if not slip.employee_id.bank_account_id and not slip.employee_id.bank_account_id.acc_number:
                    raise UserError(_('Please define bank account for the %s employee') % (slip.employee_id.name,))
                payslip_line = self.env['hr.payslip.line'].search([('slip_id', '=', slip.id), ('code', '=', 'NET')], limit=1)
                if payslip_line:
                    self.env['hr.payroll.advice.line'].create({
                        'advice_id': advice.id,
                        'name': slip.employee_id.bank_account_number,
                        'ifsc_code': slip.employee_id.ifsc_code or '',
                        'employee_id': slip.employee_id.id,
                        'bysal': payslip_line.total
                    })
                slip.advice_id = advice.id



class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'
    _description = 'Payslip Batches'



    @api.multi
    def create_advice(self):
        for run in self:
            if run.available_advice:
                raise UserError(_("Payment advice already exists for %s, 'Set to Draft' to create a new advice.") % (run.name,))
            company = self.env.user.company_id
            advice = self.env['hr.payroll.advice'].create({
                        'batch_id': run.id,
                        'company_id': company.id,
                        'name': run.name,
                        'date': run.date_end,
                        'bank_id': company.partner_id.bank_ids and company.partner_id.bank_ids[0].bank_id.id or False
                    })
            for slip in run.slip_ids:
                # TODO is it necessary to interleave the calls ?
                slip.action_payslip_done()
                if not slip.employee_id.bank_account_id or not slip.employee_id.bank_account_id.acc_number:
                    raise UserError(_('Please define bank account for the %s employee') % (slip.employee_id.name))
                payslip_line = self.env['hr.payslip.line'].search([('slip_id', '=', slip.id), ('code', '=', 'NET')], limit=1)
                if payslip_line:
                    self.env['hr.payroll.advice.line'].create({
                        'advice_id': advice.id,
                        'name': slip.employee_id.bank_account_number,
                        'ifsc_code': slip.employee_id.ifsc_code or '',
                        'employee_id': slip.employee_id.id,
                        'bysal': payslip_line.total
                    })
        self.write({'available_advice': True})



class HrPayrollAdviceLine(models.Model):
    '''
    Bank Advice Lines
    '''
    _name = 'hr.payroll.advice.line'
    _description = 'Bank Advice Lines'



    @api.onchange('employee_id')
    def onchange_employee_id(self):
        self.name = self.employee_id.bank_account_number
        self.ifsc_code = self.employee_id.ifsc_code or ''
