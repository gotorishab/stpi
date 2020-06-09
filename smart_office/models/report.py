from odoo import fields,api,models
import math
from datetime import datetime, timedelta, date
from pytz import timezone, UTC
from dateutil.relativedelta import relativedelta


class FileTracker(models.Model):
    _name="file.tracker.report"
    _description="File Tracking Report"


    name = fields.Char(string='Name')
    number = fields.Char(string='Number')
    type = fields.Char(string='Type')
    created_by = fields.Char(string='Created By')
    create_date = fields.Char(string='Create Date')
    assigned_by = fields.Char(string='Assigned By')
    assigned_date = fields.Char(string='Assigned Date')
    closed_by = fields.Char(string='Closed By')
    close_date = fields.Char(string='Closed Date')
    repoen_by = fields.Char(string='Reopen By')
    repoen_date = fields.Char(string='Reopen Date')
    forwarded_by = fields.Char(string='Forwarded By (User)')
    forwarded_by_dept = fields.Char(string='Forwarded By (Department)')
    forwarded_by_jobpos = fields.Char(string='Forwarded By(User Job Position)')
    forwarded_by_branch = fields.Char(string='Forwarded By(Branch)')
    forwarded_date = fields.Date(string='Forwarded Date')
    forwarded_to_user = fields.Char(string='Forwarded To (User)')
    forwarded_to_dept = fields.Char(string='Forwarded To (Department)')
    job_pos = fields.Char(string='Forwarded to(User Job Position)')
    forwarded_to_branch = fields.Char(string='Forwarded To(Branch)')
    remarks = fields.Char(string='Remarks')
    details = fields.Char(string='Details')
    action_taken = fields.Selection([('correspondence_created', 'Correspondence Created'),
                               ('file_created', 'File Creates'),
                               ('correspondence_forwarded', 'Correspondence Forwarded'),
                               ('file_forwarded', 'File Forwarded'),
                               ('assigned_to_file', 'Assigned To File'),
                               ('file_closed', 'File Closed'),
                               ('file_repoened', 'File Reopened')
                               ], string='Action Taken')