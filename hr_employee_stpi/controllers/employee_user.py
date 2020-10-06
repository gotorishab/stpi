from odoo import http
from odoo.http import request
import json

class CreateUser(http.Controller):



    @http.route(['/create_user'], type='http', auth='public', csrf=False, methods=['POST'])
    def create_hrmis_user(self, name=None, login=None, email=None, password=None, **kwargs):
        user_det = []
        if login and name and email and password:
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
            message = "Please pass login, email and name and password"
            loaded_r = json.dumps(dict(response=str(message)))
            return loaded_r



    @http.route(['/create_users'], type='json', auth='none', csrf=False,  methods=['POST'])
    def create_hrmis_users(self, name=None, login=None, email=None, password=None, **kwargs):
            user_det = []
            if login and name and email and password:
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
                            'id': rec.id,
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
                message = "Please pass login, email and name and password"
                loaded_r = json.dumps(dict(response=str(message)))
                return loaded_r



    @http.route(['/create_employee'], type='json', auth='none', csrf=False,  methods=['POST'])
    def create_hrmis_employee(self, salutation=None, name=None, department_id=None, job_id=None, parent_id=None, work_email=None, **kwargs):
            user_det = []
            if salutation and name and department_id and job_id:
                user_details_data = request.env['hr.employee'].sudo().create({
                    'salutation': salutation,
                    'name': name,
                    'department_id': department_id,
                    'job_id': job_id,
                    'parent_id': parent_id,
                    'work_email': work_email
                        })
                if user_details_data:
                    for rec in user_details_data:
                        vals = {
                            'id': rec.id,
                            'salutation': salutation,
                            'name': name,
                            'department_id': department_id,
                            'job_id': job_id,
                            'parent_id': parent_id,
                            'work_email': work_email,
                        }
                        user_det.append(vals)
                    loaded_r = json.dumps(dict(response=str(user_det)))
                    return loaded_r
                else:
                    message = "User not created"
                    loaded_r = json.dumps(dict(response=str(message)))
                    return loaded_r
            else:
                message = "Please pass salutation, department_id and name and job_id and parent_id and work_email"
                loaded_r = json.dumps(dict(response=str(message)))
                return loaded_r

