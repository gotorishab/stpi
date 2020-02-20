from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from odoo.tools import float_compare
import datetime
from datetime import datetime, timedelta,date
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from pytz import timezone, UTC
from collections import defaultdict
from odoo.tools import float_utils

class HrLeave(models.Model):
    _inherit = 'hr.leave'
    _description = 'HR Leave Changes For STPI'
    
    
    attachement = fields.Boolean(string="attachment")
    attachement_proof = fields.Binary(string="Attachment Proof")
    commuted = fields.Boolean(string="Commuted")
    employee_type = fields.Selection([('regular', 'Regular Employee'),
                                      ('contractual_with_agency', 'Contractual with Agency'),
                                      ('contractual_with_stpi', 'Contractual with STPI')], string='Employment Type',
                                      )
    gender = fields.Selection([('male','Male'),
                                     ('female','Female'),
                                     ('transgender','Transgender')   
                                    ],string="Allow Gender")
    employee_state = fields.Selection([('joined', 'Roll On'),
                          ('grounding', 'Induction'),
                          ('test_period', 'Probation'),
                          ('employment', 'Employment'),
                          ('notice_period', 'Notice Period'),
                          ('relieved', 'Resigned'),
                          ('terminate', 'Terminated'),
                          ('retired','Retired'),
                          ('suspended','Suspended'),
                          ('superannuation','Superannuation'),
                          ('deceased','Deceased'),
                          ('absconding','Absconding'),
                        ],string="Stage")
    branch_id = fields.Many2one('res.branch',string="Branch")
    leave_type_id = fields.Many2one('hr.leave.type',readonly=True)
    from_date = fields.Date(string="From Date",readonly=True)
    to_date = fields.Date(string="To Date",readonly=True)
    no_of_days_leave = fields.Float(string="No of Days Leave",readonly=True)
    status = fields.Selection([ ('draft', 'To Submit'),
                            ('cancel', 'Cancelled'),
                            ('confirm', 'To Approve'),
                            ('refuse', 'Reject'),
                            ('validate1', 'Second Approval'),
                            ('validate', 'Approved')
                            ],string="Status",readonly=True)
    applied_on = fields.Datetime(string="Applied On",readonly=True)
    days_between_last_leave = fields.Float(string="Days Between Last Leave",readonly=True)
    are_days_weekend = fields.Boolean(string="Are Days Weekend",readonly=True)
    allow_request_unit_half_2 = fields.Boolean(string='Allow Half Day')
    request_unit_half_2 = fields.Boolean(string="Half Day")
    request_date_from_period_2 = fields.Selection([
                                            ('am', 'Morning'), 
                                            ('pm', 'Afternoon')],
                                            string="Date Period Start", default='am')
    
    no_of_days_display_half = fields.Float(string="Duartion Half")
    holiday_half_pay = fields.Boolean(string="Half Pay Holiday")
    pre_post_leaves_ids = fields.One2many('hr.leave.pre.post','pre_post_leave',string='Leaves')
    commuted_leave = fields.Text(string="Leave Type")
    manager_designation_id = fields.Many2one('hr.job',string="Pending With")
    pending_since = fields.Date(string="Pending Since",readonly=True)
    duration_display = fields.Char('Requested(Days)', compute='_compute_duration_display',
        help="Field allowing to see the leave request duration in days or hours depending on the leave_type_request_unit")    # details
    
    holiday_type = fields.Selection([
        ('employee', 'By Employee'),
        ('company', 'By All Department'),
        ('branch','By Branch'),
        ('department', 'By Department'),
        ('category', 'By Employee Tag')],
        string='Allocation Mode', readonly=True, required=True, default='employee',
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
        help='By Employee: Allocation/Request for individual Employee, By Employee Tag: Allocation/Request for group of employees in category')
    by_branch_id = fields.Many2one("res.branch",string="By Branch")
    
    
    @api.constrains('request_unit_half_2')
    @api.onchange('request_unit_half_2')
    def onchange_request_date_from_period_2(self):
        for leave in self:
            if leave.request_unit_half_2 == True:
                leave.request_date_from_period = 'pm'
                leave.request_date_from_period_2 = 'am'
            else:
                leave.request_date_from_period = 'am'
                leave.request_date_from_period_2 = 'pm'

    @api.model
    def create(self, vals):
        res = super(HrLeave, self).create(vals)
        if res.holiday_status_id and res.employee_id:
            
            type = dict(res.fields_get(["employee_type"],['selection'])['employee_type']["selection"]).get(res.employee_type)
            state = dict(res.fields_get(["employee_state"],['selection'])['employee_state']["selection"]).get(res.employee_state)
