
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
    employee_name = fields.Char(string="Employee", related="employee_id.name", store=True,copy=False)
    job_id = fields.Many2one("hr.job", string="Designation", compute="get_des_and_id", store=True,copy=False)
    branch_id = fields.Many2one("res.branch", string="Branch", compute="get_des_and_id", store=True,copy=False)
    department_id = fields.Many2one("hr.department", string="Department", compute="get_des_and_id", store=True,copy=False)
    employee_no = fields.Char(string="employee Id", compute="get_des_and_id", store=True,copy=False)
    exit_reason = fields.Text("Exit Reason")
    date = fields.Date('Date',default=fields.Date.context_today)
    exit_type = fields.Selection([("Suspended", "Suspended"),
                                  ("Resigned", "Resigned"),
                                  ("Contract Expired ", "Contract Expired "),
                                  ("Superannuation", "Superannuation"),
                                  ("Terminated","Terminated"),
                                  ("Deceased","Deceased"),
                                  ("Terminated","Terminated"),
                                  ("Absconding","Absconding"),
                                  ("Transferred","Transferred")
                               ],string='Type of Exit')
    dues_finance = fields.Selection([("Yes", "Yes"),
                                  ("No", "No"),
                               ],string='No Dues', store=True)
    employee_finance = fields.Many2one("hr.employee", string='Employee Name', store=True)
    remarks_finance = fields.Char("Remarks", store=True)
    dues_general = fields.Selection([("Yes", "Yes"),
                                  ("No", "No"),
                               ],string='No Dues', store=True)
    employee_general = fields.Many2one("hr.employee", string='Employee Name', store=True)
    remarks_general = fields.Char("Remarks", store=True)
    dues_personal = fields.Selection([("Yes", "Yes"),
                                  ("No", "No"),
                               ],string='No Dues', store=True)
    remarks_personal = fields.Char("Remarks", store=True)
    employee_personal = fields.Many2one("hr.employee", string='Employee Name', store=True)
    dues_technical = fields.Selection([("Yes", "Yes"),
                                  ("No", "No"),
                               ],string='No Dues', store=True)
    remarks_technical = fields.Char("Remarks", store=True)
    employee_technical = fields.Many2one("hr.employee", string='Employee Name', store=True)

    dues_ro = fields.Selection([("Yes", "Yes"),
                                  ("No", "No"),
                               ],string='No Dues', store=True)
    remarks_ro = fields.Char("Remarks", store=True)
    employee_ro = fields.Many2one("hr.employee", string='Employee Name', store=True)

    dues_remark_finance = fields.Selection([("Yes", "Yes"),
                                  ("No", "No"),
                               ],string='No Dues', store=True)
    employee_remark_finance = fields.Many2one("hr.employee", string='Employee Name', store=True)
    remarks_remark_finance = fields.Char("Remarks", store=True)
    dues_remark_general = fields.Selection([("Yes", "Yes"),
                                  ("No", "No"),
                               ],string='No Dues', store=True)
    employee_remark_general = fields.Many2one("hr.employee", string='Employee Name', store=True)
    remarks_remark_general = fields.Char("Remarks", store=True)
    dues_remark_personal = fields.Selection([("Yes", "Yes"),
                                  ("No", "No"),
                               ],string='No Dues', store=True)
    remarks_remark_personal = fields.Char("Remarks", store=True)
    employee_remark_personal = fields.Many2one("hr.employee", string='Employee Name', store=True)
    dues_remark_technical = fields.Selection([("Yes", "Yes"),
                                  ("No", "No"),
                               ],string='No Dues', store=True)
    remarks_remark_technical = fields.Char("Remarks", store=True)
    employee_remark_technical = fields.Many2one("hr.employee", string='Employee Name', store=True)

    dues_remark_ro = fields.Selection([("Yes", "Yes"),
                                  ("No", "No"),
                               ],string='No Dues', store=True)
    remarks_remark_ro = fields.Char("Remarks", store=True)
    employee_remark_ro = fields.Many2one("hr.employee", string='Employee Name', store=True)

    state = fields.Selection([("draft", "Draft"),
                               ("verify", "Verify"),
                               ("send_for_approval", "Approval Waiting"),
                               ("complete", "Completed"),
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

    # income Tax
    pending_income_tax_ids = fields.One2many("pending.income.tax.request", "exit_transfer_id", string="Pending Income Tax request")
    submitted_income_tax_ids = fields.One2many("submitted.income.tax.request", "exit_transfer_id", string="Submitted Income Tax request")
    upcoming_income_tax_ids = fields.One2many("upcoming.income.tax.request", "exit_transfer_id", string="Upcoming Income Tax request")

    # income Tax
    pending_loan_request_ids = fields.One2many("pending.hr.loan.request", "exit_transfer_id", string="Pending Loan request")
    submitted_loan_request_ids = fields.One2many("submitted.hr.loan.request", "exit_transfer_id", string="Submitted Loan request")
    upcoming_loan_request_ids = fields.One2many("upcoming.hr.loan.request", "exit_transfer_id", string="Upcoming Loan request")
    not_transferrred_loan_request_ids = fields.One2many("nottransferred.hr.loan.request", "exit_transfer_id", string="Completed Loan request")

    # eFile
    my_correspondence_ids = fields.One2many("correspondence.exit.management", "exit_transfer_id", string="Correspondence")
    my_file_ids = fields.One2many("file.exit.management", "exit_transfer_id", string="Files")

    #Indent
    pending_indent_req_ids = fields.One2many("pending.indent.request", "exit_transfer_id", string="Pending Indent Request")
    submitted_indent_req_ids = fields.One2many("submitted.indent.request", "exit_transfer_id", string="Submitted Indent Request")
    upcoming_indent_req_ids = fields.One2many("upcoming.indent.request", "exit_transfer_id", string="Upcoming Indent Request")

    #GRN
    pending_grn_ids = fields.One2many("pending.grn", "exit_transfer_id",string="Pending Indent Request")
    submitted_grn_ids = fields.One2many("submitted.grn", "exit_transfer_id",string="Submitted Indent Request")
    upcoming_grn_ids = fields.One2many("upcoming.grn", "exit_transfer_id",string="Upcoming Indent Request")

    #Issue Request
    pending_issue_req_ids = fields.One2many("pending.issue.request", "exit_transfer_id",string="Pending Issue Request")
    submitted_issue_req_ids = fields.One2many("submitted.issue.request","exit_transfer_id",string="Submitted Issue Request" )
    upcoming_issue_req_ids = fields.One2many("upcoming.issue.request","exit_transfer_id",string="Upcoming Issue Request" )

    #GRN Request
    pending_grn_req_ids = fields.One2many("pending.grn.request", "exit_transfer_id",string="Pending GRN Request")
    submitted_grn_req_ids = fields.One2many("submitted.grn.request", "exit_transfer_id",string="Pending GRN Request")
    upcoming_grn_req_ids = fields.One2many("upcoming.grn.request", "exit_transfer_id",string="Pending GRN Request")

    #check birthday
    pending_check_birth_ids = fields.One2many("pending.check.birthday", "exit_transfer_id",string="Pending Check Birthday Request")
    submitted_check_birth_ids = fields.One2many("submitted.check.birthday", "exit_transfer_id",string="Submitted Check Birthday Request")
    upcoming_check_birth_ids = fields.One2many("upcoming.check.birthday" , "exit_transfer_id",string="Upcoming Check Birthday Request")

    #reimbursement
    pending_reimbursement_ids = fields.One2many("pending.reimbursement.request", "exit_transfer_id",string="Pending Reimbursement Request")
    submitted_reimbursement_ids = fields.One2many("submitted.reimbursement.request", "exit_transfer_id",string="Submitted Reimbursement Request")
    upcoming_reimbursement_ids = fields.One2many("upcoming.reimbursement.request", "exit_transfer_id",string="Upcoming Reimbursement Request")


    claim_lines1_ids = fields.One2many("claim.lines1","exit_transfer_id", string="1`Upcoming Lines")

    leave_no_dues = fields.Boolean()
    leave_remark = fields.Text()

    @api.onchange('dues_finance')
    @api.constrains('dues_finance')
    def get_finance_employee(self):
        for res in self:
            me_emp = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            if me_emp:
                for employee in me_emp:
                    res.employee_finance = employee.id


    @api.onchange('dues_general')
    @api.constrains('dues_general')
    def get_general_employee(self):
        for res in self:
            me_emp = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            if me_emp:
                for employee in me_emp:
                    res.employee_general = employee.id


    @api.onchange('dues_personal')
    @api.constrains('dues_personal')
    def get_personal_employee(self):
        for res in self:
            me_emp = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            if me_emp:
                for employee in me_emp:
                    res.employee_personal = employee.id


    @api.onchange('dues_technical')
    @api.constrains('dues_finance')
    def get_technical_employee(self):
        for res in self:
            me_emp = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            if me_emp:
                for employee in me_emp:
                    res.employee_technical = employee.id


    @api.onchange('dues_ro')
    @api.constrains('dues_ro')
    def get_ro_employee(self):
        for res in self:
            me_emp = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            if me_emp:
                for employee in me_emp:
                    res.employee_ro = employee.id


    @api.model
    def create(self, vals):
        res = super(ExitTransferManagement, self).create(vals)
        sequence = ''
        seq = self.env['ir.sequence'].next_by_code('exit.transfer.management')
        sequence = 'Exit Management - ' + str(seq)
        res.name = sequence
        return res

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

        group_id = self.env.ref('hr_holidays.group_hr_holidays_manager')
        if group_id:
            for ln in group_id:
                for user in ln.users:
                    if user.id == self.employee_id.user_id.id:
                        # me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                        HrEmployees = self.env['hr.employee'].sudo().search([("branch_id", "=", self.employee_id.branch_id.id)])
                        pending_leaves_ids = self.env['hr.leave'].search([("employee_id","in",HrEmployees.ids),
                                                  ("state","in",['confirm','validate1'])])
                        if pending_leaves_ids:
                            for res in pending_leaves_ids:
                                self.pending_leave_line_ids.create({
                                    "exit_transfer_id": self.id,
                                    "employee_id": res.employee_id.id,
                                    "leave_id": res.id,
                                    "leave_type_id": res.holiday_status_id.id,
                                    "from_date": res.request_date_from,
                                    "to_date": res.request_date_to,
                                    "state": res.state
                                })


        submitted_leaves_ids = self.env['hr.leave'].search([("employee_id","=",self.employee_id.id),
                                                  ("state","in",['draft','confirm','validate1'])])

        upcoming_leave_line_ids = self.env['hr.leave'].search([("employee_id","=",self.employee_id.id),
                                                  ("request_date_from",">=",self.date),
                                                  ("state","in",['validate'])])

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

        group_id = self.env.ref('tour_request.group_tour_request_approvere')
        if group_id:
            for ln in group_id:
                for user in ln.users:
                    if user.id == self.employee_id.user_id.id:
                        # me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                        HrEmployees = self.env['hr.employee'].sudo().search(
                            [("branch_id", "=", self.employee_id.branch_id.id)])
                        pending_tour_req_ids = self.env['tour.request'].search([("employee_id", "in", HrEmployees.ids),
                                                                          ("state", "in", ['waiting_for_approval'])])
                        if pending_tour_req_ids:
                            for res in pending_tour_req_ids:
                                self.pending_tour_req_ids.create({
                                    "exit_transfer_id": self.id,
                                    "tour_request_id": res.id,
                                    "employee_id": res.employee_id.id,
                                    "purpose": res.purpose,
                                    "request_date": res.date,
                                    "state": res.state
                                })

        submitted_tour_req_ids = self.env['tour.request'].search([("employee_id", "=", self.employee_id.id),
                                                          ("state", "in", ['draft', 'waiting_for_approval'])])
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
                                                          ("date",">=",self.date),("state", "in", ['approved'])])
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

        group_id = self.env.ref('tour_request.group_tour_claim_approvere')
        if group_id:
            for ln in group_id:
                for user in ln.users:
                    if user.id == self.employee_id.user_id.id:
                        # me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                        HrEmployees = self.env['hr.employee'].sudo().search(
                            [("branch_id", "=", self.employee_id.branch_id.id)])
                        pending_tour_claim_req_ids = self.env['employee.tour.claim'].search(
                            [("employee_id", "in", HrEmployees.ids),
                             ("state", "in", ['waiting_for_approval'])])
                        if pending_tour_claim_req_ids:
                            for res in pending_tour_claim_req_ids:
                                self.pending_tour_claim_req_ids.create({
                                    "exit_transfer_id": self.id,
                                    "tour_claim_id": res.id,
                                    "employee_id": res.employee_id.id,
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


        group_id = self.env.ref('employee_ltc.group_ltc_manager')
        if group_id:
            for ln in group_id:
                for user in ln.users:
                    if user.id == self.employee_id.user_id.id:
                        # me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                        HrEmployees = self.env['hr.employee'].sudo().search(
                            [("branch_id", "=", self.employee_id.branch_id.id)])
                        pending_ltc_sequence_ids = self.env['employee.ltc.advance'].search([("employee_id", "in", HrEmployees.ids),
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

        group_id = self.env.ref('employee_ltc.group_ltc_manager')
        if group_id:
            for ln in group_id:
                for user in ln.users:
                    if user.id == self.employee_id.user_id.id:
                        # me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                        HrEmployees = self.env['hr.employee'].sudo().search(
                            [("branch_id", "=", self.employee_id.branch_id.id)])
                        pending_ltc_claim_ids = self.env["employee.ltc.claim"].search([("employee_id", "in", HrEmployees.ids),
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

        group_id = self.env.ref('employee_vehicle_request.group_employee_manager_v')
        if group_id:
            for ln in group_id:
                for user in ln.users:
                    if user.id == self.employee_id.user_id.id:
                        # me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                        HrEmployees = self.env['hr.employee'].sudo().search(
                            [("branch_id", "=", self.employee_id.branch_id.id)])
                        pending_vehicle_req_ids = self.env['employee.fleet'].search([("employee", "in", HrEmployees.ids),
                                                                                    ("state", "in", ['waiting'])])
                        if pending_vehicle_req_ids:
                            for res in pending_vehicle_req_ids:
                                self.pending_vehicle_req_ids.create({
                                    "exit_transfer_id": self.id,
                                    "vehicle_id": res.id,
                                    "employee_id": res.employee.id,
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
                    "employee_id": res.employee.id,
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
                    "employee_id": res.employee.id,
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

        group_id = self.env.ref('pf_withdrawl.group_pf_withdraw_approver')
        if group_id:
            for ln in group_id:
                for user in ln.users:
                    if user.id == self.employee_id.user_id.id:
                        # me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                        HrEmployees = self.env['hr.employee'].sudo().search(
                            [("branch_id", "=", self.employee_id.branch_id.id)])
                        pending_pf_req_ids = self.env['pf.widthdrawl'].search([("employee_id", "in", HrEmployees.ids),
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

        group_id = self.env.ref('appraisal_stpi.group_manager_appraisal')
        if group_id:
            for ln in group_id:
                for user in ln.users:
                    if user.id == self.employee_id.user_id.id:
                        # me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                        HrEmployees = self.env['hr.employee'].sudo().search(
                            [("branch_id", "=", self.employee_id.branch_id.id)])
                        pending_appraisal_request_ids = self.env['appraisal.main'].search([("employee_id", "in", HrEmployees.ids),
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

        # income tax
        if self.pending_income_tax_ids:
            for line in self.pending_income_tax_ids:
                line.unlink()

        if self.submitted_income_tax_ids:
            for line in self.submitted_income_tax_ids:
                line.unlink()

        if self.upcoming_income_tax_ids:
            for line in self.upcoming_income_tax_ids:
                line.unlink()

        group_id = self.env.ref('tds.group_manager_hr_declaration')
        if group_id:
            for ln in group_id:
                for user in ln.users:
                    if user.id == self.employee_id.user_id.id:
                        # me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                        HrEmployees = self.env['hr.employee'].sudo().search(
                            [("branch_id", "=", self.employee_id.branch_id.id)])
                        pending_income_tax_ids = self.env['hr.declaration'].search([("employee_id", "in", HrEmployees.ids),
                                                                                    ("state", "in", ['to_approve'])])
                        if pending_income_tax_ids:
                            for res in pending_income_tax_ids:
                                self.pending_income_tax_ids.create({
                                    "exit_transfer_id": self.id,
                                    "running_fy_id": res.id,
                                    "date_range_id": res.date_range.id,
                                    "employee_id": res.employee_id.id,
                                    "total_gross": res.tax_salary_final,
                                    "taxable_income": res.taxable_income,
                                    "tax_payable": res.tax_payable,
                                    "tax_paid": res.tax_paid,
                                    "total_rem": res.pending_tax,
                                    "state": res.state
                                })

        submitted_income_tax_ids = self.env['hr.declaration'].search([("employee_id", "=", self.employee_id.id),
                                                                      ("state", "in", ['draft', 'to_approve'])])

        if submitted_income_tax_ids:
            for res in submitted_income_tax_ids:
                self.submitted_income_tax_ids.create({
                    "exit_transfer_id": self.id,
                    "running_fy_id": res.id,
                    "date_range_id": res.date_range.id,
                    "employee_id": res.employee_id.id,
                    "total_gross": res.tax_salary_final,
                    "taxable_income": res.taxable_income,
                    "tax_payable": res.tax_payable,
                    "tax_paid": res.tax_paid,
                    "total_rem": res.pending_tax,
                    "state": res.state
                })

        upcoming_income_tax_ids = self.env['hr.declaration'].search([("employee_id", "=", self.employee_id.id),
                                                                     ("date", ">=", self.date),
                                                                     ("state", "in", ['approved'])])

        if upcoming_income_tax_ids:
            for res in upcoming_income_tax_ids:
                self.upcoming_income_tax_ids.create({
                    "exit_transfer_id": self.id,
                    "running_fy_id": res.id,
                    "date_range_id": res.date_range.id,
                    "employee_id": res.employee_id.id,
                    "total_gross": res.tax_salary_final,
                    "taxable_income": res.taxable_income,
                    "tax_payable": res.tax_payable,
                    "tax_paid": res.tax_paid,
                    "total_rem": res.pending_tax,
                    "state": res.state
                })



        # Loan
        if self.pending_loan_request_ids:
            for line in self.pending_loan_request_ids:
                line.unlink()

        if self.submitted_loan_request_ids:
            for line in self.submitted_loan_request_ids:
                line.unlink()



        group_id = self.env.ref('ohrms_loan.group_loan_approver')
        if group_id:
            for ln in group_id:
                for user in ln.users:
                    if user.id == self.employee_id.user_id.id:
                        # me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                        HrEmployees = self.env['hr.employee'].sudo().search(
                            [("branch_id", "=", self.employee_id.branch_id.id)])
                        pending_loan_request_ids = self.env['hr.loan'].search([("employee_id", "in", HrEmployees.ids),
                                                                                    ("state", "in", ['waiting_approval_1','waiting_approval_2'])])
                        if pending_loan_request_ids:
                            for res in pending_loan_request_ids:
                                self.pending_loan_request_ids.create({
                                    "exit_transfer_id": self.id,
                                    "loan_id": res.id,
                                    "type_id": res.type_id.id,
                                    "employee_id": res.employee_id.id,
                                    "installment": res.installment,
                                    "total_amount": res.total_amount,
                                    "total_interest": res.total_interest,
                                    "total_paid_amount": res.total_paid_amount,
                                    "balance_amount": res.balance_amount,
                                    "state": res.state
                                })

        submitted_loan_request_ids = self.env['hr.loan'].search([("employee_id", "=", self.employee_id.id),
                                                                      ("state", "in", ['waiting_approval_1', 'waiting_approval_2', 'draft'])])

        if submitted_loan_request_ids:
            for res in submitted_loan_request_ids:
                self.submitted_loan_request_ids.create({
                    "exit_transfer_id": self.id,
                    "loan_id": res.id,
                    "type_id": res.type_id.id,
                    "employee_id": res.employee_id.id,
                    "installment": res.installment,
                    "total_amount": res.total_amount,
                    "total_interest": res.total_interest,
                    "total_paid_amount": res.total_paid_amount,
                    "balance_amount": res.balance_amount,
                    "state": res.state
                })

        if self.exit_type == 'Transferred':
            if self.upcoming_loan_request_ids:
                for line in self.upcoming_loan_request_ids:
                    line.unlink()
            upcoming_loan_request_ids = self.env['hr.loan'].search([("employee_id", "=", self.employee_id.id),
                                                                         ("state", "in", ['approve']),('balance_amount', '!=', 0)],limit=1)

            if upcoming_loan_request_ids:
                paid = 0
                unpaid = 0
                for res in upcoming_loan_request_ids:
                    for line in res.loan_lines:
                        if line.paid:
                            paid+=1
                        else:
                            unpaid+=1
                    self.upcoming_loan_request_ids.create({
                        "exit_transfer_id": self.id,
                        "loan_id": res.id,
                        "no_of_emi_paid": paid,
                        "no_of_emi_pending": unpaid,
                    })
        else:
            if self.not_transferrred_loan_request_ids:
                for line in self.not_transferrred_loan_request_ids:
                    line.unlink()
            not_transferrred_loan_request_ids = self.env['hr.loan'].search([("employee_id", "=", self.employee_id.id),
                                                                         ("state", "in", ['approve']),('balance_amount', '!=', 0)],limit=1)

            if not_transferrred_loan_request_ids:
                paid = 0
                unpaid = 0
                for res in not_transferrred_loan_request_ids:
                    for line in res.loan_lines:
                        if line.paid:
                            paid+=1
                        else:
                            unpaid+=1
                    self.not_transferrred_loan_request_ids.create({
                        "exit_transfer_id": self.id,
                        "loan_id": res.id,
                        "no_of_emi_paid": paid,
                        "no_of_emi_pending": unpaid,
                    })

        # File management
        if self.my_correspondence_ids:
            for line in self.my_correspondence_ids:
                line.unlink()

        if self.my_file_ids:
            for line in self.my_file_ids:
                line.unlink()

        my_correspondence_ids = self.env['muk_dms.file'].search([("current_owner_id", "=", self.env.user.id)])

        if my_correspondence_ids:
            for res in my_correspondence_ids:
                self.my_correspondence_ids.create({
                    "exit_transfer_id": self.id,
                    "correspondence_id": res.id,
                    "letter_no": res.letter_number,
                    "file_assign_id": res.folder_id.id,
                })

        my_file_ids = self.env['folder.master'].search([("current_owner_id", "=", self.env.user.id)])

        if my_file_ids:
            for res in my_file_ids:
                self.my_file_ids.create({
                    "exit_transfer_id": self.id,
                    "file_name": res.folder_name,
                    "file_id": res.id,
                    "number": res.number,
                    "state": res.state
                })

        #Indent Request
        if self.pending_indent_req_ids:
            for line in self.pending_indent_req_ids:
                line.unlink()

        if self.submitted_indent_req_ids:
            for line in self.submitted_indent_req_ids:
                line.unlink()

        if self.upcoming_indent_req_ids:
            for line in self.upcoming_indent_req_ids:
                line.unlink()

        group_id = self.env.ref('indent_stpi.group_Indent_request_manager')
        if group_id:
            for ln in group_id:
                for user in ln.users:
                    if user.id == self.employee_id.user_id.id:
                        # me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                        HrEmployees = self.env['hr.employee'].sudo().search(
                            [("branch_id", "=", self.employee_id.branch_id.id)])
                        pending_indent_req_ids = self.env['indent.request'].search([("employee_id", "in", HrEmployees.ids),
                                                                                    ("state", "in", ['to_approve']),
                                                                                    ("indent_type", "in", ['issue'])])

                        if pending_indent_req_ids:
                            for res in pending_indent_req_ids:
                                self.pending_indent_req_ids.create({
                                    "exit_transfer_id": self.id,
                                    "number": res.indent_sequence,
                                    "indent_id": res.id,
                                    "employee_id": res.employee_id.id,
                                    "indent_type": res.indent_type,
                                    "state" : res.state,
                                })

        submitted_indent_req_ids = self.env['indent.request'].search([("employee_id", "=", self.employee_id.id),
                                                                    ("state", "in", ['draft', 'to_approve']),
                                                                      ("indent_type", "in", ['issue'])])

        if submitted_indent_req_ids:
            for res in submitted_indent_req_ids:
                self.submitted_indent_req_ids.create({
                    "exit_transfer_id": self.id,
                    "number": res.indent_sequence,
                    "indent_id": res.id,
                    "employee_id": res.employee_id.id,
                    "indent_type": res.indent_type,
                    "state": res.state,
                })

        upcoming_indent_req_ids = self.env['indent.request'].search([("employee_id", "=", self.employee_id.id),
                                                                     ("date_of_receive", ">=", self.date),#requested_date
                                                                      ("state", "in", ['approved']),
                                                                      ("indent_type", "in", ['issue']),
                                                                     ])

        if upcoming_indent_req_ids:
            for res in upcoming_indent_req_ids:
                self.upcoming_indent_req_ids.create({
                    "exit_transfer_id": self.id,
                    "number": res.indent_sequence,
                    "indent_id": res.id,
                    "employee_id": res.employee_id.id,
                    "indent_type": res.indent_type,
                    "state": res.state,
                })

        # GRN
        if self.pending_grn_ids:
            for line in self.pending_grn_ids:
                line.unlink()

        if self.submitted_grn_ids:
            for line in self.submitted_grn_ids:
                line.unlink()

        if self.upcoming_grn_ids:
            for line in self.upcoming_grn_ids:
                line.unlink()

        group_id = self.env.ref('indent_stpi.group_Indent_request_manager')
        if group_id:
            for ln in group_id:
                for user in ln.users:
                    if user.id == self.employee_id.user_id.id:
                        # me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                        HrEmployees = self.env['hr.employee'].sudo().search(
                            [("branch_id", "=", self.employee_id.branch_id.id)])
                        pending_grn_ids = self.env['indent.request'].search([("employee_id", "in", HrEmployees.ids),
                                                                                    ("state", "in", ['to_approve']),
                                                                                    ("indent_type", "in", ['grn'])])

                        if pending_grn_ids:
                            for res in pending_grn_ids:
                                self.pending_grn_ids.create({
                                    "exit_transfer_id": self.id,
                                    "number": res.indent_sequence,
                                    "indent_id": res.id,
                                    "employee_id": res.employee_id.id,
                                    "indent_type": res.indent_type,
                                    "state": res.state,
                                })

        submitted_grn_ids = self.env['indent.request'].search([("employee_id", "=", self.employee_id.id),
                                                                      ("state", "in", ['draft', 'to_approve']),
                                                                                    ("indent_type", "in", ['issue'])])

        if submitted_grn_ids:
            for res in submitted_grn_ids:
                self.submitted_grn_ids.create({
                    "exit_transfer_id": self.id,
                    "number": res.indent_sequence,
                    "indent_id": res.id,
                    "employee_id": res.employee_id.id,
                    "indent_type": res.indent_type,
                    "state": res.state,
                })

        upcoming_grn_ids = self.env['indent.request'].search([("employee_id", "=", self.employee_id.id),
                                                              ("date_of_receive", ">=", self.date),
                                                              ("state", "in", ['approved']),
                                                              ("indent_type", "in", ['issue'])])

        if upcoming_grn_ids:
            for res in upcoming_grn_ids:
                self.upcoming_grn_ids.create({
                    "exit_transfer_id": self.id,
                    "number": res.indent_sequence,
                    "indent_id": res.id,
                    "employee_id": res.employee_id.id,
                    "indent_type": res.indent_type,
                    "state": res.state,
                })

        # Issue Request
        if self.pending_issue_req_ids:
            for line in self.pending_issue_req_ids:
                line.unlink()

        if self.submitted_issue_req_ids:
            for line in self.submitted_issue_req_ids:
                line.unlink()

        if self.upcoming_issue_req_ids:
            for line in self.upcoming_issue_req_ids:
                line.unlink()

        group_id = self.env.ref('indent_stpi.group_issue_request_manager')
        if group_id:
            for ln in group_id:
                for user in ln.users:
                    if user.id == self.employee_id.user_id.id:
                        # me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                        HrEmployees = self.env['hr.employee'].sudo().search(
                            [("branch_id", "=", self.employee_id.branch_id.id)])
                        pending_issue_req_ids = self.env['issue.request'].search([("employee_id", "in", HrEmployees.ids),
                                                                                      ("state", "in", ['to_approve']),
                                                                                    ("indent_type", "in", ['issue'])])

                        if pending_issue_req_ids:
                            for res in pending_issue_req_ids:
                                self.pending_issue_req_ids.create({
                                    "exit_transfer_id": self.id,
                                    "employee_id": res.employee_id.id,
                                    "issue_id": res.id,
                                    "indent_grn": res.Indent_id.id,
                                    "item_category_id": res.item_category_id.id,
                                    "item_id": res.item_id.id,
                                    "requested_quantity": res.requested_quantity,
                                    "approved_quantity": res.approved_quantity,
                                    "state": res.state,
                                })

        submitted_issue_req_ids = self.env['issue.request'].search([("employee_id", "=", self.employee_id.id),
                                                               ("state", "in", ['draft', 'to_approve']),
                                                                     ("indent_type", "in", ['issue'])])
        if submitted_issue_req_ids:
            for res in submitted_issue_req_ids:
                self.submitted_issue_req_ids.create({
                    "exit_transfer_id": self.id,
                    "employee_id": res.employee_id.id,
                    "issue_id": res.id,
                    "indent_grn": res.Indent_id.id,
                    "item_category_id": res.item_category_id.id,
                    "item_id": res.item_id.id,
                    "requested_quantity": res.requested_quantity,
                    "approved_quantity": res.approved_quantity,
                    "state": res.state,
                })

        upcoming_issue_req_ids = self.env['issue.request'].search([("employee_id", "=", self.employee_id.id),
                                                                   ("requested_date", ">=", self.date),#approved_date
                                                                   ("state", "in", ['approved']),
                                                                   ("indent_type", "in", ['issue'])])
        if upcoming_issue_req_ids:
            for res in upcoming_issue_req_ids:
                self.upcoming_issue_req_ids.create({
                    "exit_transfer_id": self.id,
                    "employee_id": res.employee_id.id,
                    "issue_id": res.id,
                    "indent_grn": res.Indent_id.id,
                    "item_category_id": res.item_category_id.id,
                    "item_id": res.item_id.id,
                    "requested_quantity": res.requested_quantity,
                    "approved_quantity": res.approved_quantity,
                    "state": res.state,
                })

        #GRN Request
        if self.pending_grn_req_ids:
            for line in self.pending_grn_req_ids:
                line.unlink()

        if self.submitted_grn_req_ids:
            for line in self.submitted_grn_req_ids:
                line.unlink()

        if self.upcoming_grn_req_ids:
            for line in self.upcoming_grn_req_ids:
                line.unlink()

        group_id = self.env.ref('indent_stpi.group_issue_request_manager')
        if group_id:
            for ln in group_id:
                for user in ln.users:
                    if user.id == self.employee_id.user_id.id:
                        # me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                        HrEmployees = self.env['hr.employee'].sudo().search(
                            [("branch_id", "=", self.employee_id.branch_id.id)])
                        pending_grn_req_ids = self.env['issue.request'].search([("employee_id", "in", HrEmployees.ids),
                                                                                ("state", "in", ['to_approve']),
                                                                                    ("indent_type", "in", ['grn'])])
                        if pending_grn_req_ids:
                            for res in pending_grn_req_ids:
                                self.pending_grn_req_ids.create({
                                    "exit_transfer_id": self.id,
                                    "employee_id": res.employee_id.id,
                                    "issue_id": res.id,
                                    "indent_grn": res.Indent_id.id,
                                    "item_category_id": res.item_category_id.id,
                                    "item_id": res.item_id.id,
                                    "requested_quantity": res.requested_quantity,
                                    "approved_quantity": res.approved_quantity,
                                    "state": res.state,
                                })
        submitted_grn_req_ids = self.env['issue.request'].search([("employee_id", "=", self.employee_id.id),
                                                                     ("state", "in", ['draft', 'to_approve']),
                                                                  ("indent_type", "in", ['grn'])])
        if submitted_grn_req_ids:
            for res in submitted_grn_req_ids:
                self.submitted_grn_req_ids.create({
                    "exit_transfer_id": self.id,
                    "employee_id": res.employee_id.id,
                    "issue_id": res.id,
                    "indent_grn": res.Indent_id.id,
                    "item_category_id": res.item_category_id.id,
                    "item_id": res.item_id.id,
                    "requested_quantity": res.requested_quantity,
                    "approved_quantity": res.approved_quantity,
                    "state": res.state,
                })

        upcoming_grn_req_ids = self.env['issue.request'].search([("employee_id", "=", self.employee_id.id),
                                                                 ("requested_date", ">=", self.date),
                                                                 ("state", "in", ['approved']),
                                                                 ("indent_type", "in", ['grn'])])
        if upcoming_grn_req_ids:
            for res in upcoming_grn_req_ids:
                self.upcoming_grn_req_ids.create({
                    "exit_transfer_id": self.id,
                    "employee_id": res.employee_id.id,
                    "issue_id": res.id,
                    "indent_grn": res.Indent_id.id,
                    "item_category_id": res.item_category_id.id,
                    "item_id": res.item_id.id,
                    "requested_quantity": res.requested_quantity,
                    "approved_quantity": res.approved_quantity,
                    "state": res.state,
                })

        #Check Birthday
        if self.pending_check_birth_ids:
            for line in self.pending_check_birth_ids:
                line.unlink()

        if self.submitted_check_birth_ids:
            for line in self.submitted_check_birth_ids:
                line.unlink()

        if self.upcoming_check_birth_ids:
            for line in self.upcoming_check_birth_ids:
                line.unlink()

        group_id = self.env.ref('birthday_check.group_approvar_birthday')
        if group_id:
            for ln in group_id:
                for user in ln.users:
                    if user.id == self.employee_id.user_id.id:
                        # me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                        HrEmployees = self.env['hr.employee'].sudo().search(
                            [("branch_id", "=", self.employee_id.branch_id.id)])
                        pending_check_birth_ids = self.env['cheque.requests'].search([("employee_id", "in", HrEmployees.ids),
                                                                                ("state", "in", ['to_approve'])])

                        if pending_check_birth_ids:
                            for res in pending_check_birth_ids:
                                self.pending_check_birth_ids.create({
                                    "exit_transfer_id": self.id,
                                    "check_id": res.id,    #chek_id
                                    "employee_id": res.employee_id.id,
                                    "name": res.name,
                                    "birthday": res.birthday,
                                    "state": res.state,
                                })

        submitted_check_birth_ids = self.env['cheque.requests'].search([("employee_id", "=", self.employee_id.id),
                                                                      ("state", "in", ['draft', 'to_approve'])])

        if submitted_check_birth_ids:
            for res in submitted_check_birth_ids:
                self.submitted_check_birth_ids.create({
                    "exit_transfer_id": self.id,
                    "check_id": res.id,  # chek_id
                    "employee_id": res.employee_id.id,
                    "name": res.name,
                    "birthday": res.birthday,
                    "state": res.state,
                })

        upcoming_check_birth_ids = self.env['cheque.requests'].search([("employee_id", "=", self.employee_id.id),
                                                                       ("create_date", ">=", datetime.now()),#("birthday", ">=", self.birthday),
                                                                        ("state", "in", ['approved'])])

        if upcoming_check_birth_ids:
            for res in upcoming_check_birth_ids:
                self.upcoming_check_birth_ids.create({
                    "exit_transfer_id": self.id,
                    "check_id": res.id,  # chek_id
                    "employee_id": res.employee_id.id,
                    "name": res.name,
                    "birthday": res.birthday,
                    "state": res.state,
                })

        #reimbursement

        if self.pending_reimbursement_ids:
            for line in self.pending_reimbursement_ids:
                line.unlink()

        if self.submitted_reimbursement_ids:
            for line in self.submitted_reimbursement_ids:
                line.unlink()

        if self.upcoming_reimbursement_ids:
            for line in self.upcoming_reimbursement_ids:
                line.unlink()

        group_id = self.env.ref('reimbursement_stpi.group_approving_authority')
        if group_id:
            for ln in group_id:
                for user in ln.users:
                    if user.id == self.employee_id.user_id.id:
                        # me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                        HrEmployees = self.env['hr.employee'].sudo().search(
                            [("branch_id", "=", self.employee_id.branch_id.id)])
                        pending_reimbursement_ids = self.env['reimbursement'].search([("employee_id", "in", HrEmployees.ids),
                                                                                      ("state", "in", ['to_approve'])])
                        if pending_reimbursement_ids:
                            for res in pending_reimbursement_ids:
                                self.pending_reimbursement_ids.create({
                                    "exit_transfer_id": self.id,
                                    "reiburs_id": res.id,
                                    "employee_id": res.employee_id.id,
                                    "name": res.name,
                                    "claim_sub": res.date_range.id,
                                    "claimed_amount":res.claimed_amount,
                                    "net_amount": res.net_amount,
                                    "state": res.state,
                                })

        submitted_reimbursement_ids = self.env['reimbursement'].search([("employee_id", "=", self.employee_id.id),
                                                                      ("state", "in", ['draft','to_approve'])])
        if submitted_reimbursement_ids:
            for res in submitted_reimbursement_ids:
                self.submitted_reimbursement_ids.create({
                    "exit_transfer_id": self.id,
                    "reiburs_id": res.id,
                    "employee_id": res.employee_id.id,
                    "name": res.name,
                    "claim_sub": res.date_range.id,
                    "claimed_amount": res.claimed_amount,
                    "net_amount": res.net_amount,
                    "state": res.state,
                })

        upcoming_reimbursement_ids = self.env['reimbursement'].search([("employee_id", "=", self.employee_id.id),
                                                                       ("create_date", ">=", datetime.now()),
                                                                        ("state", "in", ['approved'])])
        if upcoming_reimbursement_ids:
            for res in upcoming_reimbursement_ids:
                self.upcoming_reimbursement_ids.create({
                    "exit_transfer_id": self.id,
                    "reiburs_id": res.id,
                    "employee_id": res.employee_id.id,
                    "name": res.name,
                    "claim_sub": res.date_range.id,
                    "claimed_amount": res.claimed_amount,
                    "net_amount": res.net_amount,
                    "state": res.state,
                })

        self.update({"state":"verify"})
        if self.employee_id.user_id:
            approval_date = datetime.now() + timedelta(days=2)
            self.activity_schedule(summary='Exit Transfer Management',activity_type_id=1,date_deadline=datetime.now().date(),user_id=self.employee_id.user_id.id)

    def button_confirm(self):
        for res in self:
            res.employee_remark_finance = res.employee_finance.id
            res.dues_remark_finance = res.dues_finance
            res.remarks_remark_finance = res.remarks_finance
            res.employee_remark_general = res.employee_general.id
            res.dues_remark_general = res.dues_general
            res.remarks_remark_general = res.remarks_general
            res.employee_remark_personal = res.employee_personal.id
            res.dues_remark_personal = res.dues_personal
            res.remarks_remark_personal = res.remarks_personal
            res.employee_remark_technical = res.employee_technical.id
            res.dues_remark_technical = res.dues_technical
            res.remarks_remark_technical = res.remarks_technical
            res.employee_remark_ro = res.employee_ro.id
            res.dues_remark_ro = res.dues_ro
            res.remarks_remark_ro = res.remarks_ro
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


    def leave_cancel(self):
        if self.exit_transfer_id:
            self.exit_transfer_id.update({"state":"cancel"})
            self.update({"state":"cancel"})

class PendingEmployeeLeave(models.Model):
    _name = "pending.leave.lines"
    _description = 'Pending Leave Lines'

    exit_transfer_id = fields.Many2one("exit.transfer.management", string ="Exit/Transfer Id", readonly=True)
    leave_id = fields.Many2one("hr.leave", string="Leave Id")
    leave_type_id = fields.Many2one("hr.leave.type", string="Leave Type")
    employee_id = fields.Many2one("hr.employee", string="Requested By")
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


