from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date

class GrnNumber(models.Model):
    _name = 'grn.seqid'
    _description = "GRN Seqid"

class EmployeeIndentAdvance(models.Model):
    _name = 'indent.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description='Indent Request'

    def _default_employee(self):
        return self.env['hr.employee'].sudo().search([('user_id', '=', self.env.uid)], limit=1)

    indent_sequence = fields.Char('Number',track_visibility='always')

    vendor_info = fields.Text('Vendor Information',track_visibility='always')
    bill_no = fields.Char('Bill Number',track_visibility='always')
    amount = fields.Float('Amount',track_visibility='always')
    received_by = fields.Many2one('hr.employee','Received By',track_visibility='always')
    item_checked_by = fields.Char('Item Checked By',track_visibility='always')
    date_of_receive = fields.Date('Date of Receive',track_visibility='always')

    employee_id = fields.Many2one('hr.employee', string='Employee', default=_default_employee ,track_visibility='always')
    branch_id = fields.Many2one('res.branch', string='Branch', store=True)
    job_id = fields.Many2one('hr.job', string='Functional Designation', store=True)
    department_id = fields.Many2one('hr.department', string='Department', store=True)
    requested_date = fields.Date('Date', default=fields.Date.today())
    item_ids = fields.One2many('indent.request.items','request_id', string='Items')
    indent_type = fields.Selection([('issue', 'Issue'), ('grn', 'GRN')
                               ],track_visibility='always', string='Type')

    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
                               ], required=True, default='draft',track_visibility='always', string='Status')


    @api.onchange('employee_id')
    @api.constrains('employee_id')
    def onchange_emp_get_base(self):
        for rec in self:
            rec.job_id = rec.employee_id.job_id.id
            rec.department_id = rec.employee_id.department_id.id
            rec.branch_id = rec.employee_id.branch_id.id

    @api.multi
    def button_to_approve(self):
        for res in self:
            res.write({'state': 'to_approve'})
          
          
    @api.multi
    def button_approved(self):
        for res in self:
            res.write({'state': 'approved'})
            for item in res.item_ids:
                if not item.item_id.serial_bool:
                    create_ledger_family = self.env['issue.request'].sudo().create(
                        {
                            'Indent_id': res.id,
                            'employee_id': res.employee_id.id,
                            'branch_id': res.branch_id.id,
                            'Indent_item_id': item.id,
                            'item_category_id': item.item_category_id.id,
                            'item_id': item.item_id.id,
                            'serial_bool': item.item_id.serial_bool,
                            'asset': item.item_id.asset,
                            'specification': item.specification,
                            'requested_quantity': item.requested_quantity,
                            'approved_quantity': item.requested_quantity,
                            'requested_date': item.requested_date,
                            'indent_state': res.state,
                            'indent_type': res.indent_type,
                            'state': 'to_approve',
                        }
                    )
                else:
                    n = item.requested_quantity
                    for i in range(n):
                        create_ledger_family = self.env['issue.request'].sudo().create(
                            {
                                'Indent_id': res.id,
                                'employee_id': res.employee_id.id,
                                'branch_id': res.branch_id.id,
                                'Indent_item_id'
                                : item.id,
                                'item_category_id': item.item_category_id.id,
                                'item_id': item.item_id.id,
                                'serial_bool': item.item_id.serial_bool,
                                'asset': item.item_id.asset,
                                'specification': item.specification,
                                'requested_quantity': 1,
                                'approved_quantity': 1,
                                'requested_date': item.requested_date,
                                'indent_state': res.state,
                                'indent_type': res.indent_type,
                                'state': 'to_approve',
                            }
                        )



    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})

    @api.multi
    def button_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    @api.model
    def create(self, vals):
        res =super(EmployeeIndentAdvance, self).create(vals)
        if res.indent_type == 'issue':
            seq = self.env['ir.sequence'].next_by_code('indent.request')
            sequence = 'IR' + str(seq)
        else:
            seq = self.env['ir.sequence'].next_by_code('grn.seqid')
            sequence = 'GRN' + str(seq)
        res.indent_sequence = sequence

        search_id = self.env['indent.request'].sudo().search(
            [('employee_id', '=', res.employee_id.id),
             ('state', 'not in', ['approved','rejected']), ('id', '!=', res.id)])
        for emp in search_id:
            if emp:
                raise ValidationError(
                    "One of the Indent Request is already in process.")
        return res

    @api.multi
    @api.depends('indent_sequence')
    def name_get(self):
        res = []
        for record in self:
            if record.indent_sequence:
                name = record.indent_sequence
            else:
                name = 'IR'
            res.append((record.id, name))
        return res



class FamilyDetails(models.Model):
    _name = 'indent.request.items'
    _description = "Indent Item Details"


    # @api.onchange('item_category_id')
    # def change_item_category_id(self):
    #     return {'domain': {'item_id': [('child_indent_stock', '=', self.item_category_id.id)
    #         ]}}

    request_id = fields.Many2one('indent.request', string='Item ID')
    item_category_id = fields.Many2one('indent.stock', string='Item Category')
    item_id = fields.Many2one('child.indent.stock', string='Item')
    specification = fields.Text('Specifications')
    requested_quantity = fields.Integer('Qty.')
    approved_quantity = fields.Integer('Approved Qty.')
    issue_approved = fields.Boolean('Issue approved')
    requested_date = fields.Date('Required Date', default=fields.Date.today())
    approved_date = fields.Date('Approved Date')
    indent_type = fields.Selection([('issue', 'Issue'), ('grn', 'GRN')
                               ],track_visibility='always', string='Type', related="request_id.indent_type")


    @api.onchange('item_id')
    # @api.constrains('item_id')
    def change_item_category_id(self):
        for rec in self:
            rec.specification = rec.item_id.specification