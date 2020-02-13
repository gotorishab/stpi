from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError,UserError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import re

class EmployeeProfile(models.Model):
    _name = "employee.profile"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Employee Profile"


    employee_id = fields.Many2one('hr.employee', string="Employee", store = True, track_visibility='onchange')
    date = fields.Date(string='Requested Date', default=fields.Date.today())
    designation = fields.Many2one('hr.job', string="Designation")
    branch_id= fields.Many2one('res.branch', string="Branch")
    department = fields.Many2one('hr.department', string="Department")
    address_ids = fields.One2many('employee.update.address', 'employee_update_profile', string='Address', track_visibility='always')
    address_current_ids = fields.One2many('employee.current.address', 'employee_current_profile', string='Current Address', track_visibility='always')

    resume_line_current_ids = fields.One2many('hr.resume.line.current', 'employee_current_profile', string="Resumé lines")
    employee_skill_current_ids = fields.One2many('hr.employee.skill.current', 'employee_current_profile', string="Skills")

    resume_line_ids = fields.One2many('hr.resume.line.update', 'employee_update_profile', string="Resumé lines")
    employee_skill_ids = fields.One2many('hr.employee.skill.update', 'employee_update_profile', string="Skills")





    category = fields.Many2one('employee.category', string='Category', track_visibility='always')
    religion = fields.Many2one('employee.religion', string='Religion', track_visibility='always')
    minority = fields.Boolean('Minority', default=False, track_visibility='always')

    emergency_contact = fields.Char("Emergency Contact")
    emergency_phone = fields.Char("Emergency Phone")
    phone = fields.Char('Phone (Home)', track_visibility='always')

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
    passport_id = fields.Char('Passport No')

    birthday = fields.Date('Date of Birth')
    place_of_birth = fields.Char('Place of Birth')
    country_of_birth = fields.Many2one('res.country', string="Country of Birth")

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

    new_emergency_contact = fields.Char("Emergency Contact")
    new_emergency_phone = fields.Char("Emergency Phone")
    new_phone = fields.Char('Phone (Home)', track_visibility='always')

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
    new_pan_no = fields.Char('PAN Card No.', track_visibility='always')
    new_pan_upload = fields.Binary('Upload(PAN)', track_visibility='always')
    new_aadhar_no = fields.Char('Aadhar Card No.', track_visibility='always')
    new_aadhar_upload = fields.Binary('Upload(Aadhar)', track_visibility='always')
    new_passport_upload = fields.Binary('Upload(Passport)', track_visibility='always')
    new_bank_name = fields.Char(string='Bank Name')
    new_bank_account_number = fields.Char(string='Bank Account number')
    new_ifsc_code = fields.Char(string='IFSC Code')
    new_passport_id = fields.Char(string='Passport No.')



    new_birthday = fields.Date('Date of Birth')
    new_place_of_birth = fields.Char('Place of Birth')
    new_country_of_birth = fields.Many2one('res.country', string="Country of Birth")


    new_salutation = fields.Many2one('res.partner.title', string='Salutation', track_visibility='always')

    new_fax_number = fields.Char('FAX number', track_visibility='always')

    @api.multi
    @api.depends('employee_id')
    def name_get(self):
        res = []
        name = ''
        for record in self:
            if record.employee_id:
                name = 'Employee Profile - ' + str(record.employee_id.name) + ' - Update'
            else:
                name = 'Employee Profile'
            res.append((record.id, name))
        return res

    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approval', 'Waiting for Approval'), ('approved', 'Approved'), ('rejected', 'Rejected')
                               ], required=True, string='Status', default='draft',track_visibility='always')


    @api.constrains('employee_id')
    @api.onchange('employee_id')
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
            rec.emergency_contact = rec.employee_id.emergency_contact
            rec.emergency_phone = rec.employee_id.emergency_phone
            rec.phone = rec.employee_id.phone
            rec.birthday = rec.employee_id.birthday
            rec.place_of_birth = rec.employee_id.place_of_birth
            rec.country_of_birth = rec.employee_id.country_of_birth.id
            rec.pan_no = rec.employee_id.pan_no
            rec.pan_upload = rec.employee_id.pan_upload
            rec.aadhar_no = rec.employee_id.aadhar_no
            rec.aadhar_upload = rec.employee_id.aadhar_upload
            rec.passport_id = rec.employee_id.passport_id
            rec.passport_upload = rec.employee_id.passport_upload
            rec.bank_name = rec.employee_id.bank_name
            rec.bank_account_number = rec.employee_id.bank_account_number
            rec.ifsc_code = rec.employee_id.ifsc_code
            rec.salutation = rec.employee_id.salutation.id
            rec.employee_type = rec.employee_id.employee_type
            rec.recruitment_type = rec.employee_id.recruitment_type
            rec.fax_number = rec.employee_id.fax_number
            address_current_ids = []
            rec.address_current_ids.unlink()
            for address in rec.employee_id.address_ids:
                address_current_ids.append((0, 0, {
                    'employee_current_profile': rec.id,
                    'employee_id': address.employee_id.id,
                    'address_type': address.address_type,
                    'state_id': address.state_id.id,
                    'country_id': address.country_id.id,
                    'street': address.street,
                    'street2': address.street2,
                    'zip': address.zip,
                    'is_correspondence_address': address.is_correspondence_address,
                    'city': address.city,
                }))
            rec.address_current_ids = address_current_ids
            resume_line_current_ids = []
            for address in rec.employee_id.resume_line_ids:
                resume_line_current_ids.append((0, 0, {
                    'employee_current_profile': rec.id,
                    'resume_employee_id': address.resume_employee_id.id,
                    'name': address.name,
                    'date_start': address.date_start,
                    'date_end': address.date_end,
                    'description': address.description,
                    'upload_qualification_proof': address.upload_qualification_proof,
                    'line_type_id': address.line_type_id.id,
                    'type_name': address.type_name,
                    'title': address.title.id,
                    'specialization': address.specialization,
                    'sequence': address.sequence,
                    'acquired': address.acquired,
                }))
            rec.resume_line_current_ids.unlink()
            rec.resume_line_current_ids = resume_line_current_ids
            employee_skill_current_ids = []
            for address in rec.employee_id.employee_skill_ids:
                employee_skill_current_ids.append((0, 0, {
                    'employee_current_profile': rec.id,
                    'employee_id': address.employee_id.id,
                    'skill_id': address.skill_id.id,
                    'skill_level_id': address.skill_level_id.id,
                    'skill_type_id': address.skill_type_id.id,
                    'level_progress': address.level_progress,
                }))
            rec.employee_skill_current_ids.unlink()
            rec.employee_skill_current_ids = employee_skill_current_ids


    @api.onchange('employee_id')
    def onchange_emp_temp_get_data(self):
        for rec in self:
            address_ids = []
            for address in rec.employee_id.address_ids:
                address_ids.append((0, 0, {
                    'employee_current_profile': rec.id,
                    'employee_id': address.employee_id.id,
                    'address_type': address.address_type,
                    'state_id': address.state_id.id,
                    'country_id': address.country_id.id,
                    'street': address.street,
                    'street2': address.street2,
                    'zip': address.zip,
                    'is_correspondence_address': address.is_correspondence_address,
                    'city': address.city,
                }))
            rec.address_ids.unlink()
            rec.address_ids = address_ids
            resume_line_ids = []
            for address in rec.employee_id.resume_line_ids:
                resume_line_ids.append((0, 0, {
                    'employee_current_profile': rec.id,
                    'resume_employee_id': address.resume_employee_id.id,
                    'name': address.name,
                    'date_start': address.date_start,
                    'date_end': address.date_end,
                    'description': address.description,
                    'upload_qualification_proof': address.upload_qualification_proof,
                    'line_type_id': address.line_type_id.id,
                    'type_name': address.type_name,
                    'title': address.title.id,
                    'specialization': address.specialization,
                    'sequence': address.sequence,
                    'acquired': address.acquired,
                }))
            rec.resume_line_ids.unlink()
            rec.resume_line_ids = resume_line_ids
            employee_skill_ids = []
            for address in rec.employee_id.employee_skill_ids:
                employee_skill_ids.append((0, 0, {
                    'employee_current_profile': rec.id,
                    'employee_id': address.employee_id.id,
                    'skill_id': address.skill_id.id,
                    'skill_level_id': address.skill_level_id.id,
                    'skill_type_id': address.skill_type_id.id,
                    'level_progress': address.level_progress,
                }))
            rec.employee_skill_ids.unlink()
            rec.employee_skill_ids = employee_skill_ids


    @api.multi
    def button_to_approve(self):
        for rec in self:
            rec.write({'state': 'waiting_for_approval'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})

    @api.multi
    def unlink(self):
        for tour in self:
            if tour.state != 'draft':
                raise UserError(
                    'You cannot delete a Update Request which is not in draft state')
        return super(EmployeeProfile, self).unlink()

    @api.multi
    def button_revert(self):
        self.ensure_one()
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        ctx = dict(
            default_composition_mode='comment',
            default_res_id=self.id,

            default_model='employee.profile',
            default_is_log='True',
            custom_layout='mail.mail_notification_light'
        )
        mw = {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
        self.write({'state': 'draft'})
        return mw


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
            if rec.new_emergency_contact:
                rec.employee_id.emergency_contact = rec.new_emergency_contact
            if rec.new_emergency_phone:
                rec.employee_id.emergency_phone = rec.new_emergency_phone
            if rec.new_phone:
                rec.employee_id.phone = rec.new_phone
            if rec.new_birthday:
                rec.employee_id.birthday = rec.new_birthday
            if rec.new_place_of_birth:
                rec.employee_id.place_of_birth = rec.new_place_of_birth
            if rec.new_country_of_birth:
                rec.employee_id.country_of_birth = rec.new_country_of_birth
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
            if rec.new_passport_id:
                rec.employee_id.passport_id = rec.new_passport_id
            if rec.new_bank_name:
                rec.employee_id.bank_name = rec.new_bank_name
            if rec.new_bank_account_number:
                rec.employee_id.bank_account_number = rec.new_bank_account_number
            if rec.new_ifsc_code:
                rec.employee_id.ifsc_code = rec.new_ifsc_code
            if rec.new_salutation:
                rec.employee_id.salutation = rec.new_salutation.id
            if rec.new_fax_number:
                rec.employee_id.fax_number = rec.new_fax_number
            rec.write({'state': 'approved'})
            if rec.address_ids:
                address_ids = []
                for address in rec.address_ids:
                    address_ids.append((0, 0, {
                        'employee_id': address.employee_id.id,
                        'address_type': address.address_type,
                        'state_id': address.state_id.id,
                        'country_id': address.country_id.id,
                        'street': address.street,
                        'street2': address.street2,
                        'zip': address.zip,
                        'is_correspondence_address': address.is_correspondence_address,
                        'city': address.city,
                    }))
                rec.employee_id.address_ids.unlink()
                rec.employee_id.address_ids = address_ids
            if rec.resume_line_ids:
                resume_line_ids = []
                for address in rec.resume_line_ids:
                    resume_line_ids.append((0, 0, {
                        'resume_employee_id': address.resume_employee_id.id,
                        'name': address.name,
                        'date_start': address.date_start,
                        'date_end': address.date_end,
                        'description': address.description,
                        'upload_qualification_proof': address.upload_qualification_proof,
                        'line_type_id': address.line_type_id.id,
                        'type_name': address.type_name,
                        'title': address.title.id,
                        'specialization': address.specialization,
                        'sequence': address.sequence,
                        'acquired': address.acquired,
                    }))
                rec.employee_id.resume_line_ids.unlink()
                rec.employee_id.resume_line_ids = resume_line_ids
            if rec.employee_skill_ids:
                employee_skill_ids = []
                for address in rec.employee_skill_ids:
                    employee_skill_ids.append((0, 0, {
                        'employee_id': address.employee_id.id,
                        'skill_id': address.skill_id.id,
                        'skill_level_id': address.skill_level_id.id,
                        'skill_type_id': address.skill_type_id.id,
                        'level_progress': address.level_progress,
                    }))
                rec.employee_id.employee_skill_ids.unlink()
                rec.employee_id.employee_skill_ids = employee_skill_ids




class CurrentAddress(models.Model):
    _name = "employee.current.address"
    _description = "Employee Current Address"


    address_type = fields.Selection([('permanent_add', 'Permanent Add'),
                                     ('present_add', 'Present Add'),
                                     ('office_add', 'Office Add'),
                                     ('hometown_add', 'HomeTown Add'),
                                    ],string='Address Type',required=True)
    employee_id = fields.Many2one('hr.employee','Employee Id')
    employee_current_profile = fields.Many2one('employee.profile','Employee Profile')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', change_default=True)
    is_correspondence_address = fields.Boolean('Is Correspondence Address')
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')



class UpdateAddress(models.Model):
    _name = "employee.update.address"
    _description = "Employee Address"


    def default_country(self):
        return self.env['res.country'].search([('name', '=', 'India')], limit=1)


    address_type = fields.Selection([('permanent_add', 'Permanent Add'),
                                     ('present_add', 'Present Add'),
                                     ('office_add', 'Office Add'),
                                     ('hometown_add', 'HomeTown Add'),
                                    ],string='Address Type',required=True)
    employee_update_profile = fields.Many2one('employee.profile')
    employee_id = fields.Many2one('hr.employee', 'Employee Id')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', change_default=True)
    is_correspondence_address = fields.Boolean('Is Correspondence Address')
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country', default = default_country)

    @api.constrains('employee_update_profile')
    def get_emp_id(self):
        for rec in self:
            rec.employee_id = rec.employee_update_profile.employee_id.id


class ResumeLineCurrent(models.Model):
    _name = 'hr.resume.line.current'
    _description = "Resumé line of an employee"

    employee_current_profile = fields.Many2one('employee.profile', 'Employee Current Profile')
    resume_employee_id = fields.Many2one('hr.employee')
    name = fields.Char(string='Title')
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date()
    description = fields.Text(string="Description")
    upload_qualification_proof = fields.Binary(string="Upload")
    line_type_id = fields.Many2one('hr.resume.line.type', string="Type")
    type_name = fields.Char(related='line_type_id.name')
    title = fields.Many2one('hr.education', string='Qualification')
    specialization = fields.Char(string='Specialization')
    sequence = fields.Integer(default=100)
    acquired = fields.Selection([('at_appointment_time', 'At Appointment time'),
                                 ('subsequently_acquired', 'Subsequently Acquired'),
                                 ], default='at_appointment_time', string="Acquired")


class ResumeLineUpdate(models.Model):
    _name = 'hr.resume.line.update'
    _description = "Resumé line of an employee - Update"

    employee_update_profile = fields.Many2one('employee.profile', 'Employee Updated Profile')
    resume_employee_id = fields.Many2one('hr.employee', ondelete='cascade')
    name = fields.Char(string='Title')
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date()
    description = fields.Text(string="Description")
    upload_qualification_proof = fields.Binary(string="Upload")
    line_type_id = fields.Many2one('hr.resume.line.type', string="Type")
    type_name = fields.Char(related='line_type_id.name')
    title = fields.Many2one('hr.education', string='Qualification')
    specialization = fields.Char(string='Specialization')
    sequence = fields.Integer(default=100)
    acquired = fields.Selection([('at_appointment_time', 'At Appointment time'),
                                 ('subsequently_acquired', 'Subsequently Acquired'),
                                 ], default='at_appointment_time', string="Acquired")


    @api.constrains('employee_update_profile')
    def get_emp_id(self):
        for rec in self:
            rec.resume_employee_id = rec.employee_update_profile.employee_id.id


class EmployeeSkillCurrent(models.Model):
    _name = 'hr.employee.skill.current'
    _description = "Skill level for an employee Current"

    employee_current_profile = fields.Many2one('employee.profile', 'Employee Current Profile')
    employee_id = fields.Many2one('hr.employee')
    skill_id = fields.Many2one('hr.skill')
    skill_level_id = fields.Many2one('hr.skill.level')
    skill_type_id = fields.Many2one('hr.skill.type')
    level_progress = fields.Integer(related='skill_level_id.level_progress')



class EmployeeSkillUpdtae(models.Model):
    _name = 'hr.employee.skill.update'
    _description = "Skill level for an employee update"

    employee_update_profile = fields.Many2one('employee.profile', 'Employee Update Profile')
    employee_id = fields.Many2one('hr.employee')
    skill_id = fields.Many2one('hr.skill')
    skill_level_id = fields.Many2one('hr.skill.level')
    skill_type_id = fields.Many2one('hr.skill.type')
    level_progress = fields.Integer(related='skill_level_id.level_progress')


    @api.constrains('employee_update_profile')
    def get_emp_id(self):
        for rec in self:
            rec.employee_id = rec.employee_update_profile.employee_id.id
