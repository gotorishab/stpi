from odoo import fields,models,api

class LoanType(models.Model):

    _name='loan.type'
    _description ='Loan Type'
    _rec_name ='type_emp'

    type_emp=fields.Char(string='Name')
    interest=fields.Float(string='Interest Rate%')
    category_ids = fields.Many2many('hr.employee.category', string='Tags')
    max_emi=fields.Integer(string="Max No.EMI")
    filter_domain = fields.Char(string="Domain")

    threshold_emi = fields.Integer(string='Threshold EMI')
    threshold_below_emi = fields.Integer(string='Interest EMI Below/Equal to Threshold')
    threshold_above_emi = fields.Integer(string='Interest EMI above Threshold')





