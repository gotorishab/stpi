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
            return {
                'name': 'Outgoing Files',
                'view_type': 'form',
                'view_mode': 'kanban,tree,graph,pivot,form',
                'res_model': 'muk_dms.file',
                'type': 'ir.actions.act_window',
                'target': 'current',
                # 'view_id': self.env.ref('hr_applicant.view_employee_relative_tree').id,
                'domain': [('previous_owner', 'in', self.env.user.id)],
                }


