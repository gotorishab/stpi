from odoo import api, fields, models, _
from odoo.http import request
from datetime import date


class HealthBusinessType(models.Model):
    _name = "health.manage.zoneaudit"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Health Manage zoneaudit"


    unit_id = fields.Many2one('health.unit.master',string='Unit :', track_visibility='always')
    month = fields.Selection([('January', 'January'),
                                    ('February', 'February'),
                                    ('March', 'March'),
                                    ('April', 'April'),
                                    ('May', 'May'),
                                    ('June', 'June'),
                                    ('July', 'July'),
                                    ('August', 'August'),
                                    ('September', 'September'),
                                    ('October', 'October'),
                                    ('November', 'November'),
                                    ('December', 'December')
                                    ], string="Month :", track_visibility='always')
    year = fields.Char('Year', track_visibility='always', default=str(date.today().year))
    upload = fields.Binary('Upload Audit File', track_visibility='always')
    description = fields.Char('Description :', track_visibility='always')


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

