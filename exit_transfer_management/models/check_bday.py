from odoo import models, fields, api

class PendingCheckBirthday(models.Model):
    _name = "pending.check.birthday"
    _description = "Pending Check Birthday"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    check_id = fields.Many2one("cheque.requests", string="Check Id")
    employee_id = fields.Many2one('hr.employee', string="Employee Id")
    name = fields.Char(string='Employee Name')
    birthday = fields.Date('Date of Birth') #groups="hr.group_hr_user
    state = fields.Selection(
        [('draft', 'Draft'),
         ('to_approve', 'To Approve'),
         ('approved', 'Approved'),
         ('rejected', 'Rejected')
         ], required=True, default='draft')

    def button_approved(self):
        if self.check_id:
            self.check_id.sudo().button_approved()
            self.update({"state": "approved"})

    def button_reject(self):
        if self.check_id:
            self.check_id.sudo().button_reject()
            self.update({"state": "rejected"})

class SubmittedCheckBirthday(models.Model):
    _name = "submitted.check.birthday"
    _description = "Submitted Check Birthday"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    check_id = fields.Many2one("cheque.requests", string="Check Id")
    employee_id = fields.Many2one('hr.employee', string="Employee Id")
    name = fields.Char(string='Employee Name')
    birthday = fields.Date('Date of Birth') #groups="hr.group_hr_user
    state = fields.Selection(
        [('draft', 'Draft'),
         ('to_approve', 'To Approve'),
         ('approved', 'Approved'),
         ('rejected', 'Rejected')
         ], required=True, default='draft')

    def button_reject(self):
        if self.check_id:
            self.check_id.sudo().button_reject()
            self.update({"state": "rejected"})

class UpcomingCheckBirthday(models.Model):
    _name = "upcoming.check.birthday"
    _description = "Upcoming Check Birthday"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    check_id = fields.Many2one("cheque.requests", string="Check Id")
    employee_id = fields.Many2one('hr.employee', string="Employee Id")
    name = fields.Char(string='Employee Name')
    birthday = fields.Date('Date of Birth') #groups="hr.group_hr_user
    state = fields.Selection(
        [('draft', 'Draft'),
         ('to_approve', 'To Approve'),
         ('approved', 'Approved'),
         ('rejected', 'Rejected')
         ], required=True, default='draft')