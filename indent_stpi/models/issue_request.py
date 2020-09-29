from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date



class IndentLedger(models.Model):
    _name = 'issue.request'
    _description = "Issue Request"

    Indent_id = fields.Many2one('indent.request', string='Indent')
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    branch_id = fields.Many2one('res.branch', string='Branch', store=True)
    item_category_id = fields.Many2one('indent.stock', string='Item Category')
    item_id = fields.Many2one('child.indent.stock', string='Item')
    specification = fields.Text('Specifications')
    requested_quantity = fields.Integer('Requested Quantity')
    requested_date = fields.Integer('Requested Date')
    #
    # relative_name = fields.Char(string='Relative Name')
    # relation = fields.Char(string='Relative')
    # block_year = fields.Many2one('indent.stock', string='Indent Stock')
    # child_block_year=fields.Many2one('child.indent.stock', 'Availing Indent for year')
    # Indent_date = fields.Date(string='Indent Date')
    # place_of_trvel=fields.Selection([('hometown', 'Hometown'), ('india', 'Anywhere in India'), ('conversion', 'Conversion of Hometown')], default='hometown', string='Indent Type')

    indent_state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], string='Indent Status')

    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], string='Status')

