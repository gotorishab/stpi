from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date




class EmployeeLtcAdvance(models.Model):
    _name = 'employee.ltc.advance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description='Advance Request'


    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    ltc_sequence = fields.Char('LTC number',track_visibility='always')
    employee_id = fields.Many2one('hr.employee', string='Employee', default=_default_employee,track_visibility='always')
    date = fields.Date(string="Requested Date", default=datetime.now().date(),track_visibility='always')
    place_of_trvel=fields.Selection([('hometown', 'Hometown'), ('india', 'Anywhere in India'), ('conversion', 'Conversion of Hometown')], default='hometown', string='Place of Travel',track_visibility='always')
    hometown_address = fields.Char(string='Address',track_visibility='always')
    block_year=fields.Char('Block year',track_visibility='always')
    slect_leave = fields.Many2one('hr.leave',string = 'Leave', domain="[('employee_id', '=', employee_id)]",track_visibility='always')
    leave_period = fields.Char(string = 'Leave period', compute='compute_get_leave_details',track_visibility='always')
    total_leaves = fields.Char(string = 'Total Leaves',track_visibility='always')
    left_leaves = fields.Char(string = 'Left Leaves',track_visibility='always')
    depart_date=fields.Date('Departue Date', compute='compute_get_leave_details',track_visibility='always')
    arrival_date=fields.Date('Arrival Date', compute='compute_get_leave_details',track_visibility='always')
    advance_ammount=fields.Char('Advance Amount Required',track_visibility='always')
    single_fare=fields.Float('Single Train Fare/ Bus fare from the office to Place of Visit by Shortest Route',track_visibility='always')
    single_fare_approved=fields.Float('Approved Amount',track_visibility='always')
    attach_file = fields.Binary('Attach a File',track_visibility='always')
    family_details = fields.Many2many('employee.relative', string='Family Details', domain="[('employee_id', '=', employee_id),('ltc', '=', True)]",track_visibility='always')
    partner_working=fields.Selection([('yes', 'Yes'), ('no', 'No')], default='no', string='Whether Wife/ Husband is employed and if so whether entitled to LTC',track_visibility='always')
    mode_of_travel=fields.Selection([('road', 'By Road'),('train', 'By Train'),('air', 'By Air')], default='road', string='Mode of Travel',track_visibility='always')
    el_encashment=fields.Selection([('yes', 'Yes'), ('no', 'No')], default='no', string='Require EL Encashment',track_visibility='always')
    no_of_days = fields.Float('No. of days', default='10',track_visibility='always')
    amount = fields.Char(string='Amount', compute='_compute_amount',track_visibility='always')
    total_basic_salary = fields.Char(string='Total Basic',track_visibility='always')
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
                               ], required=True, default='draft',track_visibility='always')



    @api.onchange('employee_id','place_of_trvel')
    def get_home_address(self):
        for line in self:
            my_add = ''
            for rec in line.employee_id.address_ids:
                if ('address_type', '=', 'hometown_add'):
                    my_add = str(rec.street) + ' ' + str(rec.street2) + ', ' + str(rec.city) + ', ' + str(rec.state_id.name) + ', ' + str(rec.country_id.name) + ' - ' + str(rec.zip)
            if line.employee_id and line.place_of_trvel == 'hometown':
                line.hometown_address = my_add
            else:
                line.hometown_address = ''
            line.slect_leave = False
            line.leave_period = False
            line.depart_date = False
            line.arrival_date = False


    @api.depends('slect_leave')
    def compute_get_leave_details(self):
        for line in self:
            if line.slect_leave:
                line.leave_period = line.slect_leave.number_of_days_display
                line.depart_date = line.slect_leave.request_date_from
                line.arrival_date = line.slect_leave.request_date_to



    @api.depends('no_of_days')
    def _compute_amount(self):
        for line in self:
            if line.no_of_days:
                sum = 0
                leave_my = self.env['hr.leave.report'].search([('employee_id', '=', line.employee_id.id)])
                # total_basic = self.env['monthly.salary.structure'].search([('employee_id','=',line.employee_id.id),('name', '=', 'Basic Salary')],order='employee_id desc', limit=1)
                total_wage = self.env['hr.contract'].search([('employee_id','=',line.employee_id.id),('state','=','open'),('date_start', '<=', line.date),('date_end', '>=', line.date)], limit=1)
                if total_wage:
                    line.total_basic_salary = total_wage.wage
                    total_basic_ltc = total_wage.wage
                    line.amount = (((float(total_basic_ltc))*float(line.no_of_days))/30)
                for i in leave_my:
                    sum += i.number_of_days
                line.total_leaves = str(sum)
                line.left_leaves = float(line.total_leaves) - line.no_of_days

    @api.multi
    def button_to_approve(self):
        for rec in self:
            if rec.single_fare:
                rec.single_fare_approved = ((rec.single_fare)*90)/100
            else:
                rec.single_fare_approved = 0
            if rec.employee_id.date_of_join and (rec.employee_id.date_of_join + relativedelta(years=1)) <= datetime.now().date():
                rec.write({'state': 'to_approve'})
            else:
                raise ValidationError(
                    _('You are not eligible to take LTC, You have to complete atleast 1 year'))


    @api.multi
    def button_approved(self):
        for rec in self:
            rec.write({'state': 'approved'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})

    @api.multi
    def button_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    @api.model
    def create(self, vals):
        res =super(EmployeeLtcAdvance, self).create(vals)
        seq = self.env['ir.sequence'].next_by_code('employee.ltc.advance')
        sequence = 'LTC' + seq
        res.ltc_sequence = sequence
        return res

    @api.multi
    @api.depends('ltc_sequence')
    def name_get(self):
        res = []
        for record in self:
            if record.ltc_sequence:
                name = record.ltc_sequence
            else:
                name = 'LTC'
            res.append((record.id, name))
        return res


    @api.onchange('no_of_days')
    def check_number_of_days(self):
        for rec in self:
            if rec.no_of_days:
                if float(rec.no_of_days) > 10.0:
                    raise ValidationError(
                                    _('Employee will allow maximum 10 days'))
                elif float(rec.no_of_days) < 0.0:
                    raise ValidationError(
                                    _('Employee will allow minimum 0 days'))




