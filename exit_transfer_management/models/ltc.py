from odoo import models, fields, api

#LTC and Claim

class PendingEmployeeLtcRequest(models.Model):
    _name = 'pending.employee.ltc.request'
    _description = 'Ltc Request and Claim'

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    ltc_sequence_id = fields.Many2one("employee.ltc.advance", string='LTC number',readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    place_of_trvel = fields.Selection(
        [('hometown', 'Hometown'), ('india', 'Anywhere in India'), ('conversion', 'Conversion of Hometown')],
        default='hometown', string='Place of Travel', track_visibility='always')

    block_year_id = fields.Many2one('block.year', string='Block year')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('cancel', 'Cancelled'),
        ('rejected', 'Rejected')
    ], string='Status')

    def ltc_approved(self):
        if self.ltc_sequence_id:
            self.ltc_sequence_id.sudo().button_approved()
            self.update({"state":"approved"})

    def ltc_rejected(self):
        if self.ltc_sequence_id:
            self.ltc_sequence_id.sudo().button_reject()
            self.update({"state":"rejected"})

class EmployeeLtcRequest(models.Model):
    _name = 'employee.ltc.request'
    _description = 'Ltc Request and Claim'

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    ltc_sequence_id = fields.Many2one("employee.ltc.advance", string='LTC number',readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    place_of_trvel = fields.Selection(
        [('hometown', 'Hometown'), ('india', 'Anywhere in India'), ('conversion', 'Conversion of Hometown')],
        default='hometown', string='Place of Travel', track_visibility='always')

    block_year_id = fields.Many2one('block.year', string='Block year')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected')
    ], string='Status')

    def ltc_cancel(self):
        if self.ltc_sequence_id:
            self.ltc_sequence_id.sudo().button_cancel()
            self.update({"state": "cancelled"})



class UpcomingEmployeeLtcRequest(models.Model):
    _name = 'upcoming.employee.ltc.request'
    _description = 'Ltc Request and Claim'

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    ltc_sequence_id = fields.Many2one("employee.ltc.advance", string='LTC number',readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    place_of_trvel = fields.Selection(
        [('hometown', 'Hometown'), ('india', 'Anywhere in India'), ('conversion', 'Conversion of Hometown')],
        default='hometown', string='Place of Travel', track_visibility='always')

    block_year_id = fields.Many2one('block.year', string='Block year')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected')
    ], string='Status')

    def leave_cancel(self):
        if self.ltc_sequence_id:
            self.ltc_sequence_id.sudo().button_cancel()
            self.update({"state":"cancelled"})