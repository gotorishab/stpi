# Vehicle Request
pending_vehile_req_ids = fields.One2many("pending.vehicle.request", "exit_transfer_id", string="Pending Vehicle Request")
submitted_vehile_req_ids = fields.One2many("submitted.vehicle.request", "exit_transfer_id", string="Submitted Vehicle Request")
upcoming_vehile_req_ids = fields.One2many("upcoming.vehicle.request", "exit_transfer_id", string="Upcoming Vehicle Request")



# Vehicle Request
if self.pending_vehile_req_ids:
    for line in self.pending_vehile_req_ids:
        line.unlink()

if self.submitted_vehile_req_ids:
    for line in self.submitted_vehile_req_ids:
        line.unlink()

if self.upcoming_vehile_req_ids:
    for line in self.upcoming_vehile_req_ids:
        line.unlink()

pending_vehile_req_ids = self.env['employee.fleet'].search([("employee_id", "=", self.employee_id.id),
                                                          ("state", "in", ['draft', 'waiting'])])
if pending_vehile_req_ids:
    for res in pending_vehile_req_ids:
        self.pending_vehile_req_ids.create({
            "exit_transfer_id": self.id,
            "vehicle_id": res.id,
            "from_location": res.from_location,
            "to_location": res.to_location,
            "state": res.state
        })

submitted_vehile_req_ids = self.env['employee.fleet'].search([("employee_id", "=", self.employee_id.id),
                                                          ("state", "in", ['draft', 'confirm'])])
if submitted_vehile_req_ids:
    for res in submitted_vehile_req_ids:
        self.submitted_vehile_req_ids.create({
            "exit_transfer_id": self.id,
            "vehicle_id": res.id,
            "from_location": res.from_location,
            "to_location": res.to_location,
            "state": res.state
        })

upcoming_vehile_req_ids = self.env['employee.fleet'].search([("employee_id", "=", self.employee_id.id),
                                                             ("date", ">=", self.date),
                                                             ("state", "in", ['draft', 'confirm'])])
if upcoming_vehile_req_ids:
    for res in upcoming_vehile_req_ids:
        self.upcoming_vehile_req_ids.create({
            "exit_transfer_id": self.id,
            "vehicle_id": res.id,
            "from_location": res.from_location,
            "to_location": res.to_location,
            "state": res.state
        })

# Vehicle Request
class PendingVehicleRequest(models.Model):
    _name = "pending.vehicle.request"
    _description = "Pending Vehicle Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    vehicle_id =fields.Many2one('employee.fleet', string='Vehicle Request_Id')
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
    _name = "submitted.vehicle.request"
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
