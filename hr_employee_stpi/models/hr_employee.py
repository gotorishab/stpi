# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
import re




class IdentifyIdSeq(models.Model):
    _name = 'identify.seqid'
    _description = "Identify Seqid"

class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    #header
    employee_type = fields.Selection([('regular','Regular Employee'),
                                     ('contractual_with_agency','Contractual with Agency'),
                                     ('contractual_with_stpi','Contractual with STPI')],string='Employment Type',track_visibility='always', store=True)

    recruitment_type = fields.Selection([
                                    ('d_recruitment','Direct Recruitment(DR)'),
                                    ('transfer','Transfer(Absorption)'),
                                    ('i_absorption','Immediate Absorption'),
                                    ('deputation','Deputation'),
                                    ('c_appointment','Compassionate Appointment'),
                                    ('promotion','Promotion'),
                                         ],'Recruitment Type',track_visibility='always', store=True)

    salutation = fields.Many2one('res.partner.title',track_visibility='always')

    fax_number = fields.Char('FAX number',track_visibility='always')
    
    #added by Sangita 
    pay_level = fields.Many2one('payslip.pay.level', string='Pay Band')

    #citizenship
    # citizen_country_id = fields.Many2one('res.country','Country name')


    def default_country(self):
        return self.env['res.country'].search([('name', '=', 'India')], limit=1)

    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', groups="hr.group_hr_user", default=default_country)
    citizen_number = fields.Char('Citizen Number',track_visibility='always')
    citizen_eligibility_date =fields.Date(string='Date of Eligibility',track_visibility='always')
    citizen_file_data = fields.Binary('Upload',track_visibility='always')
    date_of_eligibility = fields.Date('Date of Eligibility', track_visibility='always')
    citizen_file_name = fields.Char('File Name',track_visibility='always')
    show_citizen_field = fields.Boolean('Show Field',default=False,copy=False,track_visibility='always')

    #religion
    category = fields.Many2one('employee.category',string='Category',track_visibility='always')
    religion = fields.Many2one('employee.religion',string='Religion',track_visibility='always')
    minority = fields.Boolean('Minority',default=False,track_visibility='always')

     #office work
    gender = fields.Selection(selection_add=[('transgender', 'Transgender')])
    recruitment_file_no = fields.Char('Recruitment File No.',track_visibility='always')
    office_file_no = fields.Char('Office Order No.',track_visibility='always')
    mode_of_recruitment = fields.Char('Mode Of Recruitment',track_visibility='always')
    post = fields.Char('Post',track_visibility='always')
    date_of_join = fields.Date('Date of Joining',track_visibility='always')
    office_order_date = fields.Date('Office Order Date',track_visibility='always')

    #contact
    personal_email =fields.Char('Personal Email',track_visibility='always')
    phone = fields.Char('Phone (Home)',track_visibility='always')

    #work_infroamtion
    ex_serviceman =fields.Selection([('no','No'),
                                     ('yes','Yes')],string='Whether Ex Service Man',track_visibility='always')

    #physical
    height = fields.Float('Height (in CMs)',track_visibility='always')
    weight = fields.Float('Weight (in KGs)',track_visibility='always')
    blood_group = fields.Selection([('a+','A+'),
                                     ('a-','A-'),
                                     ('b+','B+'),
                                     ('b-','B-'),
                                     ('o+', 'O+'),
                                     ('o-', 'O-'),
                                     ('ab+','AB+'),
                                     ('ab-','AB-')],string='Blood Group',track_visibility='always')
    differently_abled = fields.Selection([('no','No'),
                                          ('yes','Yes')], default = 'no', string='Differently Abled?',track_visibility='always')
    kind_of_disability = fields.Selection([('vh', 'No'),
                                           ('hh', 'Yes'),
                                           ('ph', 'Yes')], string='Kind of Disability',
                                          track_visibility='always')
    perc_disability = fields.Char('% of Disability',track_visibility='always')
    certificate_upload = fields.Binary('Upload certificate',track_visibility='always')
    personal_remark =fields.Char('Personal mark of Identification',track_visibility='always')



    #Identification
    identify_id = fields.Char(string='Identification No.',copy=False, store=True, track_visibility='always', compute='_compute_identify_no')
    pan_no = fields.Char('PAN Card No.',track_visibility='always')
    pan_upload = fields.Binary('Upload(PAN)',track_visibility='always')
    aadhar_no = fields.Char('Aadhar Card No.',track_visibility='always')
    aadhar_upload = fields.Binary('Upload(Aadhar)',track_visibility='always')
    passport_upload = fields.Binary('Upload(Passport)',track_visibility='always')
    bank_account_number = fields.Char(string='Bank Account number')
    ifsc_code = fields.Char(string='IFSC Code')

    # category_ids = fields.Many2many('hr.employee.category', 'employee_category_rel', 'emp_id', 'category_id', 'Tags', required=False)

    # added by sangita
    def get_document_ids(self):

        for document in self:
            document_ids = self.env['hr.employee.document'].sudo().search([('employee_ref', '=', document.id)])
            print("?????????????????????????", document_ids)
        #             for doc in document_ids:

        return document_ids

    def get_leave_record(self):
        for leave in self:
            if leave.id:
                SQL = """
                           select hla.create_date as date,
                            hla.number_of_days as days,
                            hla.holiday_status_id as holiday
                            from hr_leave_allocation as hla 
                            inner join hr_leave_type as hly on hly.id = hla.holiday_status_id
                            where employee_id = %s and state in ('validate') and holiday_type = 'employee'
                            group by
                            hla.id,
                            hla.employee_id,
                            hla.holiday_status_id
                        """
                self.env.cr.execute(SQL, (
                    leave.id,
                ))
                res = self.env.cr.fetchall()
                #                 r = [i for i in res]
                print("??????????????????????casual_leavescasual_leaves", res)
                return res

    def find_age(self):
        age = (date.today() - self.birthday) // timedelta(days=365.2425)
        #         print("?????????????????????????age",age)
        return age

    def relative_types(self):
        for relative in self:
            relativ_id = self.env['employee.relative'].search([('employee_id', '=', relative.id)])
            #             print("????????????fffffffffff???????????????",relativ_id)
            for rel_type in relativ_id:
                relative_type = rel_type.relative_type
        #                 print("relative_typerelative_typerelative_type",relative_type)
        return relative_type

    def reltive_details(self):
        for relative in self:
            if relative:
                SQL = """

                        select er.name,
                            rt.name,
                            ROUND(er.age) as roundage
                         from employee_relative as er
                            inner join hr_employee as he on he.id = er.employee_id
                            inner join relative_type as rt on rt.id = er.relate_type
                            where er.employee_id = %s
                    """
                self.env.cr.execute(SQL, (
                    relative.id,
                ))

                res = self.env.cr.fetchall()

                return res

    def get_ltc_record(self):
        for ltc in self:
            if ltc.id:
                SQL = """
                        select he.name as emp,
                            ela.hometown_address,
                            ela.el_encashment
                            from employee_ltc_advance as ela
                            inner join hr_employee as he on he.id = ela.employee_id
                            where ela.employee_id = %s

                            group by 
                            he.name,
                            ela.hometown_address,
                            ela.el_encashment

                    """
                self.env.cr.execute(SQL, (
                    ltc.id,
                ))

                res = self.env.cr.fetchall()

                return res

    def leave_available_balance(self):
        for leave in self:
            if leave:
                SQL = """
                        select hlr.holiday_status_id as holiday,
                            sum(hlr.number_of_days) as days 
                            from hr_leave_report hlr 
                            inner join hr_leave_type as hly on hly.id = hlr.holiday_status_id
                            where employee_id = %s and holiday_type = 'employee' and state not in ('refuse')
                            group by 
                            hlr.holiday_status_id
                    """

                self.env.cr.execute(SQL, (
                    leave.id,
                ))
                res = self.env.cr.fetchall()
                #                 r = [i for i in res]
                #                 print("??????????????????????casual_leavescasual_leaves",res)
                return res



    @api.depends('employee_type')
    def _compute_identify_no(self):
        for res in self:
            if res.employee_type == 'regular':
                seq = self.env['ir.sequence'].next_by_code('hr.employee')
                res.identify_id = 'STPI' + str(seq)
            else:
                seq = self.env['ir.sequence'].next_by_code('identify.seqid')
                res.identify_id = 'STPITEMP' + str(seq)


    # @api.model
    # def create(self, vals):
    #     res =super(HrEmployee, self).create(vals)
    #     print('==========================',vals)
    #     if res.employee_type == 'regular':
    #         seq = self.env['ir.sequence'].next_by_code('hr.employee')
    #         res.identify_id = 'STPI' + str(seq)
    #     else :
    #         seq = self.env['ir.sequence'].next_by_code('identify.seqid')
    #         res.identify_id = 'STPITEMP' + str(seq)
    #     return res

    @api.constrains('date_of_join', 'office_order_date')
    @api.onchange('date_of_join','office_order_date')
    def _check_office_order_date(self):
        for record in self:
            if record.office_order_date and record.date_of_join and (record.office_order_date > record.date_of_join):
                raise ValidationError("Date of Joining should always be greater then equals to Office Order Date")


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


    @api.constrains('pan_no')
    @api.onchange('pan_no')
    def _check_pan_number(self):
        for rec in self:
            if rec.pan_no and not re.match(r'^[A-Za-z]{5}[0-9]{4}[A-Za-z]$', str(rec.pan_no)):
                raise ValidationError(_("Please enter correct PAN number..."))

    @api.constrains('birthday')
    def _check_birthday_app(self):
        for employee in self:
            today = datetime.now().date()
            if employee.birthday  and employee.birthday > today:
                raise ValidationError(_('Please enter correct date of birth'))



    @api.constrains('office_order_date')
    def _check_office_order_date_app(self):
        for employee in self:
            today = datetime.now().date()
            if employee.office_order_date and employee.office_order_date > today:
                raise ValidationError(_('Please enter correct office order date'))



    @api.onchange('pan_no')
    def set_upper(self):
        if self.pan_no:
            self.pan_no = str(self.pan_no).upper()
            




    address_ids = fields.One2many('employee.address','employee_id',string='Address',track_visibility='always')

    #Personal File Detail
    file_no = fields.Char('File No',track_visibility='always')
    file_open_date = fields.Date('File Open Date',track_visibility='always')
    file_close_date = fields.Date('File close Date',track_visibility='always')
    file_remark = fields.Text('Remark',track_visibility='always')


    @api.onchange('country_id')
    def ckech_nationality(self):
        if self.country_id:
            if self.country_id.name != 'India':
                self.show_citizen_field =True
            else:
                self.show_citizen_field =False




    def set_employee_training(self):
        if self:
            return {
                'name': 'Employee Training',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'employee.training',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'view_id': self.env.ref('l10n_in_hr_fields.employee_training_tree_view').id,
                'domain': [('employee_id', '=', self.id)],
                'context':{
                        'default_employee_id': self.id}
            }

    # def set_last_employer(self):
    #     if self:
    #         return {
    #             'name': 'Last Employer',
    #             'view_type': 'form',
    #             'view_mode': 'tree',
    #             'res_model': 'employee.last_employer',
    #             'type': 'ir.actions.act_window',
    #             'target': 'current',
    #             'view_id': self.env.ref('l10n_in_hr_fields.employee_last_employer_tree_view').id,
    #             'domain': [('employee_id', '=', self.id)],
    #             'context':{
    #                     'default_employee_id': self.id}
    #         }

    # def set_employee_transfer(self):
    #     if self:
    #         return {
    #             'name': 'Hr Employee Transfer',
    #             'view_type': 'form',
    #             'view_mode': 'tree,form',
    #             'res_model': 'hr.employee.transfer',
    #             'type': 'ir.actions.act_window',
    #             'target': 'current',
    #             # 'view_id': self.env.ref('l10n_in_hr_fields.employeetransfer_form_view').id,
    #             'domain': [('employee_id', '=', self.id)],
    #             'context':{
    #                     'default_employee_id': self.id}
    #         }
    #



    # def get_family_detail(self):
    #     if self:
    #         return {
    #             'name': 'Family Details',
    #             'view_type': 'form',
    #             'view_mode': 'tree',
    #             'res_model': 'employee.relative',
    #             'type': 'ir.actions.act_window',
    #             'target': 'current',
    #             'view_id': self.env.ref('hr_applicant.view_employee_relative_tree').id,
    #             'domain': [('employee_id', '=', self.id)],
    #             'context': {
    #                 'default_employee_id': self.id}
    #             }



