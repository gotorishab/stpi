from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date

class IndentStock(models.Model):
    _name = 'indent.stock'
    _description = "Indent Stock"

    name = fields.Char('Name')
    branch_id = fields.Many2one('res.branch', string='Branch', store=True)
    child_indent_stocks = fields.One2many('child.indent.stock', 'child_indent_stock', string='Availing Indent for year Ids')




class ChildIndentStock(models.Model):
    _name = 'child.indent.stock'
    _description = " Availing Indent for year"

    name = fields.Char('Name')
    specification = fields.Text('Specifications')
    opening_quantity = fields.Integer('Opening Quantity')
    remaining_quantity = fields.Integer('Remaining Quantity')
    child_indent_stock = fields.Many2one('indent.stock', string='Indent Stock')

