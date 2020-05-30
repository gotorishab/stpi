# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import calendar
from datetime import datetime,date
from datetime import datetime,timedelta
import datetime

from dateutil.relativedelta import relativedelta
# from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import math

class AppraisalMangWizard(models.TransientModel):
    _name = 'wizard.appraisal.mang'
    _description = 'Wizard Appraisal Management'
    
    
    date_range = fields.Many2one('date.range','Date range')
    date_from = fields.Date(string="Date From",required=True)
    date_to = fields.Date(string="Date To",required=True)

    type = fields.Selection([('by_emp', 'Employee'),
                             ('by_dept', 'Department')
                             ], string="Type", default="by_emp")

    emp_ids = fields.Many2many('hr.employee', string="Employee")
    dept_ids = fields.Many2many('hr.department', string="Department")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)

    def report_pdf(self):
        report_id = self.env['ir.actions.report']
        context = self.env.context
        report_id = self.env['ir.actions.report'].with_context(context).search(
            [('report_name', '=', 'appraisal_management_report.report_appraisal_mang')], limit=1)

        if not report_id:
            raise UserError(
                _("Bad Report Reference") + _("This report is not loaded into the database: "))
        # print("--------------", report_id)

        return {
            'context': context,
            'type': 'ir.actions.report',
            'report_name': report_id.report_name,
            'report_type': report_id.report_type,
            'report_file': report_id.report_file,
            'name': report_id.name,
        }


    @api.onchange('date_range')
    def get_dates(self):
        for s in self:
            if s.date_range:
                s.date_from = s.date_range.date_start
                s.date_to = s.date_range.date_end

    def get_month_days(self):
        delta = self.date_to - self.date_from
        return delta.days if delta.days <= 31 else 31
 
    def last_day_of_month(self,any_day):
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
        return next_month - datetime.timedelta(days=next_month.day)

    def _get_data(self,emp):
        res = []
        
        startDate = fields.Date.from_string(self.date_from)
        endDate = fields.Date.from_string(self.date_to)
        
        start_date = start = datetime.datetime.strptime(str(startDate), '%Y-%m-%d').date()
#         print("!!!!!!!!!!!!!!!!!!!!",start_date)
        end_date = datetime.datetime.strptime(str(endDate), '%Y-%m-%d').date()
        
        while start_date <= end_date:
            
            lwp_leaves_count = 0.0
            lwop_leaves_count = 0.0
            absent_attend = 0.0
            late_coming_count = 0.0
            late_coming_min_cou = 0.0
            half_day_dec = 0.0
            leave_adj = 0.0
            no_punching = 0.0
            
            
            last_day_for_month = self.last_day_of_month(datetime.date(start_date.year,start_date.month,1))
            # print("======================",last_day_for_month)

            s_date = start_date
            while s_date <= last_day_for_month:

                lwp_leave_ids = self.env['hr.leave'].search([('date_from', '<=', s_date),
                                        ('date_to', '>=', s_date),
                                        ('state','!=', 'refuse'),
                                        ('employee_id', '=', emp.id)])
                # print("======================", lwp_leave_ids,s_date)
                if lwp_leave_ids:
                    for l_id in lwp_leave_ids:
                        if l_id.holiday_status_id.unpaid:
                            if l_id.request_unit_half:
                                lwop_leaves_count += 0.5
                            else:
                                lwop_leaves_count +=1
                        else:
                            if l_id.request_unit_half:
                                lwp_leaves_count += 0.5
                            else:
                                lwp_leaves_count +=1

                s_date += timedelta(days=1)

    #             lwop_leave_ids = self.env['hr.leave'].search([('date_from', '>=', start_date),
    #                                                           ('date_to', '<=', last_day_for_month + timedelta(days=1)),
    #                                                           ('state', '!=', 'refuse'),
    #                                                           ('holiday_status_id.unpaid', '=',True),
    #                                                           ('employee_id', '=', emp.id)])
    # #             print("leaves===================",lwp_leave_ids)
    #             if lwop_leave_ids:
    #                 for l_id in lwop_leave_ids:
    #                     lwop_leaves_count += l_id.number_of_days_display

            curatted_atte_ids = self.env['currated.attendance'].search([('expected_start','>=',start_date),
                                                                        ('expected_end','<=',last_day_for_month),
                                                                        ('employee_id','=',emp.id),
                                                                        ('absent','=',True)])
             
