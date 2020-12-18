from odoo import api, fields, models, _
from odoo.http import request
from datetime import date


class HealthBusinessType(models.Model):
    _name = "health.manage.nearmiss"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Health Manage Near Miss Information"


    unit_id = fields.Many2one('health.unit.master',string='Unit :', track_visibility='always')
    location = fields.Char('Location :')
    from_date = fields.Date('From Date :')
    to_date = fields.Date('To Date :')
    area_in_charge = fields.Char('Area In Charge : :', track_visibility='always')
    near_miss_location = fields.Char('Location of Near Miss :', track_visibility='always')
    near_miss_dt = fields.Datetime('Date and Time of Near Miss :', track_visibility='always')
    description = fields.Char('Description :', track_visibility='always')
    reported_by = fields.Char('Reported by :')
    employee_id = fields.Char('Employee Id :')
    department_id = fields.Many2one('hr.department')

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
