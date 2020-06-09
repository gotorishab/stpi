# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, date, timedelta


class PullInto(models.TransientModel):
    _name = "pull.into.custom"
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
    def pull_intos_action_button(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        previous_owner = []
        current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        for file in self.env['muk_dms.file'].browse(active_ids):
            self.env['file.tracker.report'].create({
                'name': str(file.name),
                'number': str(file.letter_number),
                'type': 'Correspondence',
                'forwarded_by': str(current_employee.user_id.name),
                'forwarded_by_dept': str(current_employee.department_id.name),
                'forwarded_by_jobpos': str(current_employee.job_id.name),
                'forwarded_by_branch': str(current_employee.branch_id.name),
                'forwarded_date': datetime.now().date(),
                'forwarded_to_user': str(self.user.name),
                'forwarded_to_dept': str(self.department.name),
                'job_pos': str(self.jobposition.name),
                'forwarded_to_branch': str(self.user.branch_id.name),
                'remarks': self.remarks,
                'details': 'Correspondence Forwarded'
            })
            file.last_owner_id = file.current_owner_id.id
            file.current_owner_id = self.env.user.id
            file.responsible_user_id = self.env.user.id
            file.sec_owner = []
            previous_owner.append(self.env.user.id)
            previous_owner.append(file.last_owner_id.id)
            file.previous_owner = [(6,0,previous_owner)]





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