from odoo import fields,models,api

class AllowedLoanAmount(models.Model):
    _name='allowed.loan.amount'
    _description ='Allowed Loan Amount'

    pay_level_id = fields.Many2one('hr.payslip.paylevel', string='Pay Level')
    loan_type = fields.Many2one('loan.type' ,string='Loan Type')
    amount = fields.Float('Amount')
