from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re

class HRApplicant(models.Model):
    _inherit='hr.applicant'
    _description ='Applicant'



    def default_country(self):
        return self.env['res.country'].search([('name', '=', 'India')], limit=1)

    category_id = fields.Many2one('employee.category', string='Category')
    religion_id = fields.Many2one('employee.religion', string='Religion')
    ex_serviceman = fields.Selection([('no', 'No'),
                                      ('yes', 'Yes')], string='Whether Ex Service Man', track_visibility='always')

    minority = fields.Boolean(string="Minority",track_visibility='always')
    employee_type = fields.Selection([('regular', 'Regular Employee'),
                                      ('contractual_with_agency', 'Contractual with Agency'),
                                      ('contractual_with_stpi', 'Contractual with STPI')], string='Employment Type',
                                     )
    branch_id = fields.Many2one('res.branch', string='Branch', store=True)
    recruitment_type = fields.Selection([
        ('d_recruitment', 'Direct Recruitment(DR)'),
        ('transfer', 'Transfer(Absorption)'),
        ('i_absorption', 'Immediate Absorption'),
        ('deputation', 'Deputation'),
        ('c_appointment', 'Compassionate Appointment'),
        ('promotion', 'Promotion'),
    ], 'Recruitment Type', track_visibility='always')

    dob = fields.Date(string='Birth Date')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string='Gender')
    # nationality = fields.Many2one('res.country', string='Nationality')
    title = fields.Many2one('res.partner.title', string='Salutation')
    get_total_match_religion = fields.Integer(string="Get Total Match Religion",compute="get_total_match_religion_data")
    santioned_position = fields.Float(string="Santioned Position",compute="get_santioned_position_emp")
    cur_no_of_emp = fields.Float('current no of employee',compute="get_santioned_position_emp")
    get_total_match_category = fields.Integer('Get Total Match Category',compute="get_total_match_category_data")

    pay_level_id = fields.Many2one('hr.payslip.paylevel', string='Pay Level')
    pay_level = fields.Many2one('payslip.pay.level', string='Pay Band', domain="[('entry_pay_id', '=', pay_level_id)]")

    struct_id = fields.Many2one('hr.payroll.structure', string='Salary Type')

    country_id = fields.Many2one(
        'res.country', 'Country', default=default_country)
    citizen_number = fields.Char('Citizen Number',track_visibility='always')
    citizen_eligibility_date =fields.Date(string='Date of Eligibility',track_visibility='always')
    citizen_file_data = fields.Binary('Upload',track_visibility='always')
    date_of_eligibility = fields.Date('Date of Eligibility', track_visibility='always')
    citizen_file_name = fields.Char('File Name',track_visibility='always')
    show_citizen_field = fields.Boolean('Show Field',default=False,copy=False,track_visibility='always')
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
    kind_of_disability = fields.Char('Kind of Disability', track_visibility='always')
    perc_disability = fields.Char('% of Disability', track_visibility='always')
    certificate_upload = fields.Binary('Upload certificate', track_visibility='always')
    personal_remark = fields.Char('Personal mark of Identification', track_visibility='always')

    pan_no = fields.Char('PAN Card No.', track_visibility='always')
    pan_upload = fields.Binary('Upload(PAN)', track_visibility='always')
    aadhar_no = fields.Char('Aadhar Card No.', track_visibility='always')
    aadhar_upload = fields.Binary('Upload(Aadhar)', track_visibility='always')
    passport_upload = fields.Binary('Upload(Passport)', track_visibility='always')

    bank_account_id = fields.Many2one(
        'res.partner.bank', 'Bank Account Number',
        domain="[('partner_id', '=', address_home_id)]",
        groups="hr.group_hr_user",
        help='Employee bank salary account')

    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', groups="hr.group_hr_user", default='single')
    spouse_complete_name = fields.Char(string="Spouse Complete Name", groups="hr.group_hr_user")
    spouse_birthdate = fields.Date(string="Spouse Birthdate", groups="hr.group_hr_user")
    children = fields.Integer(string='Number of Children', groups="hr.group_hr_user")

    address_home_id = fields.Many2one(
        'res.partner', 'Private Address',
        help='Enter here the private address of the employee, not the one linked to your company.',
        groups="hr.group_hr_user")
    is_address_home_a_company = fields.Boolean(
        'The employee adress has a company linked',
        compute='_compute_is_address_home_a_company',
    )
    emergency_contact = fields.Char("Emergency Contact", groups="hr.group_hr_user")
    emergency_phone = fields.Char("Emergency Phone", groups="hr.group_hr_user")
    km_home_work = fields.Integer(string="Km home-work", groups="hr.group_hr_user")
    passport_id = fields.Char('Passport No', groups="hr.group_hr_user")
    place_of_birth = fields.Char('Place of Birth', groups="hr.group_hr_user")
    country_of_birth = fields.Many2one('res.country', string="Country of Birth", groups="hr.group_hr_user")
    fax_number = fields.Char('FAX number', track_visibility='always')

    # work
    job_title = fields.Char("Post")
    address_id = fields.Many2one(
        'res.partner', 'Work Address')
    work_phone = fields.Char('Work Phone')
    mobile_phone = fields.Char('Work Mobile')
    work_email = fields.Char('Work Email')
    work_location = fields.Char('Work Location')
    # office work
    recruitment_file_no = fields.Char('Recruitment File No.', track_visibility='always')
    office_file_no = fields.Char('Office Order No.', track_visibility='always')
    mode_of_recruitment = fields.Char('Mode Of Recruitment', track_visibility='always')
    post = fields.Char('Post', track_visibility='always')
    date_of_join = fields.Date('Date of Join', track_visibility='always')
    office_order_date = fields.Date('Office Order Date', track_visibility='always')

    # employee in company
    job_id = fields.Many2one('hr.job', 'Functional Designation')
    department_id = fields.Many2one('hr.department', 'Department')
    parent_id = fields.Many2one('hr.employee', 'Manager')
    child_ids = fields.One2many('hr.employee', 'parent_id', string='Subordinates')
    coach_id = fields.Many2one('hr.employee', 'Coach')
    category_ids = fields.Many2many(
        'hr.employee.category', 'employee_category_rel',
        'emp_id', 'category_id',
        string='Tags')

    personal_email = fields.Char('Personal Email', track_visibility='always')
    phone = fields.Char('Phone (Home)', track_visibility='always')

    address_ids = fields.One2many('applicant.address', 'applicant_id', string='Address', track_visibility='always')

    resume_line_applicant_ids = fields.One2many('hr.resume.line', 'resume_applicant_id', string="Resumé lines")
    applicant_skill_ids = fields.One2many('hr.employee.skill', 'applicant_id', string="Skills")


    @api.constrains('parent_id')
    def _check_parent_id(self):
        for employee in self:
            if not employee._check_recursion():
                raise ValidationError(_('You cannot create a recursive hierarchy.'))



    @api.constrains('partner_mobile','partner_phone')
    @api.onchange('partner_mobile','partner_phone')
    def _check_mobile_phone(self):
        for rec in self:
            if rec.partner_mobile and not rec.partner_mobile.isnumeric():
                raise ValidationError(_("Phone number must be a number"))
            if rec.partner_mobile and len(rec.partner_mobile) != 10:
                raise ValidationError(_("Please enter correct Mobile number."
                                        "It must be of 10 digits"))
            if rec.partner_phone and not rec.partner_phone.isnumeric():
                raise ValidationError(_("Phone number must be a number"))
            if rec.partner_phone and len(rec.partner_phone) != 10:
                raise ValidationError(_("Please enter correct phone number."
                                        "It must be of 10 digits"))


    @api.onchange('job_id')
    def _onchange_job_id(self):
        if self.job_id:
            self.job_title = self.job_id.name
            self.pay_level_id = self.job_id.pay_level_id.id


    @api.onchange('pay_level')
    def _onchange_pay_level(self):
        if self.pay_level:
            self.salary_expected = self.pay_level.entry_pay
            self.salary_proposed = self.pay_level.entry_pay


    @api.onchange('address_id')
    def _onchange_address(self):
        self.work_phone = self.address_id.phone
        self.mobile_phone = self.address_id.mobile

    @api.onchange('company_id')
    def _onchange_company(self):
        address = self.company_id.partner_id.address_get(['default'])
        self.address_id = address['default'] if address else False

    @api.onchange('department_id')
    def _onchange_department(self):
        self.parent_id = self.department_id.manager_id



    @api.constrains('aadhar_no')
    @api.onchange('aadhar_no')
    def _check_aadhar_number(self):
        for rec in self:
            if rec.aadhar_no:
                for e in rec.aadhar_no:
                    if not e.isdigit():
                        raise ValidationError(_("Please enter correct Aadhar number, it must be numeric..."))
                if len(rec.aadhar_no) != 12:
                    raise ValidationError(_("Please enter correct Aadhar number, it must be of 12 digits..."))

    @api.constrains('date_of_join', 'office_order_date')
    @api.onchange('date_of_join','office_order_date')
    def _check_office_order_date(self):
        for record in self:
            if record.office_order_date and record.date_of_join and (record.office_order_date > record.date_of_join):
                raise ValidationError("Date of Joining should always be greater then equals to Office Order Date")


    @api.constrains('pan_no')
    @api.onchange('pan_no')
    def _check_pan_number(self):
        for rec in self:
            if rec.pan_no and not re.match(r'^[A-Za-z]{5}[0-9]{4}[A-Za-z]$', str(rec.pan_no)):
                raise ValidationError(_("Please enter correct PAN number..."))



    @api.onchange('pan_no')
    def set_upper(self):
        if self.pan_no:
            self.pan_no = str(self.pan_no).upper()


    @api.depends('address_home_id.parent_id')
    def _compute_is_address_home_a_company(self):
        """Checks that choosen address (res.partner) is not linked to a company.
        """
        for employee in self:
            try:
                employee.is_address_home_a_company = employee.address_home_id.parent_id.id is not False
            except AccessError:
                employee.is_address_home_a_company = False


    @api.onchange('country_id')
    def ckech_nationality(self):
        if self.country_id:
            if self.country_id.name != 'India':
                self.show_citizen_field =True
            else:
                self.show_citizen_field =False





    @api.multi
    def create_employee_from_applicant(self):
        res = super(HRApplicant, self).create_employee_from_applicant()
        if res.get('res_id', False):
            emp_id = self.env['hr.employee'].search([('id','=',res.get('res_id'))])
            if emp_id:
                emp_id.update({'employee_type': self.employee_type,
                        'recruitment_type': self.recruitment_type,
                        'salutation': self.title,
                        'country_id': self.country_id,
                        'gender': self.gender,
                        'birthday': self.dob,
                        'differently_abled': self.differently_abled,
                        'category': self.category_id,
                        'religion': self.religion_id,
                        'post': self.post,
                        'date_of_join': self.date_of_join,
                        'office_order_date': self.office_order_date,
                        'job_id': self.job_id,
                        'branch_id': self.branch_id,
                        'department_id': self.department_id,
                        'parent_id': self.parent_id,
                        'personal_email': self.personal_email,
                        'phone': self.phone,
                        'blood_group': self.blood_group,
                        'weight': self.weight,
                        'citizen_number': self.citizen_number,
                        'citizen_eligibility_date': self.citizen_eligibility_date,
                        'citizen_file_data': self.citizen_file_data,
                        'date_of_eligibility': self.date_of_eligibility,
                        'citizen_file_name': self.citizen_file_name,
                        'kind_of_disability': self.kind_of_disability,
                        'perc_disability': self.perc_disability,
                        'certificate_upload': self.certificate_upload,
                        'personal_remark': self.personal_remark,
                        'ex_serviceman': self.ex_serviceman,
                        'pan_no': self.pan_no,
                        'pan_upload': self.pan_upload,
                        'aadhar_no': self.aadhar_no,
                        'aadhar_upload': self.aadhar_upload,
                        'passport_upload': self.passport_upload,
                        'bank_account_id': self.bank_account_id,
                        'emergency_contact': self.emergency_contact,
                        'emergency_phone': self.emergency_phone,
                        'km_home_work': self.km_home_work,
                        'place_of_birth': self.place_of_birth,
                        'country_of_birth': self.country_of_birth,
                        'children': self.children,
                        'minority': self.minority,
                        'recruitment_file_no': self.recruitment_file_no,
                        'office_file_no': self.office_file_no,
                        'address_id': self.partner_id,
                        'work_email': self.email_from,
                        'work_phone': self.partner_phone,
                        'mobile_phone': self.partner_mobile,
                        'fax_number': self.fax_number,
                })
                if self.employee_type == 'regular' and self.recruitment_type == 'd_recruitment':
                    emp_id.sudo().start_test_period()
                    create_contract = self.env['hr.contract'].create(
                        {
                            'state': 'open',
                            'name': emp_id.name,
                            'employee_id': emp_id.id,
                            'department_id': emp_id.department_id.id,
                            'job_id': emp_id.job_id.id,
                            'pay_level_id': self.pay_level_id.id,
                            'pay_level': self.pay_level.id,
                            'struct_id': self.struct_id.id,
                            'date_start': datetime.now().date(),
                            'date_end': datetime.now().date() + relativedelta(years=3),
                            'employee_type': self.employee_type,
                            'wage': self.salary_proposed,
                        }
                    )
                elif self.employee_type == 'regular' and self.recruitment_type == 'transfer':
                    emp_id.sudo().start_test_period()
                    create_contract = self.env['hr.contract'].create(
                        {
                            'state': 'open',
                            'name': emp_id.name,
                            'employee_id': emp_id.id,
                            'department_id': emp_id.department_id.id,
                            'job_id': emp_id.job_id.id,
                            'pay_level_id': self.pay_level_id.id,
                            'pay_level': self.pay_level.id,
                            'struct_id': self.struct_id.id,
                            'date_start': datetime.now().date(),
                            'employee_type': self.employee_type,
                            
                            'wage': self.salary_proposed,
                        }
                    )
                elif self.employee_type == 'regular' and self.recruitment_type == 'i_absorption':
                    emp_id.sudo().start_test_period()
                    create_contract = self.env['hr.contract'].create(
                        {
                            'state': 'open',
                            'name': emp_id.name,
                            'employee_id': emp_id.id,
                            'department_id': emp_id.department_id.id,
                            'job_id': emp_id.job_id.id,
                            'pay_level_id': self.pay_level_id.id,
                            'pay_level': self.pay_level.id,
                            'struct_id': self.struct_id.id,
                            'date_start': datetime.now().date(),
                            'employee_type': self.employee_type,
                            'wage': self.salary_proposed,
                        }
                    )
                elif self.employee_type == 'regular' and self.recruitment_type == 'deputation':
                    emp_id.sudo().set_as_employee()
                    create_contract = self.env['hr.contract'].create(
                        {
                            'state': 'open',
                            'name': emp_id.name,
                            'employee_id': emp_id.id,
                            'department_id': emp_id.department_id.id,
                            'job_id': emp_id.job_id.id,
                            'pay_level_id': self.pay_level_id.id,
                            'pay_level': self.pay_level.id,
                            'struct_id': self.struct_id.id,
                            'date_start': datetime.now().date(),
                            'employee_type': self.employee_type,
                            'wage': self.salary_proposed,
                        }
                    )
                elif self.employee_type == 'regular' and self.recruitment_type == 'c_appointment':
                    emp_id.sudo().start_test_period()
                    create_contract = self.env['hr.contract'].create(
                        {
                            'state': 'open',
                            'name': emp_id.name,
                            'employee_id': emp_id.id,
                            'department_id': emp_id.department_id.id,
                            'job_id': emp_id.job_id.id,
                            'pay_level_id': self.pay_level_id.id,
                            'pay_level': self.pay_level.id,
                            'struct_id': self.struct_id.id,
                            'date_start': datetime.now().date(),
                            'employee_type': self.employee_type,
                            'wage': self.salary_proposed,
                        }
                    )
                elif self.employee_type == 'regular' and self.recruitment_type == 'promotion':
                    emp_id.sudo().start_test_period()
                    create_contract = self.env['hr.contract'].create(
                        {
                            'state': 'open',
                            'name': emp_id.name,
                            'employee_id': emp_id.id,
                            'department_id': emp_id.department_id.id,
                            'job_id': emp_id.job_id.id,
                            'pay_level_id': self.pay_level_id.id,
                            'pay_level': self.pay_level.id,
                            'struct_id': self.struct_id.id,
                            'date_start': datetime.now().date(),
                            'date_end': datetime.now().date() + relativedelta(years=3),
                            'employee_type': self.employee_type,
                            'wage': self.salary_proposed,
                        }
                    )

        return res



    def get_total_match_religion_data(self):
        
        if self.religion_id:
            emp_ids = self.env['hr.employee'].search([('religion','=',self.religion_id.id),('job_id','=',self.job_id.id)])
            employee_ids = self.env['hr.employee'].search([])
            for s in self:
                religion = len(emp_ids)
                emp = len(employee_ids)
                s.get_total_match_religion = round(religion/emp*100)

    def get_total_match_category_data(self):
        
        if self.category_id:
            emp_ids = self.env['hr.employee'].search([('category','=',self.category_id.id),('job_id','=',self.job_id.id)])
            employee_ids = self.env['hr.employee'].search([])
            for s in self:
                category = len(emp_ids)
                emp = len(employee_ids)
                s.get_total_match_category = round(category/emp*100)
        
    def get_santioned_position_emp(self):