class EmployeeAddress(models.Model):
    _name = 'employee.address'
    _description = 'Address'

    def default_country(self):
        return self.env['res.country'].search([('name', '=', 'India')], limit=1)

    address_type = fields.Selection([('permanent_add', 'Permanent Add'),
                                     ('present_add', 'Present Add'),
                                     ('office_add', 'Office Add'),
                                     ('hometown_add', 'HomeTown Add'),
                                    ],string='Address Type',required=True)
    employee_id = fields.Many2one('hr.employee','employee Id')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', change_default=True)
    is_correspondence_address = fields.Boolean('Is Correspondence Address')
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country', default = default_country)
    count = fields.Integer('Count')

    @api.onchange('street', 'street2','zip', 'country_id','is_correspondence_address', 'city','state_id')
    def _onchange_hometown_address(self):
        for rec in self:
            rec.count = 0
            if rec.address_type == 'hometown_add':
                rec.count += 1
            if rec.count >2:
                raise ValidationError("You cannot change Homettown address more than 2 times")

    @api.constrains('address_type','employee_id')
    def check_unique_add(self):
        for rec in self:
            count = 0
            emp_id = self.env['employee.address'].search([('address_type', '=', rec.address_type),('employee_id', '=', rec.employee_id.id)])
            for e in emp_id:
                count+=1
            if count >1:
                raise ValidationError("The Address Type must be unique")