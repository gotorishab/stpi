from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from datetime import datetime, date
import re

class TourRequest(models.Model):

    _name = "tour.request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Tour Request"


    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)


    employee_id = fields.Many2one('hr.employee', string="Requested By", default=_default_employee,track_visibility='always')
    date = fields.Date(string='Requested Date', default=fields.Date.today())
    designation = fields.Many2one('hr.job', string="Designation", compute='compute_des_dep')
    branch_id= fields.Many2one('res.branch', string="Branch", compute='compute_des_dep')
    department = fields.Many2one('hr.department', string="Department", compute='compute_des_dep')
    purpose = fields.Char(string="Purpose",track_visibility='always')
    employee_journey = fields.One2many('tour.request.journey','employee_journey', string="Employee Journey")
    tour_sequence = fields.Char('Tour number',track_visibility='always')
    claimed = fields.Boolean('Claimed')
    advance_requested = fields.Float('Advance Requested')
    vehicle_required = fields.Selection([('yes', 'Yes'), ('no', 'No')],string='Vehicle Required?',track_visibility='always')
    vehicle_address = fields.Char('Address')
    vehicle_phone = fields.Char("Phone Number")
    vehicle_date_from = fields.Date('Date')
    vehicle_day1 = fields.Selection([('full', 'Full'), ('half', 'Half')],string='Day:')
    vehicle_date_to = fields.Date('Returning Date')
    vehicle_day2 = fields.Selection([('full', 'Full'), ('half', 'Half')],string='Day:')
    vehicle_remarks = fields.Text('Remarks')


    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approval', 'Waiting for Approval'), ('approved', 'Approved'), ('rejected', 'Rejected')
                               ], required=True, string='Status', default='draft',track_visibility='always')

    @api.multi
    def button_to_approve(self):
        for rec in self:
            rec.write({'state': 'waiting_for_approval'})
    #
    # @api.multi
    # def button_forwarded(self):
    #     for rec in self:
    #         rec.write({'state': 'forwarded'})

    @api.multi
    def button_approved(self):
        for rec in self:
            rec.write({'state': 'approved'})

    # @api.multi
    # def button_processed(self):
    #     for rec in self:
    #         rec.write({'state': 'processed'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})

    @api.multi
    def button_reset_to_draft(self):
        self.ensure_one()
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        ctx = dict(
            default_composition_mode='comment',
            default_res_id=self.id,

            default_model='tour.request',
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

    @api.depends('employee_id')
    def compute_des_dep(self):
        for rec in self:
            rec.designation = rec.employee_id.job_id.id
            rec.department = rec.employee_id.department_id.id
            rec.branch_id = rec.employee_id.job_id.branch_id.id

    @api.multi
    @api.depends('employee_id')
    def name_get(self):
        res = []
        name = ''
        for record in self:
            if record.employee_id:
                name = record.employee_id.name + ' - Tour Request'
            else:
                name = 'Tour Request'
            res.append((record.id, name))
        return res


    @api.model
    def create(self, vals):
        res =super(TourRequest, self).create(vals)
        sequence = ''
        seq = self.env['ir.sequence'].next_by_code('tour.request')
        sequence = 'Tour Request - ' + seq
        res.tour_sequence = sequence
        return res

    @api.multi
    @api.depends('tour_sequence')
    def name_get(self):
        res = []
        for record in self:
            if record.tour_sequence:
                name = record.tour_sequence
            else:
                name = 'Tour Request'
            res.append((record.id, name))
        return res


class TourRequestJourney(models.Model):

    _name = "tour.request.journey"
    _description = "Tour Request Journey Details"

    employee_id = fields.Many2one('hr.employee', string="Employee", related='employee_journey.employee_id')
    employee_journey = fields.Many2one('tour.request')
    tour_sequence = fields.Char(related='employee_journey.tour_sequence', string='Tour Sequence')

    travel_mode = fields.Many2one('travel.mode', string='Mode of Travel')
    mode_detail = fields.Char('Flight/Train No.')
    mode_of_travlel = fields.Selection([('air', 'By Air'), ('train', 'By Train'), ('road', 'By Road'), ('sea', 'By Sea')], string='Mode of Travel')
    coc_air = fields.Selection([('first', 'First Class'), ('business', 'Business Class'), ('economy', 'Economy Class')], string='Class of Accomodation')
    coc_train = fields.Selection([('ac1', 'AC 1-Tier'), ('ac2', 'AC 2-Tier'), ('ac3', 'AC 3-Tier'), ('1st', 'First Class'), ('ac_chair', 'A.C Chair Class'), ('sleeper', 'Sleeper'), ('2nd_sit', 'Second Sitting')], string='Class of Accomodation')
    coc_bus = fields.Selection([('ac', 'AC'), ('n_ac', 'Non AC'), ('seater', 'Seater'), ('semi_sleep', 'Semi Sleeper'), ('sleeper', 'Sleeper')], string='Class of Accomodation')
    coc_sea = fields.Selection([('higher', 'Higher Class'), ('lower', 'Lower Class')], string='Class of Accomodation')
    departure_date = fields.Date('Departure Date')
    departure_time = fields.Float('Departure Time')
    arrival_time = fields.Float('Arrival Time')
    arrival_date = fields.Date('Arrival Date')
    from_l = fields.Many2one('res.city', string='From City')
    to_l = fields.Many2one('res.city', string='To City')
    travel_entitled = fields.Boolean('Is Travel Mode Entitled?')
    boarding = fields.Boolean('Boarding required?')
    lodging = fields.Boolean('Lodging required?')
    conveyance = fields.Boolean('Local Conveyance required?')




class EmployeeTourClaim(models.Model):
    _name = 'employee.tour.claim'
    _description = 'Tour Claim'




    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    @api.multi
    @api.depends('detail_of_journey')
    def _compute_approved_amount(self):
        pass
        total_claimed = 0.0
        total_approved = 0.0
        for record in self:
            for line in record.detail_of_journey:
                if line:
                    total_claimed += line.amount_claimed
                    total_approved += line.approved_approved
                record.total_claimed_amount = total_claimed
                record.total_approved_amount = total_approved
                record.balance_left = (record.total_claimed_amount) - record.total_approved_amount


    employee_id = fields.Many2one('hr.employee', string='Employee', default=_default_employee)
    designation = fields.Many2one('hr.job', string="Designation", compute='compute_des_dep')
    department = fields.Many2one('hr.department', string="Department", compute='compute_des_dep')
    detail_of_journey = fields.One2many('tour.claim.journey','employee_journey')
    balance_left = fields.Float(string="Balance left", readonly=True, compute='_compute_approved_amount')
    total_approved_amount = fields.Float(string="Total Approved Amount", compute='_compute_approved_amount',store=True)
    tour_sequence = fields.Char(string="tour sequence")
    total_claimed_amount = fields.Float(string="Total Claimed Amount", compute='_compute_approved_amount')

    state = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Waiting for Approval'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], required=True, default='draft', string='Status')

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
    def button_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    @api.multi
    def button_approved(self):
        for rec in self:
            rec.write({'state': 'approved'})

    @api.multi
    def get_journey_details(self):
        detail_of_journey = []
        for rec in self:
            rec.detail_of_journey.unlink()
            if rec.employee_id:
                tour_req = self.env['tour.request.journey'].search([('employee_id', '=', rec.employee_id.id)], order='tour_sequence desc')
                for i in tour_req:
                    detail_of_journey.append((0, 0, {
                        'tour_sequence': i.tour_sequence,
                        'departure_date': i.departure_date,
                        'arrival_date': i.arrival_date,
                        'from_l': i.from_l,
                        'to_l': i.to_l,
                        'employee_journey': self.id
                    }))
                self.detail_of_journey = detail_of_journey


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

    tour_sequence = fields.Char('Tour number')
    employee_journey = fields.Many2one('employee.tour.claim', invisible=1)
    departure_date = fields.Date('Departure Date')
    arrival_date = fields.Date('Arrival Date')
    from_l = fields.Many2one('res.city', string='From City')
    to_l = fields.Many2one('res.city', string='To City')
    arranged_by = fields.Selection([('self', 'Self'), ('company', 'Company')], string='Arranged By')
    amount_claimed = fields.Float('Amount Claimed')
    distance = fields.Float('Distance')
    approved_approved = fields.Float('Approved Amount')

    state = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Waiting for Approval'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], related='employee_journey.state')

    @api.constrains('approved_approved')
    @api.onchange('approved_approved')
    def onchange_approved_amount(self):
        for rec in self:
            if rec.amount_claimed and rec.approved_approved and rec.amount_claimed < rec.approved_approved:
                raise ValidationError(
                    _("Approved Amount must be less than or equal to Claimed amount")
                )


class TravelMode(models.Model):

    _name = "travel.mode"
    _description = "Travel Mode"

    name = fields.Char('Name')