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
        for rec in self:
            if rec.user.id == False:
                raise UserError(_("%s is not configured to owned this file") % rec.employee.name)
            else:
                if rec.defid.current_owner_id.id == rec.env.user.id:
                    current_employee  = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                    sec_own = []
                    previous_owner = []
                    rec.defid.last_owner_id = rec.env.user.id
                    rec.defid.current_owner_id = rec.user.id
                    rec.defid.responsible_user_id = rec.user.id
                    for line in rec.sec_own_ids:
                        sec_own.append(line.employee.user_id.id)
                    rec.defid.sec_owner = [(6,0,sec_own)]
                    previous_owner.append(rec.env.user.id)
                    rec.defid.previous_owner = [(6,0,previous_owner)]
                    self.env['file.tracking.information'].create({
                        'create_let_id': rec.defid.id,
                        'forwarded_date': datetime.now().date(),
                        'forwarded_to_user': rec.user.id,
                        'forwarded_to_dept': rec.department.id,
                        'job_pos': rec.jobposition.id,
                        'forwarded_by':rec.env.uid,
                        'remarks':rec.remarks
                    })
                    self.env['file.tracker.report'].create({
                        'name': str(rec.defid.name),
                        'number': str(rec.defid.letter_number),
                        'type': 'Correspondence',
                        'forwarded_by': str(current_employee.user_id.name),
                        'forwarded_by_dept': str(current_employee.department_id.name),
                        'forwarded_by_jobpos': str(current_employee.job_id.name),
                        'forwarded_by_branch': str(current_employee.branch_id.name),
                        'forwarded_date': datetime.now().date(),
                        'forwarded_to_user': str(rec.user.name),
                        'forwarded_to_dept': str(rec.department.name),
                        'job_pos': str(rec.jobposition.name),
                        'forwarded_to_branch': str(rec.user.branch_id.name),
                        'action_taken': 'correspondence_forwarded',
                        'remarks': rec.remarks,
                        'details': 'Correspondence Forwarded'
                    })
                else:
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

