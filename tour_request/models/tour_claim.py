from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError,UserError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import re

class EmployeeTourClaim(models.Model):
    _name = 'employee.tour.claim'
    _description = 'Tour Claim'

    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)


    @api.multi
    @api.depends('tour_request_id')
    def _compute_approved_amount(self):
        total_claimed = 0.0
        advance_requested = 0.0
        for record in self:
            record.advance_requested = record.tour_request_id.advance_requested
            for line in record.detail_of_journey_lodging:
                if line:
                    total_claimed += ((line.daily_lodging_charge + line.daily_boarding_charge + line.daily_boarding_lodginf_charge)*line.no_of_days + line.other_details)
            record.total_claimed_amount = total_claimed
            record.balance_left = record.total_claimed_amount - record.advance_requested - record.amount_paid


    employee_id = fields.Many2one('hr.employee', string='Employee', default=_default_employee)
    designation = fields.Many2one('hr.job', string="Designation", compute='compute_des_dep')
    department = fields.Many2one('hr.department', string="Department", compute='compute_des_dep', store=True)
    tour_request_id = fields.Many2one('tour.request', string='Select Tour', store=True)
    detail_of_journey = fields.One2many('tour.claim.journey','employee_journey')
    detail_of_journey_lodging = fields.One2many('tour.claim.journey.lodging','employee_journey')
    detail_of_journey_leave = fields.One2many('employee.leave.taken','employee_journey')
    advance_requested = fields.Float(string="Advance Requested", readonly=True, compute='_compute_approved_amount')
    balance_left = fields.Float(string="Balance left", readonly=True, compute='_compute_approved_amount')
    tour_sequence = fields.Char(string="tour sequence")
    total_claimed_amount = fields.Float(string="Total Claimed Amount", compute='_compute_approved_amount')
    amount_paid = fields.Float(string="Amount Paid")

    from_date_camp = fields.Date(string='From Date')
    to_date_camp = fields.Date(string='To Date')

    leave_taken = fields.Many2one('hr.leave', string='Date of absence from place of halt ')
    state = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Waiting for Approval'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('paid', 'Paid')
         ], required=True, default='draft', string='Status')
    action_app = fields.Boolean('Action Approve bool', invisible=1)
    action_clos = fields.Boolean('Action Paid Close bool', invisible=1)


    @api.constrains('from_date_camp','to_date_camp')
    def check_date_system_halt(self):
        for record in self:
            lowest_from_date_camp = datetime.now().date()
            largest_to_date_camp = datetime.now().date()
            for f_d in record.tour_request_id.employee_journey:
                if f_d.departure_date <= lowest_from_date_camp:
                    lowest_from_date_camp = f_d.departure_date
                if f_d.arrival_date >= largest_to_date_camp:
                    largest_to_date_camp = f_d.arrival_date

            if record.from_date_camp and (record.from_date_camp < lowest_from_date_camp or record.from_date_camp > largest_to_date_camp):
                raise ValidationError(
                            "Please enter correct from date in 'Not being actually in camp on Sunday' ")

            if record.to_date_camp and (record.to_date_camp < lowest_from_date_camp or record.to_date_camp > largest_to_date_camp):
                raise ValidationError(
                            "Please enter correct to date in 'Not being actually in camp on Sunday' ")

            if record.from_date_camp and record.to_date_camp and record.from_date_camp > record.to_date_camp:
                raise ValidationError(
                            "Please enter correct to date in 'Not being actually in camp on Sunday'. From Date must be less than To Date ")




    @api.onchange('tour_request_id')
    @api.constrains('tour_request_id')
    def get_journey_details_tour(self,working_list=None):
        for rec in self:
            detail_of_journey = []
            detail_of_journey_lodging = []
            detail_of_journey_leave = []
            for i in rec.tour_request_id.employee_journey:
                detail_of_journey.append((0, 0, {
                    'employee_journey': rec.id,
                    'departure_date': i.departure_date,
                    'departure_time': i.departure_time,
                    'arrival_date': i.arrival_date,
                    'arrival_time': i.arrival_time,
                    'from_l': i.from_l.id,
                    'to_l': i.to_l.id,
                }))

            # rec.detail_of_journey.unlink()
            else:
                rec.detail_of_journey = working_list
            for i in rec.tour_request_id.employee_journey:
                detail_of_journey_leave.append((0, 0, {
                    'employee_journey': rec.id,
                    'employee_id': rec.employee_id.id,
                    'departure_date': i.departure_date,
                    'arrival_date': i.arrival_date,
                    'from_l': i.from_l.id,
                    'to_l': i.to_l.id,
                }))
            # rec.detail_of_journey_leave.unlink()
            else:
                rec.detail_of_journey_leave = working_list
            for i in rec.tour_request_id.employee_journey:
                detail_of_journey_lodging.append((0, 0, {
                    'employee_journey': rec.id,
                    'from_date': i.departure_date,
                    'to_date': i.arrival_date,
                    'from_l': i.from_l.id,
                    'to_l': i.to_l.id,
                    'travel_mode': i.travel_mode.id,
                    'mode_detail': i.mode_detail,
                    'travel_entitled': i.travel_entitled,
                    'boarding': i.boarding,
                    'lodging': i.lodging,
                    'conveyance': i.conveyance,
                }))
            # rec.detail_of_journey_lodging.unlink()
            else:
                rec.detail_of_journey_lodging = working_list
            rec.detail_of_journey = detail_of_journey
            rec.detail_of_journey_leave = detail_of_journey_leave
            rec.detail_of_journey_lodging = detail_of_journey_lodging



    @api.depends('employee_id')
    def compute_des_dep(self):
        for rec in self:
            rec.designation = rec.employee_id.job_id.id
            rec.department = rec.employee_id.department_id.id

    @api.multi
    def button_submit(self):
        for rec in self:
            rec.write({'state': 'submitted'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})

    @api.multi
    def unlink(self):
        for tour in self:
            if tour.state != 'draft':
                raise UserError(
                    'You cannot delete a Tour Claim which is not in draft state')
        return super(EmployeeTourClaim, self).unlink()

    @api.multi
    def button_reset_to_draft(self):
        self.ensure_one()
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        ctx = dict(
            default_composition_mode='comment',
            default_res_id=self.id,

            default_model='employee.tour.claim',
            default_is_log='True',
            custom_layout='mail.mail_notification_light'
        )
        mw = {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
        self.write({'state': 'draft'})
        return mw

    @api.multi
    def button_approved(self):
        for rec in self:
            rec.write({'state': 'approved'})

    def button_pay(self):
        for rec in self:
            rec.amount_paid = rec.total_claimed_amount - rec.advance_requested
            rec.tour_request_id.claimed = True
            rec.write({'state': 'paid'})


    @api.multi
    @api.depends('employee_id')
    def name_get(self):
        res = []
        name = ''
        for record in self:
            if record.employee_id:
                name = str(record.employee_id.name) + ' - Tour Claim'
            else:
                name = 'Tour Claim'
            res.append((record.id, name))
        return res


class TourClaimJourney(models.Model):
    _name = "tour.claim.journey"
    _description = "Tour Claim Journey Details"


    employee_journey = fields.Many2one('employee.tour.claim', string='Tour Claim')
    departure_date = fields.Date('Departure Date')
    arrival_date = fields.Date('Arrival Date')
    from_l = fields.Many2one('res.city', string='From City')
    to_l = fields.Many2one('res.city', string='To City')
    departure_time = fields.Float('Departure Time')
    arrival_time = fields.Float('Arrival Time')
    amount_claimed = fields.Float('Amount Claimed')
    distance = fields.Float('Distance')
    arranged_by = fields.Selection([('self', 'Self'), ('company', 'Company')], string='Arranged By')
    state = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Waiting for Approval'), ('approved', 'Approved'),
         ('rejected', 'Rejected'), ('paid', 'Paid')
         ], related='employee_journey.state')



