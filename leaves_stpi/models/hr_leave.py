from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class HrLeave(models.Model):
    _inherit = 'hr.leave'
    _description = 'HR Leave Changes For STPI'
    
    
    attachement = fields.Boolean(string="attachment")
    attachement_proof = fields.Binary(string="Attachment Proof",required=True)
    
    
    @api.constrains('holiday_status_id')
    @api.onchange('holiday_status_id')
    def get_validate_on_holiday_status_id(self):
        for leave in self:
            if leave.holiday_status_id:
                if leave.holiday_status_id.maximum_allow_leave < leave.number_of_days_display:
                    raise ValidationError(_('You are not allow more then leave present'))
                
            if leave.holiday_status_id:
                if leave.holiday_status_id.cerificate == True:
                    leave.attachement = True
                    
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

            