from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date



class IndentLedger(models.Model):
    _name = 'stock.log.book'
    _description = "Issue Request"

    Indent_id = fields.Many2one('indent.request', string='Indent')
    Indent_item_id = fields.Many2one('indent.request.items', string='Indent Item')
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    branch_id = fields.Many2one('res.branch', string='Branch', store=True)
    item_category_id = fields.Many2one('indent.stock', string='Item Category')
    item_id = fields.Many2one('child.indent.stock', string='Item')
    specification = fields.Text('Specifications')
    serial_bool = fields.Boolean(string='Serial Number')
    serial_number = fields.Char(string='Serial Number')
    requested_quantity = fields.Integer('Requested Quantity')
    approved_quantity = fields.Integer('Approved Quantity')
    requested_date = fields.Date('Requested Date')
    approved_date = fields.Date('Approved Date', default=fields.Date.today())
    issue = fields.Integer('Issue')
    received = fields.Integer('Received')
    balance = fields.Integer('Balance')


    indent_type = fields.Selection([('issue', 'Issue'), ('grn', 'GRN')
                               ],track_visibility='always', string='Type')

    indent_state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], string='Indent Status')

    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], string='Status')

