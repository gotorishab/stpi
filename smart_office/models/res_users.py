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
            'name': res.document_type,
            'username': int(seq),
            'password': enclosure_details,
            'user_id': current_employee.user_id.id,
            'attachment[]': res.content
        }
        print('==============================name=============================', int(seq))
        print('==============================enclosure_details=============================', enclosure_details)
        print('==============================user_id=============================', current_employee.user_id.id)
        # print('==============================res.content=============================', res.content)
        req = requests.post('http://103.92.47.152/STPI/www/web-service/add-letter/', data=data,
                            json=None)
        try:
            print('=====================================================', req)
            pastebin_url = req.text
            print('===========================pastebin_url==========================', pastebin_url)
            dictionary = json.loads(pastebin_url)
            res.php_letter_id = str(dictionary["response"]["letterData"]["id"])
        except Exception as e:
            print('=============Error==========', e)