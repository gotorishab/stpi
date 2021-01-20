from odoo import api, fields, models, _
from odoo.http import request


class HealthBusinessType(models.Model):
    _name = "health.manage.monthlyincident"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Health Manage monthly incident"

    unit_id = fields.Many2one('health.unit.master',string='Select Unit :', track_visibility='always')
    location = fields.Char('Location :', track_visibility='always')
    safety_coordinator = fields.Many2one('res.users',string='Safety Coordinator :', track_visibility='always')
    date = fields.Date(string='Date')


    incident_detail_ids = fields.One2many('health.monthlyincident.details','health_incident_id',string='Details', track_visibility='always')

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



class HealthAccidentCause(models.Model):
    _name = "health.monthlyincident.details"
    _description = "Health Monthly Incident Details"

    health_incident_id = fields.Many2one('health.manage.monthlyincident',string='Select incident :')
    department_id = fields.Many2one('vhr.department',string='Name of Department :')
    no_employees_ytd = fields.Float('No of Employees (YTD)')
    no_employees_month = fields.Float('No of Employees (Month)')
    man_hrs_worked_ytd = fields.Float('Man hours Worked (YTD)')
    man_hrs_worked_month = fields.Float('Man hours Worked (Month)')
    min_accident_ytd = fields.Float('Minor Accidents (YTD)')
    min_accident_month = fields.Float('Minor Accidents (Month)')
    maj_accident_ytd = fields.Float('Major Accidents (YTD)')
    maj_accident_month = fields.Float('Major Accidents (Month)')
    man_days_lost_ytd = fields.Float('Man Days Lost from Work (YTD)')
    man_days_lost_month = fields.Float('Man Days Lost from Work (Month)')
    total_accident_ytd = fields.Float('Total Accidents (YTD)')
    total_accident_month = fields.Float('Total Accidents (Month)')
    frequency_rate_ytd = fields.Float('Frequency Rate (YTD)')
    frequency_rate_month = fields.Float('Frequency Rate (Month)')
    severity_rate_ytd = fields.Float('Severity Rate (YTD)')
    severity_rate_month = fields.Float('Severity Rate (Month)')
    incident_rate_ytd = fields.Float('Incident Rate (YTD)')
    incident_rate_month = fields.Float('Incident Rate (Month)')