from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date, timedelta
import requests
import json
import datetime
from dateutil.relativedelta import relativedelta

class BirthdayChequeRequest(models.TransientModel):
    _name = 'marking.report.wizard'
    _description = 'Wizard of Marking Report'


    def button_current_month(self):
        if self:
            my_ids = []
            employee = self.env['hr.employee'].sudo().search([])
            for emp in employee:
                if emp.birthday:
                    if emp.birthday.strftime("%m") == datetime.datetime.now().strftime("%m"):
                        employee_birth = self.env['vardhman.employee.birthday'].create({
                            'name': emp.name,
                            'image': emp.image_1920,
                            'job_title': emp.job_title,
                            'birthday': emp.birthday,
                        })
                        my_ids.append(employee_birth.id)
            print('==================my_ids========================', my_ids)
            return {
                'domain': [('id', 'in', my_ids)],
                'name': 'Employees - Current Month Birthday',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'vardhman.employee.birthday',
                'view_id': False,
                'views': [(self.env.ref('intranet_home.view_vardhman_birthday_kanban').id, 'kanban'),
                          (self.env.ref('intranet_home.view_vardhman_birthday_list').id, 'tree'),
                          (self.env.ref('intranet_home.view_vardhman_birthday_form').id, 'form')],
                'type': 'ir.actions.act_window'
            }
