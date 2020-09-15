from odoo import models, fields, api, _
from datetime import time, datetime,timedelta
from datetime import date, datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'
    _description= ' Resource Calendar Branch'
    
    branch_id = fields.Many2one('res.branch',string="Branch",required=True)
    max_allowed_rh = fields.Float(string='Max RH')
    # max_allowed_gh = fields.Float(string='Max Allowed Gestured Holiday')
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    week_list = fields.Selection([
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday')
    ], string='Weekday')

    rh_leave_type=fields.Many2one('hr.leave.type', string='RH Leave Type')

    assign_holiday_action_perform = fields.Selection([('assign_weekends', 'Assign to existing list'),
                                                 ('delete_all_existing_list', 'Delete the existing list'),
                                                 ('delete_all_existing_list_and_assign_weekends', 'Delete existing and assign'),
                                                 ], string='Action performed', default='delete_all_existing_list_and_assign_weekends',
                                                )


    #
    #
    #
    # @api.onchange('name','date')
    # def check_unquie_holiday(self):
    #     for rec in self:
    #         count = 0
    #         emp_id = self.env['resource.calendar.leaves'].search(
    #             [('date', '=', a.date),('name', '=', a.name), ('calendar_id', '=', rec.calendar_id.id)])
    #         for e in emp_id:
    #             count += 1
    #         if count > 1:
    #             raise ValidationError("Holiday must be unique")
    #
    #         for dup in rec.global_leave_ids:
    #             if dup.date


    @api.multi
    def assign_weekends(self):
        for rec in self:
            if not (rec.from_date and rec.to_date and rec.week_list):
                raise ValidationError(
                    _("Please enter all the required fields, from date, to date and Weekday"))
            else:
                excluded = [int(rec.week_list)]
                global_leave_ids = []
                if int(rec.week_list) == 1:
                    week_day = 'Monday'
                elif int(rec.week_list) == 2:
                    week_day = 'Tuesday'
                elif int(rec.week_list) == 3:
                    week_day = 'Wednesday'
                elif int(rec.week_list) == 4:
                    week_day = 'Thursday'
                elif int(rec.week_list) == 5:
                    week_day = 'Friday'
                elif int(rec.week_list) == 6:
                    week_day = 'Saturday'
                elif int(rec.week_list) == 7:
                    week_day = 'Sunday'
                else:
                    week_day = ''
                a = time()
                b = time(23, 56, 56)
                fdate = rec.from_date
                while fdate <= rec.to_date:
                    if fdate.isoweekday() in excluded:
                        entered_date = datetime.strptime(str(fdate), '%Y-%m-%d')
                        date_from = entered_date - timedelta(hours=5, minutes=30, seconds=00)
                        date_to = entered_date + timedelta(hours=18, minutes=28, seconds=58)
                        global_leave_ids.append((0, 0, {
                            'calendar_id': rec.id,
                            'name': week_day,
                            'date': fdate,
                            'date_from': date_from,
                            'date_to': date_to,
                        }))
                    fdate += relativedelta(days=1)
                rec.global_leave_ids = a = global_leave_ids
                # count = 0
                # emp_id = self.env['resource.calendar.leaves'].search(
                #     [('date', '=', a.date), ('name', '=', a.name), ('calendar_id', '=', rec.calendar_id.id)])
                # for e in emp_id:
                #     count += 1
                # if count > 1:
                #     raise ValidationError("Holiday must be unique")

    @api.multi
    def perform_ah_action(self):
        for rec in self:
            if rec.assign_holiday_action_perform == 'assign_weekends':
                rec.assign_weekends()
            elif rec.assign_holiday_action_perform == 'delete_all_existing_list':
                rec.delete_all_existing_list()
            elif rec.assign_holiday_action_perform == 'delete_all_existing_list_and_assign_weekends':
                rec.delete_all_existing_list_and_assign_weekends()
            else:
                pass



    @api.multi
    def delete_all_existing_list(self):
        for rec in self:
            rec.global_leave_ids.unlink()

    @api.multi
    def delete_all_existing_list_and_assign_weekends(self):
        for rec in self:
            rec.global_leave_ids.unlink()
            if not (rec.from_date and rec.to_date and rec.week_list):
                raise ValidationError(
                    _("Please enter all the required fields, from date, to date and Weekday"))
            else:
                excluded = [int(rec.week_list)]
                global_leave_ids = []
                if int(rec.week_list) == 1:
                    week_day = 'Monday'
                elif int(rec.week_list) == 2:
                    week_day = 'Tuesday'
                elif int(rec.week_list) == 3:
                    week_day = 'Wednesday'
                elif int(rec.week_list) == 4:
                    week_day = 'Thursday'
                elif int(rec.week_list) == 5:
                    week_day = 'Friday'
                elif int(rec.week_list) == 6:
                    week_day = 'Saturday'
                elif int(rec.week_list) == 7:
                    week_day = 'Sunday'
                else:
                    week_day = ''
                a = time()
                b = time(23, 56, 56)
                fdate = rec.from_date
                while fdate <= rec.to_date:
                    if fdate.isoweekday() in excluded:
                        entered_date = datetime.strptime(str(fdate), '%Y-%m-%d')
                        date_from = entered_date - timedelta(hours=5, minutes=30, seconds=00)
                        date_to = entered_date + timedelta(hours=18, minutes=28, seconds=58)
                        global_leave_ids.append((0, 0, {
                            'calendar_id': rec.id,
                            'name': week_day,
                            'date': fdate,
                            'date_from': date_from,
                            'date_to': date_to,
                        }))
                    fdate += relativedelta(days=1)
                rec.global_leave_ids = a = global_leave_ids


    @api.multi
    def allow_public_holiday_on_caledar(self):
        for resource in self:
            employee_ids = self.env['hr.employee'].search([('branch_id','=',resource.branch_id.id)])
            for employee in employee_ids:
                employee.resource_calendar_id = self.id
                
                
class ResourceCalendarLeaves(models.Model):
    _inherit = 'resource.calendar.leaves'
    _description= ' Resource Calendar Leaves'
    
    date = fields.Date(string="Date",required=True)
    holiday_type = fields.Selection([('rh', 'RH'),
                                      ('gh', 'GH')], string='Holiday Type',
                                     )
    restricted_holiday = fields.Boolean(string='Restricted Holiday')
    gestured_holiday = fields.Boolean(string='Gestured Holiday')
    rh_leave_type=fields.Many2one('hr.leave.type', string='RH Leave Type')

    @api.onchange('holiday_type')
    @api.constrains('holiday_type')
    def onchange_h_type(self):
        for rec in self:
            if rec.holiday_type == 'rh':
                rec.restricted_holiday = True
                rec.gestured_holiday = False
            elif rec.holiday_type == 'gh':
                rec.restricted_holiday = False
                rec.gestured_holiday = True
            else:
                rec.restricted_holiday = False
                rec.gestured_holiday = False



    @api.onchange('date')
    def onchange_date(self):
        a = time()
        b = time(23, 56, 56)
        for line in self:
            if line.date:
                entered_date = datetime.strptime(str(line.date), '%Y-%m-%d')
#                 print("??????????????????????",entered_date)
                line.date_from = entered_date - timedelta(hours=5,minutes=30,seconds=00)
                line.date_to = entered_date + timedelta(hours=18,minutes=28,seconds=58)


