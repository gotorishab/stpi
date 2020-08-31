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

    dob = fields.Date(string='Date of Birth')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string='Gender')
    gende = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('transgender', 'Transgender')
    ], string='Gender', track_visibility='always')
    # nationality = fields.Many2one('res.country', string='Nationality')
    title = fields.Many2one('res.partner.title', string='Salutation')
    get_total_match_religion = fields.Integer(string="Get Total Match Religion",compute="get_total_match_religion_data")
    santioned_position = fields.Float(string="Sanctioned Position",compute="get_santioned_position_emp")
    cur_no_of_emp = fields.Float('current no of employee',compute="get_santioned_position_emp")
    get_total_match_category = fields.Integer('Get Total Match Category',compute="get_total_match_category_data")

    pay_level_id = fields.Many2one('hr.payslip.paylevel', string='Pay Level')
    pay_level = fields.Many2one('payslip.pay.level', string='Pay Band')

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
    kind_of_disability = fields.Selection([('vh', 'Visually Handicapped'),
                                          ('hh', 'Hearing Handicapped'),
                                           ('ph', 'Physically Handicapped')],
                                          string='Kind of Disability',
                                         track_visibility='always')
    perc_disability = fields.Char('% of Disability', track_visibility='always')
    certificate_upload = fields.Binary('Upload certificate', track_visibility='always')
    personal_remark = fields.Char('Personal mark of Identification', track_visibility='always')

    pan_no = fields.Char('PAN Card No.', track_visibility='always')
    pan_upload = fields.Binary('Upload(PAN)', track_visibility='always')
    aadhar_no = fields.Char('Aadhar Card No.', track_visibility='always')
    aadhar_upload = fields.Binary('Upload(Aadhar)', track_visibility='always')
    passport_upload = fields.Binary('Upload(Passport)', track_visibility='always')

    bank_name = fields.Char(string='Bank Name')
    bank_account_number = fields.Char(string='Bank Account number')
    ifsc_code = fields.Char(string='IFSC Code')
    # penalty_awarded = fields.Selection(
    #     [('yes', 'Yes'), ('no', 'No')],
    #     string='Any Penalty awarded during the last 10 years')
    # penalty_awarded = fields.Selection(
    #     [('yes', 'Yes'), ('no', 'No')],
    #     string='Any Penalty awarded during the last 10 years')
    # action_can_know = fields.Selection(
    #     [('yes', 'Yes'), ('no', 'No')],
    #     string='Any action or inquiry is going on as far as candidate knowledge')
    # criminal_pending = fields.Selection(
    #     [('yes', 'Yes'), ('no', 'No')],
    #     string='Any criminal/ vigilance case is pending or contemplated')
    # relative_terms_css = fields.Selection(
    #     [('yes', 'Yes'), ('no', 'No')],
    #     string='Any relative defined in terms of CCS')
    # achievements_app = fields.Text('Achievements')
    # achievements_app = fields.Text('Additional Information')


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

    @api.constrains('parent_id')
    def _check_parent_id(self):
        for employee in self:
            if not employee._check_recursion():
                raise ValidationError(_('You cannot create a recursive hierarchy.'))


    @api.constrains('personal_email')
    def _check_personal_mail_val(self):
        for employee in self:
            regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
            if not (re.search(regex, employee.personal_email)):
                raise ValidationError(_('Please enter correct Personal Mail Address.'))


    @api.constrains('dob')
    def _check_dob_app(self):
        for employee in self:
            today = datetime.now().date()
            if employee.dob and employee.dob > today:
                raise ValidationError(_('Please enter correct date of birth'))

    @api.onchange('branch_id')
    @api.constrains('branch_id')
    def get_partner_from_branch(self):
        for rec in self:
            rec.partner_id = rec.branch_id.partner_id.id


    @api.constrains('office_order_date')
    def _check_office_order_date_app(self):
        for employee in self:
            today = datetime.now().date()
            if employee.office_order_date and employee.office_order_date > today:
                raise ValidationError(_('Please enter correct office order date'))



    @api.constrains('emergency_phone','phone')
    @api.onchange('emergency_phone','phone')
    def _check_mobile_phone(self):
        for rec in self:
            if rec.emergency_phone and not rec.emergency_phone.isnumeric():
                raise ValidationError(_("Phone number must be a number"))
            if rec.emergency_phone and len(rec.emergency_phone) != 10:
                raise ValidationError(_("Please enter correct Mobile number."
                                        "It must be of 10 digits"))
            if rec.phone and not rec.phone.isnumeric():
                raise ValidationError(_("Phone number must be a number"))
            if rec.phone and len(rec.phone) != 10:
                raise ValidationError(_("Please enter correct phone number."
                                        "It must be of 10 digits"))


    @api.onchange('name')
    @api.constrains('name')
    def onchange_name_get_pname(self):
        for rec in self:
            if rec.name:
                rec.partner_name = rec.name


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



    @api.constrains('name')
    @api.onchange('name')
    def _check_name_validation(self):
        for rec in self:
            if rec.name:
                for e in rec.name:
                    if not(e.isalpha() or e == ' '):
                        raise ValidationError(_("Please enter correct Name."))



    @api.constrains('bank_account_number')
    @api.onchange('bank_account_number')
    def _check_bank_acc_number(self):
        for rec in self:
            if rec.bank_account_number:
                for e in rec.bank_account_number:
                    if not e.isdigit():
                        raise ValidationError(_("Please enter correct Account number, it must be numeric..."))


    @api.constrains('aadhar_no')
    @api.onchange('aadhar_no')
    def _check_aadhar_number(self):
        for rec in self:
            if rec.aadhar_no:
                for e in rec.aadhar_no:
                    if not e.isdigit():
                        raise ValidationError(_("Please enter correct Aadhar number, it must be numeric."))
                if len(rec.aadhar_no) != 12:
                    raise ValidationError(_("Please enter correct Aadhar number, it must be of 12 digits."))

    @api.constrains('date_of_join', 'office_order_date')
    @api.onchange('date_of_join','office_order_date')
    def _check_office_order_date(self):
        for record in self:
            if record.office_order_date and record.date_of_join and (record.office_order_date > record.date_of_join):
                raise ValidationError("Date of Joining should always be greater then equals to Office Order Date")


    # @api.constrains('pan_no')
    # @api.onchange('pan_no')
    # def _check_pan_number(self):
    #     for rec in self:
    #         if rec.pan_no and not re.match(r'^[A-Za-z]{5}[0-9]{4}[A-Za-z]$', str(rec.pan_no)):
    #             raise ValidationError(_("Please enter correct PAN number."))



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
            resume_line_ids = []
            employee_skill_ids = []
            address_ids = []
            if emp_id:
                for emp in self.resume_line_applicant_ids:
                    resume_line_ids.append((0, 0, {
                    'resume_employee_id': emp_id.id,
                    'name': emp.name,
                    'date_start': emp.date_start,
                    'date_end': emp.date_end,
                    'description': emp.description,
                    'upload_qualification_proof': emp.upload_qualification_proof,
                    'line_type_id': emp.line_type_id.id,
                    'type_name': emp.type_name,
                    'title': emp.title.id,
                    'specialization': emp.specialization,
                    'sequence': emp.sequence,
                    'acquired': emp.acquired
                }))
                for emp in self.applicant_skill_ids:
                    employee_skill_ids.append((0, 0, {
                        'employee_id': emp_id.id,
                        'skill_id': emp.skill_id,
                        'skill_level_id': emp.skill_level_id.id,
                        'skill_type_id': emp.skill_type_id.id,
                        'level_progress': emp.level_progress
                    }))
                for emp in self.address_ids:
                    address_ids.append((0, 0, {
                        'employee_id': emp_id.id,
                        'address_type': emp.address_type,
                        'state_id': emp.state_id.id,
                        'country_id': emp.country_id.id,
                        'street': emp.street,
                        'street2': emp.street2,
                        'zip': emp.zip,
                        'is_correspondence_address': emp.is_correspondence_address,
                        'city': emp.city,
                        'count': emp.count,
                    }))
                emp_id.update({'employee_type': self.employee_type,
                        'recruitment_type': self.recruitment_type,
                        'salutation': self.title,
                        'country_id': self.country_id,
                        'gender': self.gender,
                        'gende': self.gende,
                        'birthday': self.dob,
                        'differently_abled': self.differently_abled,
                        'category': self.category_id,
                        'resume_line_ids': resume_line_ids,
                        'employee_skill_ids': employee_skill_ids,
                        'address_ids': address_ids,
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
                        'bank_account_number': self.bank_account_number,
                        'ifsc_code': self.ifsc_code,
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
                        # 'work_email': self.email_from,
                        # 'work_phone': self.partner_phone,
                        # 'mobile_phone': self.partner_mobile,
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
        pass
        #
        # if self.religion_id:
        #     emp_ids = self.env['hr.employee'].search([('religion','=',self.religion_id.id),('job_id','=',self.job_id.id)])
        #     employee_ids = self.env['hr.employee'].search([])
        #     for s in self:
        #         religion = len(emp_ids)
        #         emp = len(employee_ids)
        #         s.get_total_match_religion = round(religion/emp*100)

    def get_total_match_category_data(self):
        pass
        #
        # if self.category_id:
        #     emp_ids = self.env['hr.employee'].search([('category','=',self.category_id.id),('job_id','=',self.job_id.id)])
        #     employee_ids = self.env['hr.employee'].search([])
        #     for s in self:
        #         category = len(emp_ids)
        #         emp = len(employee_ids)
        #         s.get_total_match_category = round(category/emp*100)

    def get_santioned_position_emp(self):
        pass
#         emp_count_san = 0.0
#         for s in self:
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

    @api.constrains('address_type','employee_id')
    def check_unique_add(self):
        for rec in self:
            count = 0
            emp_id = self.env['applicant.address'].search([('address_type', '=', rec.address_type),('applicant_id', '=', rec.applicant_id.id)])
            for e in emp_id:
                count+=1
            if count >1:
                raise ValidationError("The Address Type must be unique")

