# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, date, timedelta


class PullInto(models.TransientModel):
    _name = "create.user.employee"
    _description = "Create User"


    def create_user_action(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        for rec in self.env['hr.employee'].browse(active_ids):
            if rec.user_id == False and rec.work_email != False and rec.name != False and rec.unit_id != False:
                Users = rec.env['res.users'].with_context({'no_reset_password': True, 'mail_create_nosubscribe': True})
                user = Users.create({
                    'name': rec.name,
                    'login': rec.work_email,
                    'password': '1234',
                    'confirm_password': '1234',
                    'email': rec.work_email,
                    'notification_type': 'inbox',
                    'default_branch_id': rec.unit_id.id,
                    'sel_groups_1_9_10': 1,
                })

                try:
                    # comp_model = self.env['res.users'].sudo().search([('login', '=', rec.login)], limit=1)
                    _body = (_(
                        (
                            "<ul><b>User Created: {0} </b></ul> ").format(rec.login)))
                    rec.message_post(body=_body)
                    rec.user_id = user.id
                except Exception as e:
                    print('=============Error==========', e)