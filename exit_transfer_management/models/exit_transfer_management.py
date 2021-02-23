
# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime,timedelta

class ExitTransferManagement(models.Model):
    _name = 'exit.transfer.management'
    _description = 'Exit Transfer Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"

    @api.depends("employee_id")
    def get_des_and_id(self):
        if self.employee_id:
            self.job_id = self.employee_id.job_id.id
            self.employee_no = self.employee_id.identify_id
            self.branch_id = self.employee_id.branch_id.id
            self.department_id = self.employee_id.department_id.id

    name = fields.Char()
    employee_id = fields.Many2one("hr.employee", string="Employee Name")
    job_id = fields.Many2one("hr.job", string="Designation", compute="get_des_and_id", store=True,copy=False)
    branch_id = fields.Many2one("res.branch", string="Branch", compute="get_des_and_id", store=True,copy=False)
    department_id = fields.Many2one("hr.department", string="Department", compute="get_des_and_id", store=True,copy=False)
    employee_no = fields.Char(string="employee Id", compute="get_des_and_id", store=True,copy=False)
    exit_reason = fields.Text("Exit Reason")
    date = fields.Date('Date',default=fields.Date.context_today)
    state = fields.Selection([("draft", "Draft"),
                               ("verify", "Verify"),
                               ("send_for_approval", "Send for Approval"),
                               ("complete", "Approved"),
                               ("cancel","Cancel")
                               ],string='Status', copy=False, default='draft', required=True, readonly=True)
    leave_line_ids = fields.One2many("leave.lines","exit_transfer_id", string="Submitted Lines")
    pending_leave_line_ids = fields.One2many("pending.leave.lines","exit_transfer_id", string="Pending Lines")
    upcoming_leave_line_ids = fields.One2many("upcoming.leave.lines","exit_transfer_id", string="Upcoming Lines")

    pending_tour_req_ids = fields.One2many("pending.tour.request","exit_transfer_id", string="Upcoming Lines")
    submitted_tour_req_ids = fields.One2many("submitted.tour.request","exit_transfer_id", string="Upcoming Lines")
    upcoming_tour_req_ids = fields.One2many("upcoming.tour.request","exit_transfer_id", string="Upcoming Lines")

    # LTC and Advance
    pending_ltc_sequence_ids = fields.One2many("pending.employee.ltc.request", "exit_transfer_id",
                                               string="Pending for Approval LTC Advance")
    submitted_ltc_sequence_ids = fields.One2many("employee.ltc.request", "exit_transfer_id", string="Submitted LTC Advance")
    upcoming_ltc_sequence_ids = fields.One2many("upcoming.employee.ltc.request", "exit_transfer_id", string="Upcoming LTC Advance")

    # LTC Claim
    pending_ltc_claim_ids = fields.One2many("pending.ltc.claim.request", "exit_transfer_id", string="Pending  LTC Claim")
    submitted_ltc_claim_ids = fields.One2many("ltc.claim.request", "exit_transfer_id", string="Submitted  LTC Claim")
    upcoming_ltc_claim_ids = fields.One2many("upcoming.ltc.claim.request", "exit_transfer_id", string="Upcoming  LTC Claim")

    #tour Claim
    pending_tour_claim_req_ids = fields.One2many("pending.tour.claim.request", "exit_transfer_id", string="Pending Tour Claim")
    submitted_tour_claim_req_ids = fields.One2many("submitted.tour.claim.request", "exit_transfer_id", string=" Submitted Tour Claim")
    upcoming_tour_claim_req_ids = fields.One2many("upcoming.tour.claim.request", "exit_transfer_id", string=" Upcoming Tour Claim")

    # Vehicle Request
    pending_vehicle_req_ids = fields.One2many("pending.vehicle.request", "exit_transfer_id", string="Pending Vehicle Request")
    submitted_vehicle_req_ids = fields.One2many("submitted.vehicle.request", "exit_transfer_id", string="Submitted Vehicle Request")
    upcoming_vehicle_req_ids = fields.One2many("upcoming.vehicle.request", "exit_transfer_id", string="Upcoming Vehicle Request")

    # PF Request
    pending_pf_req_ids = fields.One2many("pending.pf.request", "exit_transfer_id", string="Pending Vehicle Request")
    submitted_pf_req_ids = fields.One2many("submitted.pf.request", "exit_transfer_id", string="Submitted Vehicle Request")
    upcoming_pf_req_ids = fields.One2many("upcoming.pf.request", "exit_transfer_id", string="Upcoming Vehicle Request")

    # Appraisal Request
    pending_appraisal_request_ids = fields.One2many("pending.appraisal.request", "exit_transfer_id", string="Upcoming Vehicle Request")
    submitted_appraisal_request_ids = fields.One2many("submitted.appraisal.request", "exit_transfer_id", string="Upcoming Vehicle Request")
    upcoming_appraisal_request_ids = fields.One2many("upcoming.appraisal.request", "exit_transfer_id", string="Upcoming Vehicle Request")

    claim_lines1_ids = fields.One2many("claim.lines1","exit_transfer_id", string="1`Upcoming Lines")

    leave_no_dues = fields.Boolean()
    leave_remark = fields.Text()

    @api.model
    def create(self, vals):
        if vals:
            vals.update({
                'name': self.env['ir.sequence'].get('exit.transfer.management')
            })
        result = super(ExitTransferManagement, self).create(vals)
        return result

    def button_verify(self):
        if self.pending_leave_line_ids:
            for line in self.pending_leave_line_ids:
                line.unlink()

        if self.leave_line_ids:
            for line in self.leave_line_ids:
                line.unlink()

        if self.upcoming_leave_line_ids:
            for line in self.upcoming_leave_line_ids:
                line.unlink()

        pending_leaves_ids = self.env['hr.leave'].search([("employee_id","=",self.employee_id.id),
                                                  ("state","in",['draft','confirm'])])


        submitted_leaves_ids = self.env['hr.leave'].search([("employee_id","=",self.employee_id.id),
                                                  ("state","in",['draft','confirm','validate1'])])

        upcoming_leave_line_ids = self.env['hr.leave'].search([("employee_id","=",self.employee_id.id),
                                                  ("request_date_from",">=",self.date),
                                                  ("state","in",['validate'])])

        if pending_leaves_ids:
            for res in pending_leaves_ids:
                self.pending_leave_line_ids.create({
                    "exit_transfer_id": self.id,
                    "leave_id": res.id,
                    "leave_type_id": res.holiday_status_id.id,
                    "from_date": res.request_date_from,
                    "to_date": res.request_date_to,
                    "state": res.state
                })


        if submitted_leaves_ids:
            for res in submitted_leaves_ids:
                self.leave_line_ids.create({
                    "exit_transfer_id": self.id,
                    "leave_id": res.id,
                    "leave_type_id": res.holiday_status_id.id,
                    "from_date": res.request_date_from,
                    "to_date": res.request_date_to,
                    "state": res.state
                })

        if upcoming_leave_line_ids:
            for res in upcoming_leave_line_ids:
                self.upcoming_leave_line_ids.create({
                    "exit_transfer_id": self.id,
                    "leave_id": res.id,
                    "leave_type_id": res.holiday_status_id.id,
                    "from_date": res.request_date_from,
                    "to_date": res.request_date_to,
                    "state": res.state
                })

        #tour and travel
        if self.pending_tour_req_ids:
            for line in self.pending_tour_req_ids:
                line.unlink()

        if self.submitted_tour_req_ids:
            for line in self.submitted_tour_req_ids:
                line.unlink()

        if self.upcoming_tour_req_ids:
            for line in self.upcoming_tour_req_ids:
                line.unlink()

        pending_tour_req_ids = self.env['tour.request'].search([("employee_id", "=", self.employee_id.id),
                                                          ("state", "in", ['draft', 'waiting_for_approval'])])
        if pending_tour_req_ids:
            for res in pending_tour_req_ids:
                self.pending_tour_req_ids.create({
                    "exit_transfer_id": self.id,
                    "tour_request_id": res.id,
                    "purpose": res.purpose,
                    "request_date": res.date,
                    "state": res.state
                })

        submitted_tour_req_ids = self.env['tour.request'].search([("employee_id", "=", self.employee_id.id),
                                                          ("state", "in", ['approved'])])
        if submitted_tour_req_ids:
            for res in submitted_tour_req_ids:
                self.submitted_tour_req_ids.create({
                    "exit_transfer_id": self.id,
                    "tour_request_id": res.id,
                    "purpose": res.purpose,
                    "request_date": res.date,
                    "state": res.state
                })

        upcoming_tour_req_ids = self.env['tour.request'].search([("employee_id", "=", self.employee_id.id),
                                                          ("date",">=",self.date)])
        if upcoming_tour_req_ids:
            for res in upcoming_tour_req_ids:
                self.upcoming_tour_req_ids.create({
                    "exit_transfer_id": self.id,
                    "tour_request_id": res.id,
                    "purpose": res.purpose,
                    "request_date": res.date,
                    "state": res.state
                })

        # tour claim
        if self.pending_tour_claim_req_ids:
            for line in self.pending_tour_claim_req_ids:
                line.unlink()

        if self.submitted_tour_claim_req_ids:
            for line in self.submitted_tour_claim_req_ids:
                line.unlink()

        if self.upcoming_tour_claim_req_ids:
            for line in self.upcoming_tour_claim_req_ids:
                line.unlink()

        pending_tour_claim_req_ids = self.env['employee.tour.claim'].search([("employee_id", "=", self.employee_id.id),
                                                                             ("state", "in",['waiting_for_approval'])])
        if pending_tour_claim_req_ids:
            for res in pending_tour_claim_req_ids:
                self.pending_tour_claim_req_ids.create({
                    "exit_transfer_id": self.id,
                    "tour_claim_id": res.id,
                    "total_claimed_amount": res.total_claimed_amount,
                    "balance_left": res.balance_left,
                    "state": res.state
                })

        submitted_tour_claim_req_ids = self.env['employee.tour.claim'].search([("employee_id", "=", self.employee_id.id),
                                                                               ("state", "in",['draft', 'waiting_for_approval'])])
        if submitted_tour_claim_req_ids:
            for res in submitted_tour_claim_req_ids:
                self.submitted_tour_claim_req_ids.create({
                    "exit_transfer_id": self.id,
                    "tour_claim_id": res.id,
                    "total_claimed_amount": res.total_claimed_amount,
                    "balance_left": res.balance_left,
                    "state": res.state
                })

        upcoming_tour_claim_req_ids = self.env['employee.tour.claim'].search([("employee_id", "=", self.employee_id.id),
                                                                              ("create_date", ">=", datetime.now()),
                                                                              ("state", "in", ['approved'])])
        if upcoming_tour_claim_req_ids:
            for res in upcoming_tour_claim_req_ids:
                self.upcoming_tour_claim_req_ids.create({
                    "exit_transfer_id": self.id,
                    "tour_claim_id": res.id,
                    "total_claimed_amount": res.total_claimed_amount,
                    "balance_left": res.balance_left,
                    "state": res.state
                })

        # LTC Advance
        if self.pending_ltc_sequence_ids:
            for line in self.pending_ltc_sequence_ids:
                line.unlink()

        if self.submitted_ltc_sequence_ids:
            for line in self.submitted_ltc_sequence_ids:
                line.unlink()

        if self.upcoming_ltc_sequence_ids:
            for line in self.upcoming_ltc_sequence_ids:
                line.unlink()

        pending_ltc_sequence_ids = self.env['employee.ltc.advance'].search([("employee_id", "=", self.employee_id.id),
                                                                            ("state", "in", ['to_approve'])])

        if pending_ltc_sequence_ids:
            for res in pending_ltc_sequence_ids:
                self.pending_ltc_sequence_ids.create({
                    "exit_transfer_id": self.id,
                    "ltc_sequence_id": res.id,
                    "employee_id": res.employee_id.id,
                    "place_of_trvel": res.place_of_trvel,
                    "block_year_id": res.block_year.id,
                    "state": res.state
                })

        submitted_ltc_sequence_ids = self.env['employee.ltc.advance'].search([("employee_id", "=", self.employee_id.id),
                                                                          ("state", "in", ['draft', 'to_approve'])])

        if submitted_ltc_sequence_ids:
            for res in submitted_ltc_sequence_ids:
                self.submitted_ltc_sequence_ids.create({
                    "exit_transfer_id": self.id,
                    "ltc_sequence_id": res.id,
                    "employee_id": res.employee_id.id,
                    "place_of_trvel": res.place_of_trvel,
                    "block_year_id": res.block_year.id,
                    "state": res.state
                })

        upcoming_ltc_sequence_ids = self.env['employee.ltc.advance'].search([("employee_id", "=", self.employee_id.id),
                                                                             ("depart_date", ">=", self.date),
                                                                             ("state", "in", ['approved'])])
        if upcoming_ltc_sequence_ids:
            for res in upcoming_ltc_sequence_ids:
                self.upcoming_ltc_sequence_ids.create({
                    "exit_transfer_id": self.id,
                    "ltc_sequence_id": res.id,
                    "employee_id": res.employee_id.id,
                    "place_of_trvel": res.place_of_trvel,
                    "block_year_id": res.block_year.id,
                    "state": res.state
                })


        # LTC Claim
        if self.pending_ltc_claim_ids:
            for line in self.pending_ltc_claim_ids:
                line.unlink()

        if self.submitted_ltc_claim_ids:
            for line in self.submitted_ltc_claim_ids:
                line.unlink()

        if self.upcoming_ltc_claim_ids:
            for line in self.upcoming_ltc_claim_ids:
                line.unlink()

        pending_ltc_claim_ids = self.env["employee.ltc.claim"].search([("employee_id", "=", self.employee_id.id),
                                                                       ("state", "in", ['to_approve'])])
        if pending_ltc_claim_ids:
            for res in pending_ltc_claim_ids:
                self.pending_ltc_claim_ids.create({
                    "exit_transfer_id": self.id,
                    "ltc_availed_for_id": res.id,
                    "employee_id": res.employee_id.id,
                    "ltc_availed_for_m2o": res.ltc_availed_for_m2o.id,
                    "place_of_trvel": res.place_of_trvel,
                    "total_claimed_amount": res.total_claimed_amount,
                    "balance_left": res.balance_left,
                    "state": res.state
                })

        submitted_ltc_claim_ids = self.env['employee.ltc.claim'].search([("employee_id", "=", self.employee_id.id),
                                                                         ("state", "in", ['draft', 'to_approve'])])

        if submitted_ltc_claim_ids:
            for res in submitted_ltc_claim_ids:
                self.submitted_ltc_claim_ids.create({
                    "exit_transfer_id": self.id,
                    "ltc_availed_for_id": res.id,
                    "ltc_availed_for_m2o": res.ltc_availed_for_m2o.id,
                    "employee_id": res.employee_id.id,
                    "place_of_trvel": res.place_of_trvel,
                    "total_claimed_amount": res.total_claimed_amount,
                    "balance_left": res.balance_left,
                    "state": res.state
                })

        upcoming_ltc_claim_ids = self.env['employee.ltc.claim'].search([("employee_id", "=", self.employee_id.id),
                                                                        ("create_date", ">=", datetime.now()),
                                                                        ("state", "in", ['approved'])])
        if upcoming_ltc_claim_ids:
            for res in upcoming_ltc_claim_ids:
                self.upcoming_ltc_claim_ids.create({
                    "exit_transfer_id": self.id,
                    "ltc_availed_for_id": res.id,
                    "ltc_availed_for_m2o": res.ltc_availed_for_m2o.id,
                    "employee_id": res.employee_id.id,
                    "place_of_trvel": res.place_of_trvel,
                    "total_claimed_amount": res.total_claimed_amount,
                    "balance_left": res.balance_left,
                    "state": res.state
                })

        # Vehicle Request
        if self.pending_vehicle_req_ids:
            for line in self.pending_vehicle_req_ids:
                line.unlink()

        if self.submitted_vehicle_req_ids:
            for line in self.submitted_vehicle_req_ids:
                line.unlink()

        if self.upcoming_vehicle_req_ids:
            for line in self.upcoming_vehicle_req_ids:
                line.unlink()

        pending_vehicle_req_ids = self.env['employee.fleet'].search([("employee", "=", self.employee_id.id),
                                                                    ("state", "in", ['waiting'])])
        if pending_vehicle_req_ids:
            for res in pending_vehicle_req_ids:
                self.pending_vehicle_req_ids.create({
                    "exit_transfer_id": self.id,
                    "vehicle_id": res.id,
                    "from_location": res.from_location,
                    "to_location": res.to_location,
                    "state": res.state
                })

        submitted_vehicle_req_ids = self.env['employee.fleet'].search([("employee", "=", self.employee_id.id),
                                                                      ("state", "in", ['draft', 'waiting'])])
        if submitted_vehicle_req_ids:
            for res in submitted_vehicle_req_ids:
                self.submitted_vehicle_req_ids.create({
                    "exit_transfer_id": self.id,
                    "vehicle_id": res.id,
                    "from_location": res.from_location,
                    "to_location": res.to_location,
                    "state": res.state
                })

        upcoming_vehicle_req_ids = self.env['employee.fleet'].search([("employee", "=", self.employee_id.id),
                                                                     ("req_date", ">=", self.date),
                                                                     ("state", "in", ['confirm'])])
        if upcoming_vehicle_req_ids:
            for res in upcoming_vehicle_req_ids:
                self.upcoming_vehicle_req_ids.create({
                    "exit_transfer_id": self.id,
                    "vehicle_id": res.id,
                    "from_location": res.from_location,
                    "to_location": res.to_location,
                    "state": res.state
                })

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
                                                               ("state", "in", ['to_approve'])])
        if pending_pf_req_ids:
            for res in pending_pf_req_ids:
                self.pending_pf_req_ids.create({
                    "exit_transfer_id": self.id,
                    "pf.widthdrawl": res.id,
                    "employee_id": res.employee_id.id,
                    "advance_amount": res.advance_amount,
                    "purpose": res.purpose,
                    "state": res.state
                })

        submitted_pf_req_ids = self.env['pf.widthdrawl'].search([("employee_id", "=", self.employee_id.id),
                                                                 ("state", "in", ['draft', 'to_approve'])])
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
                                                                ("date", ">=", self.date),
                                                                ("state", "in", ['approved'])])
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

        # Appraisal Request
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
                                                                           ("state", "in", ['self_review'])])
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
                                                                            ("create_date", ">=", datetime.now()),
                                                                            ("state", "in", ['reporting_authority_review'])])
        if upcoming_appraisal_request_ids:
            for res in upcoming_appraisal_request_ids:
                self.upcoming_appraisal_request_ids.create({
                    "exit_transfer_id": self.id,
                    "employee_id": res.employee_id.id,
                    "abap_id": res.abap_id,
                    "template_id": res.template_id,
                    "state": res.state
                })


        self.update({"state":"verify"})
        if self.employee_id.user_id:
            approval_date = datetime.now() + timedelta(days=2)
            self.activity_schedule(summary='Exit Transfer Management',activity_type_id=1,date_deadline=datetime.now().date(),user_id=self.employee_id.user_id.id)

    def button_confirm(self):
        self.update({"state":"complete"})

    def button_send_for_approval(self):
        self.update({"state":"send_for_approval"})

    def button_cancel(self):
        self.update({"state":"cancel"})

    def button_redraft(self):
        self.update({"state":"draft"})



