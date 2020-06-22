# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, date, timedelta


class PullInto(models.TransientModel):
    _name = "pull.into.file.custom"
    _description = "HR Employee Cheque Action"



    department = fields.Many2one('hr.department', string = "Department")
    jobposition = fields.Many2one('hr.job', string = "Job position")
    employee = fields.Many2one('hr.employee', string='Employee')
    user = fields.Many2one('res.users', related = 'employee.user_id', string='User')
    remarks = fields.Text('Remarks')



    @api.onchange('department','jobposition')
    def _onchange_user(self):
        for rec in self:
            if rec.department.id and not rec.jobposition.id:
                return {'domain': {'employee': [('department_id', '=', rec.department.id)]}}
            elif rec.jobposition.id and not rec.department.id:
                return {'domain': {'employee': [('job_id', '=', rec.jobposition.id)]}}
            elif rec.jobposition.id and rec.department.id:
                return {'domain': {'employee': [('job_id', '=', rec.jobposition.id),('department_id', '=', rec.department.id)]}}
            else:
                return {'domain': {'employee': ['|', ('job_id', '=', rec.jobposition.id),('department_id', '=', rec.department.id)]}}



    @api.multi
    def pull_into_files_action_button(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        previous_owner = []
        current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        for file in self.env['folder.master'].browse(active_ids):
            current_file_employee = self.env['hr.employee'].search([('user_id', '=', file.current_owner_id.id)], limit=1)
            self.env['file.tracker.report'].create({
                'name': str(file.folder_name),
                'number': str(file.number),
                'type': 'File',
                'pulled_by': str(current_file_employee.user_id.name),
                'pulled_by_dept': str(current_file_employee.department_id.name),
                'pulled_by_jobpos': str(current_file_employee.job_id.name),
                'pulled_by_branch': str(current_file_employee.branch_id.name),
                'pulled_date': datetime.now().date(),
                'pulled_to_user': str(self.user.name),
                'pulled_to_dept': str(self.department.name),
                'pulled_to_job_pos': str(self.jobposition.name),
                'pulled_to_branch': str(self.user.branch_id.name),
                'action_taken': 'file_pulled',
                'remarks': self.remarks,
                'details': 'File pulled'
            })
            file.last_owner_id = file.current_owner_id.id
            file.current_owner_id = self.env.user.id
            file.responsible_user_id = self.env.user.id
            file.previous_owner = [(4,file.last_owner_id.id)]
            file.previous_owner = [(4,file.current_owner_id.id)]
            file.sec_owner = [(4,file.last_owner_id.id)]
            file.sec_owner = [(4,file.current_owner_id.id)]






    #     context = dict(self._context or {})
    #     active_ids = context.get('active_ids', []) or []
    #     for employee in self.env['cheque.requests'].browse(active_ids):
    #         if employee.state == 'to_approve':
    #             employee.sudo().button_approved()
    #
    #
    # @api.multi
    # def pull_intos_action_reject_button(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_ids', []) or []
    #     for employee in self.env['cheque.requests'].browse(active_ids):
    #         if employee.state == 'to_approve':
    #             employee.sudo().button_reject()