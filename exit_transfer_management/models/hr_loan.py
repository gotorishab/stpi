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
    remarks=fields.Char('Remarks')
    document=fields.Binary('Document')
    continue_emi = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], default='no', string="Are you wish to continue")

    def button_continue_emi(self):
        for res in self:
            if res.continue_emi == 'yes':
                pass
            else:
                loan_close_id = self.env['hr.loan.close'].create({
                    "employee_id": self.loan_id.employee_id.id,
                    "loan_id": res.loan_id.id,
                    "remarks": res.remarks,
                    "document_proof": res.document,
                })
                loan_close_id.sudo().button_submit()

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



class CompletedHrLoanRequest(models.Model):
    _name = 'nottransferred.hr.loan.request'
    _description = 'Hr Loan Request Not Transferred'


    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    loan_id = fields.Many2one("hr.loan", string="Loan")
    no_of_emi_paid=fields.Integer('Number of EMI Paid')
    no_of_emi_pending=fields.Integer('Number of EMI Pending')
    remarks=fields.Char('Remarks')
    document=fields.Binary('Document')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval_1', 'Submitted'),
        ('waiting_approval_2', 'Waiting Approval'),
        ('approve', 'Approved'),
        ('refuse', 'Refused'),
        ('cancel', 'Canceled'),
    ], string="Status")

    def button_continue_emi(self):
        for res in self:
            loan_close_id = self.env['hr.loan.close'].create({
                "employee_id": self.loan_id.employee_id.id,
                "loan_id": res.loan_id.id,
                "remarks": res.remarks,
                "document_proof": res.document,
            })
            loan_close_id.sudo().button_submit()


