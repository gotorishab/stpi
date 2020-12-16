from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
import jwt
import xmlrpc.client



class IndentLedger(models.Model):
    _name = 'issue.request'
    _description = "Issue Request"

    Indent_id = fields.Many2one('indent.request', string='Indent/GRN')
    Indent_item_id = fields.Many2one('indent.request.items', string='Indent Item')
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    branch_id = fields.Many2one('res.branch', string='Branch', store=True)
    item_category_id = fields.Many2one('indent.stock', string='Item Category')
    item_id = fields.Many2one('child.indent.stock', string='Item')
    specification = fields.Text('Specifications')
    serial_bool = fields.Boolean(string='Serial Number')
    serial_number = fields.Char(string='Serial Number')
    asset = fields.Boolean('is Asset?')
    requested_quantity = fields.Integer('Requested Quantity')
    approved_quantity = fields.Integer('Approved Quantity')
    requested_date = fields.Date('Requested Date')
    approved_date = fields.Date('Approved Date', default=fields.Date.today())
    coe_asset_id = fields.Char('Asset id')


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
            # sbook = self.env['stock.log.book'].sudo().search([('branch_id', '=', res.branch_id.id),('item_id', '=', res.item_id.id)])
            sum = 0
            sum = res.item_id.balance
            if int(sum) < int(res.approved_quantity) and res.indent_type == 'issue':
                raise ValidationError(_("Required quantity not in stock"))
                # raise ValidationError(_("You are not able to approve more than {qty} {item_id}, as stock balance is {qty}".format(qty=sum, item_id=res.item_id.name)))
            else:
                qty = res.approved_quantity
                if res.indent_type == 'issue':
                    balance = sum - qty
                    res.item_id.issue += qty
                else:
                    balance = sum + qty
                    res.item_id.received += qty
                res.item_id.balance = res.item_id.received - res.item_id.issue
                # res.item_id.serial_number = res.serial_number
                create_service_log_book = self.env['stock.log.book'].sudo().create(
                    {
                        'employee_id': res.employee_id.id,
                        'branch_id': res.branch_id.id,
                        'Indent_id': res.Indent_id.id,
                        'Indent_item_id': res.Indent_item_id.id,
                        'item_category_id': res.item_category_id.id,
                        'item_id': res.item_id.id,
                        'serial_bool': res.serial_bool,
                        'serial_number': res.serial_number,
                        'specification': res.specification,
                        'requested_quantity': res.requested_quantity,
                        'requested_date': res.requested_date,
                        'approved_quantity': res.approved_quantity,
                        'indent_type': res.indent_type,
                        'opening': sum,
                        'quantity': qty,
                        'balance': balance
                    }
                )
                search_id = self.env['indent.request.items'].sudo().search([('id', '=', res.Indent_item_id.id)],limit=1)
                for sr in search_id:
                    sr.write({
                        'issue_approved': True,
                        'approved_quantity': res.approved_quantity,
                        'approved_date': res.approved_date
                    })
                res.write({'state': 'approved'})


    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})


    @api.multi
    def fill_asset_details(self):
        server_connection_id = self.env['server.connection'].search([('active', '=', True)])
        url = server_connection_id.url
        db = server_connection_id.db_name
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        print('==========models================', models)
        uid = self.env.user.id
        password = self.env.user.password
        id = models.execute_kw(db, uid, password, 'account.asset.asset', 'create', [{"name": self.item_id.name,"serial_number": self.serial_number,"category_id":1,"value":1}])
        print('==========asset_data================', id)
        self.coe_asset_id = id
        asset_id = id
        key = ",jy`\;4Xpe7%KKL$.VNJ'.s6)wErQa"
        connection_rec = self.env['server.connection'].search([], limit=1)
        if not connection_rec:
            raise UserError(_('No Server Configuration Found !'))
        encoded_jwt = jwt.encode({'token': self.env.user.token}, key)
        action = {
            'name': connection_rec.name,
            'type': 'ir.actions.act_url',
            'url': str(connection_rec.url).strip() + "/asset/indent?login=" + str(
                self.env.user.login) + "&password=" + str(encoded_jwt.decode("utf-8")) + "&menu_id=" + str(asset_id),
            'target': 'new',
        }
        return action