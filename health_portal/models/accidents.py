from odoo import api, fields, models, _
from odoo.http import request


class HealthBusinessType(models.Model):
    _name = "health.manage.accidents"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Health Manage Accidents"

    unit_id = fields.Many2one('health.unit.master',string='Select Unit :', track_visibility='always')
    date = fields.Date(string='Accident Date :', track_visibility='always')
    affected_name = fields.Char('Name of Affected :', track_visibility='always')
    location = fields.Char('Location :', track_visibility='always')
    maj_min = fields.Selection([('major', 'Major'),
                                   ('minor', 'Minor')
                                   ], string="Minor/ Major :", track_visibility='always')
    details = fields.Char('Accident Details :', track_visibility='always')
    route_cause = fields.Char('Route cause:', track_visibility='always')
    reason_id = fields.Many2one('health.accident.master',string='Select Reason :', track_visibility='always')
    implement_date = fields.Date(string='Date of implementation of preventive action :', track_visibility='always')
    action_taken = fields.Text('Preventive Action Taken :', track_visibility='always')
    route_cause_why_ids = fields.One2many('health.accident.causewhy','health_accident_id',string='Root Cause Why', track_visibility='always')

    state = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('cancelled', 'Cancelled')
         ], required=True, default='draft', string='Status', track_visibility='always')

    def button_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    def button_approved(self):
        for rec in self:
            rec.write({'state': 'approved'})

    def button_submit(self):
        for rec in self:
            rec.write({'state': 'submitted'})

    def button_cancel(self):
        for rec in self:
            rec.write({'state': 'cancelled'})



class HealthAccidentCause(models.Model):
    _name = "health.accident.causewhy"
    _description = "Health Accident Root Cause"

    health_accident_id = fields.Many2one('health.manage.accidents',string='Select accident :')
    why = fields.Char(string='Why :')
    Answer = fields.Char(string='Answer :')