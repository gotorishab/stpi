from odoo import models, fields, api

class PendingIndentRequest(models.Model):
    _name = "pending.indent.request"
    _description ="Pending Indent Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    number = fields.Char('Indent Number')
    indent_id = fields.Many2one("indent.request", string="Indent Request")
    employee_id = fields.Many2one('hr.employee', string='Employee')
    indent_type = fields.Selection([('issue', 'Issue'), ('grn', 'GRN')
                                    ],string='Type')
    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], string='Status')

    def button_approved(self):
        if self.indent_id:
            self.indent_id.sudo().button_approved()
            self.update({"state":"approved"})

    def button_reject(self):
        if self.indent_id:
            self.indent_id.sudo().button_reject()
            self.update({"state":"rejected"})

class SubmittedIndentRequest(models.Model):
    _name = "submitted.indent.request"
    _description =" Submitted Indent Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    number = fields.Char('Indent Number')
    indent_id = fields.Many2one("indent.request", string="Indent Request")
    employee_id = fields.Many2one('hr.employee', string='Employee')
    indent_type = fields.Selection([('issue', 'Issue'), ('grn', 'GRN')
                                    ], track_visibility='always', string='Type')
    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], required=True, default='draft', track_visibility='always', string='Status')

    def button_reject(self):
        if self.indent_id:
            self.indent_id.sudo().button_reject()
            self.update({"state": "rejected"})

class UpcomingIndentRequest(models.Model):
    _name = "upcoming.indent.request"
    _description =" Upcoming Indent Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    number = fields.Char('Indent Number')
    indent_id = fields.Many2one("indent.request", string="Indent Request")
    employee_id = fields.Many2one('hr.employee', string='Employee')
    indent_type = fields.Selection([('issue', 'Issue'), ('grn', 'GRN')
                                    ], track_visibility='always', string='Type')
    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], required=True, default='draft', track_visibility='always', string='Status')


class PendingGRN(models.Model):
    _name = "pending.grn"
    _description = "Pending GRN "

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    number = fields.Char('Number')
    indent_id = fields.Many2one("indent.request", string="Indent Request")
    employee_id = fields.Many2one('hr.employee', string='Employee')
    indent_type = fields.Selection([('issue', 'Issue'), ('grn', 'GRN')
                                    ], track_visibility='always', string='Type')
    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], required=True, default='draft', track_visibility='always', string='Status')

    def button_approved(self):
        if self.indent_id:
            self.indent_id.sudo().button_approved()
            self.update({"state": "approved"})

    def button_reject(self):
        if self.indent_id:
            self.indent_id.sudo().button_reject()
            self.update({"state": "rejected"})

class SubmittedGRN(models.Model):
    _name = "submitted.grn"
    _description = "Submitted GRN "

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    number = fields.Char('Number')
    indent_id = fields.Many2one("indent.request", string="Indent Request")
    employee_id = fields.Many2one('hr.employee', string='Employee')
    indent_type = fields.Selection([('issue', 'Issue'), ('grn', 'GRN')
                                    ], track_visibility='always', string='Type')
    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], required=True, default='draft', track_visibility='always', string='Status')

    def button_reject(self):
        if self.indent_id:
            self.indent_id.sudo().button_reject()
            self.update({"state": "rejected"})

class UpcomingGRN(models.Model):
    _name = "upcoming.grn"
    _description = "Upcoming GRN "

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    number = fields.Char('Number')
    indent_id = fields.Many2one("indent.request", string="Indent Request")
    employee_id = fields.Many2one('hr.employee', string='Employee')
    indent_type = fields.Selection([('issue', 'Issue'), ('grn', 'GRN')
                                    ], track_visibility='always', string='Type')
    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], required=True, default='draft', track_visibility='always', string='Status')


class IssueRequestEmp(models.Model):
    _name = "issue.request.emp"
    _description ="Issues Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    issue_id = fields.Many2one("issue.request", string="Issue Request")
    indent_grn = fields.Many2one('indent.request', string='Indent/GRN')
    item_category_id = fields.Many2one('indent.stock', string='Item Category')
    item_id = fields.Many2one('child.indent.stock', string='Item')
    requested_quantity = fields.Integer('Requested Quantity')
    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve_proceed', 'To Approve 1'), ('to_approve', 'To Approve'),
         ('approved', 'Approved'), ('rejected', 'Rejected')
         ], string='Status')

    def button_approved(self):
        if self.issue_id:
            self.issue_id.sudo().button_approved()
            self.update({"state": "approved"})

    def button_reject(self):
        if self.issue_id:
            self.issue_id.sudo().button_reject()
            self.update({"state": "rejected"})


class GRNRequestEmp(models.Model):
    _name = "grn.request.emp"
    _description ="GRN Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    issue_id = fields.Many2one("issue.request", string="Issue Request")
    indent_grn = fields.Many2one('indent.request', string='Indent/GRN')
    item_category_id = fields.Many2one('indent.stock', string='Item Category')
    item_id = fields.Many2one('child.indent.stock', string='Item')
    requested_quantity = fields.Integer('Requested Quantity')
    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve_proceed', 'To Approve 1'), ('to_approve', 'To Approve'),
         ('approved', 'Approved'), ('rejected', 'Rejected')
         ], string='Status')

    def button_approved(self):
        if self.issue_id:
            self.issue_id.sudo().button_approved()
            self.update({"state": "approved"})

    def button_reject(self):
        if self.issue_id:
            self.issue_id.sudo().button_reject()
            self.update({"state": "rejected"})


