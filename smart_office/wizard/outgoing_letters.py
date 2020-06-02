from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date, timedelta
import requests
import json

class IncomingLetterWizard(models.TransientModel):
    _name = 'letter.outgoing'
    _description = 'Wizard of Outgoing Files'

    letter_id = fields.Many2one('muk_dms.file', string='Letter')

    def show_outgoing_letter(self):
        if self:
            previous_owner = []
            files = self.env['muk_dms.file'].search()
            for file in files:
                file.srch_id = self.env.user.id
                previous_owner += file.previous_owner
            return {
                'name': 'Outgoing Files',
                'view_type': 'form',
                'view_mode': 'kanban,tree,graph,pivot,form',
                'res_model': 'muk_dms.file',
                'type': 'ir.actions.act_window',
                'target': 'current',
                # 'view_id': self.env.ref('hr_applicant.view_employee_relative_tree').id,
                'domain': [('srch_id', 'in', previous_owner)],
                }


    def show_outgoing_sec_letter(self):
        if self:
            emp = self.env['hr.employee'].search([('parent_id', '=', self.env.user.id)])
            return {
                'name': 'Incoming Files',
                'view_type': 'form',
                'view_mode': 'kanban,tree,graph,pivot,form',
                'res_model': 'muk_dms.file',
                'type': 'ir.actions.act_window',
                'target': 'current',
                # 'view_id': self.env.ref('hr_applicant.view_employee_relative_tree').id,
                'domain': [('previous_owner', 'in', emp)],
                }


