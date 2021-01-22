from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date

class SerialNumber(models.Model):
    _name = 'indent.serialnumber'
    _description = "Indent Serial number"

    name = fields.Char('Serial Number')
    grn = fields.Boolean('GRN')
    issue = fields.Boolean('Issue')
    branch_id = fields.Many2one('res.branch', string='Branch', store=True)
    item_category_id = fields.Many2one('indent.stock', string='Item Category')
    item_id = fields.Many2one('child.indent.stock', string='Item')


    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], string='Status', default='draft')


    @api.multi
    def send_for_approval(self):
        for res in self:
            res.write({'state': 'to_approve'})


    @api.multi
    def button_approved(self):
        for res in self:
            res.write({'state': 'approved'})


    @api.multi
    def button_reject(self):
        for res in self:
            res.write({'state': 'rejected'})

    @api.multi
    def button_send_back(self):
        for res in self:
            res.write({'state': 'draft'})


class ItemMaster(models.Model):
    _name = 'indent.stock'
    _description = "Item Master"


    def _default_branch_id(self):
        emp = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.uid)], limit=1)
        return emp.branch_id.id


    name = fields.Char('Name')
    branch_id = fields.Many2one('res.branch', string='Branch', default=_default_branch_id, store=True)
    child_indent_stocks = fields.One2many('child.indent.stock', 'child_indent_stock', string='Availing Indent for year Ids')




    @api.multi
    def unlink(self):
        for rec in self:
            for line in rec.child_indent_stocks:
                line.sudo().unlink()
        return super(ItemMaster, self).unlink()


class ChildIndentStock(models.Model):
    _name = 'child.indent.stock'
    _description = " Availing Indent for year"


    def _default_branch_id(self):
        emp = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.uid)], limit=1)
        return emp.branch_id.id

    name = fields.Char('Name')
    specification = fields.Text('Specifications')
    branch_id = fields.Many2one('res.branch', string='Branch', default=_default_branch_id, store=True)
    asset = fields.Boolean('is Asset?')
    child_indent_stock = fields.Many2one('indent.stock', string='Item Master')
    serial_bool = fields.Boolean(string='Serial Number')
    issue = fields.Integer('Issue')
    received = fields.Integer('Received')
    balance = fields.Integer('Balance')