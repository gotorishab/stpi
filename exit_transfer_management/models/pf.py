from odoo import models, fields, api
# PF Request
class PendingPFRequest(models.Model):
    _name = "pending.pf.request"
    _description = "Pending PF Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    pf_id = fields.Many2one('pf.widthdrawl', string='PF Request_Id')
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    advance_amount = fields.Float(string="Advance Amount")
    purpose = fields.Text(string="Purpose")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected')
    ], string='Status')

    def pf_approved(self):
        if self.pf_id:
            self.pf_id.sudo().button_approved()
            self.update({"state": "approved"})

    def pf_rejected(self):
        if self.pf_id:
            self.pf_id.sudo().button_reject()
            self.update({"state": "rejected"})

class SubmittedPFRequest(models.Model):
    _name = "submitted.pf.request"
    _description = "Submitted PF Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    pf_id = fields.Many2one('pf.widthdrawl', string='PF Request_Id')
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    advance_amount = fields.Float(string="Advance Amount")
    purpose = fields.Text(string="Purpose")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected')
    ], string='Status')

    def pf_cancel(self):
        if self.pf_id:
            self.pf_id.sudo().button_cancel()
            self.update({"state": "cancelled"})


class UpcomingPFRequest(models.Model):
    _name = "upcoming.pf.request"
    _description = "Upcoming PF Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    pf_id = fields.Many2one('pf.widthdrawl', string='PF Request_Id')
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    advance_amount = fields.Float(string="Advance Amount")
    purpose = fields.Text(string="Purpose")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected')
    ], string='Status')

