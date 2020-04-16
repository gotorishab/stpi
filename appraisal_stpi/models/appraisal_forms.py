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
    appraisal_sequence = fields.Char(string='Appraisal Sequence', track_visibility='always')
    abap_period = fields.Many2one('date.range', string='APAR Period', track_visibility='always')
    branch_id = fields.Many2one('res.branch', string='Branch', compute='get_basic_details', store=True, track_visibility='always')
    category_id = fields.Many2one('employee.category', string='Category', compute='get_basic_details', track_visibility='always')
    dob = fields.Date(string='Date of Birth', compute='get_basic_details', track_visibility='always')
    job_id = fields.Many2one('hr.job', string='Functional Designation', compute='get_basic_details', track_visibility='always')
    struct_id = fields.Many2one('hr.payroll.structure', string='Salary Structure', compute='get_basic_details', track_visibility='always')
    pay_level_id = fields.Many2one('hr.payslip.paylevel', string='Pay Level', compute='get_basic_details', track_visibility='always')
    pay_level = fields.Many2one('payslip.pay.level', string='Pay Band', compute='get_basic_details', track_visibility='always')
    template_id = fields.Many2one('appraisal.template', track_visibility='always', compute='get_basic_details')
    duties_description = fields.Text(string='Duties Description', track_visibility='always')
    targets = fields.Text(string='Targets', track_visibility='always')
    achievement = fields.Text(string='achievement', track_visibility='always')
    sortfalls = fields.Text(string='Short Falls', track_visibility='always')
    immovatable_property = fields.Text(string='immovatable_property', track_visibility='always')
    comment_oa = fields.Text('Comment', track_visibility='always')
    train_gen = fields.Text('Training', track_visibility='always')
    soh = fields.Text('State of Health', track_visibility='always')
    inte_general = fields.Text('Integrity', track_visibility='always')
    pen_picture = fields.Text('Pen Picture', track_visibility='always')
    len_rev = fields.Text('Length Review', track_visibility='always')
    ag_no = fields.Selection([('yes', 'Yes'),
                                       ('no', 'No'),
                              ], 'Ag No', track_visibility='always')
    dis_mod = fields.Text('Dis Mod', track_visibility='always')
    pen_pic_rev = fields.Text('Pen Picture of review officer', track_visibility='always')
    overall_rate_num = fields.Integer('Overall Rate', compute='compue_overal_rate', track_visibility='always')
    overall_grade = fields.Char('Grade', compute='compue_overal_rate', track_visibility='always')
    kpia_ids = fields.One2many('appraisal.kpi','kpia_id', string='KPIA IDS', track_visibility='always')
    app_ids = fields.One2many('targets.achievement','app_id', string='Targets/Achievement', track_visibility='always')
    state = fields.Selection([('draft', 'Draft'), ('self_review', 'Self Reviewed'), ('line_manager_review', 'Line Manager Reviewed'),
                              ('hod_review', 'HOD Reviewed'), ('completed', 'Completed'), ('rejected', 'Rejected')
                              ], required=True, default='draft', track_visibility='always', string='Status')


    @api.depends('kpia_ids')
    def compue_overal_rate(self):
        for rec in self:
            for line in rec.kpia_ids:
                avg = (int(line.reporting_auth) + int(line.reviewing_auth))/2
                rec.overall_rate_num = 5
            over_rate = self.env['overall.rate'].search([('from_int', '<=', rec.overall_rate_num), ('to_int', '>=', rec.overall_rate_num)], limit=1)
            rec.overall_grade = over_rate.name


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
            rec.template_id = emp_contract.pay_level_id.template_id.id
            rec.pay_level = emp_contract.pay_level.id
            # kpi_kpa = []
            # for i in rec.template_id.kpi_kpa_ids:
            #     kpi_kpa.append((0, 0, {
            #         'kpia_id': rec.id,
            #         'kpi': i.kpi,
            #         'kra': i.kra,
            #     }))
            # rec.kpia_ids = kpi_kpa

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



class TargetsAchievement(models.Model):
    _name = 'targets.achievement'
    _description = 'Achievements'

    app_id = fields.Many2one('appraisal.main', string='Appraisal ID')
    targets = fields.Char('Targets')
    achievements = fields.Char('Achievements')



class HrPaySlip(models.Model):
    _inherit='hr.payslip.paylevel'

    template_id = fields.Many2one('appraisal.template')
