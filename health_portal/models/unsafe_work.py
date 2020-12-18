from odoo import api, fields, models, _
from odoo.http import request
from datetime import date


class HealthBusinessType(models.Model):
    _name = "health.manage.unsafework"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Health Manage Safety Committee Meeting"


    unit_id = fields.Many2one('health.unit.master',string='Unit :', track_visibility='always')
    location = fields.Char('Location :')
    safety_officer = fields.Char('Name of the Safety Officer / Coordinator :')
    location_unsafe = fields.Char('Location of Unsafe Work :')
    responsible_worker = fields.Char('Responsible Worker / Department:')
    observation_date = fields.Date('Date of Observation :')
    describe_hazard = fields.Char('Describe Potential Hazard :', track_visibility='always')
    address_problem = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')
         ], string='Were you able to address the problem to the department:', track_visibility='always')
    action_taken = fields.Char('Action Taken by the Responsible Worker/ Department :', track_visibility='always')
    received_concern = fields.Char('Received By Concern Person :', track_visibility='always')
    closed_officer = fields.Char('Closed Out by Safety Officer / Coordinator:', track_visibility='always')

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
