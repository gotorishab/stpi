from odoo import fields,models,api

class AllowedLoanAmount(models.Model):
    _name='allowed.loan.amount'
    _description ='Allowed Loan Amount'

    pay_level = fields.Many2one('payslip.pay.level', string='Pay Band')
    amount = fields.Float('Amount')
