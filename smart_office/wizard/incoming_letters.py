from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date, timedelta
import requests
import json

class IncomingLetterWizard(models.TransientModel):
    _name = 'letter.incoming'
    _description = 'Wizard of Incoming Files'

    letter_id = fields.Many2one('muk_dms.file', string='Letter')

    def show_incoming_letter(self):
        if self:
            my_id = []
            files = self.env['muk_dms.file'].search([])
            srch_id = self.env.user.id
            for file in files:
                if srch_id in file.sec_owner.ids or srch_id == file.current_owner_id.id:
                    my_id.append(file.id)

            return {
                'name': 'Incoming Files',
                'view_type': 'form',
                'view_mode': 'kanban,tree,graph,pivot,form',
                'res_model': 'muk_dms.file',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': [('id', 'in', my_id)],
                }



    def show_incoming_sec_letter(self):
        if self:
            # emp = self.env['hr.employee'].search(['|', ('parent_id', '=', self.env.user.id), ('parent_id.parent_id', '=', self.env.user.id)])
            # my_emp_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            # my_job_id = my_emp_id.job_id.status_level
            # emp = self.env['hr.employee'].search([('job_id.status_level', '>=', my_job_id)])
            my_ids = []
            employee = self.env['hr.employee'].search([])
            for emp in employee:
                if emp.parent_id == self.env.user.id or emp.parent_id.parent_id == self.env.user.id or emp.parent_id.parent_id.parent_id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id == self.env.user.id or emp.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id == self.env.user.id:
                    my_ids.append(emp.id)
            return {
                'name': 'Incoming Files',
                'view_type': 'form',
                'view_mode': 'kanban,tree,graph,pivot,form',
                'res_model': 'muk_dms.file',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'create': False,
                # 'view_id': self.env.ref('hr_applicant.view_employee_relative_tree').id,
                'domain': [('current_owner_id.id', 'in', my_ids)],
                }


