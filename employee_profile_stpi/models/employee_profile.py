from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError,UserError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import re

class EmployeeProfile(models.Model):
    _name = "employee.profile"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Employee Profile"


    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)


    employee_id = fields.Many2one('hr.employee', string="Requested By", default=_default_employee,track_visibility='always')
    date = fields.Date(string='Requested Date', default=fields.Date.today())
    designation = fields.Many2one('hr.job', string="Designation")
    branch_id= fields.Many2one('res.branch', string="Branch")
    department = fields.Many2one('hr.department', string="Department")

    category = fields.Many2one('employee.category', string='Category', track_visibility='always')
    religion = fields.Many2one('employee.religion', string='Religion', track_visibility='always')
    minority = fields.Boolean('Minority', default=False, track_visibility='always')

    height = fields.Float('Height (in CMs)', track_visibility='always')
    weight = fields.Float('Weight (in KGs)', track_visibility='always')
    blood_group = fields.Selection([('a+', 'A+'),
                                    ('a-', 'A-'),
                                    ('b+', 'B+'),
                                    ('b-', 'B-'),
                                    ('o+', 'O+'),
                                    ('o-', 'O-'),
                                    ('ab+', 'AB+'),
                                    ('ab-', 'AB-')], string='Blood Group', track_visibility='always')
    differently_abled = fields.Selection([('no', 'No'),
                                          ('yes', 'Yes')], default='no', string='Differently Abled?',
                                         track_visibility='always')
    kind_of_disability = fields.Selection([('vh', 'No'),
                                           ('hh', 'Yes'),
                                           ('ph', 'Yes')], string='Kind of Disability',
                                          track_visibility='always')
    perc_disability = fields.Char('% of Disability', track_visibility='always')
    certificate_upload = fields.Binary('Upload certificate', track_visibility='always')
    personal_remark = fields.Char('Personal mark of Identification', track_visibility='always')
    identify_id = fields.Char(string='Identification No.', copy=False, store=True, track_visibility='always')
    pan_no = fields.Char('PAN Card No.', track_visibility='always')
    pan_upload = fields.Binary('Upload(PAN)', track_visibility='always')
    aadhar_no = fields.Char('Aadhar Card No.', track_visibility='always')
    aadhar_upload = fields.Binary('Upload(Aadhar)', track_visibility='always')
    passport_upload = fields.Binary('Upload(Passport)', track_visibility='always')
    bank_name = fields.Char(string='Bank Name')
    bank_account_number = fields.Char(string='Bank Account number')
    ifsc_code = fields.Char(string='IFSC Code')
    employee_type = fields.Selection([('regular', 'Regular Employee'),
                                      ('contractual_with_agency', 'Contractual with Agency'),
                                      ('contractual_with_stpi', 'Contractual with STPI')], string='Employment Type',
                                     track_visibility='always', store=True)

    recruitment_type = fields.Selection([
        ('d_recruitment', 'Direct Recruitment(DR)'),
        ('transfer', 'Transfer(Absorption)'),
        ('i_absorption', 'Immediate Absorption'),
        ('deputation', 'Deputation'),
        ('c_appointment', 'Compassionate Appointment'),
        ('promotion', 'Promotion'),
    ], 'Recruitment Type', track_visibility='always', store=True)

    salutation = fields.Many2one('res.partner.title', track_visibility='always')

    fax_number = fields.Char('FAX number', track_visibility='always')

    new_category = fields.Many2one('employee.category', string='Category', track_visibility='always')
    new_religion = fields.Many2one('employee.religion', string='Religion', track_visibility='always')
    new_minority = fields.Boolean('Minority', default=False, track_visibility='always')

    new_height = fields.Float('Height (in CMs)', track_visibility='always')
    new_weight = fields.Float('Weight (in KGs)', track_visibility='always')
    new_blood_group = fields.Selection([('a+', 'A+'),
                                    ('a-', 'A-'),
                                    ('b+', 'B+'),
                                    ('b-', 'B-'),
                                    ('o+', 'O+'),
                                    ('o-', 'O-'),
                                    ('ab+', 'AB+'),
                                    ('ab-', 'AB-')], string='Blood Group', track_visibility='always')
    new_differently_abled = fields.Selection([('no', 'No'),
                                          ('yes', 'Yes')], default='no', string='Differently Abled?',
                                         track_visibility='always')
    new_kind_of_disability = fields.Selection([('vh', 'No'),
                                           ('hh', 'Yes'),
                                           ('ph', 'Yes')], string='Kind of Disability',
                                          track_visibility='always')
    new_perc_disability = fields.Char('% of Disability', track_visibility='always')
    new_certificate_upload = fields.Binary('Upload certificate', track_visibility='always')
    new_personal_remark = fields.Char('Personal mark of Identification', track_visibility='always')
    new_identify_id = fields.Char(string='Identification No.', copy=False, store=True, track_visibility='always')
    new_pan_no = fields.Char('PAN Card No.', track_visibility='always')
    new_pan_upload = fields.Binary('Upload(PAN)', track_visibility='always')
    new_aadhar_no = fields.Char('Aadhar Card No.', track_visibility='always')
    new_aadhar_upload = fields.Binary('Upload(Aadhar)', track_visibility='always')
    new_passport_upload = fields.Binary('Upload(Passport)', track_visibility='always')
    new_bank_name = fields.Char(string='Bank Name')
    new_bank_account_number = fields.Char(string='Bank Account number')
    new_ifsc_code = fields.Char(string='IFSC Code')
    new_employee_type = fields.Selection([('regular', 'Regular Employee'),
                                      ('contractual_with_agency', 'Contractual with Agency'),
                                      ('contractual_with_stpi', 'Contractual with STPI')], string='Employment Type',
                                     track_visibility='always', store=True)
    new_recruitment_type = fields.Selection([
        ('d_recruitment', 'Direct Recruitment(DR)'),
        ('transfer', 'Transfer(Absorption)'),
        ('i_absorption', 'Immediate Absorption'),
        ('deputation', 'Deputation'),
        ('c_appointment', 'Compassionate Appointment'),
        ('promotion', 'Promotion'),
    ], 'Recruitment Type', track_visibility='always', store=True)

    new_salutation = fields.Many2one('res.partner.title', track_visibility='always')

    new_fax_number = fields.Char('FAX number', track_visibility='always')


    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approval', 'Waiting for Approval'), ('approved', 'Approved'), ('rejected', 'Rejected')
                               ], required=True, string='Status', default='draft',track_visibility='always')



    @api.onchange('employee_id')
    @api.constrains('employee_id')
    def onchange_emp_get_data(self):
        for rec in self:
            rec.designation = rec.employee_id.job_id.id
            rec.department = rec.employee_id.department_id.id
            rec.branch_id = rec.employee_id.branch_id.id
            rec.category = rec.employee_id.category.id
            rec.religion = rec.employee_id.religion.id
            rec.minority = rec.employee_id.minority
            rec.height = rec.employee_id.height
            rec.weight = rec.employee_id.weight
            rec.blood_group = rec.employee_id.blood_group
            rec.differently_abled = rec.employee_id.differently_abled
            rec.kind_of_disability = rec.employee_id.kind_of_disability
            rec.perc_disability = rec.employee_id.perc_disability
            rec.certificate_upload = rec.employee_id.certificate_upload
            rec.personal_remark = rec.employee_id.personal_remark
            rec.identify_id = rec.employee_id.identify_id
            rec.pan_no = rec.employee_id.pan_no
            rec.pan_upload = rec.employee_id.pan_upload
            rec.aadhar_no = rec.employee_id.aadhar_no
            rec.aadhar_upload = rec.employee_id.aadhar_upload
            rec.passport_upload = rec.employee_id.passport_upload
            rec.bank_name = rec.employee_id.bank_name
            rec.bank_account_number = rec.employee_id.bank_account_number
            rec.ifsc_code = rec.employee_id.ifsc_code
            rec.salutation = rec.employee_id.salutation.id
            rec.employee_type = rec.employee_id.employee_type
            rec.recruitment_type = rec.employee_id.recruitment_type
            rec.fax_number = rec.employee_id.fax_number

    @api.multi
    def button_approved(self):
        for rec in self:
            if rec.new_category:
                rec.employee_id.category = rec.new_category.id
            if rec.new_religion:
                rec.employee_id.religion = rec.new_religion.id
            if rec.new_minority:
                rec.employee_id.minority = rec.new_minority
            if rec.new_height:
                rec.employee_id.height = rec.new_height
            if rec.new_weight:
                rec.employee_id.weight = rec.new_weight
            if rec.new_blood_group:
                rec.employee_id.blood_group = rec.new_blood_group
            if rec.new_differently_abled:
                rec.employee_id.differently_abled = rec.new_differently_abled
            if rec.new_kind_of_disability:
                rec.employee_id.kind_of_disability = rec.new_kind_of_disability
            if rec.new_perc_disability:
                rec.employee_id.perc_disability = rec.new_perc_disability
            if rec.new_certificate_upload:
                rec.employee_id.certificate_upload = rec.new_certificate_upload
            if rec.new_personal_remark:
                rec.employee_id.personal_remark = rec.new_personal_remark
            if rec.new_pan_no:
                rec.employee_id.pan_no = rec.new_pan_no
            if rec.new_pan_upload:
                rec.employee_id.pan_upload = rec.new_pan_upload
            if rec.new_aadhar_no:
                rec.employee_id.aadhar_no = rec.new_aadhar_no
            if rec.new_aadhar_upload:
                rec.employee_id.aadhar_upload = rec.new_aadhar_upload
            if rec.new_passport_upload:
                rec.employee_id.passport_upload = rec.new_passport_upload
            if rec.new_bank_name:
                rec.employee_id.bank_name = rec.new_bank_name
            if rec.new_bank_account_number:
                rec.employee_id.bank_account_number = rec.new_bank_account_number
            if rec.new_ifsc_code:
                rec.employee_id.ifsc_code = rec.new_ifsc_code
            if rec.new_salutation:
                rec.employee_id.salutation = rec.new_salutation.id
            if rec.new_employee_type:
                rec.employee_id.employee_type = rec.new_employee_type
            if rec.new_recruitment_type:
                rec.employee_id.recruitment_type = rec.new_recruitment_type
            if rec.new_fax_number:
                rec.employee_id.fax_number = rec.new_fax_number
            rec.write({'state': 'approved'})