from odoo import api, fields, models, _
from odoo.http import request
from datetime import date


class HealthBusinessType(models.Model):
    _name = "health.manage.safetycomm"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Health Manage Safety Committee Meeting"


    unit_id = fields.Many2one('health.unit.master',string='Unit :', track_visibility='always')
    venue = fields.Char('Venue :')
    date = fields.Date('Date :')
    agenda = fields.Char('Agenda :')
    outcome = fields.Char('Mandated Outcome of the Meeting :')
    management = fields.Char('Management Representatives :')
    workers = fields.Char('Workers Representatives :')
    action_ids = fields.One2many('health.manage.safetyaction','safety_meeting_id',string='Details')

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


class HealthSafetyAction(models.Model):
    _name = "health.manage.safetyaction"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Health Manage Safety Committee Meeting Details"

    safety_meeting_id = fields.Many2one('health.manage.safetycomm',string='Safety Meeting :', track_visibility='always')
    action_point = fields.Char('Action Point :')
    person_responsible = fields.Char('Person Responsible :')
    support_team = fields.Char('Support Team :')
    target_date = fields.Date('Target Date')