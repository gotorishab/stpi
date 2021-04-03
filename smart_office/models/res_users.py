from odoo import fields, models, api, _
from datetime import datetime, date, timedelta
import requests
import json
from odoo.exceptions import UserError

class ResUesrs(models.Model):
    _inherit= 'res.users'

    @api.model
    def create(self, vals):
        res = super(ResUesrs, self).create(vals)
        res.password = '1234'
        res.confirm_password = '1234'
        data = {
            'name':res.name,
            'username':res.login,
            'password':'1234',
            'userid':res.id,
            'wing_id':11,
            'section_id': 22,
            'designation_id':19,
            'email':res.email or 'abc@gmail.com',
            'mobile':res.phone or '1234567890',
            'user_type_id':'3',
            'is_wing_head':0,
            'user_id':res.id,
        }
        print("********************", data)
        try:
            # print('=====================================================', req)
            req = requests.post('http://103.92.47.152/STPI/www/web-service/add-user/', data=data,
                            json=None)
            pastebin_url = req.text
            print('===========================pastebin_url==========================', pastebin_url)
            dictionary = json.loads(pastebin_url)
        except Exception as e:
            print('=============Error==========', e)
        return res



class HrDepartment(models.Model):
    _inherit= 'hr.department'

    @api.model
    def create(self, vals):
        res = super(HrDepartment, self).create(vals)
        data = {
            'name': res.name,
            'dept_id': res.name,
            'user_id': res.name,
        }

        req = requests.post('http://103.92.47.152/STPI/www/web-service/department/', data=data,
                            json=None)
        try:
            # print('=====================================================', req)
            pastebin_url = req.text
            print('===========================pastebin_url==========================', pastebin_url)
            dictionary = json.loads(pastebin_url)
        except Exception as e:
            print('=============Error==========', e)
        return res


class HrJob(models.Model):
    _inherit= 'hr.job'

    @api.model
    def create(self, vals):
        res = super(HrJob, self).create(vals)
        data = {
            'name': res.name,
            'designation_id': res.name,
            'user_id': res.name,
        }

        req = requests.post('http://103.92.47.152/STPI/www/web-service/designation/', data=data,
                            json=None)
        try:
            # print('=====================================================', req)
            pastebin_url = req.text
            print('===========================pastebin_url==========================', pastebin_url)
            dictionary = json.loads(pastebin_url)
        except Exception as e:
            print('=============Error==========', e)
        return res

class HrEmployee(models.Model):
    _inherit = "hr.employee"


    def create_employee_scheduler(self):
        all_employees = self.env['hr.employee'].sudo().search([('user_id', '=', False)])
        if all_employees:
            for rec in all_employees:
                Users = self.env['res.users'].with_context(
                    {'no_reset_password': True, 'mail_create_nosubscribe': True})
                user = Users.create({
                    'name': rec.name,
                    'login': rec.identify_id,
                    'password': '1234',
                    'confirm_password': '1234',
                    'email': rec.work_email or 'abc@gmail.com',
                    'notification_type': 'inbox',
                    'default_branch_id': rec.branch_id.id,
                    'sel_groups_1_9_10': 1,
                })
                print('===================User===============',user.id)
                rec.user_id = user.id
                print('===================Employee User===============',rec.user_id)
