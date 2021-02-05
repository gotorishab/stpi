from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError,UserError
import re
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar


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
                if gr_id.name != 'tuition_fee':
                    return {'domain': {'date_range': [('type_id', '=', gr_id.date_range_type.id),('date_end', '<=', datetime.now().date())]}}
                else:
                    return {'domain': {'date_range': [('type_id', '=', gr_id.date_range_type.id),('date_start', '<=', datetime.now().date())]}}


    name = fields.Selection([
        ('lunch', 'Lunch Subsidy'),
        ('telephone', 'Telephone Reimbursement'),
        ('broadband', 'Broadband Reimbursement'),
        ('mobile', 'Mobile Reimbursement'),
        ('medical', 'Medical Reimbursement'),
        ('tuition_fee', 'Tuition Fee claim'),
        ('hostel', 'Hostel claim'),
        ('briefcase', 'Briefcase Reimbursement'),
        ('quarterly', 'Newspaper Reimbursements'),
        ('el_encashment', 'EL Encashment'),
    ], string='Reimbursement Type', store=True, track_visibility='always')
    reimbursement_sequence = fields.Char('Reimbursement number', track_visibility='always')
    employee_id = fields.Many2one('hr.employee', store=True, track_visibility='always', string='Requested By')
    job_id = fields.Many2one('hr.job', string='Functional Designation', store=True, track_visibility='always')
    branch_id = fields.Many2one('res.branch', string='Branch', store=True, track_visibility='always')
    department_id = fields.Many2one('hr.department', string='Department', store=True, track_visibility='always')

    el_in_account = fields.Float('Maximum EL')
    el_taking = fields.Float('EL Taking')

    claimed_amount = fields.Float(string='Claimed Amount', track_visibility='always')
    net_amount = fields.Float(string='Eligible Amount', store=True, compute='compute_net_amount', track_visibility='always')
    date_range_type = fields.Many2one('date.range.type', string='Applicable Period', track_visibility='always')
    date_range = fields.Many2one('date.range', string='Date Range', track_visibility='always')

    amount_lunch = fields.Float(string='Daily Eligible Amount', track_visibility='always')
    maximum_eligible_amount = fields.Char(string='Maximum Eligible Amount', track_visibility='always', compute='compute_net_amount')
    lunch_tds_amt = fields.Float('Amount for TDS', track_visibility='always')
    working_days = fields.Char(string='Number of days: ', track_visibility='always')
    tution_document = fields.Binary(string='Document', track_visibility='always')

    # amount_tel = fields.Float(string='Claimed Amount')
    # amount_mob = fields.Float(string='Claimed Amount')
    service_provider = fields.Many2one('reimbursement.service.provider',string='Service Provider', track_visibility='always')
    phone = fields.Binary(string='Attachment', track_visibility='always')
    bill_no = fields.Char(string='Bill number', track_visibility='always')
    bill_due_date = fields.Date(string='Bill Due Date', track_visibility='always')
    mobile_no = fields.Char(string='Telephone or Landline number')

    invoice_number = fields.Char('Invoice Number')
    invoice_date = fields.Date('Invoice Date')
    last_brief_date = fields.Date('Previous Claim Date')
    billing_from = fields.Date('Billing From')
    billing_to = fields.Date('Billing To')

    brief_date = fields.Date(string='Date')
    no_of_months = fields.Integer(string='No of months', default=12)
    attach_news = fields.Binary(string='Attachment')
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
            previous = self.env['reimbursement'].search([('employee_id', '=', rec.employee_id.id),('state', '!=', 'rejected'),('name', '=', 'briefcase')],limit=1,order="brief_date desc")
            if previous:
                if previous.brief_date:
                    rec.last_brief_date = previous.brief_date

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
            if rec.employee_id:
                if rec.name == 'telephone' or rec.name == 'mobile':
                    rec.mobile_no = rec.employee_id.mobile_phone
                if rec.name == 'el_encashment':
                    sum = 0
                    serch_id = self.env['hr.leave.report'].search([('employee_id', '=', rec.employee_id.id),('holiday_status_id.name', '=', 'Earned Leave')])
                    for lv in serch_id:
                        sum += lv.number_of_days
                    rec.el_in_account = sum


    def get_late_coming_report(self):
        lst = []
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        print('===========ids===============', active_ids)
        for employee in self.env['reimbursement'].browse(active_ids):
            print('===========id===============', employee.id)
            lst.append(employee.id)
        print('===========lst===============',lst)
        return self.env['reimbursement'].search([('id', 'in', lst)])

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



    @api.depends('claimed_amount','el_taking','name','date_range')
    def compute_net_amount(self):
        for rec in self:
            gr_id = self.env['reimbursement.configuration'].search([('name', '=', rec.name),('branch_id', '=', rec.branch_id.id),('pay_level_ids', '=', rec.employee_id.job_id.pay_level_id.id),('job_ids', '=', rec.employee_id.job_id.id),('employee_type', '=', rec.employee_id.employee_type)],order='name desc', limit=1)
            if not gr_id:
                gr_id = self.env['reimbursement.configuration'].search([('name', '=', rec.name),('branch_id', '=', rec.branch_id.id),('pay_level_ids', '=', rec.employee_id.job_id.pay_level_id.id)],order='name desc', limit=1)
            if gr_id:
                if gr_id.full == False:
                    rec.maximum_eligible_amount = str(gr_id.allowed)
                    if int(rec.claimed_amount) > int(gr_id.allowed):
                        rec.net_amount = gr_id.allowed
                    else:
                        rec.net_amount = int(rec.claimed_amount)
                else:
                    rec.maximum_eligible_amount = 'No Limit'
                    rec.net_amount = int(rec.claimed_amount)
            else:
                rec.net_amount = int(rec.claimed_amount)
                maximum_eligible_amount = 'No Limit'
            if rec.employee_id and rec.name == 'medical':
                total_wage = self.env['hr.contract'].sudo().search(
                    [('employee_id', '=', rec.employee_id.id), ('state', '=', 'open'),
                     ], limit=1)
                if total_wage:
                    if int(rec.claimed_amount) > int(total_wage.updated_basic)/4:
                        rec.net_amount = float(total_wage.updated_basic)/4
                    else:
                        rec.net_amount = int(rec.claimed_amount)

            elif rec.employee_id and rec.name == 'tuition_fee':
                child_id = self.env['employee.relative'].sudo().search(
                    [('employee_id', '=', rec.employee_id.id)])
                count = 0
                ff = 0
                for cc in child_id:
                    if cc.relate_type_name == 'Son' or cc.relate_type_name == 'Daughter':
                        if cc.tuition and cc.divyang == False:
                            count += 1
                        if cc.tuition and cc.divyang == True:
                            count += 2
                        if cc.twins == True:
                            ff = 1

                if count > 2 and ff!=1:
                    mult = 2
                elif count > 2 and ff==1:
                    mult = 3
                else:
                    mult = count
                if int(rec.claimed_amount) > (2250 * int(mult))*int(rec.no_of_months):
                    rec.net_amount = (2250 * int(mult))*int(rec.no_of_months)
                else:
                    rec.net_amount = int(rec.claimed_amount)
            elif rec.employee_id and rec.name == 'el_encashment':
                now = datetime.now()
                day = int(calendar.monthrange(now.year, now.month)[1])
                total_wage = self.env['hr.contract'].sudo().search(
                    [('employee_id', '=', rec.employee_id.id), ('state', '=', 'open'),
                     ], limit=1)
                if total_wage:
                    rec.net_amount = int((total_wage.updated_basic)/day) * int(rec.el_taking)



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
                    if rec.name == 'el_encashment':
                        if rec.el_in_account < rec.el_taking:
                            raise ValidationError(
                                "Net Earned leave must be greater than Earned leave Taking")
                        if rec.el_in_account < 60:
                            raise ValidationError(
                                "Net Earned leave must be greater than 60")
                        if rec.el_taking > 30:
                            raise ValidationError(
                                "Earned leave Taking must be less than 30")
                        if int(rec.el_in_account - rec.el_taking) < 30:
                            raise ValidationError(
                                "After deduction, Earned leave must be greater than 30")
                        search_id = self.env['reimbursement'].search(
                            [('employee_id', '=', rec.employee_id.id), ('name', '=', rec.name),
                             ('state', 'not in', ['draft', 'rejected'])])
                        count = 0
                        for record in search_id:
                            count+=1
                        if count > 6:
                            raise ValidationError(
                                "Total must be less than 6")
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


class ReimbursementServiceProvider(models.Model):

    _name = "reimbursement.service.provider"
    _description = "Reimbursement Service Provider"

    name = fields.Char('Name')