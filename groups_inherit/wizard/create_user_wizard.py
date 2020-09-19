from odoo import api, fields, models,_
import requests
import json


class createuser_wizard(models.TransientModel):
    _name = 'createuser.wizard'

    @api.model
    def _get_branch(self):
        return self.env.user.default_branch_id

    res_id = fields.Integer('ID')
    res_model = fields.Char('Model')

    name = fields.Char('Name')
    login = fields.Char('Login')
    groups_id = fields.Many2many('res.groups',string='Groups', domain="[('stpi', '=', True)]")
    branch_ids = fields.Many2many('res.branch', default=_get_branch)
    default_branch_id = fields.Many2one('res.branch', string='Default branch',default=_get_branch)
    employee_id = fields.Many2one('hr.employee', string='Employee')

    def button_confirm(self):
        for rec in self:
            model_id = rec.env[rec.res_model].browse(rec.res_id)
            Users = rec.env['res.users'].with_context({'no_reset_password': True, 'mail_create_nosubscribe': True})
            user = Users.create({
                'name': rec.name,
                'login': rec.login,
                'email': model_id.work_email,
                'notification_type': 'inbox',
                'default_branch_id':rec.default_branch_id.id,
                'sel_groups_1_9_10':1,
                'branch_ids': [(6, 0, rec.branch_ids.ids)]
            })
            for group in rec.groups_id:
                group.users += user
            data = {
                'name': rec.name,
                'username': rec.login,
                'password': rec.password,
                'userid': user.id,
                'wing_id': rec.employee_id.department_id.id,
                'section_id': 1,
                'designation_id': rec.employee_id.job_id.id,
                'email': rec.login,
                'mobile': rec.employee_id.phone,
                'user_type_id': 3,
                'is_wing_head': rec.name,
                'user_id': rec.env.uid,
            }

            req = requests.post('http://103.92.47.152/STPI/www/web-service/add-user/', data=data,
                                json=None)
            try:
                # print('=====================================================', req)
                pastebin_url = req.text
                print('===========================pastebin_url==========================', pastebin_url)
                dictionary = json.loads(pastebin_url)
                comp_model = self.env['res.users'].search([('login', '=', rec.login)], limit=1)
                _body = (_(
                    (
                        "<ul><b>User Created: {0} </b></ul> ").format(rec.login)))
                model_id.message_post(body=_body)
                model_id.user_id = comp_model.id
            except Exception as e:
                print('=============Error==========', e)



