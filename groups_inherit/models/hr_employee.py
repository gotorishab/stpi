# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
import re


class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    @api.multi
    def create_user(self):
        return {
            'name': 'Create User',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('groups_inherit.view_createuser_wizard').id,
            'res_model': 'createuser.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_employee_id': self.id,
                'default_res_model': self._name,
                'default_res_id': self.id,
                'default_name': self.name,
                'default_login': self.identify_id,
                }
        }
    