#             print("?????????????????????????curatted_atte_ids",curatted_atte_ids)
            if curatted_atte_ids:
                absent_attend = len(curatted_atte_ids)
             
            curatted_atte_late_com_ids = self.env['currated.attendance'].search([('expected_start','>=',start_date),
                                                                        ('expected_end','<=',last_day_for_month),
                                                                        ('employee_id','=',emp.id),
                                                                        ('late_coming','=',True)])
#             print("+++++++++++++curatted_atte_late_com_ids",curatted_atte_late_com_ids)
            
            if curatted_atte_late_com_ids:
                late_coming_count = len(curatted_atte_late_com_ids)
                     
            late_com_min_id = self.env['currated.attendance'].search([('expected_start','>=',start_date),
                                                                        ('expected_end','<=',last_day_for_month),
                                                                        ('employee_id','=',emp.id),
                                                                        ])
            if late_com_min_id:
                for late_coming in late_com_min_id:
                    late_coming_min_cou += round(late_coming.late_coming_min / 60)
                     
            half_day_ded_ids = self.env['currated.attendance'].search([('expected_start','>=',start_date),
                                                                        ('expected_end','<=',last_day_for_month),
                                                                        ('employee_id','=',emp.id),
                                                                        ('half_day_ded','=',True)])
            if half_day_ded_ids:
                half_day_dec = len(half_day_ded_ids)
                    
            leave_adj_ids = self.env['hr.leave'].search([('date_from', '>=', start_date), 
                                    ('date_to', '<=', last_day_for_month),
                                    ('state','!=', 'refuse'),
                                    ('holiday_status_id.casual_leaves', '=', True),
                                    ('adjusted_late_coming', '=', True),
                                    ('employee_id', '=', emp.id)])
#             print("Leave AdjustmentLeave AdjustmentLeave Adjustment===================",len(leave_adj_ids))
            if leave_adj_ids:
                leave_adj = len(leave_adj_ids)
#             print("leave_adj------------------",leave_adj)
            
            no_punching_ids = self.env['hr.leave'].search([('date_from', '>=', start_date), 
                                    ('date_to', '<=', last_day_for_month),
                                    ('state','!=', 'refuse'),
                                    ('holiday_status_id.casual_leaves', '=', True),
                                    ('adjusted_no_punching', '=', True),
                                    ('employee_id', '=', emp.id)])
#             print("no_punching_ids no_punching_ids no_punching_ids===================",len(no_punching_ids))
            
            if no_punching_ids:
                no_punching = len(no_punching_ids)
            
            
            start_date += relativedelta(months=1)
            res.append({'month_name': startDate.strftime('%B')+"-"+str(startDate.year),
                        'lwp_leave':lwp_leaves_count,
                        'lwop_leave':lwop_leaves_count,
                        'absent':absent_attend,
                        'late_coming':late_coming_count,
                        'late_coming_min':late_coming_min_cou,
                        'half_day':half_day_dec,
                        'adj_late_acoming':leave_adj,
                        'adj_no_punching':no_punching})
            startDate += relativedelta(months=+1)
#         print("===res", res)
        return res


    def add_time_zone(self,date):
        # print("--------------------sting_date--------------------",sting_date)
        datetime_value = date + timedelta(hours=5, minutes=30, seconds=00)
        return datetime_value

    def get_emp_ids(self):
        emp_ids = self.env['hr.employee']
#         print("?????????????????????????",emp_ids)
        if not self.emp_ids:
            emp_ids = self.env['hr.employee'].search([])
#             print("!!!!!!!!!!!!!!!!!!!!",emp_ids)
        else:
            emp_ids = self.emp_ids
#             print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@",emp_ids)
        return emp_ids

    @api.model
    def value_to_html(self, value):
        sign = math.copysign(1.0, value)
        hours, minutes = divmod(abs(value) * 60, 60)
        minutes = round(minutes)
        if minutes == 60:
            minutes = 0
            hours += 1
        return '%d:%02d' % (sign * hours, minutes)



    def _date_is_day_off(self, date,emp):
        list = []
        for off in emp.weekoff_ids:
            week_int = self.dayNameFromWeekday(off.name)
            list.append(week_int)
        # return date.weekday() in (calendar.SATURDAY, calendar.SUNDAY,)
        return date.weekday() in list

    def _get_day(self,emp):
        res = []
        start_date = fields.Date.from_string(self.date_from)
        self.total_working_days = 0
        for x in range(0,self.get_month_days()+1):

            color = ''
            color = '#ababab' if self._date_is_day_off(start_date,emp) else ''
