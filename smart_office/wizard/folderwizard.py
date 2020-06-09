from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date, timedelta
import requests
import json

class FileWizard(models.Model):
    _name = 'folder.wizard'
    _description = 'Wizard of File Wizard'
    _rec_name = 'user'

    department = fields.Many2one('hr.department', string = "Department")
    jobposition = fields.Many2one('hr.job', string = "Job position")
    employee = fields.Many2one('hr.employee', string='Employee')
    user = fields.Many2one('res.users', related = 'employee.user_id', string='User')

    s1department = fields.Many2one('hr.department', string = "Department")
    s1jobposition = fields.Many2one('hr.job', string = "Job position")
    s1employee = fields.Many2one('hr.employee', string='Employee')
    s1user = fields.Many2one('res.users', related = 's1employee.user_id', string='User')

    s2department = fields.Many2one('hr.department', string = "Department")
    s2jobposition = fields.Many2one('hr.job', string = "Job position")
    s2employee = fields.Many2one('hr.employee', string='Employee')
    s2user = fields.Many2one('res.users', related = 's2employee.user_id', string='User')

    s3department = fields.Many2one('hr.department', string = "Department")
    s3jobposition = fields.Many2one('hr.job', string = "Job position")
    s3employee = fields.Many2one('hr.employee', string='Employee')
    s3user = fields.Many2one('res.users', related = 's3employee.user_id', string='User')
    remarks = fields.Text('Remarks')

    defid = fields.Many2one('folder.master', invisible=1)
    sec_own_ids = fields.One2many('secondary.folder.owner', 'sec_own_id')



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


    @api.onchange('s1department','s1jobposition')
    def _onchange_user_one(self):
        for rec in self:
            if rec.s1department.id and not rec.s1jobposition.id:
                return {'domain': {'s1employee': [('department_id', '=', rec.s1department.id)]}}
            elif rec.s1jobposition.id and not rec.s1department.id:
                return {'domain': {'s1employee': [('job_id', '=', rec.s1jobposition.id)]}}
            elif rec.s1jobposition.id and rec.s1department.id:
                return {'domain': {'s1employee': [('job_id', '=', rec.s1jobposition.id),('department_id', '=', rec.s1department.id)]}}
            else:
                return {'domain': {'s1employee': ['|', ('job_id', '=', rec.s1jobposition.id),('department_id', '=', rec.s1department.id)]}}


    @api.onchange('s2department','s2jobposition')
    def _onchange_user_two(self):
        for rec in self:
            if rec.s2department.id and not rec.s2jobposition.id:
                return {'domain': {'s2employee': [('department_id', '=', rec.s2department.id)]}}
            elif rec.s2jobposition.id and not rec.s2department.id:
                return {'domain': {'s2employee': [('job_id', '=', rec.s2jobposition.id)]}}
            elif rec.s2jobposition.id and rec.s2department.id:
                return {'domain': {'s2employee': [('job_id', '=', rec.s2jobposition.id),('department_id', '=', rec.s2department.id)]}}
            else:
                return {'domain': {'s2employee': ['|', ('job_id', '=', rec.s2jobposition.id),('department_id', '=', rec.s2department.id)]}}


    @api.onchange('s3department','s3jobposition')
    def _onchange_user_three(self):
        for rec in self:
            if rec.s3department.id and not rec.s3jobposition.id:
                return {'domain': {'s3employee': [('department_id', '=', rec.s3department.id)]}}
            elif rec.s3jobposition.id and not rec.s3department.id:
                return {'domain': {'s3employee': [('job_id', '=', rec.s3jobposition.id)]}}
            elif rec.s3jobposition.id and rec.s3department.id:
                return {'domain': {'s3employee': [('job_id', '=', rec.s3jobposition.id),('department_id', '=', rec.s3department.id)]}}
            else:
                return {'domain': {'s3employee': ['|', ('job_id', '=', rec.s3jobposition.id),('department_id', '=', rec.s3department.id)]}}


    def confirm_button(self):
        for rec in self:
            if rec.user.id == False:
                raise UserError(_("%s is not configured to owned this file") % rec.employee.name)
            else:
                if rec.defid.current_owner_id.id == rec.env.user.id:
                    file_count = 0
                    sec_own = []
                    previous_owner = []
                    rec.defid.last_owner_id = rec.env.user.id
                    rec.defid.current_owner_id = rec.user.id
                    for line in rec.sec_own_ids:
                        sec_own.append(line.employee.user_id.id)
                    rec.defid.sec_owner = [(6,0,sec_own)]
                    previous_owner.append(rec.env.user.id)
                    rec.defid.previous_owner = [(6,0,previous_owner)]
                    current_employee  = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                    self.env['folder.tracking.information'].create({
                        'create_let_id': rec.defid.id,
                        'forwarded_date': datetime.now().date(),
                        'forwarded_to_user': rec.user.id,
                        'forwarded_to_dept': rec.department.id,
                        'job_pos': rec.jobposition.id,
                        'forwarded_by': rec.env.uid,
                        'remarks': rec.remarks
                    })
                    f_details = ""
                    if file_count == 0:
                        f_details = "File forwarded with no correspondence"
                    elif file_count == 1:
                        f_details = "File forwarded with single correspondence"
                    elif file_count > 1:
                        f_details = "File forwarded with multiple Correspondence"
                    else:
                        f_details = ""
                    self.env['file.tracker.report'].create({
                        'name': str(rec.defid.folder_name),
                        'number': str(rec.defid.number),
                        'type': 'File',
                        'forwarded_by': str(current_employee.user_id.name),
                        'forwarded_by_dept': str(current_employee.department_id.name),
                        'forwarded_by_jobpos': str(current_employee.job_id.name),
                        'forwarded_by_branch': str(current_employee.branch_id.name),
                        'forwarded_date': datetime.now().date(),
                        'forwarded_to_user': str(rec.user.name),
                        'forwarded_to_dept': str(rec.department.name),
                        'forwarded_to_branch': str(rec.user.branch_id.name),
                        'job_pos': str(rec.jobposition.name),
                        'remarks': rec.remarks,
                        'details': f_details
                    })
                    for file in rec.defid.file_ids:
                        file_count+=1
                        file.last_owner_id = rec.env.user.id
                        file.responsible_user_id = rec.env.user.id
                        file.current_owner_id = rec.user.id
                        for line in rec.sec_own_ids:
                            file.sec_owner += line.employee.user_id.id
                        file.previous_owner += rec.env.user.id
                        self.env['file.tracking.information'].create({
                            'create_let_id': file.id,
                            'forwarded_date': datetime.now().date(),
                            'forwarded_to_user': rec.user.id,
                            'forwarded_to_dept': rec.department.id,
                            'job_pos': rec.jobposition.id,
                            'forwarded_by':rec.env.uid,
                            'remarks': rec.remarks
                        })
                        self.env['file.tracker.report'].create({
                            'name': str(file.name),
                            'number': str(file.letter_number),
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
                            'remarks': rec.remarks,
                            'details': "Correspondence Forwarded through File {}".format(rec.defid.number)
                        })

                else:
                    raise ValidationError("You are not able to forward this file, as you are not the Primary owner of this file")



class SecondaryOwners(models.Model):
    _name = 'secondary.folder.owner'
    _description = 'Secondary Owners'

    sec_own_id = fields.Many2one('folder.wizard')
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

