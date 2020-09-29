from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date

class EmployeeIndentAdvance(models.Model):
    _name = 'indent.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description='Indent Request'

    def _default_employee(self):
        return self.env['hr.employee'].sudo().search([('user_id', '=', self.env.uid)], limit=1)

    indent_sequence = fields.Char('Indent number',track_visibility='always')
    employee_id = fields.Many2one('hr.employee', string='Requested By', default=_default_employee,track_visibility='always')
    branch_id = fields.Many2one('res.branch', string='Branch', store=True)
    job_id = fields.Many2one('hr.job', string='Functional Designation', store=True)
    department_id = fields.Many2one('hr.department', string='Department', store=True)
   
    item_ids = fields.One2many('indent.request.items','request_id', string='Relatives')
   
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
        seq = self.env['ir.sequence'].next_by_code('indent.request')
        sequence = 'IR' + seq
        res.indent_sequence = sequence
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
    _description = "Indent Family Details"


    @api.onchange('item_category_id')
    def change_item_category_id(self):
        return {'domain': {'item_id': [('child_indent_stock', '=', self.item_category_id.id)
            ]}}

    request_id = fields.Many2one('indent.request', string='Relative ID')
    item_category_id = fields.Many2one('indent.stock', string='Item Category')
    item_id = fields.Many2one('child.indent.stock', string='Item')
    specification = fields.Text('Specifications')
    requested_quantity = fields.Integer('Requested Quantity')
    approved_quantity = fields.Integer('Approved Quantity')
    requested_date = fields.Integer('Requested Date')
    approved_date = fields.Integer('Approved Date')


