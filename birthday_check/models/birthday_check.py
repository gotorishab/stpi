from odoo import api, fields, models, tools, _
import calendar
import datetime
from dateutil.relativedelta import relativedelta

class BirthdayCheck(models.Model):
    _inherit = "hr.employee"
    _description = "Birthday Cheque"

    is_previous_month = fields.Boolean(compute="_check_previous_month", store=True)
    is_current_month = fields.Boolean(compute="_check_current_month", store=True)
    is_next_month = fields.Boolean(compute="_check_next_month", store=True)


    @api.depends('birthday')
    def _check_previous_month(self):
        for rec in self:
            first_day = datetime.date.today().replace(day=1) - relativedelta(months=1)
            last_day = datetime.date.today().replace(day=1) - relativedelta(days=1)
            if rec.birthday:
                if first_day <= rec.birthday <= last_day:
                    rec.is_previous_month = True
                else:
                    rec.is_previous_month = False

    @api.depends('birthday')
    def _check_current_month(self):
        for rec in self:
            first_day = datetime.date.today().replace(day=1)
            last_day = datetime.date.today().replace(day=1)+ relativedelta(months=1) - relativedelta(days=1)
            if rec.birthday:
                if first_day <= rec.birthday <= last_day:
                    rec.is_current_month = True
                else:
                    rec.is_current_month = False


    @api.depends('birthday')
    def _check_next_month(self):
        for rec in self:
            first_day = datetime.date.today().replace(day=1)+ relativedelta(months=1)
            last_day = datetime.date.today().replace(day=1)+ relativedelta(months=2) - relativedelta(days=1)
            if rec.birthday:
                if first_day <= rec.birthday <= last_day:
                    rec.is_next_month = True
                else:
                    rec.is_next_month = False


