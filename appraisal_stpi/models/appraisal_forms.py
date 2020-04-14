from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta

class AppraisalForms(models.Model):
    _name = 'appraisal.main'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Appraisal'


    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    employee_id = fields.Many2one('hr.employee', string='Requested By', default=_default_employee, track_visibility='always')
    appraisal_sequence = fields.Char(string='Appraisal Sequence')
    abap_period = fields.Many2one('date.range', string='ABAP Period')
    branch_id = fields.Many2one('res.branch', string='Branch', compute='get_basic_details')
    category_id = fields.Many2one('employee.category', string='Category', compute='get_basic_details')
    dob = fields.Date(string='Date of Birth', compute='get_basic_details')
    job_id = fields.Many2one('hr.job', string='Functional Designation', compute='get_basic_details')
    struct_id = fields.Many2one('hr.payroll.structure', string='Salary Structure', compute='get_basic_details')
    pay_level_id = fields.Many2one('hr.payslip.paylevel', string='Pay Level', compute='get_basic_details')
    pay_level = fields.Many2one('payslip.pay.level', string='Pay Band', compute='get_basic_details')
    template_id = fields.Many2one('appraisal.template')
    duties_description = fields.Text(string='Duties Description')
    targets = fields.Text(string='Targets')
    achievement = fields.Text(string='achievement')
    sortfalls = fields.Text(string='Short Falls')
    immovatable_property = fields.Text(string='immovatable_property')
    kpia_ids = fields.One2many('appraisal.kpi','kpia_id', string='KPIA IDS')
    state = fields.Selection([('draft', 'Draft'), ('self_review', 'Self Reviewed'), ('line_manager_review', 'Line Manager Reviewed'),
                              ('hod_review', 'HOD Reviewed'), ('completed', 'Completed'), ('rejected', 'Rejected')
                              ], required=True, default='draft', track_visibility='always', string='Status')


    @api.multi
    @api.depends('employee_id')
    def get_basic_details(self):
        for rec in self:
            rec.category_id = rec.employee_id.category.id
            rec.dob = rec.employee_id.birthday
            rec.job_id = rec.employee_id.job_id.id
            rec.branch_id = rec.employee_id.branch_id.id
            emp_contract = self.env['hr.contract'].search([('employee_id', '=', rec.employee_id.id), ('state', '=', 'open')], limit=1)
            rec.struct_id = emp_contract.struct_id.id
            rec.pay_level_id = emp_contract.pay_level_id.id
            rec.pay_level = emp_contract.pay_level.id

    @api.onchange('template_id')
    @api.constrains('template_id')
    def get_template_details_details(self,working_list=None):
        for rec in self:
            kpi_kpa = []
            for i in rec.template_id.kpi_kpa_ids:
                kpi_kpa.append((0, 0, {
                    'kpia_id': rec.id,
                    'kpi': i.kpi,
                    'kra': i.kra,
                }))
            else:
                rec.kpia_ids = working_list
            rec.kpia_ids = kpi_kpa


    @api.model
    def create(self, vals):
        res =super(AppraisalForms, self).create(vals)
        sequence = ''
        seq = self.env['ir.sequence'].next_by_code('appraisal.main')
        sequence = str(res.employee_id.name) + ' - Appraisal - ' + str(seq)
        res.appraisal_sequence = sequence
        return res

    @api.multi
    @api.depends('appraisal_sequence')
    def name_get(self):
        res = []
        for record in self:
            if record.appraisal_sequence:
                name = record.appraisal_sequence
            else:
                name = 'Appraisal'
            res.append((record.id, name))
        return res

    @api.multi
    def button_self_reviewed(self):
        for rec in self:
            rec.write({'state': 'self_review'})

    @api.multi
    def button_line_manager_reviewed(self):
        for rec in self:
            rec.write({'state': 'line_manager_review'})

    @api.multi
    def button_hod_reviewed(self):
        for rec in self:
            rec.write({'state': 'hod_review'})

    @api.multi
    def button_completed(self):
        for rec in self:
            rec.write({'state': 'completed'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})


class KPIForm(models.Model):
    _name = 'appraisal.kpi'
    _description = 'KPI Forms'

    kpia_id = fields.Many2one('appraisal.main', string='KPIA IDS')
    kpi = fields.Char('KPI')
    kra = fields.Char('KRA')
    reporting_auth = fields.Selection([('1', '1'),
                                   ('2', '2'),
                                   ('3', '3'),
                                   ('4', '4'),
                                   ('5', '5'),
                                   ('6', '6'),
                                   ('7', '7'),
                                   ('8', '8'),
                                   ('9', '9'),
                                   ('10', '10'),
                                       ], 'Reporting Authority')
    reviewing_auth = fields.Selection([('1', '1'),
                                   ('2', '2'),
                                   ('3', '3'),
                                   ('4', '4'),
                                   ('5', '5'),
                                   ('6', '6'),
                                   ('7', '7'),
                                   ('8', '8'),
                                   ('9', '9'),
                                   ('10', '10'),], 'Reviewing Authority')
    reviewing_auth_user = fields.Many2one('res.users')



    @api.onchange('reviewing_auth')
    @api.constrains('reviewing_auth')
    def get_user_name(self):
        for rec in self:
            rec.reviewing_auth_user = rec.env.uid
