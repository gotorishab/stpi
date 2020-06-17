from odoo import fields, models, api, _
from datetime import datetime, date, timedelta
import requests
import json
from odoo.exceptions import UserError

class DispatchDocument(models.Model):
    _name = 'dispatch.document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Dispatch Document'


    cooespondence_ids = fields.Many2many('muk_dms.file', string='Correspondence')
    current_user_id = fields.Many2one('res.users')
    branch_id = fields.Many2one('res.branch', 'Branch')
    department_id = fields.Many2one('hr.department', 'Department')
    job_id = fields.Many2one('hr.job', 'Job Position')
    created_on = fields.Date(string='Date', default = fields.Date.today())
    select_template = fields.Many2one('select.template.html')
    template_html = fields.Html('Template')
    version = fields.Char('Version')
    previousversion = fields.Char('Previous Version')
    folder_id = fields.Many2one('folder.master', string="File")
    state = fields.Selection(
        [('draft', 'Draft'), ('in_progress', 'In Progress'), ('dispatched', 'Dispatched')
         ], required=True, default='draft', string='Status', track_visibility='always')