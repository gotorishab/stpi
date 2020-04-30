from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date, timedelta
import requests
import json

class FileWizard(models.TransientModel):
    _name = 'file.wizard'
    _description = 'Wizard of File Wizard'
    _rec_name = 'user'

    department = fields.Many2one('hr.department', string = "Department")
    jobposition = fields.Many2one('hr.job', string = "Job position")
    employee = fields.Many2one('hr.employee', string='Employee')
    user = fields.Many2one('res.users', related = 'employee.user_id', string='User')
    defid = fields.Many2one('muk_dms.file', invisible=1)


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
                if rec.defid.responsible_user_id.id == rec.env.user.id:
                    rec.defid.responsible_user_id = rec.user.id
                    self.env['file.tracking.information'].create({
                         'create_let_id': rec.defid.id,
                        'forwarded_date': datetime.now().date(),
                        'forwarded_to_user': rec.user.id,
                        'forwarded_to_dept': rec.department.id,
                        'job_pos': rec.jobposition.id,
                        'forwarded_by':rec.env.uid
                    })
                else:
                    raise ValidationError("You are not able to forward this file, as you are not the owner of this file")



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