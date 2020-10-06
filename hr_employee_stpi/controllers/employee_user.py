from odoo import http
from odoo.http import request
import json

class FileForwardData(http.Controller):



    @http.route(['/create_user'], type='http', auth='public', csrf=False, methods=['POST'])
    def create_hrmis_user(self, name=None, login=None, email=None, password=None, **kwargs):
        user_det = []
        if login and name and email:
            user_details_data = request.env['res.users'].sudo().create({
                'name': name,
                'login': login,
                'password': '1234',
                'confirm_password': '1234',
                'email': email,
                'notification_type': 'inbox',
                'sel_groups_1_9_10':1,
                    })
            if user_details_data:
                for rec in user_details_data:
                    vals = {
                        'name': name,
                        'login': login,
                        'email': email,
                        'password': password,
                    }
                    user_det.append(vals)
                loaded_r = json.dumps(dict(response=str(user_det)))
                return loaded_r
            else:
                message = "User not created"
                loaded_r = json.dumps(dict(response=str(message)))
                return loaded_r
        else:
            message = "Please pass login, email and name"
            loaded_r = json.dumps(dict(response=str(message)))
            return loaded_r
