# PF Request
pending_pf_req_ids = fields.One2many("pending.pf.request", "exit_transfer_id", string="Pending Vehicle Request")
submitted_pf_req_ids = fields.One2many("submitted.pf.request", "exit_transfer_id", string="Submitted Vehicle Request")
upcoming_pf_req_ids = fields.One2many("upcoming.pf.request", "exit_transfer_id", string="Upcoming Vehicle Request")

# PF Request
if self.pending_pf_req_ids:
    for line in self.pending_pf_req_ids:
        line.unlink()

if self.submitted_pf_req_ids:
    for line in self.submitted_pf_req_ids:
        line.unlink()

if self.upcoming_pf_req_ids:
    for line in self.upcoming_pf_req_ids:
        line.unlink()


pending_pf_req_ids = self.env['pf.widthdrawl'].search([("employee_id", "=", self.employee_id.id),
                                                  ("state", "in", ['draft', 'waiting_for_approval'])])
if pending_tour_req_ids:
    for res in pending_tour_req_ids:
        self.pending_tour_req_ids.create({
            "exit_transfer_id": self.id,
            "pf.widthdrawl": res.id,
            "employee_id": res.employee_id.id,
            "advance_amount": res.advance_amount,
            "purpose": res.purpose,
            "state": res.state
        })


submitted_pf_req_ids = self.env['pf.widthdrawl'].search([("employee_id", "=", self.employee_id.id),
                                                  ("state", "in", ['draft', 'waiting_for_approval'])])
if submitted_pf_req_ids:
    for res in submitted_pf_req_ids:
        self.submitted_pf_req_ids.create({
            "exit_transfer_id": self.id,
            "pf.widthdrawl": res.id,
            "employee_id": res.employee_id.id,
            "advance_amount": res.advance_amount,
            "purpose": res.purpose,
            "state": res.state
        })

upcoming_pf_req_ids = self.env['pf.widthdrawl'].search([("employee_id", "=", self.employee_id.id),
                                                  ("state", "in", ['draft', 'waiting_for_approval'])])
if upcoming_pf_req_ids:
    for res in upcoming_pf_req_ids:
        self.upcoming_pf_req_ids.create({
            "exit_transfer_id": self.id,
            "pf.widthdrawl": res.id,
            "employee_id": res.employee_id.id,
            "advance_amount": res.advance_amount,
            "purpose": res.purpose,
            "state": res.state
        })

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