#         emp_count_san = 0.0
        for s in self:
            pass
#             for line in s.job_id.budget_id:
# #                 print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
#                 s.santioned_position = line.employee_count
# #                 print("???????????????????????????????",s.santioned_position)
#             s.cur_no_of_emp = s.job_id.no_of_employee
# #             print("==============================",s.cur_no_of_emp)
                
    @api.multi
    def get_religion_from_job_position(self):
        
        return{
            'name': _('Religion'),
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'hr.employee',
            'src_model' : 'hr.applicant',
            'type': 'ir.actions.act_window',
            'context': { 
                        'search_default_job_id': self.job_id.id,
                        'group_by':'religion'},
            'search_view_id' : self.env.ref('hr.view_employee_tree').id
            }    
 
    @api.multi
    def get_category_from_job_position(self):
        
        return{
            'name': _('Category'),
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'hr.employee',
            'src_model' : 'hr.applicant',
            'type': 'ir.actions.act_window',
            'context': { 
                        'search_default_job_id': self.job_id.id,
                        'group_by':'category'},
            'search_view_id' : self.env.ref('hr.view_employee_tree').id
            }  



class InheritRelative(models.Model):

    _inherit = 'applicant.relative'
    _description = "Applicant Relatives"


    relate_type = fields.Many2one('relative.type', string = "Relative Type")


