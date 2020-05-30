from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import time, datetime,timedelta
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date, datetime
import datetime
from odoo.tools import float_utils
from collections import defaultdict
from pytz import utc


class WizardLateComing(models.TransientModel):
    _name = 'pf.ledger.wizard'
    _description = 'PF Ledger'
    

    # def _default_employee(self):
    #     return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    def _default_from_date(self):
        epoch_year = date.today().year
        year_start = date(epoch_year, 4, 1)
        return year_start

    def _default_to_date(self):
        epoch_year = date.today().year
        year_end = date(epoch_year, 3, 31)
        return year_end

    @api.onchange('ledger_for_year')
    def get_dates(self):
        for rec in self:
            rec.from_date = rec.ledger_for_year.date_start
            rec.to_date = rec.ledger_for_year.date_end

    @api.onchange('employee_id')
    def get_branch_job(self):
        for rec in self:
            rec.branch_id = rec.employee_id.branch_id
            rec.job_id = rec.employee_id.job_id

    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    
    report_of = fields.Selection([('pf_ledger','PF Ledger'),
                                  ],string="Report On", default='pf_ledger')
    employee_id = fields.Many2one('hr.employee','Requested By', default=_default_employee)
    ledger_for_year = fields.Many2one('date.range', string='Ledger for the year')
    from_date = fields.Date(string='From Date', default=_default_from_date)
    to_date = fields.Date(string='To Date', default=_default_to_date)
    branch_id = fields.Many2one('res.branch', string='Branch')
    job_id = fields.Many2one('hr.job', string='Functional Designation')


    @api.multi
    def confirm_report(self):
        for rec in self:
            dr = self.env['pf.ledger.report'].search([('employee_id', '=', rec.employee_id.id),('ledger_for_year', 'in', rec.ledger_for_year.id)])
            for lines in dr:
                lines.unlink()
            from_date = rec.from_date
            while from_date < rec.to_date:
                if str(from_date.month) == '1':
                    month = 'January'
                elif str(from_date.month) == '2':
                    month = 'February'
                elif str(from_date.month) == '3':
                    month = 'March'
                elif str(from_date.month) == '4':
                    month = 'April'
                elif str(from_date.month) == '5':
                    month = 'May'
                elif str(from_date.month) == '6':
                    month = 'June'
                elif str(from_date.month) == '7':
                    month = 'July'
                elif str(from_date.month) == '8':
                    month = 'August'
                elif str(from_date.month) == '9':
                    month = 'September'
                elif str(from_date.month) == '10':
                    month = 'October'
                elif str(from_date.month) == '11':
                    month = 'November'
                elif str(from_date.month) == '12':
                    month = 'December'
                else:
                    month = ''
                self.env['pf.ledger.report'].create({
                    'employee_id': rec.employee_id.id,
                    'ledger_for_year': rec.ledger_for_year.id,
                    'branch_id': rec.branch_id.id,
                    'month': month,
                })
                from_date += from_date + relativedelta(months=1)
            return {
                'name': 'PF Ledger',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'pf.ledger.report',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': [('employee_id', '=', rec.employee_id.id),('ledger_for_year', 'in', rec.ledger_for_year.id)]
            }


    #
    # @api.multi
    # def confirm_report(self):
    #     for rec in self:
    #         dr = self.env['pf.ledger.report'].search([('branch_id', 'in', rec.branch_ids.ids)])
    #         for lines in dr:
    #             lines.unlink()
    #         dr_b = self.env['resource.calendar.leaves'].search([('calendar_id.branch_id', 'in', rec.branch_ids.ids)])
    #         for emp in dr_b:
    #             print('========================================================',emp.date)
    #         # for emp in rec.employee_id.resource_calendar_id.global_leave_ids:
    #             if rec.from_date and rec.to_date and rec.from_date <= emp.date <= rec.to_date:
    #                 month = ''
    #                 if str(emp.date.month) == '1':
    #                     month = 'January'
    #                 elif str(emp.date.month) == '2':
    #                     month = 'February'
    #                 elif str(emp.date.month) == '3':
    #                     month = 'March'
    #                 elif str(emp.date.month) == '4':
    #                     month = 'April'
    #                 elif str(emp.date.month) == '5':
    #                     month = 'May'
    #                 elif str(emp.date.month) == '6':
    #                     month = 'June'
    #                 elif str(emp.date.month) == '7':
    #                     month = 'July'
    #                 elif str(emp.date.month) == '8':
    #                     month = 'August'
    #                 elif str(emp.date.month) == '9':
    #                     month = 'September'
    #                 elif str(emp.date.month) == '10':
    #                     month = 'October'
    #                 elif str(emp.date.month) == '11':
    #                     month = 'November'
    #                 elif str(emp.date.month) == '12':
    #                     month = 'December'
    #                 else:
    #                     month = ''
    #                 cr = self.env['pf.ledger.report'].create({
    #                     'name': emp.name,
    #                     'date': emp.date,
    #                     'branch_id': emp.calendar_id.branch_id.id,
    #                     'holiday_id': emp.calendar_id.id,
    #                     'month': month,
    #                 })
    #
    #     return {
    #         'name': 'Leave Holiday Report',
    #         'view_type': 'form',
    #         'view_mode': 'tree',
    #         'res_model': 'pf.ledger.report',
    #         'type': 'ir.actions.act_window',
    #         'target': 'current',
    #         'domain': [('branch_id', '=', self.branch_ids.ids)],
    #         'context': {
    #                         'name': 'Sunday',
    #                     }
    #         }
    #

    #
    # @api.multi
    # def confirm_existing_report(self):
    #     for rec in self:
    #         dr = self.env['pf.ledger.report'].search([('branch_id', 'in', rec.branch_ids.ids)])
    #         for lines in dr:
    #             lines.unlink()
    #         emp_ids = self.env['hr.employee'].search([('branch_id', 'in', rec.branch_ids.ids)])
    #         for employees in emp_ids:
    #             for emp in employees.resource_calendar_id.global_leave_ids:
    #                 if rec.from_date <= emp.date <= rec.to_date:
    #                     month = ''
    #                     if str(emp.date.month) == '1':
    #                         month = 'January'
    #                     elif str(emp.date.month) == '2':
    #                         month = 'February'
    #                     elif str(emp.date.month) == '3':
    #                         month = 'March'
    #                     elif str(emp.date.month) == '4':
    #                         month = 'April'
    #                     elif str(emp.date.month) == '5':
    #                         month = 'May'
    #                     elif str(emp.date.month) == '6':
    #                         month = 'June'
    #                     elif str(emp.date.month) == '7':
    #                         month = 'July'
    #                     elif str(emp.date.month) == '8':
    #                         month = 'August'
    #                     elif str(emp.date.month) == '9':
    #                         month = 'September'
    #                     elif str(emp.date.month) == '10':
    #                         month = 'October'
    #                     elif str(emp.date.month) == '11':
    #                         month = 'November'
    #                     elif str(emp.date.month) == '12':
    #                         month = 'December'
    #                     else:
    #                         month = ''
    #                     cr = self.env['pf.ledger.report'].create({
    #                         'employee_id': rec.employee_id.id,
    #                         'name': emp.name,
    #                         'date': emp.date,
    #                         'branch_id': emp.calendar_id.branch_id.id,
    #                         'holiday_id': emp.calendar_id.id,
    #                         'month': month,
    #                     })
    #
    #     return {
    #         'name': 'Leave Holiday Report',
    #         'view_type': 'form',
    #         'view_mode': 'tree',
    #         'res_model': 'pf.ledger.report',
    #         'type': 'ir.actions.act_window',
    #         'target': 'current',
    #         'domain': [('branch_id', 'in', self.branch_ids.ids)],
    #     }
