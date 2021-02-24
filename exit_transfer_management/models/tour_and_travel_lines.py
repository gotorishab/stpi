from odoo import models, fields, api


class PendingTourAndTravelLine(models.Model):
    _name = 'pending.tour.request'
    _description = 'Pending Tours request'

    exit_transfer_id = fields.Many2one("exit.transfer.management", string ="Exit/Transfer Id", readonly=True)
    tour_request_id = fields.Many2one("tour.request",string="Tour Request Id")
    purpose = fields.Char("Purpose")
    request_date = fields.Date("Requester Date")
    state = fields.Selection([("draft","Draft"),
                              ("waiting_for_approval","Waiting For Approval"),
                              ("approved","Approved"),
                              ("rejected","Rejected"),
                              ],string="Status")

    def tour_approved(self):
        if self.tour_request_id:
            self.tour_request_id.sudo().button_approved()
            self.update({"state":"approved"})

    def tour_rejected(self):
        if self.tour_request_id:
            self.tour_request_id.sudo().button_reject()
            self.update({"state":"rejected"})

class SubmittedTourAndTravelLine(models.Model):
    _name = 'submitted.tour.request'
    _description = 'Pending Tours request'

    exit_transfer_id = fields.Many2one("exit.transfer.management", string ="Exit/Transfer Id", readonly=True)
    tour_request_id = fields.Many2one("tour.request",string="Tour Request Id")
    purpose = fields.Char("Purpose")
    request_date = fields.Date("Requester Date")
    state = fields.Selection([("draft","Draft"),
                              ("waiting_for_approval","Waiting For Approval"),
                              ("approved","Approved"),
                              ("rejected","Rejected"),
                              ],string="Status")


    def tour_cancel(self):
        if self.tour_request_id:
            self.tour_request_id.update({"state":"draft"})
            self.update({"state":"draft"})

class upcomingTourAndTravelLine(models.Model):
    _name = 'upcoming.tour.request'
    _description = 'Pending Tours request'

    exit_transfer_id = fields.Many2one("exit.transfer.management", string ="Exit/Transfer Id", readonly=True)
    tour_request_id = fields.Many2one("tour.request",string="Tour Request Id")
    purpose = fields.Char("Purpose")
    request_date = fields.Date("Requester Date")
    state = fields.Selection([("draft","Draft"),
                              ("waiting_for_approval","Waiting For Approval"),
                              ("approved","Approved"),
                              ("rejected","Rejected"),
                              ],string="Status")
#Tour Claim
class PendingTourClaimRequest(models.Model):
    _name = "pending.tour.claim.request"
    _description = "Pending Tour Claim Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    tour_claim_id = fields.Many2one('employee.tour.claim', string='Tour Claim Id')
    total_claimed_amount = fields.Float('Total Claimed Amount')
    balance_left = fields.Float(string="Balance left")
    state = fields.Selection([("draft", "Draft"),
                              ("waiting_for_approval", "Waiting For Approval"),
                              ("approved", "Approved"),
                              ("rejected", "Rejected"),
                              ], string="Status")
    def tourclaim_approved(self):
        if self.tour_claim_id:
            self.tour_claim_id.button_approved()
            self.update({"state":"approved"})

    def tourclaim_rejected(self):
        if self.tour_claim_id:
            self.tour_claim_id.button_reject()
            self.update({"state":"rejected"})

class SubmittedTourClaimRequest(models.Model):
    _name = "submitted.tour.claim.request"
    _description = "Pending Tour Claim Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    tour_claim_id = fields.Many2one('employee.tour.claim', string='Tour Claim Id')
    total_claimed_amount = fields.Float('Total Claimed Amount')
    balance_left = fields.Float(string="Balance left")
    state = fields.Selection([("draft", "Draft"),
                              ("waiting_for_approval", "Waiting For Approval"),
                              ("approved", "Approved"),
                              ("rejected", "Rejected"),
                              ], string="Status")

    def tourclaim_cancel(self):
        if self.tour_claim_id:
            self.tour_claim_id.update({"state":"draft"})
            self.update({"state":"draft"})


class UpcomingTourClaimRequest(models.Model):
    _name = "upcoming.tour.claim.request"
    _description = "Pending Tour Claim Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    tour_claim_id = fields.Many2one('employee.tour.claim', string='Tour Claim Id')
    total_claimed_amount = fields.Float('Total Claimed Amount')
    balance_left = fields.Float(string="Balance left")
    state = fields.Selection([("draft", "Draft"),
                              ("waiting_for_approval", "Waiting For Approval"),
                              ("approved", "Approved"),
                              ("rejected", "Rejected"),
                              ], string="Status")

class ClaimLines(models.Model):
    _name = 'claim.lines1'
    _description = 'claim Lines'
    exit_transfer_id = fields.Many2one("exit.transfer.management", string ="Exit/Transfer Id", readonly=True)