class ApplicantTraining(models.Model):
    _name='applicant.training'
    _description ='Applicant Training'

    # def default_employee(self):
    #     print("------------------context", self._context.get('active_id'))
    #     if 'params' in self._context.keys():
    #         return self._context.get('params')['id']
    #     else:
    #         return False

    # employee_id = fields.Many2one('hr.employee', string='employee', default=lambda self: self.default_employee())
    employee_id = fields.Many2one('hr.employee', string='employee')
    course = fields.Char('Course Title')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    location = fields.Text('Location')
    trainer_name = fields.Char('Trainer Name')
    training_type = fields.Selection([('internal','Internal'),
                                      ('external','External'),
                                      ('professional','Professional'),
                                      ('functional','Functional'),
                                      ('technical','Technical'),
                                      ('certification', 'Certification'),
                                      ],string='Training Type')
    organization_name = fields.Text('Organization Name')
    cert_file_data = fields.Binary('Certificate upload')
    cert_file_name = fields.Char('Certificate Name')
    skills = fields.Many2one('hr.skill', string = 'Skills')

class ApplicantAddress(models.Model):
    _name = 'applicant.address'
    _description = 'Applicant Address'

    def default_country(self):
        return self.env['res.country'].search([('name', '=', 'India')], limit=1)

    address_type = fields.Selection([('permanent_add', 'Permanent Add'),
                                     ('present_add', 'Present Add'),
                                     ('office_add', 'Office Add'),
                                     ('hometown_add', 'HomeTown Add'),
                                     ], string='Address Type', required=True)
    applicant_id = fields.Many2one('hr.applicant', 'employee Id')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', change_default=True)
    is_correspondence_address = fields.Boolean('Is Correspondence Address')
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country', default=default_country)
    count = fields.Integer('Count')

    @api.onchange('street', 'street2', 'zip', 'country_id', 'is_correspondence_address', 'city', 'state_id')
    def _onchange_hometown_address(self):
        for rec in self:
            rec.count = 0
            if rec.address_type == 'hometown_add':
                rec.count += 1
            if rec.count > 2:
                raise ValidationError("You cannot change Homettown address more than 2 times")

