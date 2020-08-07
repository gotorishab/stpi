# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PfTransfer(models.TransientModel):
    """
    This wizard will confirm the all the selected draft invoices
    """

    _name = "employee.pf.transfer.wizard"
    _description = "PF Transfer"

    employee_pf = fields.Many2one('pf.employee')
    employee_pf_details = fields.One2many('employee.pf.transfer.details','wizard_emp_transfer', string='PF Transfer Details')




    @api.multi
    def confirm_button(self):
        pass




class PFTransferDetails(models.Model):
    _name = 'employee.pf.transfer.details'
    _description = 'Employee PF Transfer Details'

    wizard_emp_transfer = fields.Many2one('employee.pf.transfer.wizard')
    pf_details_id = fields.Many2one('pf.employee', string="Employee")
    employee_id = fields.Many2one('hr.employee')
    date = fields.Date('Date')
    type = fields.Selection([
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
    ], string="Type")
    pf_code = fields.Char(string='PF code')
    description = fields.Char(string='Description')
    amount = fields.Float('Amount')
    reference = fields.Char('Reference')