from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from odoo.tools import float_compare

class HrLeave(models.Model):
    _inherit = 'hr.leave'
    _description = 'HR Leave Changes For STPI'
    
    
    attachement = fields.Boolean(string="attachment")
    attachement_proof = fields.Binary(string="Attachment Proof")
    commuted = fields.Boolean(string="Commuted")
    
#     @api.onchange('employee_id')
#     def get_employee_detail(self):
#         for hr in self:
#             print("???//////////////////////////",hr.employee_id.state,hr.employee_id.employee_type,hr.employee_id.gender)
    
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

            