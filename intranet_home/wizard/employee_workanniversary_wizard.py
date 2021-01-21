from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date, timedelta
import requests
import json
import datetime
from dateutil.relativedelta import relativedelta

class work_anniversaryChequeRequest(models.TransientModel):
    _name = 'employee.workanniversary.wizard'
    _description = 'Wizard of Work Anniversary Selection'

    no_of_years = fields.Integer('Number of Years')

    def button_current_month(self):
        if self:
            my_ids = []
            employee = self.env['hr.employee'].sudo().search([])
            for emp in employee:
                if emp.work_anniversary:
                    if emp.work_anniversary.strftime("%m") == datetime.datetime.now().strftime("%m"):
                        employee_birth = self.env['vardhman.employee.workanniversary'].create({
                            'name': emp.name,
                            'image': emp.image_1920,
                            'job_title': emp.job_title,
                            'work_anniversary': emp.work_anniversary,
                        })
                        my_ids.append(employee_birth.id)
            print('==================my_ids========================', my_ids)
            return {
                'domain': [('id', 'in', my_ids)],
                'name': 'Employees - Current Month work_anniversary',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'vardhman.employee.workanniversary',
                'view_id': False,
                'views': [(self.env.ref('intranet_home.view_vardhman_workanniversary_kanban').id, 'kanban'),
                          (self.env.ref('intranet_home.view_vardhman_workanniversary_list').id, 'tree'),
                          (self.env.ref('intranet_home.view_vardhman_workanniversary_form').id, 'form')],
                'type': 'ir.actions.act_window'
            }


    def button_previous_month(self):
        if self:
            my_ids = []
            employee = self.env['hr.employee'].sudo().search([])
            for emp in employee:
                if emp.work_anniversary:
                    if (datetime.datetime.now().replace(day=15) - relativedelta(months=1)).strftime("%m") == emp.work_anniversary.strftime("%m"):
                        employee_birth = self.env['vardhman.employee.workanniversary'].create({
                            'name': emp.name,
                            'image': emp.image_1920,
                            'job_title': emp.job_title,
                            'work_anniversary': emp.work_anniversary,
                        })
                        my_ids.append(employee_birth.id)
            print('==================my_ids========================', my_ids)
            return {
                'domain': [('id', 'in', my_ids)],
                'name': 'Employees - Previous Month work_anniversary',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'vardhman.employee.workanniversary',
                'view_id': False,
                'views': [(self.env.ref('intranet_home.view_vardhman_workanniversary_kanban').id, 'kanban'),
                          (self.env.ref('intranet_home.view_vardhman_workanniversary_list').id, 'tree'),
                          (self.env.ref('intranet_home.view_vardhman_workanniversary_form').id, 'form')],
                'type': 'ir.actions.act_window'
            }



    def button_next_month(self):
        if self:
            my_ids = []
            employee = self.env['hr.employee'].sudo().search([])
            for emp in employee:
                if emp.work_anniversary:
                    if (datetime.datetime.now().replace(day=15)+ relativedelta(months=1)).strftime("%m") == emp.work_anniversary.strftime("%m"):
                        employee_birth = self.env['vardhman.employee.workanniversary'].create({
                            'name': emp.name,
                            'image': emp.image_1920,
                            'job_title': emp.job_title,
                            'work_anniversary': emp.work_anniversary,
                        })
                        my_ids.append(employee_birth.id)
            print('==================my_ids========================', my_ids)
            return {
                'domain': [('id', 'in', my_ids)],
                'name': 'Employees - Next Month work_anniversary',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'vardhman.employee.workanniversary',
                'view_id': False,
                'views': [(self.env.ref('intranet_home.view_vardhman_workanniversary_kanban').id, 'kanban'),
                          (self.env.ref('intranet_home.view_vardhman_workanniversary_list').id, 'tree'),
                          (self.env.ref('intranet_home.view_vardhman_workanniversary_form').id, 'form')],
                'type': 'ir.actions.act_window'
            }




    def button_custom_year(self):
        if self:
            my_ids = []
            employee = self.env['hr.employee'].sudo().search([])
            for emp in employee:
                if emp.work_anniversary:
                    if relativedelta(datetime.date.today(), emp.work_anniversary).years <= self.no_of_years:
                    # if (datetime.datetime.now().replace(day=15)+ relativedelta(months=1)).strftime("%m") == emp.work_anniversary.strftime("%m"):
                        employee_birth = self.env['vardhman.employee.workanniversary'].create({
                            'name': emp.name,
                            'image': emp.image_1920,
                            'job_title': emp.job_title,
                            'work_anniversary': emp.work_anniversary,
                        })
                        my_ids.append(employee_birth.id)
            print('==================my_ids========================', my_ids)
            return {
                'domain': [('id', 'in', my_ids)],
                'name': 'Employees - Next Month work_anniversary',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'vardhman.employee.workanniversary',
                'view_id': False,
                'views': [(self.env.ref('intranet_home.view_vardhman_workanniversary_kanban').id, 'kanban'),
                          (self.env.ref('intranet_home.view_vardhman_workanniversary_list').id, 'tree'),
                          (self.env.ref('intranet_home.view_vardhman_workanniversary_form').id, 'form')],
                'type': 'ir.actions.act_window'
            }


    def button_all_month(self):
        if self:
            my_ids = []
            employee = self.env['hr.employee'].sudo().search([])
            for emp in employee:
                if emp.work_anniversary:
                    employee_birth = self.env['vardhman.employee.workanniversary'].create({
                        'name': emp.name,
                        'image': emp.image_1920,
                        'job_title': emp.job_title,
                        'work_anniversary': emp.work_anniversary,
                    })
                    my_ids.append(employee_birth.id)
            print('==================my_ids========================', my_ids)
            return {
                'domain': [('id', 'in', my_ids)],
                'name': 'Employees - Next Month work_anniversary',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'vardhman.employee.workanniversary',
                'view_id': False,
                'views': [(self.env.ref('intranet_home.view_vardhman_workanniversary_kanban').id, 'kanban'),
                          (self.env.ref('intranet_home.view_vardhman_workanniversary_list').id, 'tree'),
                          (self.env.ref('intranet_home.view_vardhman_workanniversary_form').id, 'form')],
                'type': 'ir.actions.act_window'
            }
