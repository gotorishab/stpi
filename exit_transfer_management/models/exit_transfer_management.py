
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

    # LTC and Claim
    ltc_sequence_ids = fields.One2many("employee.ltc.request", "exit_transfer_id", string="Submitted Lines")
    pending_ltc_sequence_ids = fields.One2many("pending.employee.ltc.request", "exit_transfer_id", string="Upcoming Lines")
    upcoming_ltc_sequence_ids = fields.One2many("upcoming.employee.ltc.request", "exit_transfer_id", string="Upcoming Lines")

    claim_lines1_ids = fields.One2many("claim.lines1","exit_transfer_id", string="Upcoming Lines")

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

        # LTC and Claim
        if self.pending_ltc_sequence_ids:
            for line in self.pending_ltc_sequence_ids:
                line.unlink()

        if self.sumbitted_sequence_ids:
            for line in self.sumbitted_sequence_ids:
                line.unlink()

        if self.upcoming_ltc_sequence_ids:
            for line in self.upcoming_ltc_sequence_ids:
                line.unlink()

        pending_ltc_sequence_ids = self.env['employee.ltc.advance'].search([("employee_id", "=", self.employee_id.id),
                                                                            ("state", "in", ['draft', 'to_approve'])])

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

        sumbitted_sequence_ids = self.env['employee.ltc.advance'].search([("employee_id", "=", self.employee_id.id),
                                                                          ("state", "in", ['draft', 'to_approve'])])

        if sumbitted_sequence_ids:
            for res in sumbitted_sequence_ids:
                self.sumbitted_sequence_ids.create({
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

#LTC and Claim
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
        ('cancel', 'Cancelled'),
        ('rejected', 'Rejected')
    ], string='Status')

    def ltc_cancel(self):
        if self.exit_transfer_id:
            self.exit_transfer_id.update({"state":"cancel"})
            self.update({"state":"cancel"})


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

    def leave_approved(self):
        if self.ltc_sequence_id:
            self.ltc_sequence_id.update({"state":"approved"})
            self.update({"state":"approved"})

    def leave_rejected(self):
        if self.ltc_sequence_id:
            self.ltc_sequence_id.update({"state":"rejected"})
            self.update({"state":"rejected"})


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
        ('cancel', 'Cancelled'),
        ('rejected', 'Rejected')
    ], string='Status')

    def leave_cancel(self):
        if self.ltc_sequence_id:
            self.ltc_sequence_id.update({"state":"cancel"})
            self.update({"state":"cancel"})