class ApplicantResume(models.Model):
    _inherit = 'hr.resume.line'

    resume_applicant_id = fields.Many2one('hr.applicant', ondelete='cascade')


    @api.onchange('title','specialization')
    def set_data(self):
        if not self.name and self.title:
            self.name = self.title.name
        if self.title and self.specialization:
            self.name = self.title.name + ' - ' + self.specialization


class ApplicantSkill(models.Model):
    _inherit = 'hr.employee.skill'
    _description = "Skill level for an employee"

    applicant_id = fields.Many2one('hr.applicant', ondelete='cascade')

#
# class SlctTrng_inhe(models.Model):
#     _inherit = 'select.training'
#
#
#     @api.multi
#     def action_done(self):
#         applicant = self.env['hr.applicant'].search(
#             [('id', '=', self._context.get('active_id'))])
#         employee_dict = applicant.create_employee_from_applicant()
#         course_obj = self.env['training.courses']
#         class_obj = self.env['training.class']
#         attendee_obj = self.env['list.of.attendees']
#         for rec in self:
#             if rec.is_triaing_needed:
#                 course = course_obj.search(
#                     [('job_id', '=', applicant.job_id.id)])
#                 if not course:
#                     course = course_obj.create({
#                         'name': 'Training Course for ' + str(
#                             applicant.job_id.name),
#                         'job_id': applicant.job_id.id,
#                         'duration': 1,
#                         'duration_type': 'month'})
#                 training_class = class_obj.search(
#                     [('course_id', '=', course.id)])
#                 if not training_class:
#                     training_class = class_obj.create({
#                         'course_id': course.id,
#                         'training_attendees': 1,
#                         'training_start_date': datetime.date.today() +
#                         datetime.timedelta(days=1),
#                         'training_end_date': datetime.date.today() +
#                         datetime.timedelta(days=1) + relativedelta(
#                             months=1, days=-1),
#                         'state': 'approved'})
#                 attendee_obj.create({
#                     'class_id': training_class.id,
#                     'employee_id': employee_dict.get('res_id', False),
#                     'training_start_date': training_class.training_start_date,
#                     'training_end_date': training_class.training_end_date,
#                     'date_of_arrival': training_class.training_start_date,
#                     'state': 'in_training'})
#         return True
#
