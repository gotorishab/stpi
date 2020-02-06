from odoo import fields,models,api

class AllowedLoanAmount(models.Model):
    _name='allowed.loan.amount'
    _description ='Allowed Loan Amount'

    pay_level_id = fields.Many2one('hr.payslip.paylevel', string='Pay Level')
    amount = fields.Float('Amount')
