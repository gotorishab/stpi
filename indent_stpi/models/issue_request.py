from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date



class IndentLedger(models.Model):
    _name = 'issue.request'
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


    indent_type = fields.Selection([('issue', 'Issue'), ('grn', 'GRN')
                               ],track_visibility='always', string='Type')

    indent_state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], string='Indent Status')

    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], string='Status')

    @api.multi
    def button_approved(self):
        for res in self:
            if int(res.requested_quantity) < int(res.approved_quantity):
                raise ValidationError(_("You are not able to approve more than {qty} {item_id}, as requested quantity is {qty}".format(qty=res.requested_quantity, item_id=res.item_id.name)))
            sbook = self.env['stock.log.book'].sudo().search([('branch_id', '=', res.branch_id.id),('item_id', '=', res.item_id.id)])
            sum = 0
            for ln in sbook:
                sum += ln.balance
            qty = res.approved_quantity
            if res.indent_type == 'issue':
                balance = sum - qty
            else:
                balance = sum + qty
            create_service_log_book = self.env['stock.log.book'].sudo().create(
                {
                    'Indent_id': res.Indent_id.id,
                    'employee_id': res.employee_id.id,
                    'branch_id': res.branch_id.id,
                    'Indent_item_id': res.Indent_item_id.id,
                    'item_category_id': res.item_category_id.id,
                    'item_id': res.item_id.id,
                    'serial_bool': res.serial_bool,
                    'specification': res.specification,
                    'requested_quantity': res.requested_quantity,
                    'requested_date': res.requested_date,
                    'indent_type': res.indent_type,
                    'opening': sum,
                    'quantity': qty,
                    'balance': balance
                }
            )
            newsbook = self.env['stock.log.book'].sudo().search([('branch_id', '=', res.branch_id.id),('item_id', '=', res.item_id.id)])
            sum1 = 0
            for lin in newsbook:
                sum1 += lin.balance
            search_id = self.env['indent.request.items'].sudo().search([('id', '=', res.Indent_item_id.id)],limit=1)
            for sr in search_id:
                sr.write({
                    'approved_quantity': res.approved_quantity,
                    'approved_date': res.approved_date
                })
            res.write({'state': 'approved'})
            # else:
            #     raise ValidationError(_("You are not able to approve more than {qty} {item_id}".format(qty=res.item_id.remaining_quantity, item_id=res.item_id.name)))

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})
