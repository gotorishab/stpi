from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date

class EmployeeLtcAdvance(models.Model):
    _name = 'employee.ltc.advance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description='Advance Request'

    def _default_employee(self):
        return self.env['hr.employee'].sudo().search([('user_id', '=', self.env.uid)], limit=1)

    @api.onchange('block_year','slect_leave')
    def change_slect_leave(self):
        return {'domain':
                    {
                        'slect_leave': [('ltc', '=', True),('ltc_apply_done', '=', False),('state', '!=', 'validate'),('employee_id', '=', self.employee_id.id),('request_date_from', '>=', self.block_year.date_start),('request_date_to', '<=', self.block_year.date_end)],
                        'child_block_year': [('child_block_year_id', '=', self.block_year.id)]
                           }}

    #
    # @api.onchange('block_year')
    # def open_child_block_year_wiz(self):
    #     for rec in self:
    #         return {
    #             'name': 'Availing LTC for year',
    #             'view_type': 'form',
    #             'view_mode': 'tree',
    #             'res_model': 'child.bl.wiz',
    #             'type': 'ir.actions.act_window',
    #             'target': 'new',
    #             'view_id': self.env.ref('employee_ltc.child_block_year_wizard_form_view').id,
    #             'context': {
    #                 'default_block_year': rec.block_year.id,
    #                 'default_ltc_id': rec.id
    #             }
    #             }

    ltc_sequence = fields.Char('LTC number',track_visibility='always')
    employee_id = fields.Many2one('hr.employee', string='Requested By', default=_default_employee,track_visibility='always')
    branch_id = fields.Many2one('res.branch', string='Branch', store=True)
    job_id = fields.Many2one('hr.job', string='Functional Designation', store=True)
    department_id = fields.Many2one('hr.department', string='Department', store=True)
    date = fields.Date(string="Requested Date", default=datetime.now().date(),track_visibility='always')
    place_of_trvel=fields.Selection([('hometown', 'Hometown'), ('india', 'Anywhere in India'), ('conversion', 'Conversion of Hometown')], default='hometown', string='Place of Travel',track_visibility='always')
    hometown_address = fields.Char(string='Address',track_visibility='always')
    block_year=fields.Many2one('block.year', 'Block year',track_visibility='always')
    slect_leave = fields.Many2one('hr.leave',string = 'Leave',track_visibility='always')
    leave_period = fields.Char(string = 'Leave period',track_visibility='always')
    total_leaves = fields.Char(string = 'Total Leaves',track_visibility='always')
    left_leaves = fields.Char(string = 'Left Leaves',track_visibility='always')
    depart_date=fields.Date('Departue Date',track_visibility='always')
    arrival_date=fields.Date('Arrival Date',track_visibility='always')
    advance_ammount=fields.Float('Advance Amount Required',track_visibility='always')
    single_fare=fields.Float('Single Train Fair/ Bus Fair from the office to Place of Visit by Shortest Route',track_visibility='always')
    single_fare_approved=fields.Float('Approved Amount',track_visibility='always')
    attach_file = fields.Binary('Attach a File',track_visibility='always')
    all_particulars_verified=fields.Selection([('yes', 'Yes'), ('no', 'No')], default='yes', string='All particulars verified?', track_visibility='always')
    relative_ids = fields.One2many('family.details.ltc','relative_id', string='Relatives')
    are_you_coming = fields.Boolean('Are you coming?')
    family_details = fields.Many2many('employee.relative', string='Family Details', domain="[('employee_id', '=', employee_id),('ltc', '=', True)]",track_visibility='always')
    partner_working=fields.Selection([('yes', 'Yes'), ('no', 'No')], default='no', string='Whether Wife/ Husband is employed and if so whether entitled to LTC',track_visibility='always')
    mode_of_travel=fields.Selection([('road', 'By Road'),('train', 'By Train'),('air', 'By Air')], default='road', string='Mode of Travel',track_visibility='always')
    el_encashment=fields.Selection([('yes', 'Yes'), ('no', 'No')], default='no', string='Require EL Encashment',track_visibility='always')
    no_of_days = fields.Float('No. of days', default='10',track_visibility='always')
    amount = fields.Float(string='Amount', compute='_compute_amount',track_visibility='always')
    child_block_year=fields.Many2one('child.block.year', 'Availing LTC for year')
    total_basic_salary = fields.Float(string='Total Basic',track_visibility='always')
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
                               ], required=True, default='draft',track_visibility='always', string='Status')


    @api.onchange('employee_id')
    @api.constrains('employee_id')
    def onchange_emp_get_base(self):
        for rec in self:
            rec.job_id = rec.employee_id.job_id.id
            rec.department_id = rec.employee_id.department_id.id
            rec.branch_id = rec.employee_id.branch_id.id

    @api.onchange('place_of_trvel')
    def false_everything(self):
        for line in self:
            line.slect_leave = False
            line.leave_period = False
            line.depart_date = False
            line.arrival_date = False

    @api.onchange('employee_id','place_of_trvel')
    @api.constrains('employee_id','place_of_trvel')
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



    @api.multi
    def unlink(self):
        for loan in self:
            if loan.state not in ('draft', 'cancel'):
                raise UserError(
                    'You cannot delete a LTC which is not in draft or cancelled state')
            else:
                rep_ids = self.env['ledger.ltc'].sudo().search([
                    ('ltc_id', '=', loan.id),
                ])
                for line in rep_ids:
                    line.sudo().unlink()
        return super(EmployeeLtcAdvance, self).unlink()


    @api.onchange('slect_leave')
    # @api.constrains('slect_leave')
    def onchange_get_leave_details(self):
        for line in self:
            if line.slect_leave:
                line.leave_period = line.slect_leave.number_of_days_display
                line.depart_date = line.slect_leave.request_date_from
                line.arrival_date = line.slect_leave.request_date_to

    @api.onchange('depart_date','arrival_date')
    @api.constrains('depart_date','arrival_date')
    def onchange_get_period_leave(self):
        for line in self:
            if line.slect_leave:
                if type(line.arrival_date - line.depart_date) != int:
                    line.leave_period = (line.arrival_date - line.depart_date).days + 1
                else:
                    line.leave_period = (line.arrival_date - line.depart_date) + 1



    @api.depends('no_of_days')
    def _compute_amount(self):
        for line in self:
            if line.no_of_days:
                sum = 0
                leave_my = self.env['hr.leave.report'].sudo().search([('employee_id', '=', line.employee_id.id)])
                # total_basic = self.env['monthly.salary.structure'].sudo().search([('employee_id','=',line.employee_id.id),('name', '=', 'Basic Salary')],order='employee_id desc', limit=1)
                total_wage = self.env['hr.contract'].sudo().search([('employee_id','=',line.employee_id.id),('state','=','open'),('date_start', '<=', line.date)], limit=1)
                if total_wage:
                    print('=======================================Updated basic=====================')
                    line.total_basic_salary = total_wage.updated_basic
                    total_basic_ltc = total_wage.updated_basic
                    line.amount = (((float(total_basic_ltc)/30)*float(line.no_of_days)))
                    print('=======================================Updated basic amount=====================',line.total_basic_salary)
                    print('=======================================Updated basic amount=====================',line.amount)
                for i in leave_my:
                    sum += i.number_of_days
                line.total_leaves = str(sum)
                line.left_leaves = float(line.total_leaves) - line.no_of_days


    @api.onchange('no_of_days')
    @api.constrains('no_of_days')
    def get_amount_onchange_days(self):
        for line in self:
            if line.no_of_days:
                sum = 0
                # leave_my = self.env['hr.leave.report'].sudo().search([('employee_id', '=', line.employee_id.id)])
                # total_basic = self.env['monthly.salary.structure'].sudo().search([('employee_id','=',line.employee_id.id),('name', '=', 'Basic Salary')],order='employee_id desc', limit=1)
                total_wage = self.env['hr.contract'].sudo().search([('employee_id','=',line.employee_id.id),('state','=','open'),('date_start', '<=', line.date)], limit=1)
                if total_wage:
                    print('=======================================Updated basic=====================')
                    line.total_basic_salary = total_wage.updated_basic
                    total_basic_ltc = total_wage.updated_basic
                    line.amount = (((float(total_basic_ltc)/30)*float(line.no_of_days)))
                print('=======================================Updated basic amount=====================',line.total_basic_salary)
                print('=======================================Updated basic amount=====================',line.amount)


    @api.multi
    def button_to_approve(self):
        for res in self:
            # pp = datetime.now().date() - relativedelta(years=4)
            # if res.are_you_coming == True:
            #     if res.slect_leave:
            #         res.slect_leave.ltc_apply_done = True
            #     val_ids = self.env['ledger.ltc'].sudo().search([
            #         ('employee_id', '=', res.employee_id.id),
            #         ('relative_name', '=', res.employee_id.name),
            #         ('ltc_date', '>=', pp),
            #     ])
            #     if res.employee_id.date_of_join + relativedelta(year=8) >= datetime.now().date():
            #         count_india = 0
            #         count_home = 0
            #         for ltc_pre in val_ids:
            #             if ltc_pre.place_of_trvel == res.place_of_trvel and ltc_pre.block_year == res.block_year and ltc_pre.child_block_year == res.child_block_year:
            #                 raise ValidationError(
            #                     _('You are not allowed to take LTC for this block year'))
            #             if ltc_pre.block_year == res.block_year and ltc_pre.child_block_year == res.child_block_year:
            #                 raise ValidationError(
            #                     _(
            #                         'You are not allowed to take LTC for this block year, as you have already applied for this block year'))
            #             if ltc_pre.place_of_trvel == 'india':
            #                 count_india += 1
            #             if res.place_of_trvel == 'india' and count_india > 1:
            #                 raise ValidationError(
            #                     _(
            #                         'You are not allowed to take LTC for this block year as you are able to take Anywhere in India LTC, once in 4 years'))
            #             if ltc_pre.place_of_trvel == 'hometown':
            #                 count_home += 1
            #             if res.place_of_trvel == 'hometown' and count_home > 4:
            #                 raise ValidationError(
            #                     _(
            #                         'You are not allowed to take LTC for this block year as you are able to take Hometown LTC, maximum of 4 times in 4 years'))
            #     else:
            #         count_total = 0
            #         count_india = 0
            #         for ltc_pre in val_ids:
            #             if ltc_pre.place_of_trvel == res.place_of_trvel and ltc_pre.block_year == res.block_year and ltc_pre.child_block_year == res.child_block_year:
            #                 raise ValidationError(
            #                     _('You are not allowed to take LTC for this block year'))
            #             if ltc_pre.place_of_trvel == 'india':
            #                 count_india += 1
            #             if res.place_of_trvel == 'india' and count_india > 1:
            #                 raise ValidationError(
            #                     _(
            #                         'You are not allowed to take LTC for this block year as you are able to take Anywhere in India LTC, once in 4 years'))
            #             if ltc_pre.place_of_trvel == 'hometown':
            #                 count_india += 1
            #             if res.place_of_trvel == 'hometown' and count_india > 2:
            #                 raise ValidationError(
            #                     _(
            #                         'You are not allowed to take LTC for this block year as you are able to take Hometown LTC, twice in 4 years'))
            # for lines in res.relative_ids:
            #     rel_ids = self.env['ledger.ltc'].sudo().search([
            #         ('employee_id', '=', res.employee_id.id),
            #         ('relative_name', '=', lines.name.name),
            #         ('ltc_date', '>=', pp),
            #     ])
            #     if res.employee_id.date_of_join + relativedelta(year=8) >= datetime.now().date():
            #         count_india = 0
            #         count_home = 0
            #         for ltc_pre in rel_ids:
            #             if ltc_pre.place_of_trvel == res.place_of_trvel and ltc_pre.block_year == res.block_year:
            #                 raise ValidationError(
            #                     _('You are not allowed to take LTC for this block year'))
            #             if ltc_pre.block_year == res.block_year and ltc_pre.child_block_year == res.child_block_year:
            #                 raise ValidationError(
            #                     _(
            #                         'You are not allowed to take LTC for this block year, as you have already applied for this block year'))
            #             if ltc_pre.place_of_trvel == 'india':
            #                 count_india += 1
            #             if res.place_of_trvel == 'india' and count_india > 1:
            #                 raise ValidationError(
            #                     _(
            #                         'You are not allowed to take LTC for this block year as you are able to take Anywhere in India LTC, once in 4 years'))
            #             if ltc_pre.place_of_trvel == 'hometown':
            #                 count_home += 1
            #             if res.place_of_trvel == 'hometown' and count_home > 4:
            #                 raise ValidationError(
            #                     _(
            #                         'You are not allowed to take LTC for this block year as you are able to take Hometown LTC, maximum of 4 times in 4 years'))
            #     else:
            #         count_total = 0
            #         count_india = 0
            #         for ltc_pre in rel_ids:
            #             if res.place_of_trvel == ltc_pre.place_of_trvel and res.block_year == ltc_pre.block_year and res.child_block_year == ltc_pre.child_block_year:
            #                 raise ValidationError(
            #                     _('You are not allowed to take LTC for this block year'))
            #             if ltc_pre.place_of_trvel == 'india':
            #                 count_india += 1
            #             if res.place_of_trvel == 'india' and count_india > 1:
            #                 raise ValidationError(
            #                     _(
            #                         'You are not allowed to take LTC for this block year as you are able to take Anywhere in India LTC, once in 4 years'))
            #             if ltc_pre.place_of_trvel == 'hometown':
            #                 count_india += 1
            #             if res.place_of_trvel == 'hometown' and count_india > 2:
            #                 raise ValidationError(
            #                     _(
            #                         'You are not allowed to take LTC for this block year as you are able to take Hometown LTC, twice in 4 years'))
            if res.single_fare:
                res.single_fare_approved = ((res.single_fare)*90)/100
            else:
                res.single_fare_approved = 0
            if res.employee_id.date_of_join and (res.employee_id.date_of_join + relativedelta(years=1)) <= datetime.now().date():
                rep_ids = self.env['ledger.ltc'].sudo().search([
                    ('ltc_id', '=', res.id),
                ])
                for line in rep_ids:
                    line.sudo().write({'state': 'to_approve'})
                res.write({'state': 'to_approve'})
            else:
                raise ValidationError(
                    _('You are not eligible to take LTC, You have to complete atleast 1 year'))
            if res.hometown_address == '':
                raise ValidationError(
                    _('You are not allowed to submit. Please enter hometwon address'))


    @api.multi
    def button_approved(self):
        for res in self:
            rep_ids = self.env['ledger.ltc'].sudo().search([
                ('ltc_id', '=', res.id),
            ])
            for line in rep_ids:
                line.sudo().write({'state': 'approved'})
            res.write({'state': 'approved'})

            # if res.el_encashment == 'yes':
            #     val_id = self.env['hr.leave.type'].sudo().search([
            #             ('leave_type', '=', 'Earned Leave')
            #         ], limit=1)
            #     allocate_leave = self.env['hr.leave.allocation'].sudo().create(({'holiday_status_id': val_id.id,
            #                                                              'holiday_type': 'employee',
            #                                                              'employee_id': res.employee_id.id,
            #                                                              'number_of_days_display':(-1) * res.no_of_days,
            #                                                              'number_of_days': (-1) * res.no_of_days,
            #                                                              'name': 'Against LTC',
            #                                                              'notes': 'As Per Leave Policy'
            #                                                              })
            #     print("allocationnnnnnnnnnnnn111111111111111", allocate_leave)
            #     allocate_leave.sudo().action_approve()
            # if res.are_you_coming == True:
            #     create_ledger_self = self.env['ledger.ltc'].sudo().create((
            #         {
            #             'employee_id': res.employee_id.id,
            #             'relative_name': res.employee_id.name,
            #             'relation': 'Self',
            #             'block_year': res.block_year.id,
            #             'child_block_year': res.child_block_year.id,
            #             'ltc_date': datetime.now().date(),
            #             'place_of_trvel': res.place_of_trvel,
            #         }
            #     )
            # for relative in res.relative_ids:
            #     create_ledger_family = self.env['ledger.ltc'].sudo().create((
            #         {
            #             'employee_id': res.employee_id.id,
            #             'relative_name': relative.name.name,
            #             'relation': relative.name.relate_type.name,
            #             'block_year': res.block_year.id,
            #             'child_block_year': res.child_block_year.id,
            #             'ltc_date': datetime.now().date(),
            #             'place_of_trvel': res.place_of_trvel,
            #         }
            #     )

    @api.multi
    def button_reject(self):
        for rec in self:
            rep_ids = self.env['ledger.ltc'].sudo().search([
                ('ltc_id', '=', rec.id),
            ])
            for line in rep_ids:
                line.sudo().unlink()
            rec.write({'state': 'rejected'})

    @api.multi
    def button_reset_to_draft(self):
        for rec in self:
            rep_ids = self.env['ledger.ltc'].sudo().search([
                ('ltc_id', '=', rec.id),
            ])
            for line in rep_ids:
                line.sudo().write({'state': 'draft'})
            rec.write({'state': 'draft'})

    @api.model
    def create(self, vals):
        res =super(EmployeeLtcAdvance, self).create(vals)
        seq = self.env['ir.sequence'].next_by_code('employee.ltc.advance')
        sequence = 'LTC' + seq
        res.ltc_sequence = sequence
        pp = datetime.now().date() - relativedelta(years=4)
        if res.are_you_coming == True:
            if res.slect_leave:
                res.slect_leave.ltc_apply_done = True
        count = 0
        if res.are_you_coming == False:
            for rel in res.relative_ids:
                count += 1
            if count <= 0:
                raise ValidationError(
                    _('You are not allowed to take LTC as you have not selected any Relative or self'))
        if res.are_you_coming == True:
            create_ledger_self = self.env['ledger.ltc'].sudo().create((
                {
                    'ltc_id': res.id,
                    'employee_id': res.employee_id.id,
                    'relative_name': res.employee_id.name,
                    'relation': 'Self',
                    'block_year': res.block_year.id,
                    'child_block_year': res.child_block_year.id,
                    'ltc_date': datetime.now().date(),
                    'place_of_trvel': res.place_of_trvel,
                    'state': 'draft',
                }
            )
        for relative in res.relative_ids:
            create_ledger_family = self.env['ledger.ltc'].sudo().create((
                {
                    'ltc_id': res.id,
                    'employee_id': res.employee_id.id,
                    'relative_name': relative.name.name,
                    'relation': relative.name.relate_type.name,
                    'block_year': res.block_year.id,
                    'child_block_year': res.child_block_year.id,
                    'ltc_date': datetime.now().date(),
                    'state': 'draft',
                }
            )
        if res.are_you_coming == True:
            if res.slect_leave:
                res.slect_leave.ltc_apply_done = True
            val_ids = self.env['ledger.ltc'].sudo().search([
                ('employee_id', '=', res.employee_id.id),
                ('relative_name', '=', res.employee_id.name),
                ('ltc_date', '>=', pp),
            ])
            if res.employee_id.date_of_join + relativedelta(year=8) >= datetime.now().date():
                count_india = 0
                count_home = 0
                for ltc_pre in val_ids:
                    if ltc_pre.ltc_id.id != res.id:
                        print('===============ledger id 1========================', ltc_pre.ltc_id)
                        print('===============My id 1========================', res.id)
                        if ltc_pre.place_of_trvel == res.place_of_trvel and ltc_pre.block_year == res.block_year and ltc_pre.child_block_year == res.child_block_year:
                                raise ValidationError(
                                    _('You are not allowed to take LTC for this block year'))
                        if ltc_pre.block_year == res.block_year and ltc_pre.child_block_year == res.child_block_year:
                                raise ValidationError(
                                    _('You are not allowed to take LTC for this block year, as you have already applied for this block year'))
                        if ltc_pre.place_of_trvel == 'india':
                            count_india += 1
                        if res.place_of_trvel == 'india' and count_india > 1:
                            raise ValidationError(
                                _(
                                    'You are not allowed to take LTC for this block year as you are able to take Anywhere in India LTC, once in 4 years'))
                        if ltc_pre.place_of_trvel == 'hometown':
                            count_home += 1
                        if res.place_of_trvel == 'hometown' and count_home > 4 :
                            raise ValidationError(
                                _(
                                    'You are not allowed to take LTC for this block year as you are able to take Hometown LTC, maximum of 4 times in 4 years'))
            else:
                count_total = 0
                count_india = 0
                for ltc_pre in val_ids:
                    if ltc_pre.ltc_id.id != res.id:
                        print('===============ledger id 2========================', ltc_pre.ltc_id)
                        print('===============My id 2========================', res.id)
                        if ltc_pre.place_of_trvel == res.place_of_trvel and ltc_pre.block_year == res.block_year and ltc_pre.child_block_year == res.child_block_year:
                                raise ValidationError(
                                    _('You are not allowed to take LTC for this block year'))
                        if ltc_pre.place_of_trvel == 'india':
                            count_india += 1
                        if res.place_of_trvel == 'india' and count_india > 1 :
                            raise ValidationError(
                                _(
                                    'You are not allowed to take LTC for this block year as you are able to take Anywhere in India LTC, once in 4 years'))
                        if ltc_pre.place_of_trvel == 'hometown':
                                    count_india += 1
                        if res.place_of_trvel == 'hometown' and count_india > 2:
                            raise ValidationError(
                                _(
                                    'You are not allowed to take LTC for this block year as you are able to take Hometown LTC, twice in 4 years'))
        for lines in res.relative_ids:
            rel_ids = self.env['ledger.ltc'].sudo().search([
                ('employee_id', '=', res.employee_id.id),
                ('relative_name', '=', lines.name.name),
                ('ltc_date', '>=', pp),
            ])
            if res.employee_id.date_of_join + relativedelta(year=8) >= datetime.now().date():
                count_india = 0
                count_home = 0
                for ltc_pre in rel_ids:
                    if ltc_pre.ltc_id.id != res.id:
                        print('===============ledger id 3========================', ltc_pre.ltc_id)
                        print('===============My id 3========================', res.id)
                        if ltc_pre.place_of_trvel == res.place_of_trvel and ltc_pre.block_year == res.block_year and ltc_pre.child_block_year == res.child_block_year:
                                raise ValidationError(
                                    _('You are not allowed to take LTC for this block year'))
                        if ltc_pre.block_year == res.block_year and ltc_pre.child_block_year == res.child_block_year:
                                raise ValidationError(
                                    _('You are not allowed to take LTC for this block year, as you have already applied for this block year'))
                        if ltc_pre.place_of_trvel == 'india':
                            count_india += 1
                        if res.place_of_trvel == 'india' and count_india > 1:
                            raise ValidationError(
                                _(
                                    'You are not allowed to take LTC for this block year as you are able to take Anywhere in India LTC, once in 4 years'))
                        if ltc_pre.place_of_trvel == 'hometown':
                            count_home += 1
                        if res.place_of_trvel == 'hometown' and count_home > 4:
                            raise ValidationError(
                                _(
                                    'You are not allowed to take LTC for this block year as you are able to take Hometown LTC, maximum of 4 times in 4 years'))
            else:
                count_total = 0
                count_india = 0
                for ltc_pre in rel_ids:
                    if ltc_pre.ltc_id.id != res.id:
                        print('===============ledger id 4========================', ltc_pre.ltc_id)
                        print('===============My id 4========================', res.id)
                        if res.place_of_trvel == ltc_pre.place_of_trvel and res.block_year == ltc_pre.block_year and res.child_block_year == ltc_pre.child_block_year:
                            raise ValidationError(
                                _('You are not allowed to take LTC for this block year'))
                        if ltc_pre.place_of_trvel == 'india':
                            count_india += 1
                        if res.place_of_trvel == 'india' and count_india > 1:
                            raise ValidationError(
                                _(
                                    'You are not allowed to take LTC for this block year as you are able to take Anywhere in India LTC, once in 4 years'))
                        if ltc_pre.place_of_trvel == 'hometown':
                            count_india += 1
                        if res.place_of_trvel == 'hometown' and count_india > 2:
                            raise ValidationError(
                                _(
                                    'You are not allowed to take LTC for this block year as you are able to take Hometown LTC, twice in 4 years'))
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


class BlockYear(models.Model):
    _name = 'block.year'
    _description = "Block Year"

    name = fields.Char('Name')
    date_start = fields.Date('From Date')
    date_end = fields.Date('To Date')
    child_block_year_ids = fields.One2many('child.block.year', 'child_block_year_id', string='Availing LTC for year Ids')

    @api.model
    def create(self, vals):
        res =super(BlockYear, self).create(vals)
        search_id = self.env['block.year'].sudo().search([('id','!=',res.id)])
        for emp in search_id:
            if (emp.date_start <= res.date_start <= emp.date_end) or (emp.date_start <= res.date_end <= emp.date_end):
                raise ValidationError(_('Block year already created of this date. Please correct the date. Already created is {name}').format(name=emp.name))
        return res



class ChildBlockYear(models.Model):
    _name = 'child.block.year'
    _description = " Availing LTC for year"

    name = fields.Char('Name')
    child_block_year_id = fields.Many2one('block.year', string='Block Year')

    @api.constrains('name')
    @api.onchange('name')
    def validate_onchange(self):
        for rec in self:
            if rec.name:
                for e in rec.name:
                    if not e.isdigit():
                        raise ValidationError(_("Please enter correct Name, it must be numeric..."))
                if len(rec.name) != 4:
                    raise ValidationError(_("Please enter correct Name, it must be of 4 digits..."))


class FamilyDetails(models.Model):
    _name = 'family.details.ltc'
    _description = "LTC Family Details"


    @api.onchange('name')
    def change_leave_taken(self):
        return {'domain': {'name': [('ltc', '=', True),('employee_id', '=', self.relative_id.employee_id.id)
            ]}}

    relative_id = fields.Many2one('employee.ltc.advance', string='Relative ID')
    name = fields.Many2one('employee.relative','Name')
    relation = fields.Char(string='Relation', compute='_compute_relations')
    age = fields.Integer(string='Age', compute='_compute_relations')


    @api.depends('name')
    def _compute_relations(self):
        for rec in self:
            rec.relation = rec.name.relate_type.name
            rec.age = int(rec.name.age)

    @api.constrains('name', 'relation','age')
    def check_relative(self):
        for rec in self:
            count = 0
            emp_id = self.env['family.details.ltc'].sudo().search(
                [('name', '=', rec.name.id), ('relative_id', '=', rec.relative_id.id)])
            for e in emp_id:
                count += 1
            if count > 1:
                raise ValidationError("The Relative type must be unique")



class LtcLedger(models.Model):
    _name = 'ledger.ltc'
    _description = "LTC Ledger"

    ltc_id = fields.Many2one('employee.ltc.advance', string='LTC')
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    relative_name = fields.Char(string='Relative Name')
    relation = fields.Char(string='Relative')
    block_year = fields.Many2one('block.year', string='Block year')
    child_block_year=fields.Many2one('child.block.year', 'Availing LTC for year')
    ltc_date = fields.Date(string='LTC Date')
    place_of_trvel=fields.Selection([('hometown', 'Hometown'), ('india', 'Anywhere in India'), ('conversion', 'Conversion of Hometown')], default='hometown', string='LTC Type')
    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], string='Status')

