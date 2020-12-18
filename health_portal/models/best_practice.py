from odoo import api, fields, models, _
from odoo.http import request
from datetime import date


class HealthBusinessType(models.Model):
    _name = "health.manage.bestpractice"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Health Manage Best Practice"


    unit_id = fields.Many2one('health.unit.master',string='Unit :', track_visibility='always')
    location = fields.Char('Location :')
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
    year = fields.Char('Year :', track_visibility='always', default=str(date.today().year))
    best_practice = fields.Binary('Best Practice Image :', track_visibility='always')
    old_practice = fields.Binary('Old Practice Image :', track_visibility='always')
    details = fields.Char('Best Practice Details : :', track_visibility='always')


    state = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Submitted'), ('cancelled', 'Cancelled')
         ], required=True, default='draft', string='Status', track_visibility='always')

    def button_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    def button_submit(self):
        for rec in self:
            rec.write({'state': 'submitted'})

    def button_cancel(self):
        for rec in self:
            rec.write({'state': 'cancelled'})
