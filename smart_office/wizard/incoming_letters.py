from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date, timedelta
import requests
import json

class IncomingLetterWizard(models.TransientModel):
    _name = 'letter.incoming'
    _description = 'Wizard of Incoming Files'

    letter_id = fields.Many2one('muk_dms.file', string='Letter')

    def show_incoming_letter(self):
        if self:
            my_id = []
            files = self.env['muk_dms.file'].search()
            srch_id = self.env.user.id
            for file in files:
                if srch_id in file.sec_owner.ids:
                    my_id.append(file.id)

            return {
                'name': 'Incoming Files',
                'view_type': 'form',
                'view_mode': 'kanban,tree,graph,pivot,form',
                'res_model': 'muk_dms.file',
                'type': 'ir.actions.act_window',
                'target': 'current',
                # 'view_id': self.env.ref('hr_applicant.view_employee_relative_tree').id,
                'domain': ['|', ('id', 'in', my_id), ('current_owner_id', '=', self.env.user.id)],
                }



    def show_incoming_sec_letter(self):
        if self:
            emp = self.env['hr.employee'].search(['|', ('parent_id', '=', self.env.user.id), ('parent_id.parent_id', '=', self.env.user.id)])
            return {
                'name': 'Incoming Files',
                'view_type': 'form',
                'view_mode': 'kanban,tree,graph,pivot,form',
                'res_model': 'muk_dms.file',
                'type': 'ir.actions.act_window',
                'target': 'current',
                # 'view_id': self.env.ref('hr_applicant.view_employee_relative_tree').id,
                'domain': [('current_owner_id', 'in', emp)],
                }


