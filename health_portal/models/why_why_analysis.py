from odoo import api, fields, models, _
from odoo.http import request
from datetime import date


class HealthBusinessType(models.Model):
    _name = "health.manage.whyanalysis"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Health Manage Why-Why Analysis"

    safety_unit_name = fields.Char('SAFETY/EHS/UNIT/NAME :', track_visibility='always')
    recv = fields.Char('RECV :', track_visibility='always')
    date = fields.Date('From Date :', track_visibility='always')
    accident_no = fields.Char('ACCIDENT NO :', track_visibility='always')
    worker_no = fields.Char('Name Of The Worker:', track_visibility='always')
    debt_code = fields.Char('Dept.&Code :', track_visibility='always')
    doj = fields.Date('D.O,J:', track_visibility='always')
    supervisor_name = fields.Char('Name Of The Supervisor :', track_visibility='always')
    shift_incharge = fields.Char('Name Of Shift Incharge :', track_visibility='always')
    eitness_name = fields.Char('Name Of Two Witness :', track_visibility='always')

    ppe = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')
         ], string='Were PPE Used ? (Y/N/N/A)', track_visibility='always')
    ppe_y_ex = fields.Char('If Yes Give Example :', track_visibility='always')
    ppe_n_rs = fields.Char('If No Give Reason :', track_visibility='always')
    analysis_done_by = fields.Char('Why Why Analysis Done By :', track_visibility='always')
    description_accident = fields.Char('Description Of Accident :', track_visibility='always')
    root_cause = fields.Char('ROOT CAUSE :', track_visibility='always')
    counter_measure = fields.Char('COUNTER MEASURE :', track_visibility='always')
    concern_area_head = fields.Char('Concern Area Head', track_visibility='always')
    safety_dept = fields.Char('Safety Dept.', track_visibility='always')
    unit_head = fields.Char('Unit Head', track_visibility='always')
    analysis_why_ids = fields.One2many('health.whyanalysis.causewhy','health_whyanalysis_id',string='WHY WHY ANALYSIS & ROOT CAUSE IDENTIFICATION', track_visibility='always')


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
    _name = "health.whyanalysis.causewhy"
    _description = "Health Why-Why Analysis Root Cause"

    health_whyanalysis_id = fields.Many2one('health.manage.fireincident',string='Select Incident :')
    why = fields.Char(string='Why :')
    answer = fields.Char(string='Answer :')
    action = fields.Char(string='Action :')