#             print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLL",type)
            if  res.holiday_status_id.gende == 'transgender' or res.gender == res.holiday_status_id.gende:
#                 print("gendergendergendergendergendergender")
                for leave_type_emp in res.holiday_status_id.allow_service_leave:
                    if type not in leave_type_emp.name:
#                         print("22222222222222222222222",type,leave_type_emp.name)
                        for leave_type_state in res.holiday_status_id.allow_emp_stage: 
                            if state not in leave_type_state.name:
#                                 print("#333333333333333333333",state,leave_type_state.name)
                                raise ValidationError(_("Your re not allow to take this leave"))
            
        if res.holiday_status_id:
            if res.days_between_last_leave == 0:
                if res.leave_type_id:
                    for allowed_prefix in res.holiday_status_id.allowed_prefix_leave:
#                         print("<<<<<<<<<<<<<<<<<<<<<<<<<<",res.holiday_status_id.allowed_prefix_leave,res.leave_type_id.leave_type,allowed_prefix)
                        if res.leave_type_id.leave_type not in allowed_prefix.name:
#                             print("-----------------------------=============")
                            raise ValidationError(_('You Are not allowed to club %s with %s type')% (res.holiday_status_id.name,res.leave_type_id.name))
                        
        leave_ids = self.env['hr.leave'].search([('employee_id','=',res.employee_id.id),('id','!=',res.id)])
        print("?????????????????leave_idsleave_ids?????????",leave_ids)
        if leave_ids:
            for leave in leave_ids:
                ans = []
                if leave.request_date_from < res.request_date_from:
                    d1 = leave.request_date_from    # small date
                    d2 = res.request_date_from # big date
#                     print("////////////////////greater////////////////",d1,d2)
                    days = [d1 + timedelta(days=x) for x in range((d2-d1).days)]
#                     print("????????????????????????????????greaterrrrrrrrrrrr",days)
                elif leave.request_date_from > res.request_date_from:
                    d1 = res.request_date_from   # small date
                    d2 =  leave.request_date_from # big date
#                     print("/////////////////////////lessssssss///////////",d1,d2)
                    days = [d1 + timedelta(days=x) for x in range((d2-d1).days)]