class EmployeeLeaveTaken(models.Model):
    _name = 'employee.leave.taken'
    _description = 'Leave Taken'


    employee_id = fields.Many2one('hr.employee', string='Employee')
    employee_journey = fields.Many2one('employee.tour.claim', string='Tour Claim')
    departure_date = fields.Date('Departure Date')
    arrival_date = fields.Date('Arrival Date')

    from_l = fields.Many2one('res.city', string='From City')
    to_l = fields.Many2one('res.city', string='To City')
    leave_taken = fields.Many2one('hr.leave', string='Date of absence from place of halt ',
                                  domain="[('state','=','approved'),('request_date_from','<=',departure_date),('request_date_to','>=',arrival_date)]"
    )

    from_date_camp = fields.Date(string='From Date', compute='compute_get_leave_details')
    to_date_camp = fields.Date(string='To Date', compute='compute_get_leave_details')

    state = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Waiting for Approval'), ('approved', 'Approved'),
         ('rejected', 'Rejected'), ('paid', 'Paid')
         ], default='draft', string='Status', related='employee_journey.state')
    #
    @api.depends('leave_taken')
    def compute_get_leave_details(self):
        for line in self:
            if line.leave_taken:
                line.from_date_camp = line.leave_taken.request_date_from
                line.to_date_camp = line.leave_taken.request_date_to

class JourneyLodgingBoarding(models.Model):

    _name = "tour.claim.journey.lodging"
    _description = "Tour Claim Journey Details Lodging Boarding"

    @api.multi
    @api.depends('daily_lodging_charge', 'daily_boarding_charge', 'daily_boarding_lodginf_charge', 'no_of_days')
    def _Compute_total_amount_paid(self):
        for rec in self:
            pass
    #         rec.total_amount_paid = (rec.daily_lodging_charge + rec.daily_boarding_charge + rec.daily_boarding_lodginf_charge) * rec.no_of_days

    employee_journey = fields.Many2one('employee.tour.claim', string='Tour Claim')
    arranged_by = fields.Selection([('self', 'Self'), ('company', 'Company')], string='Arranged By')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    no_of_days = fields.Float('No. of days', compute='compute_no_of_days', store=True)
    travel_entitled = fields.Boolean('Is Travel Mode Entitled?')
    boarding = fields.Boolean('Boarding required?')
    lodging = fields.Boolean('Lodging required?')
    conveyance = fields.Boolean('Local Conveyance required?')

    name_of_hotel = fields.Char('Name of Hotel/Guest House')
    daily_lodging_charge = fields.Float('Daily Lodging Charges')
    daily_boarding_charge = fields.Float('Daily Boarding Charges')
    daily_boarding_lodginf_charge = fields.Float('Daily Lodging and Boarding Charges')
    total_amount_paid = fields.Float('Total Amount Paid', compute='_Compute_total_amount_paid')
    other_details = fields.Float('Details of other reimbursable expenses ')

    state = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Waiting for Approval'), ('approved', 'Approved'),
         ('rejected', 'Rejected'), ('paid', 'Paid')
         ], related='employee_journey.state')

    @api.constrains('from_date', 'to_date')
    def compute_no_of_days(self):
        for rec in self:
            no_of_days = (rec.to_date - rec.from_date).days
            rec.no_of_days = no_of_days


