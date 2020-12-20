from odoo import api, fields, models, _
from odoo.http import request
from datetime import date


class HealthBusinessType(models.Model):
    _name = "health.manage.docrep"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Health Document Repository"

    select_document = fields.Char('Document Type :', track_visibility='always')
    document_description = fields.Char('Document Description :', track_visibility='always')
    file = fields.Binary('File :', track_visibility='always')

    state = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('cancelled', 'Cancelled')
         ], required=True, default='draft', string='Status', track_visibility='always')

    def button_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    def button_submit(self):
        for rec in self:
            rec.write({'state': 'submitted'})

    def button_approved(self):
        for rec in self:
            rec.write({'state': 'approved'})

    def button_cancel(self):
        for rec in self:
            rec.write({'state': 'cancelled'})
