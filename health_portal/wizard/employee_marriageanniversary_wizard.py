from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date, timedelta
import requests
import json
import datetime
from dateutil.relativedelta import relativedelta

class marriage_anniversaryChequeRequest(models.TransientModel):
    _name = 'employee.marriageanniversary.wizard'
    _description = 'Wizard of marriage Anniversary Selection'


    def button_current_month(self):
        if self:
            my_ids = []
            employee = self.env['hr.employee'].sudo().search([])
            for emp in employee:
                if emp.marriage_anniversary:
                    if emp.marriage_anniversary.strftime("%m") == datetime.datetime.now().strftime("%m"):
                        employee_birth = self.env['vardhman.employee.marriageanniversary'].create({
                            'name': emp.name,
                            'image': emp.image_1920,
                            'job_title': emp.job_title,
                            'marriage_anniversary': emp.marriage_anniversary,
                        })
                        my_ids.append(employee_birth.id)
            print('==================my_ids========================', my_ids)
            return {
                'domain': [('id', 'in', my_ids)],
                'name': 'Employees - Current Month marriage_anniversary',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'vardhman.employee.marriageanniversary',
                'view_id': False,
                'views': [(self.env.ref('intranet_home.view_vardhman_marriageanniversary_kanban').id, 'kanban'),
                          (self.env.ref('intranet_home.view_vardhman_marriageanniversary_list').id, 'tree'),
                          (self.env.ref('intranet_home.view_vardhman_marriageanniversary_form').id, 'form')],
                'type': 'ir.actions.act_window'
            }


    def button_previous_month(self):
        if self:
            my_ids = []
            employee = self.env['hr.employee'].sudo().search([])
            for emp in employee:
                if emp.marriage_anniversary:
                    if (datetime.datetime.now().replace(day=15) - relativedelta(months=1)).strftime("%m") == emp.marriage_anniversary.strftime("%m"):
                        employee_birth = self.env['vardhman.employee.marriageanniversary'].create({
                            'name': emp.name,
                            'image': emp.image_1920,
                            'job_title': emp.job_title,
                            'marriage_anniversary': emp.marriage_anniversary,
                        })
                        my_ids.append(employee_birth.id)
            print('==================my_ids========================', my_ids)
            return {
                'domain': [('id', 'in', my_ids)],
                'name': 'Employees - Previous Month marriage_anniversary',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'vardhman.employee.marriageanniversary',
                'view_id': False,
                'views': [(self.env.ref('intranet_home.view_vardhman_marriageanniversary_kanban').id, 'kanban'),
                          (self.env.ref('intranet_home.view_vardhman_marriageanniversary_list').id, 'tree'),
                          (self.env.ref('intranet_home.view_vardhman_marriageanniversary_form').id, 'form')],
                'type': 'ir.actions.act_window'
            }



    def button_next_month(self):
        if self:
            my_ids = []
            employee = self.env['hr.employee'].sudo().search([])
            for emp in employee:
                if emp.marriage_anniversary:
                    if (datetime.datetime.now().replace(day=15)+ relativedelta(months=1)).strftime("%m") == emp.marriage_anniversary.strftime("%m"):
                        employee_birth = self.env['vardhman.employee.marriageanniversary'].create({
                            'name': emp.name,
                            'image': emp.image_1920,
                            'job_title': emp.job_title,
                            'marriage_anniversary': emp.marriage_anniversary,
                        })
                        my_ids.append(employee_birth.id)
            print('==================my_ids========================', my_ids)
            return {
                'domain': [('id', 'in', my_ids)],
                'name': 'Employees - Next Month marriage_anniversary',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'vardhman.employee.marriageanniversary',
                'view_id': False,
                'views': [(self.env.ref('intranet_home.view_vardhman_marriageanniversary_kanban').id, 'kanban'),
                          (self.env.ref('intranet_home.view_vardhman_marriageanniversary_list').id, 'tree'),
                          (self.env.ref('intranet_home.view_vardhman_marriageanniversary_form').id, 'form')],
                'type': 'ir.actions.act_window'
            }


    def button_all_month(self):
        if self:
            my_ids = []
            employee = self.env['hr.employee'].sudo().search([])
            for emp in employee:
                if emp.marriage_anniversary:
                    employee_birth = self.env['vardhman.employee.marriageanniversary'].create({
                        'name': emp.name,
                        'image': emp.image_1920,
                        'job_title': emp.job_title,
                        'marriage_anniversary': emp.marriage_anniversary,
                    })
                    my_ids.append(employee_birth.id)
            print('==================my_ids========================', my_ids)
            return {
                'domain': [('id', 'in', my_ids)],
                'name': 'Employees - Next Month marriage_anniversary',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'vardhman.employee.marriageanniversary',
                'view_id': False,
                'views': [(self.env.ref('intranet_home.view_vardhman_marriageanniversary_kanban').id, 'kanban'),
                          (self.env.ref('intranet_home.view_vardhman_marriageanniversary_list').id, 'tree'),
                          (self.env.ref('intranet_home.view_vardhman_marriageanniversary_form').id, 'form')],
                'type': 'ir.actions.act_window'
            }
