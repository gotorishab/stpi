from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date, timedelta
import requests
import json

class IncomingfileWizard(models.TransientModel):
    _name = 'file.incoming'
    _description = 'Wizard of Incoming Files'

    file_id = fields.Many2one('folder.master', string='file')

    def show_incoming_file(self):
        if self:
            my_id = []
            files = self.env['folder.master'].search([])
            srch_id = self.env.user.id
            for file in files:
                if srch_id in file.sec_owner.ids:
                    my_id.append(file.id)
            return {
                'name': 'Incoming Files',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'folder.master',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'create': False,
                # 'view_id': self.env.ref('hr_applicant.view_employee_relative_tree').id,
                'domain': ['|', ('id', 'in', my_id), ('current_owner_id', '=', self.env.user.id)],
                }



    def show_incoming_sec_file(self):
        if self:
            my_emp_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            my_job_id = my_emp_id.job_id.status_level
            emp = self.env['hr.employee'].search([('job_id.status_level', '>=', my_job_id)])
            my_id = []
            # files = self.env['folder.master'].search([])
            # srch_id = self.env.user.id
            # for file in files:
            #     if srch_id in file.sec_owner.ids:
            #         my_id.append(file.id)
            return {
                'name': 'Incoming Files',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'folder.master',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'create': False,
                # 'view_id': self.env.ref('hr_applicant.view_employee_relative_tree').id,
                'domain': [('current_owner_id', 'in', emp.ids)],
                }


