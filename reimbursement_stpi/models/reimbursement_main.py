from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError,UserError
import re
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class Reimbursement(models.Model):

    _name = "reimbursement"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Reimbursement"
    _order = 'create_date desc'

    @api.model
    def default_get(self, field_list):
        result = super(Reimbursement, self).default_get(field_list)
        ts_user_id = self.env.context.get('user_id', self.env.user.id)
        result['employee_id'] = self.env['hr.employee'].search([('user_id', '=', ts_user_id)], limit=1).id
        return result



    # @api.constrains('name')
    @api.onchange('name')
    def _onchange_name(self):
        for rec in self:
            rec.date_range = False
            if rec.name:
                gr_id = self.env['reimbursement.configuration'].search(
                    [('name', '=', rec.name), ('pay_level_ids', '=', rec.employee_id.job_id.pay_level_id.id), ('branch_id', '=', rec.branch_id.id),('job_ids', '=', rec.employee_id.job_id.id),('employee_type', '=', rec.employee_id.employee_type)], order='name desc', limit=1)
                # print('==========================reimb=================================', gr_id.id)
                if not gr_id:
                    gr_id = self.env['reimbursement.configuration'].search(
                    [('name', '=', rec.name), ('pay_level_ids', '=', rec.employee_id.job_id.pay_level_id.id), ('branch_id', '=', rec.branch_id.id)], order='name desc', limit=1)
                # print('==========================reimb=================================', gr_id.id)
                return {'domain': {'date_range': [('type_id', '=', gr_id.date_range_type.id),('date_end', '<=', datetime.now().date())]}}


    name = fields.Selection([
        ('lunch', 'Lunch Subsidy'),
        ('telephone', 'Telephone Reimbursement'),
        ('mobile', 'Mobile Reimbursement'),
        ('medical', 'Medical Reimbursement'),
        ('tuition_fee', 'Tuition Fee claim'),
        ('briefcase', 'Briefcase Reimbursement'),
        ('quarterly', 'Newspaper Reimbursements'),
    ], string='Reimbursement Type', store=True, track_visibility='always')
    reimbursement_sequence = fields.Char('Reimbursement number', track_visibility='always')
    employee_id = fields.Many2one('hr.employee', store=True, track_visibility='always', string='Requested By')
    job_id = fields.Many2one('hr.job', string='Functional Designation', store=True, track_visibility='always')
    branch_id = fields.Many2one('res.branch', string='Branch', store=True, track_visibility='always')
    department_id = fields.Many2one('hr.department', string='Department', store=True, track_visibility='always')

    claimed_amount = fields.Float(string='Claimed Amount', track_visibility='always')
    net_amount = fields.Float(string='Eligible Amount', compute='compute_net_amount', track_visibility='always')
    date_range_type = fields.Many2one('date.range.type', string='Applicable Period', track_visibility='always')
    date_range = fields.Many2one('date.range', string='Date Range', track_visibility='always')

    amount_lunch = fields.Float(string='Daily Eligible Amount', track_visibility='always')
    lunch_tds_amt = fields.Float('Amount for TDS', track_visibility='always')
    working_days = fields.Char(string='Number of days: ', track_visibility='always')

    # amount_tel = fields.Float(string='Claimed Amount')
    # amount_mob = fields.Float(string='Claimed Amount')
    service_provider = fields.Char(string='Service Provider', track_visibility='always')
    phone = fields.Binary(string='Phone Attachment', track_visibility='always')
    bill_no = fields.Char(string='Bill number', track_visibility='always')
    bill_due_date = fields.Date(string='Bill Due Date', track_visibility='always')
    mobile_no = fields.Char(string='Mobile Number')

    brief_date = fields.Date(string='Date')
    no_of_months = fields.Char(string='No of months', track_visibility='always')
    attach_news = fields.Binary(string='Attanhment')
    remarks = fields.Text(string='Remarks: ', track_visibility='always')

    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approval', 'Submitted'), ('forwarded', 'Forwarded'),
                              ('approved', 'Approved'), ('rejected', 'Rejected')
                              ], required=True, default='draft', track_visibility='always', string='Status')


    @api.onchange('employee_id')
    @api.constrains('employee_id')
    def onchange_emp_get_base(self):
        for rec in self:
            rec.job_id = rec.employee_id.job_id.id
            rec.department_id = rec.employee_id.department_id.id
            rec.branch_id = rec.employee_id.branch_id.id


    @api.onchange('name','employee_id','date_range')
    def only_onchange_name_employee_date(self):
        for rec in self:
            rec.claimed_amount = 0
            rec.net_amount = 0
            count = 0
            serch_id = self.env['reimbursement.attendence'].search(
                [('employee_id', '=', rec.employee_id.id), ('date_related_month', '>=', rec.date_range.date_start),
                 ('date_related_month', '<', rec.date_range.date_end)])
            for i in serch_id:
                count += i.present_days
            if rec.employee_id and rec.name == 'lunch':
                rec.amount_lunch = 75
                rec.working_days = count
                rec.claimed_amount = float(count * 75)
                rec.lunch_tds_amt = float(count * 50)

    @api.constrains('name','employee_id','date_range')
    @api.onchange('name','employee_id','date_range')
    def onchng_name_emp_date(self):
        for rec in self:
            # if rec.employee_id and rec.name == 'lunch':
            #     pass
                # count = 0
                # serch_id = self.env['reimbursement.attendence'].search([('employee_id', '=', rec.employee_id.id),('date_related_month', '>=', rec.date_range.date_start),('date_related_month', '<', rec.date_range.date_end)])
                # for i in serch_id:
                #     count += i.present_days
                # rec.amount_lunch = 75
                # rec.working_days = count
                # rec.claimed_amount = float(rec.working_days * 75)
                # rec.lunch_tds_amt = float(rec.working_days * 50)
            if rec.employee_id and rec.name == 'telephone':
                rec.mobile_no = rec.employee_id.mobile_phone



    @api.constrains('working_days')
    @api.onchange('working_days')
    def onchange_working_days(self):
        for rec in self:
            if rec.employee_id and rec.name == 'lunch' and rec.working_days:
                rec.amount_lunch = 75
                count = float(rec.working_days)
                rec.claimed_amount = float(count * 75)
                rec.lunch_tds_amt = float(count * 50)
                if type(rec.date_range.date_end - rec.date_range.date_start) != int:
                    days = (rec.date_range.date_end - rec.date_range.date_start).days
                else:
                    days = (rec.date_range.date_end - rec.date_range.date_start)
                if float(count) > float(days):
                    raise ValidationError(
                        "You can claim for %s" % rec.name + ", maximum of  %s" % (days+1) + " days")



    @api.depends('claimed_amount')
    def compute_net_amount(self):
        for rec in self:
            gr_id = self.env['reimbursement.configuration'].search([('name', '=', rec.name),('branch_id', '=', rec.branch_id.id),('pay_level_ids', '=', rec.employee_id.job_id.pay_level_id.id),('job_ids', '=', rec.employee_id.job_id.id),('employee_type', '=', rec.employee_id.employee_type)],order='name desc', limit=1)
            if not gr_id:
                gr_id = self.env['reimbursement.configuration'].search([('name', '=', rec.name),('branch_id', '=', rec.branch_id.id),('pay_level_ids', '=', rec.employee_id.job_id.pay_level_id.id)],order='name desc', limit=1)
            if gr_id:
                if int(rec.claimed_amount) > int(gr_id.allowed) and gr_id.full == False:
                    rec.net_amount = gr_id.allowed
                else:
                    rec.net_amount = int(rec.claimed_amount)
            else:
                rec.net_amount = int(rec.claimed_amount)
            if rec.employee_id and rec.name == 'medical':
                total_wage = self.env['hr.contract'].sudo().search(
                    [('employee_id', '=', rec.employee_id.id), ('state', '=', 'open'),
                     ], limit=1)
                if total_wage:
                    if int(rec.claimed_amount) > int(total_wage.updated_basic):
                        rec.net_amount = total_wage.updated_basic
                    else:
                        rec.net_amount = int(rec.claimed_amount)



    @api.multi
    def unlink(self):
        for data in self:
            if data.state not in ('draft', 'rejected'):
                raise UserError(
                    'You cannot delete a Reimbursement which is not in draft or Rejected state')
        return super(Reimbursement, self).unlink()



    @api.multi
    def button_submit(self):
        for rec in self:
            # search_id = self.env['reimbursement'].search([('employee_id', '=', rec.employee_id.id), ('name', '=', rec.name), ('date_range', '=', rec.date_range.id), ('state', '!=', 'rejected')])
            search_id = self.env['reimbursement'].search(
                [('employee_id', '=', rec.employee_id.id), ('name', '=', rec.name),
                 ('date_range', '=', rec.date_range.id),
                 ('state', '!=', 'rejected'), ('id', '!=', rec.id)])
            index = False
            for emp in search_id:
                if rec.name != 'briefcase' or rec.name != 'medical':
                    if emp:
                        raise ValidationError("This reimbursement is already applied for this duration, please correct the dates")
            else:
                index = True
            if index == True:
                if int(rec.net_amount) <= 0:
                    raise ValidationError(
                        "Amount must be greater than zero")
                else:
                    gr_id = self.env['reimbursement.configuration'].search(
                        [('name', '=', rec.name),('branch_id', '=', rec.branch_id.id), ('pay_level_ids', '=', rec.employee_id.job_id.pay_level_id.id),('job_ids', '=', rec.employee_id.job_id.id),('employee_type', '=', rec.employee_id.employee_type)],
                        order='name desc',
                        limit=1)
                    if not gr_id:
                        gr_id = self.env['reimbursement.configuration'].search(
                        [('name', '=', rec.name),('branch_id', '=', rec.branch_id.id), ('pay_level_ids', '=', rec.employee_id.job_id.pay_level_id.id)],
                        order='name desc',
                        limit=1)
                    if gr_id.open == False:
                        if rec.name != 'briefcase':
                            submit_min = rec.date_range.date_end + relativedelta(days=1)
                            submit_max = rec.date_range.date_end + relativedelta(days=gr_id.max_submit)
                            today = datetime.now().date()
                            if not(submit_min < today <= submit_max):
                                raise ValidationError(
                                    "You can claim for %s" % rec.name + " between  %s" % submit_min + " and %s" % submit_max)
                            else:
                                rec.write({'state': 'waiting_for_approval'})
                        else:
                            search_id = self.env['reimbursement'].search(
                                [('employee_id', '=', rec.employee_id.id), ('name', '=', rec.name),
                                 ('state', 'not in', ['draft', 'rejected'])])
                            for record in search_id:
                                min_date = record.brief_date + relativedelta(year=2)
                                if min_date > rec.brief_date:
                                    raise ValidationError(
                                        "You are allowed to claim for breifcase reimbursement after %s" % min_date)
                            else:
                                rec.write({'state': 'waiting_for_approval'})

                    else:
                        rec.write({'state': 'waiting_for_approval'})


    @api.model
    def create(self, vals):
        res =super(Reimbursement, self).create(vals)
        search_id = self.env['reimbursement'].search(
            [('employee_id', '=', res.employee_id.id), ('name', '=', res.name), ('date_range', '=', res.date_range.id),
             ('state', '!=', 'rejected'),('id', '!=', res.id)])
        sequence = ''
        seq = self.env['ir.sequence'].next_by_code('reimbursement')
        sequence = 'REIMBURSEMENT - ' + str(seq)
        res.reimbursement_sequence = sequence
        if res.name != 'briefcase' or res.name != 'medical':
            for emp in search_id:
                if emp:
                    raise ValidationError(
                        "This reimbursement is already applied for this duration, please correct the dates")
        return res

    @api.multi
    @api.depends('reimbursement_sequence')
    def name_get(self):
        res = []
        for record in self:
            if record.reimbursement_sequence:
                name = record.reimbursement_sequence
            else:
                name = 'REIMBURSEMENT'
            res.append((record.id, name))
        return res

    @api.multi
    def button_approved(self):
        for rec in self:
            rec.approved_date = datetime.now().date()
            rec.write({'state': 'approved'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})


    @api.multi
    def button_reset_to_draft(self):
        for rec in self:
            self.ensure_one()
            compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
            ctx = dict(
                default_composition_mode='comment',
                default_res_id=self.id,

                default_model='reimbursement',
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
            self.rejected_date = datetime.now().date()
            self.write({'state': 'draft'})
            return mw
