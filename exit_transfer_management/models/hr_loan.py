from odoo import models, fields, api

#HrLoan
class PendingHrLoanRequest(models.Model):
    _name = 'pending.hr.loan.request'
    _description = 'Hr Loan Request'

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    loan_id = fields.Many2one("hr.loan", string="Loan")
    type_id = fields.Many2one('loan.type', string="Type")
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    installment = fields.Integer(string="No Of Installments", default=0)
    total_amount = fields.Float(string="Total Amount")
    total_interest = fields.Float(string="Total Interest")
    total_paid_amount = fields.Float(string="Total Paid Amount")
    balance_amount = fields.Float(string="Balance Amount")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval_1', 'Submitted'),
        ('waiting_approval_2', 'Waiting Approval'),
        ('approve', 'Approved'),
        ('refuse', 'Refused'),
        ('cancel', 'Canceled'),
    ], string="Status")


    def tax_approved(self):
        if self.running_fy_id:
            self.running_fy_id.sudo().button_approved()
            self.state = self.running_fy_id.state

    def tax_rejected(self):
        if self.running_fy_id:
            self.running_fy_id.sudo().button_reject()
            self.state = self.running_fy_id.state

class SubmittedHrLoanRequest(models.Model):
    _name = 'submitted.hr.loan.request'
    _description = 'Hr Loan Request'

   
    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    loan_id = fields.Many2one("hr.loan", string="Loan")
    type_id = fields.Many2one('loan.type', string="Type")
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    installment = fields.Integer(string="No Of Installments", default=0)
    total_amount = fields.Float(string="Total Amount")
    total_interest = fields.Float(string="Total Interest")
    total_paid_amount = fields.Float(string="Total Paid Amount")
    balance_amount = fields.Float(string="Balance Amount")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval_1', 'Submitted'),
        ('waiting_approval_2', 'Waiting Approval'),
        ('approve', 'Approved'),
        ('refuse', 'Refused'),
        ('cancel', 'Canceled'),
    ], string="Status")

    def tax_rejected(self):
        if self.running_fy_id:
            self.running_fy_id.sudo().button_reject()
            self.state = self.running_fy_id.state

class UpcomingHrLoanRequest(models.Model):
    _name = 'upcoming.hr.loan.request'
    _description = 'Hr Loan Request'

   
    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    loan_id = fields.Many2one("hr.loan", string="Loan")
    type_id = fields.Many2one('loan.type', string="Type")
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    installment = fields.Integer(string="No Of Installments", default=0)
    total_amount = fields.Float(string="Total Amount")
    total_interest = fields.Float(string="Total Interest")
    total_paid_amount = fields.Float(string="Total Paid Amount")
    balance_amount = fields.Float(string="Balance Amount")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval_1', 'Submitted'),
        ('waiting_approval_2', 'Waiting Approval'),
        ('approve', 'Approved'),
        ('refuse', 'Refused'),
        ('cancel', 'Canceled'),
    ], string="Status")