#                     print("???????????????????????????????lessssssss?",days)
                for day in days:
                    week = day.strftime('%Y-%m-%d')
                    print("weekkkkkkk",week)
                    year, month, day = (int(x) for x in week.split('-'))    
                    answer = date(year, month, day).strftime('%A')
                    ans.append(answer)
                    print(":<<<<<<<<<<<<<<<<</<<<<<<<<<",answer,ans )
                    if ans in ['Friday', 'Saturday', 'Sunday']: 
                        print("'Friday', 'Saturday', 'Sunday'LLLLLLLLLLLLLLLLLLLLL")
                        if answer == 'Thursday':
    #                         print("<:::::::::Thursday:::::::::Friday::::::::::::::::::::::::")
                            pre_post_le = self.env['hr.leave.pre.post'].create({'pre_post_leave':res.id,
                                                                                 'pre_post':'pre',
                                                                                 'leave':'leave',
                                                                                 'leave_type_id':res.holiday_status_id.id,
                                                                                 'from_date':week,
                                                                                 'to_date':week,
                                                                                 'no_of_days_leave':1,
                                                                                 'status':leave.state,
                                                                                 'applied_on':leave.create_date,
                                                                                 'days_between_last_leave':0.0,
                                                                                 'are_days_weekend':False
                                                                                })
    #                         print("{{{{{{{{{{{{{{{{{{{{{",pre_post_le)
                        elif answer == 'Friday':
                            print("<:::::::::::::::::Friday:::::::::::::::::::::::::")
                            pre_post_le = self.env['hr.leave.pre.post'].create({'pre_post_leave':res.id,
                                                                                 'pre_post':'pre',
                                                                                 'leave':'leave',
                                                                                 'leave_type_id':res.holiday_status_id.id,
                                                                                 'from_date':week,
                                                                                 'to_date':week,
                                                                                 'no_of_days_leave':1,
                                                                                 'status':leave.state,
                                                                                 'applied_on':leave.create_date,
                                                                                 'days_between_last_leave':0.0,
                                                                                 'are_days_weekend':False
                                                                                })
    #                         print("{{{{{{{{{{{{{{{{{{{{{",pre_post_le)
                        elif answer == 'Saturday':
                            print("<::::::::::Saturday::::::::::::::::::::::::::::::::")
                            pre_post_le = self.env['hr.leave.pre.post'].create({'pre_post_leave':res.id,
                                                                                 'pre_post':'post',
                                                                                 'leave':'holiday',
                                                                                 'leave_type_id':'',
                                                                                 'from_date':week,
                                                                                 'to_date':week,
                                                                                 'no_of_days_leave':1,
                                                                                 'status':leave.state,
                                                                                 'applied_on':leave.create_date,
                                                                                 'days_between_last_leave':0.0,
                                                                                 'are_days_weekend':True
                                                                                })
    #                         print("{{{{{{{{{{{{{{{{{{{{{",pre_post_le)
                        elif answer == 'Sunday':
    #                         print("<::::::::::Sunday::::::::::::::::::::::::::::::::")
                            pre_post_le = self.env['hr.leave.pre.post'].create({'pre_post_leave':res.id,
                                                                                 'pre_post':'post',
                                                                                 'leave':'holiday',
                                                                                 'leave_type_id':'',
                                                                                 'from_date':week,
                                                                                 'to_date':week,
                                                                                 'no_of_days_leave':1,
                                                                                 'status':leave.state,
                                                                                 'applied_on':leave.create_date,
                                                                                 'days_between_last_leave':0.0,
                                                                                 'are_days_weekend':True
                                                                                })
    #                         print("{{{{{{{{{{{{{{{{{{{{{",pre_post_le)
                    
                pre_post_le = self.env['hr.leave.pre.post'].create({'pre_post_leave':res.id,
                                                                             'pre_post':'post',
                                                                             'leave':'leave',
                                                                             'leave_type_id':'',
                                                                             'from_date':leave.request_date_from,
                                                                             'to_date':leave.request_date_to,
                                                                             'no_of_days_leave':leave.number_of_days_display,
                                                                             'status':leave.state,
                                                                             'applied_on':leave.create_date,
                                                                             'days_between_last_leave':0.0,
#                                                                              'are_days_weekend':
                                                                            })
                print("prepostttttttttttttttttttttttttt",pre_post_le)
#                 if pre_post_le:
#                     print
#                     raise Va/lidationError(_('You are not create this leaves'))
        return res
    
    @api.constrains('pre_post_leaves_ids.leave')
    @api.onchange('pre_post_leaves_ids.leave')
    def onchange_pre_post_leaves_ids(self):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        for line in self.pre_post_leaves_ids:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@2")
            if line.leave == 'holiday' and line.leave == 'leave':
                raise ValidationError(_('<<<<<<<<<<<<<<<<<<<'))
    
    @api.constrains('date_from','date_to','employee_id')                
    @api.onchange('date_from','date_to','employee_id')
    def onchange_employee(self):
        for leave in self:
            leave.branch_id = leave.employee_id.branch_id.id
            leave.employee_type = leave.employee_id.employee_type
            leave.employee_state = leave.employee_id.state
            leave.gender = leave.employee_id.gende
            leave.manager_designation_id = leave.employee_id.parent_id.job_id
#             print("{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{",leave.employee_state,leave.employee_type,leave.branch_id)
            leave_ids = self.env['hr.leave'].search([('employee_id','=',leave.employee_id.id),
                                                     ('state','=','validate')],limit=1, order="request_date_to desc")
