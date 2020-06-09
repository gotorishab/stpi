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
    _name = 'file.tracker.wizard'
    _description = 'PF Ledger'
    


    @api.onchange('date_range')
    def get_dates(self):
        for rec in self:
            rec.from_date = rec.date_range.date_start
            rec.to_date = rec.date_range.date_end

    @api.onchange('employee_id')
    def get_branch_job(self):
        for rec in self:
            rec.branch_id = rec.employee_id.branch_id
            rec.job_id = rec.employee_id.job_id

    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    
    report_of = fields.Selection([('File','File'),
                                  ('Correspondence','Correspondence'),
                                  ('Both','Both'),
                                  ],string="Report On", default='both')
    search_through = fields.Selection([('Employee','Employee'),
                                  ('Branch','Branch'),
                                  ('Job','Job'),
                                  ('Department','Department'),
                                  ('All','All'),
                                  ],string="Search Via", default='Employee')

    details = fields.Char('Number/Name')
    employee_id = fields.Many2one('hr.employee','Requested By', default=_default_employee)
    date_range = fields.Many2one('date.range', string='Date Range')
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    branch_id = fields.Many2one('res.branch', string='Branch')
    job_id = fields.Many2one('hr.job', string='Functional Designation')
    department_id = fields.Many2one('hr.department', string='Department')


    @api.multi
    def confirm_report(self):
        for rec in self:
            if rec.search_through == 'Employee':
                if rec.report_of == 'Both':
                    my_ids = self.env['file.tracker.report'].search(['|', ('forwarded_by', '=', rec.employee_id.name), ('forwarded_to_user', '=', rec.employee_id.name), ('forwarded_date', '>=', rec.date_range.date_start), ('forwarded_date', '<=', rec.date_range.date_end)])
                    return {
                        'name': 'File Tracking Report',
                        'view_type': 'form',
                        'view_mode': 'tree',
                        'res_model': 'file.tracker.report',
                        'type': 'ir.actions.act_window',
                        'target': 'current',
                        'domain': [('id', 'in', my_ids.ids)],
                    }
                else:
                    my_search_id = []
                    my_ids = self.env['file.tracker.report'].search(['|', ('forwarded_by', '=', rec.employee_id.name), ('forwarded_to_user', '=', rec.employee_id.name), ('forwarded_date', '>=', rec.date_range.date_start), ('forwarded_date', '<=', rec.date_range.date_end)])
                    for my_id in my_ids:
                        if my_id.name == rec.details or my_id.number == rec.details:
                            if my_id.type == rec.report_of:
                                my_search_id.append(my_id.id)
                    return {
                        'name': 'File Tracking Report',
                        'view_type': 'form',
                        'view_mode': 'tree',
                        'res_model': 'file.tracker.report',
                        'type': 'ir.actions.act_window',
                        'target': 'current',
                        'domain': [('id', 'in', my_search_id)]
                    }
            elif rec.search_through == 'Branch':
                if rec.report_of == 'Both':
                    my_ids = self.env['file.tracker.report'].search(['|', ('forwarded_by_branch', '=', rec.branch_id.name), ('forwarded_to_branch', '=', rec.branch_id.name), ('forwarded_date', '>=', rec.date_range.date_start), ('forwarded_date', '<=', rec.date_range.date_end)])
                    return {
                        'name': 'File Tracking Report',
                        'view_type': 'form',
                        'view_mode': 'tree',
                        'res_model': 'file.tracker.report',
                        'type': 'ir.actions.act_window',
                        'target': 'current',
                        'domain': [('id', 'in', my_ids.ids)],
                    }
                else:
                    my_search_id = []
                    my_ids = self.env['file.tracker.report'].search(['|', ('forwarded_by_branch', '=', rec.branch_id.name), ('forwarded_to_branch', '=', rec.branch_id.name), ('forwarded_date', '>=', rec.date_range.date_start), ('forwarded_date', '<=', rec.date_range.date_end)])
                    for my_id in my_ids:
                        if my_id.name == rec.details or my_id.number == rec.details:
                            if my_id.type == rec.report_of:
                                my_search_id.append(my_id.id)
                    return {
                        'name': 'File Tracking Report',
                        'view_type': 'form',
                        'view_mode': 'tree',
                        'res_model': 'file.tracker.report',
                        'type': 'ir.actions.act_window',
                        'target': 'current',
                        'domain': [('id', 'in', my_search_id)]
                    }
            elif rec.search_through == 'Job':
                if rec.report_of == 'Both':
                    my_ids = self.env['file.tracker.report'].search(['|', ('forwarded_by_jobpos', '=', rec.job_id.name), ('job_pos', '=', rec.job_id.name), ('forwarded_date', '>=', rec.date_range.date_start), ('forwarded_date', '<=', rec.date_range.date_end)])
                    return {
                        'name': 'File Tracking Report',
                        'view_type': 'form',
                        'view_mode': 'tree',
                        'res_model': 'file.tracker.report',
                        'type': 'ir.actions.act_window',
                        'target': 'current',
                        'domain': [('id', 'in', my_ids.ids)],
                    }
                else:
                    my_search_id = []
                    my_ids = self.env['file.tracker.report'].search(['|', ('forwarded_by_jobpos', '=', rec.job_id.name), ('job_pos', '=', rec.job_id.name), ('forwarded_date', '>=', rec.date_range.date_start), ('forwarded_date', '<=', rec.date_range.date_end)])
                    for my_id in my_ids:
                        if my_id.name == rec.details or my_id.number == rec.details:
                            if my_id.type == rec.report_of:
                                my_search_id.append(my_id.id)
                    return {
                        'name': 'File Tracking Report',
                        'view_type': 'form',
                        'view_mode': 'tree',
                        'res_model': 'file.tracker.report',
                        'type': 'ir.actions.act_window',
                        'target': 'current',
                        'domain': [('id', 'in', my_search_id)]
                    }
            elif rec.search_through == 'Department':
                if rec.report_of == 'Both':
                    my_ids = self.env['file.tracker.report'].search(['|', ('forwarded_by_dept', '=', rec.department_id.name), ('forwarded_to_dept', '=', rec.department_id.name), ('forwarded_date', '>=', rec.date_range.date_start), ('forwarded_date', '<=', rec.date_range.date_end)])
                    return {
                        'name': 'File Tracking Report',
                        'view_type': 'form',
                        'view_mode': 'tree',
                        'res_model': 'file.tracker.report',
                        'type': 'ir.actions.act_window',
                        'target': 'current',
                        'domain': [('id', 'in', my_ids.ids)],
                    }
                else:
                    my_search_id = []
                    my_ids = self.env['file.tracker.report'].search(['|', ('forwarded_by_dept', '=', rec.department_id.name), ('forwarded_to_dept', '=', rec.department_id.name), ('forwarded_date', '>=', rec.date_range.date_start), ('forwarded_date', '<=', rec.date_range.date_end)])
                    for my_id in my_ids:
                        if my_id.name == rec.details or my_id.number == rec.details:
                            if my_id.type == rec.report_of:
                                my_search_id.append(my_id.id)
                    return {
                        'name': 'File Tracking Report',
                        'view_type': 'form',
                        'view_mode': 'tree',
                        'res_model': 'file.tracker.report',
                        'type': 'ir.actions.act_window',
                        'target': 'current',
                        'domain': [('id', 'in', my_search_id)]
                    }
            elif rec.search_through == 'All':
                if rec.report_of == 'Both':
                    my_ids = self.env['file.tracker.report'].search([('forwarded_date', '>=', rec.date_range.date_start), ('forwarded_date', '<=', rec.date_range.date_end)])
                    return {
                        'name': 'File Tracking Report',
                        'view_type': 'form',
                        'view_mode': 'tree',
                        'res_model': 'file.tracker.report',
                        'type': 'ir.actions.act_window',
                        'target': 'current',
                        'domain': [('id', 'in', my_ids.ids)],
                    }
                else:
                    my_search_id = []
                    my_ids = self.env['file.tracker.report'].search([('forwarded_date', '>=', rec.date_range.date_start), ('forwarded_date', '<=', rec.date_range.date_end)])
                    for my_id in my_ids:
                        if my_id.name == rec.details or my_id.number == rec.details:
                            if my_id.type == rec.report_of:
                                my_search_id.append(my_id.id)
                    return {
                        'name': 'File Tracking Report',
                        'view_type': 'form',
                        'view_mode': 'tree',
                        'res_model': 'file.tracker.report',
                        'type': 'ir.actions.act_window',
                        'target': 'current',
                        'domain': [('id', 'in', my_search_id)]
                    }
            else:
                if rec.report_of == 'Both':
                    my_ids = self.env['file.tracker.report'].search([('forwarded_date', '>=', rec.date_range.date_start), ('forwarded_date', '<=', rec.date_range.date_end)])
                    return {
                        'name': 'File Tracking Report',
                        'view_type': 'form',
                        'view_mode': 'tree',
                        'res_model': 'file.tracker.report',
                        'type': 'ir.actions.act_window',
                        'target': 'current',
                        'domain': [('id', 'in', my_ids.ids)],
                    }
                else:
                    my_search_id = []
                    my_ids = self.env['file.tracker.report'].search([('forwarded_date', '>=', rec.date_range.date_start), ('forwarded_date', '<=', rec.date_range.date_end)])
                    for my_id in my_ids:
                        if my_id.name == rec.details or my_id.number == rec.details:
                            if my_id.type == rec.report_of:
                                my_search_id.append(my_id.id)
                    return {
                        'name': 'File Tracking Report',
                        'view_type': 'form',
                        'view_mode': 'tree',
                        'res_model': 'file.tracker.report',
                        'type': 'ir.actions.act_window',
                        'target': 'current',
                        'domain': [('id', 'in', my_search_id)]
                    }
