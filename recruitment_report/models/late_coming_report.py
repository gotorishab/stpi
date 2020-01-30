from odoo import fields,api,models
import math
from datetime import datetime, timedelta
from pytz import timezone, UTC


class LateComingReport(models.Model):
    _name="recruitment.report"
    _description="Recruitment Report"



    emp_code = fields.Char(string="Employee Code")

    emp_name = fields.Char(string="Employee Name")
    emp_id = fields.Many2one('hr.employee',string="Employee")
    dept_id = fields.Many2one('hr.department',string="Department")

    check_in = fields.Datetime(string="Check In")
    check_out = fields.Datetime(string="Check Out")


    duty_hr = fields.Float(string="Duty Hours")
    actual_duty_hr = fields.Float(string="Actual Duty Hours")
    recruitment_min = fields.Float(string="Late Coming Min")
    roster_id = fields.Many2one('hr.attendance.roster',string="Roster")

#     branch_id = fields.Many2one('res.branch',string= 'Branch')

    def get_recruitment_report(self):
        return self.env['recruitment.report'].search([])

    @api.model
    def value_to_html(self, value):
        sign = math.copysign(1.0, value)
        hours, minutes = divmod(abs(value) * 60, 60)
        minutes = round(minutes)
        if minutes == 60:
            minutes = 0
            hours += 1
        return '%02d:%02d' % (sign * hours, minutes)

    def get_time_without_tz(self, time):
        ret_time = time + timedelta(hours=5, minutes=30)
        return datetime.strftime(ret_time, '%d-%m-%Y %H:%M:%S')
    
    @api.multi
    def name_get(self,roster_id):
        name = ''
        for record in roster_id:
            name = (str(record.employee_id.name) + '-' + str(record.shift_id.name))
        return name