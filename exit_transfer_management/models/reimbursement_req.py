from odoo import models, fields, api

#Reimbursement
class PendingReimbursementRequest(models.Model):
    _name = "pending.reimbursement.request"
    _description = "Pending Reimbursement Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    reiburs_id = fields.Many2one("reimbursement", string="Reimbursment")
    name = fields.Selection([
        ('lunch', 'Lunch Subsidy'),
        ('telephone', 'Telephone Reimbursement'),
        ('mobile', 'Mobile Reimbursement'),
        ('medical', 'Medical Reimbursement'),
        ('tuition_fee', 'Tuition Fee claim'),
        ('briefcase', 'Briefcase Reimbursement'),
        ('quarterly', 'Newspaper Reimbursements'),
    ], string='Reimbursement Type')

    claim_sub = fields.Many2one("date.range", string="Claim Submission")
    claimed_amount = fields.Float('Claimed Amount')
    net_amount = fields.Float('Eligible Amount')

    state = fields.Selection([('draft', 'Draft'),
                              ('waiting_for_approval', 'Submitted'),
                              ('forwarded', 'Forwarded'),
                              ('approved', 'Approved'),
                              ('rejected', 'Rejected')
                              ],default='draft', track_visibility='always', string='Status')
    def button_approved(self):
        if self.reiburs_id:
            self.reiburs_id.sudo().button_approved()
            self.update({"state": "approved"})

    def button_reject(self):
        if self.reiburs_id:
            self.reiburs_id.sudo().button_reject()
            self.update({"state": "rejected"})


class SubmittedReimbursementRequest(models.Model):
    _name = "submitted.reimbursement.request"
    _description = "Submitted Reimbursement Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    reiburs_id = fields.Many2one("reimbursement", string="Reimbursment")
    name = fields.Selection([
        ('lunch', 'Lunch Subsidy'),
        ('telephone', 'Telephone Reimbursement'),
        ('mobile', 'Mobile Reimbursement'),
        ('medical', 'Medical Reimbursement'),
        ('tuition_fee', 'Tuition Fee claim'),
        ('briefcase', 'Briefcase Reimbursement'),
        ('quarterly', 'Newspaper Reimbursements'),
    ], string='Reimbursement Type')

    claim_sub = fields.Many2one("date.range", string="Claim Submission")
    claimed_amount = fields.Float('Claimed Amount')
    net_amount = fields.Float('Eligible Amount')

    state = fields.Selection([('draft', 'Draft'),
                              ('waiting_for_approval', 'Submitted'),
                              ('forwarded', 'Forwarded'),
                              ('approved', 'Approved'),
                              ('rejected', 'Rejected')
                              ],default='draft', track_visibility='always', string='Status')

    def button_reject(self):
        if self.reiburs_id:
            self.reiburs_id.sudo().button_reject()
            self.update({"state": "rejected"})


class UpcomingReimbursementRequest(models.Model):
    _name = "upcoming.reimbursement.request"
    _description = "Upcoming Reimbursement Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    reiburs_id = fields.Many2one("reimbursement", string="Reimbursment")
    name = fields.Selection([
        ('lunch', 'Lunch Subsidy'),
        ('telephone', 'Telephone Reimbursement'),
        ('mobile', 'Mobile Reimbursement'),
        ('medical', 'Medical Reimbursement'),
        ('tuition_fee', 'Tuition Fee claim'),
        ('briefcase', 'Briefcase Reimbursement'),
        ('quarterly', 'Newspaper Reimbursements'),
    ], string='Reimbursement Type')

    claim_sub = fields.Many2one("date.range", string="Claim Submission")
    claimed_amount = fields.Float('Claimed Amount')
    net_amount = fields.Float('Eligible Amount')

    state = fields.Selection([('draft', 'Draft'),
                              ('waiting_for_approval', 'Submitted'),
                              ('forwarded', 'Forwarded'),
                              ('approved', 'Approved'),
                              ('rejected', 'Rejected')
                              ],default='draft', track_visibility='always', string='Status')

