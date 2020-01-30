# -*- coding: utf-8 -*-
# © 2018-Today Aktiv Software (http://aktivsoftware.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields,api,_
from odoo.exceptions import UserError, ValidationError
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from pytz import timezone, UTC
from datetime import timedelta
from collections import defaultdict
from odoo.tools import float_utils
from datetime import datetime
from pytz import utc
import math


class HrHolidays(models.Model):
    _inherit = 'hr.leave'
    _name = 'hr.leave'
    _description = "Leave"

    sandwich_rule = fields.Boolean('Sandwich Rule')
    hr_consider_sandwich_rule= fields.Boolean('Apply Sandwich Rule',default=True)
    night_shift = fields.Boolean(default=False)
    count_no_of_leave = fields.Integer('Number Of Leave')

    @api.onchange('request_date_from', 'request_date_to')
    def compute_number_of_leave(self):
        if self.request_date_from and self.request_date_to:
            self.count_no_of_leave = (self.request_date_to - self.request_date_from).days +1

    @api.onchange('number_of_days_display','hr_consider_sandwich_rule')
    def check_leave_type(self):
        if self.hr_consider_sandwich_rule and self.employee_id and self.number_of_days_display:
            time_delta = self.date_to - self.date_from
            self.number_of_days_display = math.ceil(time_delta.days + float(time_delta.seconds) / 86400)
        else:
            if self.employee_id and self.date_from and self.date_to:
                self.sandwich_rule = False
                self.number_of_days_display = self._get_number_of_days(self.date_from, self.date_to, self.employee_id.id)

    @api.onchange('date_from','date_to')
    def check_date_from_live(self):
        res = {}
        if self.employee_id:
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

    @api.onchange('request_date_from_period', 'request_hour_from', 'request_hour_to',
                  'request_date_from', 'request_date_to',
                  'employee_id')
    def _onchange_request_parameters(self):
        if not self.request_date_from:
            self.date_from = False
            return

        if self.request_unit_half or self.request_unit_hours:
            self.request_date_to = self.request_date_from

        if not self.request_date_to:
            self.date_to = False
            return

        roster_id = self.env['hr.attendance.roster'].search([('employee_id','=',self.employee_id.id),('date','=',self.date_from.date())],limit=1)
        # print("-------------roster_id", roster_id)
        if roster_id and roster_id.shift_id:
            if roster_id.shift_id.night_shift:
                self.night_shift = True
            else:
                self.night_shift = False
            domain =[('calendar_id', '=',roster_id.shift_id.id)]
        else:
            if self.employee_id.resource_calendar_id.night_shift or self.env.user.company_id.resource_calendar_id.night_shift:
                self.night_shift = True             
            else:
                self.night_shift = False
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
                hour_to = float_to_time(attendance_from.hour_to)
            else:
                hour_from = float_to_time(attendance_to.hour_from)
                hour_to = float_to_time(attendance_to.hour_to)
        elif self.request_unit_hours:
            # This hack is related to the definition of the field, basically we convert
            # the negative integer into .5 floats
            hour_from = float_to_time(
                abs(self.request_hour_from) - 0.5 if self.request_hour_from < 0 else self.request_hour_from)
            hour_to = float_to_time(
                abs(self.request_hour_to) - 0.5 if self.request_hour_to < 0 else self.request_hour_to)
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

    @api.multi
    @api.depends('number_of_days')
    def _compute_number_of_hours_display(self):
        for holiday in self:
            roster_id = self.env['hr.attendance.roster'].search([('employee_id', '=', holiday.employee_id.id), ('date', '=', holiday.date_from.date())], limit=1)
            # print("---------2----roster_id", roster_id)
            if roster_id and roster_id.shift_id:
                calendar = roster_id.shift_id
            else:
                calendar = holiday.employee_id.resource_calendar_id or self.env.user.company_id.resource_calendar_id
            if holiday.date_from and holiday.date_to:
                number_of_hours = calendar.get_work_hours_count(holiday.date_from, holiday.date_to)
                holiday.number_of_hours_display = number_of_hours or (holiday.number_of_days * HOURS_PER_DAY)
            else:
                holiday.number_of_hours_display = 0


ROUNDING_FACTOR = 16

class ResourceMixin(models.AbstractModel):
    _inherit = "resource.mixin"

    def get_work_days_data(self, from_datetime, to_datetime, compute_leaves=True, calendar=None, domain=None):
        """
            By default the resource calendar is used, but it can be
            changed using the `calendar` argument.

            `domain` is used in order to recognise the leaves to take,
            None means default value ('time_type', '=', 'leave')

            Returns a dict {'days': n, 'hours': h} containing the
            quantity of working time expressed as days and as hours.
        """
        roster_id = self.env['hr.attendance.roster'].search([('employee_id', '=', self.id), ('date', '=', from_datetime.date())], limit=1)
        # print("---------3----roster_id", roster_id)
        if roster_id and roster_id.shift_id:
            calendar = roster_id.shift_id
        else:
            calendar = calendar or self.resource_calendar_id
        resource = self.resource_id

        # naive datetimes are made explicit in UTC
        if not from_datetime.tzinfo:
            from_datetime = from_datetime.replace(tzinfo=utc)
        if not to_datetime.tzinfo:
            to_datetime = to_datetime.replace(tzinfo=utc)

        # total hours per day: retrieve attendances with one extra day margin,
        # in order to compute the total hours on the first and last days
        from_full = from_datetime - timedelta(days=1)
        to_full = to_datetime + timedelta(days=1)
        intervals = calendar._attendance_intervals(from_full, to_full, resource)
        day_total = defaultdict(float)
        for start, stop, meta in intervals:
            day_total[start.date()] += (stop - start).total_seconds() / 3600

        # actual hours per day
        if compute_leaves:
            intervals = calendar._work_intervals(from_datetime, to_datetime, resource, domain)
        else:
            intervals = calendar._attendance_intervals(from_datetime, to_datetime, resource)
        day_hours = defaultdict(float)
        for start, stop, meta in intervals:
            day_hours[start.date()] += (stop - start).total_seconds() / 3600

        # compute number of days as quarters
        days = sum(
            float_utils.round(ROUNDING_FACTOR * day_hours[day] / day_total[day]) / ROUNDING_FACTOR
            for day in day_hours
        )
        return {
            'days': days,
            'hours': sum(day_hours.values()),
        }