#             print("<<<<<<<<<<<<<<<<<<<<",leave_ids)
            if leave_ids:
                leave.leave_type_id = leave_ids.holiday_status_id.id
                leave.from_date = leave_ids.request_date_from
                leave.to_date = leave_ids.request_date_to
                leave.no_of_days_leave = leave_ids.number_of_days_display
                leave.status = leave_ids.state
                leave.applied_on = leave_ids.create_date
                days_between_last_leave = leave.request_date_from - leave_ids.request_date_to
                leave.days_between_last_leave = days_between_last_leave.days - 1
                
                d1 = leave_ids.request_date_to   # start date
                d2 = leave.request_date_from  # end date
#                 print("////////////////////////////////////",((d2-d1).days + 1),leave_ids.request_date_to )
                days = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]
#                 print("????????????????????????????????",days)
                for day in days:
                    week = day.strftime('%Y-%m-%d')
                    print("weekkkkkkk",week)
                    year, month, day = (int(x) for x in week.split('-'))    
                    answer = date(year, month, day).strftime('%A')
#                     print(":<<<<<<<<<<<<<<<<<<<<<<<<<<",answer)
                    if answer == 'Saturday' or answer == 'Sunday' or answer == 'Saturday' and answer == 'Sunday':
                        leave.are_days_weekend = True
                        raise ValidationError(_('You are not allowed to apply for leave during this date range because of Sandwich rule applicability on this leave type'))
                    
#             print("???//////////////////////////",leave_ids)
    
    @api.constrains('date_from','date_to','holiday_status_id')
    @api.onchange('date_from','date_to','holiday_status_id')
    def get_validate_on_holiday_status_id(self):
    
        if self.holiday_status_id:
            if self.holiday_status_id.maximum_allow_leave != 0:
                if self.holiday_status_id.maximum_allow_leave < self.number_of_days_display:
                    raise ValidationError(_('You are not allow more then leave present'))
            
        if self.holiday_status_id:
            if self.holiday_status_id.cerificate == True:
                self.attachement = True
            else:
                self.attachement = False
        
        if self.holiday_status_id:
            if self.holiday_status_id.commuted == True:
                self.commuted = True
                self.commuted_leave = 'Commuted Leaves'
            else:
                self.commuted = False         
        
        if self.holiday_status_id and self.number_of_days_display:
            if self.holiday_status_id.leave_type == 'Half Pay Leave':
                self.holiday_half_pay = True
                self.no_of_days_display_half = self.number_of_days_display * 2
            else:
                self.holiday_half_pay = False
            
                
            
    @api.constrains('state', 'number_of_days', 'holiday_status_id')
    def _check_holidays(self):
        for holiday in self:
            if holiday.holiday_type != 'employee' or not holiday.employee_id or holiday.holiday_status_id.allocation_type == 'no':
                continue
            leave_days = holiday.holiday_status_id.get_days(holiday.employee_id.id)[holiday.holiday_status_id.id]
            if self.holiday_status_id.leave_per_year != 0:
                if float_compare(leave_days['remaining_leaves'], 0, precision_digits=2) == -1 or \
                  float_compare(leave_days['virtual_remaining_leaves'], 0, precision_digits=2) == -1:
                    raise ValidationError(_('The number of remaining leaves is not sufficient for this leave type.\n'
                                            'Please also check the leaves waiting for validation.'))
            
    
    @api.constrains('date_from','date_to','holiday_status_id')                
    @api.onchange('date_from','date_to','holiday_status_id')
    def check_date_from_live(self):
        res = {}
        if self.employee_id:
            if self.holiday_status_id.sandwich_rule == False:
                days=[]
                for each in self.employee_id.resource_calendar_id.attendance_ids:
                    if int(each.dayofweek) not in days:
                        days.append(int(each.dayofweek))
                if self.date_from:
    
                    start_date=self.date_from
                    date_number=start_date.weekday()