class EmployeeLeave(models.Model):
    _name = "leave.lines"
    _description = 'Exit Transfer Management'

    exit_transfer_id = fields.Many2one("exit.transfer.management", string ="Exit/Transfer Id", readonly=True)
    leave_id = fields.Many2one("hr.leave", string="Leave Id")
    leave_type_id = fields.Many2one("hr.leave.type", string="Leave Type")
    from_date = fields.Date("From Date")
    to_date = fields.Date("To Date")
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('confirm', 'To Approval'),
        ('validate1', 'Second Approval'),
        ('cancel', 'Cancelled'),
        ('refuse', 'Refuse'),
        ('validate', 'Approved'),
    ], string ="Status")


    def tour_cancel(self):
        if self.exit_transfer_id:
            self.exit_transfer_id.update({"state":"cancel"})
            self.update({"state":"cancel"})

class PendingEmployeeLeave(models.Model):
    _name = "pending.leave.lines"
    _description = 'Pending Leave Lines'

    exit_transfer_id = fields.Many2one("exit.transfer.management", string ="Exit/Transfer Id", readonly=True)
    leave_id = fields.Many2one("hr.leave", string="Leave Id")
    leave_type_id = fields.Many2one("hr.leave.type", string="Leave Type")
    from_date = fields.Date("From Date")
    to_date = fields.Date("To Date")
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('confirm', 'To Approval'),
        ('validate1', 'Second Approval'),
        ('cancel', 'Cancelled'),
        ('refuse', 'Refuse'),
        ('validate', 'Approved'),
    ], string ="Status")

    def leave_approved(self):
        if self.leave_id:
            self.leave_id.update({"state":"validate"})
            self.update({"state":"validate"})

    def leave_rejected(self):
        if self.leave_id:
            self.leave_id.update({"state":"refuse"})
            self.update({"state":"refuse"})

class UpcomingEmployeeLeave(models.Model):
    _name = "upcoming.leave.lines"
    _description = 'Upcoming Leave Lines'

    exit_transfer_id = fields.Many2one("exit.transfer.management", string ="Exit/Transfer Id", readonly=True)
    leave_id = fields.Many2one("hr.leave", string="Leave Id")
    leave_type_id = fields.Many2one("hr.leave.type", string="Leave Type")
    from_date = fields.Date("From Date")
    to_date = fields.Date("To Date")
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('confirm', 'To Approval'),
        ('validate1', 'Second Approval'),
        ('cancel', 'Cancelled'),
        ('refuse', 'Refuse'),
        ('validate', 'Approved'),
    ], string ="Status")

    def leave_cancel(self):
        if self.leave_id:
            self.leave_id.update({"state":"cancel"})
            self.update({"state":"cancel"})

