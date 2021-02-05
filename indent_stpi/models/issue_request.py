from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
import jwt
import xmlrpc.client
from odoo import modules
import base64

class IndentLedger(models.Model):
    _name = 'issue.request'
    _description = "Issue Request"
    #
    # @api.multi
    # def _default_issue_type(self):
    #     for rec in self:
    #         ab = []
    #         if rec.indent_type == 'grn':
    #             return [('grn', '!=', True), ('issue', '!=', True)]
    #         else:
    #             return [('issue', '!=', True),('grn', '=', True)]

    # @api.onchange('serial_number')
    # def change_slect_leave(self):
    #     for rec in self:
    #         if rec.indent_type == 'grn':
    #             return {'domain':
    #                         {
    #                             'serial_number': [('grn', '!=', True),('issue', '!=', True)],
    #                                }}
    #         if rec.indent_type == 'issue':
    #             return {'domain':
    #                         {
    #                             'serial_number': [('issue', '!=', True),('grn', '=', True)],
    #                                }}



    Indent_id = fields.Many2one('indent.request', string='Indent/GRN')
    Indent_item_id = fields.Many2one('indent.request.items', string='Indent Item')
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    branch_id = fields.Many2one('res.branch', string='Branch', store=True)
    item_category_id = fields.Many2one('indent.stock', string='Item Category')
    item_id = fields.Many2one('child.indent.stock', string='Item')
    specification = fields.Text('Specifications')
    serial_bool = fields.Boolean(string='Serial Number')
    # serial_number = fields.Char(string='Serial Number')
    serial_number = fields.Many2one('indent.serialnumber',string='Serial Number')
    asset = fields.Boolean('is Asset?')
    requested_quantity = fields.Integer('Requested Quantity')
    approved_quantity = fields.Integer('Approved Quantity')
    requested_date = fields.Date('Requested Date')
    approved_date = fields.Date('Approved Date', default=fields.Date.today())
    coe_asset_id = fields.Char('Asset id')
    document = fields.Binary('Document')


    indent_type = fields.Selection([('issue', 'Issue'), ('grn', 'GRN')
                               ],track_visibility='always', string='Type')

    indent_state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], string='Indent Status')

    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve_proceed', 'To Approve 1'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], string='Status')

    @api.multi
    def proceed_further(self):
        for res in self:
            res.write({'state': 'to_approve'})

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
                    res.serial_number.issue = True
                    balance = sum - qty
                    res.item_id.issue += qty
                else:
                    res.serial_number.grn = True
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
                        'serial_number': res.serial_number.name,
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

    def onchange_indent_state(self):
        group_id = self.env.ref('indent_stpi.group_issue_request_manager')
        resUsers = self.env['res.users'].sudo().search([]).filtered(
            lambda r: group_id.id in r.groups_id.ids and self.branch_id.id in r.branch_ids.ids).mapped('partner_id')
        if resUsers:
            employee_partner = self.employee_id.user_id.partner_id
            if employee_partner:
                resUsers += employee_partner
            message = "%s is move to %s" % (self.name, dict(self._fields['state'].selection).get(self.state))
            self.env['mail.message'].create({'message_type': "notification",
                                             "subtype_id": self.env.ref("mail.mt_comment").id,
                                             'body': message,
                                             'subject': "Invent request",
                                             'needaction_partner_ids': [(4, p.id, None) for p in resUsers],
                                             'model': self._name,
                                             'res_id': self.id,
                                             })
            self.env['mail.thread'].message_post(
                body=message,
                partner_ids=[(4, p.id, None) for p in resUsers],
                subtype='mail.mt_comment',
                notif_layout='mail.mail_notification_light',
            )

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})

    @api.multi
    def fill_asset_details(self):
        if not self.coe_asset_id:
            server_connection_id = self.env['server.connection'].search([('active', '=', True)])
            url = server_connection_id.url
            db = server_connection_id.db_name
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            # print('==========models================', models)
            uid = 2
            # password = self.env.user.password
            password = 'admin'
            id = models.execute_kw(db, uid, password, 'account.asset.asset', 'create',
                                   [{"name": self.item_id.name,
                                     "serial_number": self.serial_number.name,
                                     "invoice_no": self.Indent_id.bill_no,
                                     "purchase_date": self.Indent_id.date_of_receive,
                                     # "first_depreciation_manual_date": self.Indent_id.date_of_receive,
                                     "code": str(str(self.Indent_id.vendor_info) + ' - ' + str(self.specification)),
                                     "salvage_value": 1,
                                     "category_id": 1,
                                     "value": 1,
                                     'login': self.env.user.login}])
            # print('==========asset_data================', id)
            self.coe_asset_id = id
            asset_id = id
        else:
            asset_id = self.coe_asset_id
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

    def button_barcode(self):
        return {
                    'name'      : _('Barcode'),
                    'type'      : 'ir.actions.act_window',
                    'res_model' : 'barcode.barcode',
                    'view_mode' : 'form',
                    'target'    : 'new'
                }

class Barcode(models.TransientModel):
    _name = 'barcode.barcode'

    def get_default_img():
        with open(modules.get_module_resource('indent_stpi', 'static/img', 'img1.png'),
              'rb') as f:
            return base64.b64encode(f.read())

    image_data = fields.Binary("Barcode", default=get_default_img())