#                     print("==================",date_number,days)
                    if date_number not in days:
                        res.update({'value': {'date_to': '','date_from': '','number_of_days_display':0.00,'sandwich_rule':False}, 'warning': {
                                   'title': 'Validation!', 'message': 'Since the leave you are applying has got weekends/holidays in between.You are requested to edit the last leave and apply covering the weekends/Holidays..'}})
                if self.date_to:
                    end_date=self.date_to
                    date_number=end_date.weekday()
                    if date_number not in days:
                        res.update({'value': {'date_to': '','number_of_days_display':0.00,'sandwich_rule':False}, 'warning': {
                                   'title': 'Validation!', 'message': 'Since the leave you are applying has got weekends/holidays in between. You are requested to edit the last leave and apply covering the weekends/Holidays..'}})

        return res
    
    @api.constrains('request_date_from','request_date_to','employee_id')
    @api.onchange('request_date_from','request_date_to','employee_id')
    def get_half_pay_leave_2(self):
        if self.request_date_from and self.request_date_to:
            if self.request_date_from == self.request_date_to:
                self.allow_request_unit_half_2 = True
            else:
                self.allow_request_unit_half_2 = False
        
    
    @api.constrains('date_from','date_to','employee_id','request_unit_half_2') 
    @api.onchange('date_from', 'date_to', 'employee_id','request_unit_half_2')
    def _onchange_leave_dates(self):
        days = 0.0
        if self.date_from and self.date_to:
            self.number_of_days = self._get_number_of_days(self.date_from, self.date_to, self.employee_id.id)
#             print("Number of daysssssssssssssqqqqqqqqqssssssssss",self.number_of_days)
            if self.request_unit_half_2 == True:
                days = self.number_of_days - 0.5
#                 print("dayssssssssssssssssss",days)
                self.number_of_days = days  
#                 print("________--------------------------",self.number_of_days)
#                 self.number_of_days_display = self.number_of_days
        else:
            self.number_of_days = 0
            
    @api.multi
    def action_refuse(self):
        today = date.today()
        if self.holiday_status_id.carried_forward != True:
            if self.request_date_from:
                year = self.request_date_from.year
                print("LLLLLLLLLLLLLLLLLLLLLLLLLLLL",year,today.year)
                if today.year != year:
                    print("?///////////////////")
                    raise ValidationError(_("You are not carried forward leave because leave is not in current year"))
                else:
                    return super(HrLeave,self).action_refuse()
        else:
            return super(HrLeave,self).action_refuse()
        
        
    @api.multi
    def action_approve(self):
        today = date.today()
        for leave in self:
            print("Pppppppppppppppppppppp")
            leave.pending_since = today
            print("????????????????????????????",leave.pending_since)
            if not leave.name:
                leave.name = '-'
                return super(HrLeave, self).action_approve()
            else:
                return super(HrLeave, self).action_approve()

    @api.multi
    def _create_resource_leave(self):
        """ This method will create entry in resource calendar leave object at the time of holidays validated """
        for leave in self:
            date_from = fields.Datetime.from_string(leave.date_from)
            date_to = fields.Datetime.from_string(leave.date_to)
            print("resource_calendar_leavesresource_calendar_leavesresource_calendar_leaves")
            self.env['resource.calendar.leaves'].create({
                'name': leave.name,
                'date_from': fields.Datetime.to_string(date_from),
                'holiday_id': leave.id,
                'date_to': fields.Datetime.to_string(date_to),
                'resource_id': leave.employee_id.resource_id.id,
                'calendar_id': leave.employee_id.resource_calendar_id.id,
                'time_type': leave.holiday_status_id.time_type,
                'date':leave.date_from
            })
        return True
    
    @api.onchange('request_date_from_period', 'request_hour_from', 'request_hour_to',
                  'request_date_from', 'request_date_to',
                  'employee_id')
    def _onchange_request_parameters(self):
        if not self.request_date_from:
            self.date_from = False
            return

        if self.request_unit_half or self.request_unit_hours:
            print()
            #comment below line because when we select half day it change the to date
#             self.request_date_to = self.request_date_from

        if not self.request_date_to:
            self.date_to = False
            return

