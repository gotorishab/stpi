from odoo import models, fields, api

# Vehicle Request
class CorrespondenceExitManagement(models.Model):
    _name = "correspondence.exit.management"
    _description = "Correspondence Exit Management"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    vehicle_id = fields.Many2one('employee.fleet', string='Vehicle Request_Id')
    from_location = fields.Char(string="From Location")
    to_location = fields.Char(string="To Location")
    state = fields.Selection([('draft', 'Draft'), ('waiting', 'Waiting for Approval'), ('cancel', 'Cancel'),
                              ('confirm', 'Approved'), ('reject', 'Rejected'), ('return', 'Returned')],
                             string="State", default="draft")

    def vehicle_approved(self):
        if self.vehicle_id:
            self.vehicle_id.button_approved()
            self.update({"state":"confirm"})

    def vehicle_rejected(self):
        if self.vehicle_id:
            self.vehicle_id.button_reject()
            self.update({"state":"reject"})

class SubmittedVehicleRequest(models.Model):
    _name = "file.exit.management"
    _description = "Submitted Vehicle Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    vehicle_id = fields.Many2one('employee.fleet', string='Vehicle Request_Id')
    from_location = fields.Char(string="From Location")
    to_location = fields.Char(string="To Location")
    state = fields.Selection([('draft', 'Draft'), ('waiting', 'Waiting for Approval'), ('cancel', 'Cancel'),
                              ('confirm', 'Approved'), ('reject', 'Rejected'), ('return', 'Returned')],
                             string="State", default="draft")

    def vehicle_cancel(self):
        if self.tour_claim_id:
            self.tour_claim_id.update({"state":"draft"})
            self.update({"state":"draft"})


class UpcomingVehicleRequest(models.Model):
    _name = "upcoming.vehicle.request"
    _description = "Upcoming Vehicle Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    vehicle_id = fields.Many2one('employee.fleet', string='Vehicle Request_Id')
    from_location = fields.Char(string="From Location")
    to_location = fields.Char(string="To Location")
    state = fields.Selection([('draft', 'Draft'), ('waiting', 'Waiting for Approval'), ('cancel', 'Cancel'),
                              ('confirm', 'Approved'), ('reject', 'Rejected'), ('return', 'Returned')],
                             string="State", default="draft")
