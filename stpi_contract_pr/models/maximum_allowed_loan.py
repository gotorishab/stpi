from odoo import fields,models,api

class AllowedLoanAmount(models.Model):
    _name='allowed.loan.amount'
    _description ='Allowed Loan Amount'

    pay_level = fields.Many2one('payslip.pay.level', string='Pay Band')
    amount = fields.Float('Amount')


#
# class HrLoanInh(models.Model):
#     _inherit='hr.loan'
#     _description ='Loan Request'
#
#
#     @api.constrains('loan_amount')
#     def check_loan_amount(self):
#         if self.loan_amount > 0.00:
#             max_all = self.env['allowed.loan.amount'].search([('pay_level', '=', self.employee_id.job_id.pay_level.id)], limit=1)
#             if max_all.amount and self.loan_amount > max_all.amount:
#                 raise UserError(_('You are not allowed to take loan more than') %max_all.amount)
