from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from odoo.tools import float_compare
import datetime 
from reportlab.lib.randomtext import leadins
from twilio.twiml.voice_response import Leave

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
                                     ('both','Both')   
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
                            ('refuse', 'Refused'),
                            ('validate1', 'Second Approval'),
                            ('validate', 'Approved')
                            ],string="Status",readonly=True)
    applied_on = fields.Datetime(string="Applied On",readonly=True)
    days_between_last_leave = fields.Float(string="Days Between Last Leave")
    are_days_weekend = fields.Boolean(string="Are Days Weekend",readonly=True)
    
    @api.model
    def create(self, vals):
        res = super(HrLeave, self).create(vals)
        if res.holiday_status_id and res.employee_id:
            
            type = dict(res.fields_get(["employee_type"],['selection'])['employee_type']["selection"]).get(res.employee_type)
            state = dict(res.fields_get(["employee_state"],['selection'])['employee_state']["selection"]).get(res.employee_state)
#             print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLL",type)
            if  res.holiday_status_id.allow_gender == 'both' or res.gender == res.holiday_status_id.allow_gender:
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
            
        return res
    
 
    @api.constrains('date_from','date_to','employee_id')                
    @api.onchange('date_from','date_to','employee_id')
    def onchange_employee(self):
        for leave in self:
            leave.branch_id = leave.employee_id.branch_id.id
            leave.employee_type = leave.employee_id.employee_type
            leave.employee_state = leave.employee_id.state
            leave.gender = leave.employee_id.gender
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
                leave.days_between_last_leave = days_between_last_leave.days
                
                d1 = leave_ids.request_date_to   # start date
                d2 = leave.request_date_from  # end date
                
                days = [d1 + datetime.timedelta(days=x) for x in range((d2-d1).days + 1)]
#                 print("????????????????????????????????",days)
                for day in days:
                    week = day.strftime('%Y-%m-%d')
                    
                    year, month, day = (int(x) for x in week.split('-'))    
                    answer = datetime.date(year, month, day).strftime('%A')
#                     print(":<<<<<<<<<<<<<<<<<<<<<<<<<<",answer)
                    if answer == 'Saturday' or answer == 'Sunday':
                        leave.are_days_weekend = True
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
                    if date_number not in days:
                        res.update({'value': {'date_to': '','date_from': '','number_of_days_display':0.00,'sandwich_rule':False}, 'warning': {
                                   'title': 'Validation!', 'message': 'This day is already holiday.'}})
                if self.date_to:
                    end_date=self.date_to
                    date_number=end_date.weekday()
                    if date_number not in days:
                        res.update({'value': {'date_to': '','number_of_days_display':0.00,'sandwich_rule':False}, 'warning': {
                                   'title': 'Validation!', 'message': 'This day is already holiday.'}})

        return res

            