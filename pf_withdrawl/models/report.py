from odoo import fields,api,models
import math
from datetime import datetime, timedelta, date
from pytz import timezone, UTC
from dateutil.relativedelta import relativedelta


class LateComingReport(models.Model):
    _name="pf.ledger.report"
    _description="PF Ledger Report"


    employee_id = fields.Many2one('hr.employee',string="Employee")
    branch_id = fields.Many2one('res.branch',string="Branch", store=True)
    # holiday_id = fields.Many2one('resource.calendar',string="Holiday Calendar")
    # name = fields.Char(string="Holiday")
    # date = fields.Date(string="Date")
    ledger_for_year = fields.Many2one('date.range', string='Ledger for the year')
    month = fields.Char(string='Month (Basic+DA)')
    epmloyee_contribution = fields.Char('Employee (A)')
    voluntary_contribution = fields.Char('Voluntary (B)')
    employer_contribution = fields.Char('Employer (C)')
    interest_employee_voluntary = fields.Char('Interest (A+B)')
    interest_employer = fields.Char('Interest (C)')
    total = fields.Char('Total')
    # is_current_month = fields.Boolean(compute="_check_current_month", store=True)
    # is_not_sat_sun = fields.Boolean(compute="_check_sat_sun", store=True)
    #
    #
    # @api.depends('date')
    # def _check_current_month(self):
    #     for rec in self:
    #         first_day = date.today().replace(day=1)
    #         last_day = date.today().replace(day=1) + relativedelta(months=1) - relativedelta(days=1)
    #         if rec.date:
    #             if first_day <= rec.date <= last_day:
    #                 rec.is_current_month = True
    #             else:
    #                 rec.is_current_month = False
    #
    # @api.depends('month')
    # def _check_sat_sun(self):
    #     for rec in self:
    #         if rec.name == 'Sunday' or rec.name == 'Saturday':
    #             rec.is_not_sat_sun = True
    #         else:
    #             rec.is_not_sat_sun = False