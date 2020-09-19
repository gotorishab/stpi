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
        data = {
            'name': res.name,
            'username': res.login,
            'password': res.password,
            'userid': res.name,
            'wing_id': res.name,
            'section_id': res.name,
            'designation_id': res.name,
            'email': res.login,
            'mobile': res.name,
            'user_type_id': res.name,
            'is_wing_head': res.name,
            'user_id': res.name,
        }

        req = requests.post('http://103.92.47.152/STPI/www/web-service/add-user/', data=data,
                            json=None)
        try:
            # print('=====================================================', req)
            pastebin_url = req.text
            print('===========================pastebin_url==========================', pastebin_url)
            dictionary = json.loads(pastebin_url)
        except Exception as e:
            print('=============Error==========', e)



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