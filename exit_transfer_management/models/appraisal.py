#Appraisal Request
pending_appraisal_request_ids = fields.One2many("pending.appraisal.request", "exit_transfer_id", string="Upcoming Vehicle Request")
submitted_appraisal_request_ids = fields.One2many("submitted.appraisal.request", "exit_transfer_id", string="Upcoming Vehicle Request")
upcoming_appraisal_request_ids = fields.One2many("upcoming.appraisal.request", "exit_transfer_id", string="Upcoming Vehicle Request")

#Appraisal Request
if self.pending_appraisal_request_ids:
    for line in self.pending_appraisal_request_ids:
        line.unlink()

if self.submitted_appraisal_request_ids:
    for line in self.submitted_appraisal_request_ids:
        line.unlink()

if self.upcoming_appraisal_request_ids:
    for line in self.upcoming_appraisal_request_ids:
        line.unlink()


pending_appraisal_request_ids = self.env['appraisal.main'].search([("employee_id", "=", self.employee_id.id),
                                                          ("state", "in", ['draft', 'self_review'])])
if pending_appraisal_request_ids:
    for res in pending_appraisal_request_ids:
        self.pending_appraisal_request_ids.create({
            "exit_transfer_id": self.id,
            "employee_id": res.employee_id.id,
            "abap_id": res.abap_id,
            "template_id": res.template_id,
            "state": res.state
        })


submitted_appraisal_request_ids = self.env['appraisal.main'].search([("employee_id", "=", self.employee_id.id),
                                                          ("state", "in", ['draft', 'self_review'])])
if submitted_appraisal_request_ids:
    for res in submitted_appraisal_request_ids:
        self.submitted_appraisal_request_ids.create({
            "exit_transfer_id": self.id,
            "employee_id": res.employee_id.id,
            "abap_id": res.abap_id,
            "template_id": res.template_id,
            "state": res.state
        })

upcoming_appraisal_request_ids = self.env['appraisal.main'].search([("employee_id", "=", self.employee_id.id),
                                                          ("state", "in", ['draft', 'self_review'])])
if upcoming_appraisal_request_ids:
    for res in upcoming_appraisal_request_ids:
        self.upcoming_appraisal_request_ids.create({
            "exit_transfer_id": self.id,
            "employee_id": res.employee_id.id,
            "abap_id": res.abap_id,
            "template_id": res.template_id,
            "state": res.state
        })
#Appraisal Request
class PendingAppraisalRequest(models.Model):
    _name = "pending.appraisal.request"
    _description = "Pending Appraisal Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    abap_id = fields.Many2one('appraisal.main', string='APAR Period')
    template_id = fields.Many2one('appraisal.main',string ='Template Id')
    state = fields.Selection([('draft', 'Draft'), ('self_review', 'Self Reviewed'),
                              ('reporting_authority_review', 'Reporting Authority Reviewed'),
                              ('reviewing_authority_review', 'Reviewing Authority Reviewed'),
                              ('completed', 'Completed'), ('raise_query', 'Raise Query'), ('rejected', 'Rejected')])

    def button_self_reviewed(self):
        if self.abap_id:
            self.abap_id.button_approved()
            self.update({"state":"self_review"})

    def button_reject(self):
        if self.abap_id:
            self.abap_id.button_reject()
            self.update({"state":"rejected"})


class SubmittedAppraisalRequest(models.Model):
    _name = "submitted.appraisal.request"
    _description = "Submitted Appraisal Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    abap_id = fields.Many2one('appraisal.main', string='APAR Period')
    template_id = fields.Many2one('appraisal.main',string ='Template Id')
    state = fields.Selection([('draft', 'Draft'), ('self_review', 'Self Reviewed'),
                              ('reporting_authority_review', 'Reporting Authority Reviewed'),
                              ('reviewing_authority_review', 'Reviewing Authority Reviewed'),
                              ('completed', 'Completed'), ('raise_query', 'Raise Query'), ('rejected', 'Rejected')])


class UpcomingAppraisalRequest(models.Model):
    _name = "upcoming.appraisal.request"
    _description = "Upcoming Appraisal Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    abap_id = fields.Many2one('appraisal.main', string='APAR Period')
    template_id = fields.Many2one('appraisal.main', string='Template Id')
    state = fields.Selection([('draft', 'Draft'), ('self_review', 'Self Reviewed'),
                              ('reporting_authority_review', 'Reporting Authority Reviewed'),
                              ('reviewing_authority_review', 'Reviewing Authority Reviewed'),
                              ('completed', 'Completed'), ('raise_query', 'Raise Query'), ('rejected', 'Rejected')])
