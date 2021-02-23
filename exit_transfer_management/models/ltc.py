from odoo import models, fields, api

#LTC and Request

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


# LTC Claim

class PendingLTCClaimRequest(models.Model):
    _name = 'pending.ltc.claim.request'
    _description = 'Pending Ltc Claim Request'

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    ltc_availed_for_id = fields.Many2one('employee.ltc.claim','LTC Claim ID',readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    place_of_trvel = fields.Selection(
        [('hometown', 'Hometown'), ('india', 'Anywhere in India'), ('conversion', 'Conversion of Hometown')],
         string='Place of Travel')
    total_claimed_amount = fields.Float('Total Claimed Amount')
    balance_left = fields.Float('Balance Left')
    ltc_availed_for_m2o = fields.Many2one('employee.ltc.advance','LTC availed for')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected')
    ], string='Status')

    def claim_approved(self):
        if self.ltc_availed_for_id:
            self.ltc_availed_for_id.sudo().button_approved()
            self.update({"state": "approved"})

    def claim_rejected(self):
        if self.ltc_availed_for_id:
            self.ltc_availed_for_id.sudo().button_reject()
            self.update({"state": "rejected"})

class LTCClaimRequest(models.Model):
    _name = 'ltc.claim.request'
    _description = 'Ltc Claim Request'

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    ltc_availed_for_id = fields.Many2one('employee.ltc.claim','LTC_Claim_ID',readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    place_of_trvel = fields.Selection(
        [('hometown', 'Hometown'), ('india', 'Anywhere in India'), ('conversion', 'Conversion of Hometown')],
         string='Place of Travel')
    total_claimed_amount = fields.Float('Total Claimed Amount')
    balance_left = fields.Float('Balance Left')
    ltc_availed_for_m2o = fields.Many2one('employee.ltc.advance','LTC availed for')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected')
    ], string='Status')

    def claim_cancel(self):
        if self.ltc_availed_for_id:
            self.ltc_availed_for_id.sudo().button_cancel()
            self.update({"state": "cancelled"})



class UpcomingLTCClaimRequest(models.Model):
    _name = 'upcoming.ltc.claim.request'
    _description = 'Upcoming Ltc Claim Request'

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    ltc_availed_for_id = fields.Many2one('employee.ltc.claim','LTC_Claim_ID',readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    place_of_trvel = fields.Selection(
        [('hometown', 'Hometown'), ('india', 'Anywhere in India'), ('conversion', 'Conversion of Hometown')],
         string='Place of Travel')
    total_claimed_amount = fields.Float('Total Claimed Amount')
    ltc_availed_for_m2o = fields.Many2one('employee.ltc.advance','LTC availed for')
    balance_left = fields.Float('Balance Left')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected')
    ], string='Status')