#         roster_id = self.env['hr.attendance.roster'].search([('employee_id','=',self.employee_id.id),('date','=',self.date_from.date())],limit=1)
#         # print("-------------roster_id", roster_id)
#         if roster_id and roster_id.shift_id:
#             if roster_id.shift_id.night_shift:
#                 self.night_shift = True
#             else:
#                 self.night_shift = False
#             domain =[('calendar_id', '=',roster_id.shift_id.id)]
#         else:
#             if self.employee_id.resource_calendar_id.night_shift or self.env.user.company_id.resource_calendar_id.night_shift:
#                 self.night_shift = True             
#             else:
#                 self.night_shift = False
        domain = [('calendar_id', '=',self.employee_id.resource_calendar_id.id or self.env.user.company_id.resource_calendar_id.id)]
        attendances = self.env['resource.calendar.attendance'].search(domain, order='dayofweek, day_period DESC')

        # find first attendance coming after first_day
        attendance_from = next((att for att in attendances if int(att.dayofweek) >= self.request_date_from.weekday()),
                               attendances[0])
        # find last attendance coming before last_day
        attendance_to = next(
            (att for att in reversed(attendances) if int(att.dayofweek) <= self.request_date_to.weekday()),
            attendances[-1])

        
        if self.request_unit_half:
            if self.request_date_from_period == 'am':
                hour_from = float_to_time(attendance_from.hour_from)
                print("hour_fromhour_fromhour_fromhour_from",hour_from)
                hour_to = float_to_time(attendance_from.hour_to)
                print("???????//hour_fromhour_fromhour_from",hour_to)
            else:
                hour_from = float_to_time(attendance_to.hour_from)
                hour_to = float_to_time(attendance_to.hour_to)
                
        elif self.request_unit_hours:
            # This hack is related to the definition of the field, basically we convert
            # the negative integer into .5 floats
            hour_from = float_to_time(
                abs(self.request_hour_from) - 0.5 if self.request_hour_from < 0 else self.request_hour_from)
#             print("111111111111111111111111111111111",hour_from)
            hour_to = float_to_time(
                abs(self.request_hour_to) - 0.5 if self.request_hour_to < 0 else self.request_hour_to)
#             print("22222222222222222222222222222",hour_to)
        elif self.request_unit_custom:
            hour_from = self.date_from.time()
            hour_to = self.date_to.time()
        else:
            hour_from = float_to_time(attendance_from.hour_from)
            hour_to = float_to_time(attendance_to.hour_to)

        tz = self.env.user.tz if self.env.user.tz and not self.request_unit_custom else 'UTC'  # custom -> already in UTC
        self.date_from = timezone(tz).localize(datetime.combine(self.request_date_from, hour_from)).astimezone(
            UTC).replace(tzinfo=None)
        self.date_to = timezone(tz).localize(datetime.combine(self.request_date_to, hour_to)).astimezone(UTC).replace(
            tzinfo=None)
        
class HRLeavePrePost(models.Model):
    _name = 'hr.leave.pre.post'
    _description = 'HR Leave Pre Post'
    
    pre_post_leave = fields.Many2one('hr.leave',string="Leaves")
    pre_post = fields.Selection([('pre','Pre'),
                                 ('post','Post')
                                ],string="Pre/Post")
    leave_type_id = fields.Many2one('hr.leave.type',readonly=True)
    from_date = fields.Date(string="From Date",readonly=True)
    to_date = fields.Date(string="To Date",readonly=True)
    no_of_days_leave = fields.Float(string="No of Days Leave",readonly=True)
    leave = fields.Selection([('holiday','H'),
                              ('leave','L')
                            ],string="Leave Is")
    status = fields.Selection([ ('draft', 'To Submit'),
                            ('cancel', 'Cancelled'),
                            ('confirm', 'To Approve'),
                            ('refuse', 'Refused'),
                            ('validate1', 'Second Approval'),
                            ('validate', 'Approved')
                            ],string="Status",readonly=True)
    applied_on = fields.Datetime(string="Applied On",readonly=True)
    days_between_last_leave = fields.Float(string="Days Between Last Leave",readonly=True)
    are_days_weekend = fields.Boolean(string="Are Days Weekend",readonly=True)

    

            