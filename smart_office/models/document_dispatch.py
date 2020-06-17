from odoo import fields, models, api, _
from datetime import datetime, date, timedelta
import requests
import json
from odoo.exceptions import UserError

class DispatchDocument(models.Model):
    _name = 'dispatch.document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Dispatch Document'


    cooespondence_ids = fields.Many2many('muk_dms.file', string='Correspondence', track_visibility='always')
    current_user_id = fields.Many2one('res.users', track_visibility='always')
    branch_id = fields.Many2one('res.branch', 'Branch', track_visibility='always')
    department_id = fields.Many2one('hr.department', 'Department', track_visibility='always')
    job_id = fields.Many2one('hr.job', 'Job Position', track_visibility='always')
    created_on = fields.Date(string='Date', default = fields.Date.today(), track_visibility='always')
    select_template = fields.Many2one('select.template.html', track_visibility='always')
    template_html = fields.Html('Template', track_visibility='always')
    version = fields.Char('Version', track_visibility='always')
    previousversion = fields.Char('Previous Version', track_visibility='always')
    folder_id = fields.Many2one('folder.master', string="File", track_visibility='always')
    state = fields.Selection(
        [('draft', 'Draft'), ('in_progress', 'In Progress'), ('dispatched', 'Dispatched')
         ], required=True, default='draft', string='Status', track_visibility='always')



    @api.multi
    def button_edit(self):
        for rec in self:
            current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            dd = self.env['dispatch.document'].create({
                'version': '2',
                'previousversion': rec.version,
                'template_html': rec.template_html,
                'select_template': rec.select_template.id,
                'current_user_id': current_employee.user_id.id,
                'department_id': current_employee.department_id.id,
                'job_id': current_employee.job_id.id,
                'branch_id': current_employee.branch_id.id,
                'created_on': datetime.now().date(),
                'folder_id': rec.folder_id.id,
                'state': 'draft',
                'cooespondence_ids': rec.cooespondence_ids.ids,
            })

    @api.multi
    def button_submit(self):
        for rec in self:
            rec.write({'state': 'in_progress'})

    @api.multi
    def button_dispatch(self):
        for rec in self:
            rec.write({'state': 'dispatched'})

    @api.multi
    def button_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})