#             if self._date_is_day_off(start_date, emp):
#                 color = '#ababab'
#             else:
#                 self.total_working_days += 1
            self.total_working_days += 1
            res.append({'day_str': start_date.strftime('%a'), 'day': start_date.day , 'color': color})
            start_date = start_date + relativedelta(days=1)
        return res

    def _get_attendance(self,emp):
        res = []
        start_date = fields.Date.from_string(self.date_from)
        self.present_days = 0
        for x in range(0,self.get_month_days()+1):
            check_in = check_out = ''
            color = ''
            present = "A"
            curated_ids = self.env['currated.attendance']
            if emp.resource_calendar_id.night_shift == False:
                curated_ids += self.env['currated.attendance'].search([('employee_id','=',emp.id),
                                                                  ('expected_start','>=',start_date),('expected_end','<=',start_date)],limit = 1)
            if emp.resource_calendar_id.night_shift == True:
                curated_ids += self.env['currated.attendance'].search([('employee_id', '=', emp.id),('expected_start', '>=', start_date),
                                                                       ('expected_end', '<=', start_date + relativedelta(days=1))], limit=1)
            if self._date_is_day_off(start_date,emp):
                present = 'WO'
            if curated_ids.check_in or curated_ids.check_out:
                present = "P"
                
                # print("======ids", curated_ids)
                if curated_ids.check_in:
                    check_in_timez = self.add_time_zone(curated_ids.check_in)
                    check_in= "" +str(check_in_timez.hour) + "." + str(check_in_timez.minute)
                if curated_ids.check_out:
                    check_out_timez = self.add_time_zone(curated_ids.check_out)
                    check_out = "" + str(check_out_timez.hour) + "." + str(check_out_timez.minute)

            # print("===dict",dict)

            leaves = self.env['hr.leave']
            if not curated_ids or (not curated_ids.check_in and not curated_ids.check_out):
                
                public_holiday = self.env['resource.calendar.leaves'].search([('calendar_id','=',emp.resource_calendar_id.id),
                                                                       ('date_from','<=',start_date),('date_to','>=',start_date),
                                                                       ('resource_id','=',False)])
                
                if public_holiday:
                    present = "HLD"
                
                leaves = leaves.search([('request_date_from', '<=', start_date), ('request_date_to', '>=', start_date),
                          ('state', '=', 'validate'), ('employee_id', '=', emp.id)],limit=1)
                if leaves:
                    present = "L"
                    color = leaves.holiday_status_id.color_name
            
            if present != "A":
                if leaves:
                    if leaves.holiday_status_id.unpaid == False:
                        self.present_days += 1
                else:
                    self.present_days += 1

            res.append( {'present': present, 'color': color,
                         'check_in':check_in,
                         'check_out':check_out,
                         'duty_hours':self.value_to_html(curated_ids.duty_hours) if curated_ids.duty_hours > 0.0 else '',
                         'late_coming': self.value_to_html(curated_ids.late_coming_min) if curated_ids.late_coming_min > 0.0 else '',
                         'early_going': self.value_to_html(curated_ids.early_going_min) if curated_ids.early_going_min > 0.0 else '',
                         'overtime': self.value_to_html(curated_ids.overtime_hours) if curated_ids.overtime_hours > 0.0 else '',
                         })

            start_date = start_date + relativedelta(days=1)
        return  res


    def _get_data_from_report(self, data):
        res = []
        Employee = self.env['hr.employee']

        res.append({'data': []})
        for emp in Employee.browse(data['emp']):
            res[0]['data'].append({
                'emp': emp.name,
                'display': self._get_leaves_summary(data['date_from'], emp.id, data['holiday_type']),
                'sum': self.sum
            })
        return res


    def _get_holidays_status(self):
        res = []
        for holiday in self.env['hr.leave.type'].search([]):
            res.append({'color': holiday.color_name, 'name': holiday.name})
        return res


    def dayNameFromWeekday(self,weekday):
        if weekday == "Monday":
            return 0
        if weekday == "Tuesday":
            return 1
        if weekday == "Wednesday":
            return 2
        if weekday == "Thursday":
            return 3
        if weekday == "Friday":
            return 4
        if weekday == "Saturday":
            return 5
        if weekday == "Sunday":
            return 6




