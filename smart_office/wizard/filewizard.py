from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date, timedelta
import requests
import json

class FileWizard(models.Model):
    _name = 'file.wizard'
    _description = 'Wizard of File Wizard'
    _rec_name = 'user'



    department = fields.Many2one('hr.department', string = "Department")
    jobposition = fields.Many2one('hr.job', string = "Job position")
    employee = fields.Many2one('hr.employee', string='Employee')
    user = fields.Many2one('res.users', related = 'employee.user_id', string='User')

    remarks = fields.Text('Remarks')

    defid = fields.Many2one('muk_dms.file', invisible=1)
    sec_own_ids = fields.One2many('secondary.file.owner', 'sec_own_id')



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


    def confirm_button(self):
        # for rec in self:
        if self.user.id == False:
            raise UserError(_("%s is not configured to owned this file") % self.employee.name)
        else:
            if self.defid.current_owner_id == self.env.user.id:
                current_employee  = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                sec_own = []
                previous_owner = []
                previous_owner.append(self.defid.current_owner_id.id)
                transfer_to_emp = self.env['hr.employee'].search([('user_id', '=', self.user.id)], limit=1)
                self.defid.previous_owner_emp = [(4, transfer_to_emp.id)]

                # self.defid.previous_owner = [(6, 0, previous_owner)]

                self.defid.last_owner_id = self.defid.current_owner_id.id
                self.defid.current_owner_id = self.user.id
                self.defid.responsible_user_id = self.user.id
                for line in self.sec_own_ids:
                    self.defid.sec_owner = [(4, line.employee.user_id.id)]
                    self.defid.previous_owner = [(4, line.employee.user_id.id)]
                    sec_own.append(line.employee.user_id.id)
                # self.defid.sec_owner = [(6,0,sec_own)]
                self.env['file.tracking.information'].create({
                    'create_let_id': self.defid.id,
                    'forwarded_date': datetime.now().date(),
                    'forwarded_to_user': self.user.id,
                    'forwarded_to_dept': self.department.id,
                    'job_pos': self.jobposition.id,
                    'forwarded_by':self.env.uid,
                    'remarks':self.remarks
                })
                self.env['file.tracker.report'].create({
                    'name': str(self.defid.name),
                    'number': str(self.defid.letter_number),
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
                    'action_taken': 'correspondence_forwarded',
                    'remarks': self.remarks,
                    'details': 'Correspondence Forwarded'
                })
            else:
                # self.defid.current_owner_id = self.env.user.id
                # self.confirm_button()
                raise ValidationError("You are not able to forward this file, as you are not the Primary owner of this file")
        return {
            'name': 'Incoming correspondence',
            'view_type': 'form',
            'view_mode': 'kanban,tree,graph,pivot,form',
            'res_model': 'muk_dms.file',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }



class SecondaryOwners(models.Model):
    _name = 'secondary.file.owner'
    _description = 'Secondary Owners'

    sec_own_id = fields.Many2one('file.wizard')
    department = fields.Many2one('hr.department', string = "Department")
    jobposition = fields.Many2one('hr.job', string = "Job position")
    employee = fields.Many2one('hr.employee', string='Employee')
    user = fields.Many2one('res.users', related = 'employee.user_id', string='User')


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

