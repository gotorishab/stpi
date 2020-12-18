from odoo import api, fields, models, _
from odoo.http import request


class HealthBusinessType(models.Model):
    _name = "health.manage.fireincident"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Health Manage fire incident"

    unit_id = fields.Many2one('health.unit.master',string='Select Unit :', track_visibility='always')
    hall_no = fields.Char('Hall No. :', track_visibility='always')
    location = fields.Char('Location :', track_visibility='always')
    date = fields.Date(string='Incident Date :', track_visibility='always')
    location_fire_incident = fields.Char('Location Of fire Incident:', track_visibility='always')
    loss_nloss = fields.Selection([('loss', 'Loss'),
                                   ('no_loss', 'No Loss')
                                   ], string="Reported Loss/No Loss:", track_visibility='always')

    details = fields.Char('Details of fire Incident :', track_visibility='always')
    route_cause = fields.Char('Route cause:', track_visibility='always')
    reason_id = fields.Many2one('health.accident.master',string='Select Reason :', track_visibility='always')
    action_taken = fields.Char('Preventive Action Taken :', track_visibility='always')

    route_cause_why_ids = fields.One2many('health.fireincident.causewhy','health_fireincident_id',string='Root Cause Why', track_visibility='always')

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



class HealthAccidentCause(models.Model):
    _name = "health.fireincident.causewhy"
    _description = "Health fireincident Root Cause"

    health_fireincident_id = fields.Many2one('health.manage.fireincident',string='Select Incident :')
    why = fields.Char(string='Why :')
    Answer = fields.Char(string='Answer :')