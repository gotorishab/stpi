from odoo import api, fields, models, _
from odoo.http import request


class HealthBusinessType(models.Model):
    _name = "health.manage.audit"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Health Manage audit"
    _rec_name = "audit_id"


    audit_id = fields.Many2one('health.audit.type.master',string='Select Audit Form :', track_visibility='always')
    unit_id = fields.Many2one('health.unit.master',string='Select Unit :', track_visibility='always')
    date = fields.Date(string='Audit Date :', track_visibility='always')
    team = fields.Char('Audit Team :', track_visibility='always')
    coordinators = fields.Char('Audit Coordinators:', track_visibility='always')
    total_mark = fields.Float('Total mark :', track_visibility='always')
    mark_obtained = fields.Float('Mark Obtained :', track_visibility='always')
    percentage = fields.Float('Percentage :', track_visibility='always')
    no_observation = fields.Float('No Of Observations :', track_visibility='always')
    month = fields.Selection([('half_yearly', 'Half Yearly'),
                                  ('monthly', 'Monthly'),
                                  ('quaterly', 'Quaterly'),
                                  ('yearly', 'Yearly')
                                  ], string="Month :", track_visibility='always')
    next_due_date = fields.Date(string='Next Due Date :', track_visibility='always')
    observation_ids = fields.One2many('health.audit.observation','health_audit_id',string='Observations', track_visibility='always')
    audit_checklist_ids = fields.One2many('health.manageaudit.checklist','health_audit_id',string='Root Cause Why', track_visibility='always')

    @api.onchange('audit_id')
    @api.constrains('audit_id')
    def get_checklist(self, working_list=None):
        for rec in self:
            checklist_ids = []
            for i in rec.audit_id.checklist_ids:
                checklist_ids.append((0, 0, {
                    'health_audit_id': rec.id,
                    'checklist_item': i.checklist_item,
                    'sub_checklist_item': i.sub_checklist_item,
                }))
            else:
                rec.audit_checklist_ids = working_list
            rec.audit_checklist_ids = checklist_ids


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



class HealthAuditObservation(models.Model):
    _name = "health.audit.observation"
    _description = "Health Audit Observation"

    health_audit_id = fields.Many2one('health.manage.audit',string='Select accident :')
    image = fields.Binary(string='Observation Image:')
    observation = fields.Char(string='Observation :')
    recomendation = fields.Char(string='Recomendation :')


class HealthAccidentCause(models.Model):
    _name = "health.manageaudit.checklist"
    _description = "Health Accident Root Cause"

    health_audit_id = fields.Many2one('health.manage.audit',string='Select accident :')
    checklist_item = fields.Char('Checklist Item :',store=True)
    sub_checklist_item = fields.Char('Sub Checklist Item :',store=True)
    maximum_score = fields.Float('Maximum Score')
    obtained_score = fields.Float('Score Obtained :')