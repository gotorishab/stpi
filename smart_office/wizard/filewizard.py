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
                    rec.defid.last_owner_id = rec.env.user.id
                    rec.defid.current_owner_id = rec.user.id
                    # rec.defid.sec_owner_one = rec.s1user.id
                    # rec.defid.sec_owner_two = rec.s2user.id
                    # rec.defid.sec_owner_three = rec.s3user.id
                    rec.defid.responsible_user_id = rec.user.id
                    for line in rec.sec_own_ids:
                        rec.defid.sec_owner += line.employee.user_id.id
                    rec.defid.previous_owner += rec.env.user.id
                    self.env['file.tracking.information'].create({
                         'create_let_id': rec.defid.id,
                        'forwarded_date': datetime.now().date(),
                        'forwarded_to_user': rec.user.id,
                        'forwarded_to_dept': rec.department.id,
                        'job_pos': rec.jobposition.id,
                        'forwarded_by':rec.env.uid
                    })
                    for emp in rec.sec_own_ids:
                        rec.defid.sec_owner += emp.user
                else:
                    raise ValidationError("You are not able to forward this file, as you are not the Primary owner of this file")



    # def confirm_button(self):
        # data = {
        #     'assign_name': 'Dilipjis',
        #     'assign_no': 1003,
        #     'assign_date': datetime.now().date(),
        #     'assign_subject': 'assign demo',
        #     'remarks': 'web remarks',
        #     'created_by': 1,
        #     'doc_flow_id': 0,
        #     'wing_id': 1,
        #     'section_id': 0,
        #     'designation_id': 78,
        # }
        # req = requests.post('http://103.92.47.152/corporate_demo/www/web-service/add-assignment/', data=data,
        #                     json=None)
        # print('==============================================', req)
        # pastebin_url = req.text
        # print("The pastebin URL is:%s" % pastebin_url)
        # req.raise_for_status()
        # status = req.status_code
        # if int(status) in (204, 404):
        #     response = False
        # else:
        #     response = req.json()
        # return (status, response)



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

