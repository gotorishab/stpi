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


    def action_approve(self):
        if self.loan_id:
            self.loan_id.sudo().action_approve()
            self.state = self.loan_id.state

    def action_refuse(self):
        if self.loan_id:
            self.loan_id.sudo().action_refuse() #action_cancel
            self.state = self.loan_id.state

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

    def action_cancel(self):
        if self.loan_id:
            self.loan_id.sudo().action_cancel()
            self.state = self.loan_id.state


class UpcomingHrLoanRequest(models.Model):
    _name = 'upcoming.hr.loan.request'
    _description = 'Hr Loan Request'

   
    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    loan_id = fields.Many2one("hr.loan", string="Loan")
    no_of_emi_paid=fields.Integer('Number of EMI Paid')
    no_of_emi_pending=fields.Integer('Number of EMI Pending')
    continue_emi = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string="Are you wish to continue")

    def button_continue_emi(self):
        for res in self:
            if res.continue_emi == 'yes':
                pass
            else:
                self.env['hr.loan.close'].create({
                    "exit_transfer_id": self.id,
                    "loan_id": res.id,
                    "no_of_emi_paid": paid,
                    "no_of_emi_pending": unpaid,
                })

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
