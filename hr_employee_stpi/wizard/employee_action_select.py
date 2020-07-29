from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date, timedelta
import requests
import json

class EmployeeActionSelection(models.TransientModel):
    _name = 'employee.action.selection'
    _description = 'Wizard of Employee Selection'


    def show_my_profile(self):
        if self:
            my_ids = []
            check_leave = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)], limit=1)
            for emp in check_leave:
                my_ids.append(emp.id)
            print('==================my_ids========================', my_ids)
            return {
                'name': 'My Profile',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'hr.employee',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': [('id', 'in', my_ids)],
                }


    def show_subordinates_profile(self):
        if self:
            my_ids = []
            employee = self.env['hr.employee'].sudo().search([])
            for emp in employee:
                if emp.parent_id.user_id.id == self.env.user.id or emp.parent_id.parent_id.user_id.id == self.env.user.id or emp.parent_id.parent_id.parent_id.user_id.id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.user_id.id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.user_id.id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.user_id.id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.user_id.id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.user_id.id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.user_id.id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.user_id.id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.user_id.id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.user_id.id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.user_id.id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.user_id.id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.user_id.id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.user_id.id == self.env.user.id:
                    my_ids.append(emp.id)
            print('==================my_ids========================', my_ids)
            return {
                'name': 'Subordinates Profile',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'hr.employee',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': [('id', 'in', my_ids)],
                }


    def employee_directory_branch(self):
        if self:
            my_ids = []
            my_employee_id = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)], limit=1)
            employee = self.env['hr.employee'].sudo().search([('branch_id', '=', my_employee_id.branch_id.id)])
            for emp in employee:
                my_ids.append(emp.id)
            print('==================my_ids========================', my_ids)
            return {
                'name': 'Employees Directory(Branch)',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'hr.employee',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': [('id', 'in', my_ids)],
                }


    def employee_directory_all(self):
        if self:
            my_ids = []
            employee = self.env['hr.employee'].sudo().search([])
            for emp in employee:
                my_ids.append(emp.id)
            print('==================my_ids========================', my_ids)
            return {
                'name': 'Employees Directory',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'hr.employee',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': [('id', 'in', my_ids)],
                }