class EmployeeLtcClaim(models.Model):
    _name = 'employee.ltc.claim'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description='Claim Submission'


    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)


    employee_id = fields.Many2one('hr.employee', string='Employee', default=_default_employee,track_visibility='always')
    amount_claimed = fields.Char('Advance Amount Claimed', compute='_compute_fetch_ltc_details',track_visibility='always')
    ltc_availed_for = fields.Char('LTC availed for', compute='_compute_fetch_ltc_details',track_visibility='always')
    leave_period = fields.Char('Leave period', compute='_compute_fetch_ltc_details',track_visibility='always')
    place_of_visit = fields.Char('Place of visit',track_visibility='always')
    detail_of_journey = fields.One2many('employee.ltc.journey','relate_to_ltc', string='Details of Journey',track_visibility='always')
    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], required=True, default='draft',track_visibility='always')


    @api.multi
    def button_to_approve(self):
        for rec in self:
            rec.write({'state': 'to_approve'})

    @api.multi
    def button_approved(self):
        for rec in self:
            rec.write({'state': 'approved'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})

    @api.multi
    def button_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})


    @api.depends('employee_id')
    def _compute_fetch_ltc_details(self):
        for rec in self:
            if rec.employee_id:
                ltc_ad = self.env['employee.ltc.advance'].search([('employee_id','=',rec.employee_id.id)],order='ltc_sequence desc', limit=1)
                rec.amount_claimed = ltc_ad.amount
                rec.leave_period =ltc_ad.leave_period
                rec.ltc_availed_for = ltc_ad.ltc_sequence

    @api.multi
    @api.depends('ltc_availed_for','employee_id')
    def name_get(self):
        res = []
        name = ''
        for record in self:
            if record.ltc_availed_for and record.employee_id:
                name = str(record.employee_id.name) + ' - ' + str(record.ltc_availed_for) + ' - LTC Claim'
            else:
                name = 'LTC Claim'
            res.append((record.id, name))
        return res


class JourneyDetails(models.Model):
    _name = 'employee.ltc.journey'
    _description = "Employee LTC Journey"

    employee_id = fields.Many2one('hr.employee', string='Employee')
    relate_to_ltc = fields.Many2one('employee.ltc.claim')
    departure_timings = fields.Datetime('Date & Time of Departure')
    arrival_timings = fields.Datetime('Date & Time of Arrival')
    from_l = fields.Char('From')
    to_l = fields.Char('To')
    distance = fields.Char('Distance(in Kms.)')

    mode_of_travlel=fields.Selection([('air', 'By Air'), ('train', 'By Train'), ('bus', 'By Bus'), ('car', 'By Car')], string='Mode of Travel')

    coc_air=fields.Selection([('first', 'First Class'), ('business', 'Business Class'), ('economy', 'Economy Class')], string='Class of Accomodation')

    coc_train=fields.Selection([('ac1', 'AC 1-Tier'), ('ac2', 'AC 2-Tier'), ('ac3', 'AC 3-Tier'), ('1st', 'First Class'), ('ac_chair', 'A.C Chair Class'), ('sleeper', 'Sleeper'), ('2nd_sit', 'Second Sitting')], string='Class of Accomodation')

    coc_bus=fields.Selection([('ac', 'AC'), ('n_ac', 'Non AC'), ('seater', 'Seater'), ('semi_sleep', 'Semi Sleeper'), ('sleeper', 'Sleeper')], string='Class of Accomodation')

    no_of_persons = fields.Char('No. of persons')
    fair_paid = fields.Char('Fair Paid')
    ticket_attach = fields.Binary('Attach Ticket')
    not_connected_by_train = fields.Boolean('Not Connected by Trains')
