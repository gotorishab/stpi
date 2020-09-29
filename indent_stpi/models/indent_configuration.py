from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date

class BlockYear(models.Model):
    _name = 'indent.stock'
    _description = "Indent Stock"

    name = fields.Char('Name')
    branch_id = fields.Many2one('res.branch', string='Branch', store=True)
    child_indent_stocks = fields.One2many('child.indent.stock', 'child_indent_stock', string='Availing Indent for year Ids')

    @api.model
    def create(self, vals):
        res =super(BlockYear, self).create(vals)
        search_id = self.env['indent.stock'].sudo().search([('id','!=',res.id)])
        for emp in search_id:
            if (emp.date_start <= res.date_start <= emp.date_end) or (emp.date_start <= res.date_end <= emp.date_end):
                raise ValidationError(_('Indent Stock already created of this date. Please correct the date. Already created is {name}').format(name=emp.name))
        return res



class ChildBlockYear(models.Model):
    _name = 'child.indent.stock'
    _description = " Availing Indent for year"

    name = fields.Char('Name')
    specification = fields.Text('Specifications')
    opening_quantity = fields.Integer('Opening Quantity')
    remaining_quantity = fields.Integer('Remaining Quantity')
    child_indent_stock = fields.Many2one('indent.stock', string='Indent Stock')

