# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
import re


class HrEmployee(models.Model):
    _inherit = 'hr.employee'


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
    # gender = fields.Selection(selection_add=[('transgender', 'Transgender')])
    gende = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('transgender', 'Transgender')
                              ], string='Gender',track_visibility='always')
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
                                    ('a1+','A1+'),
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
    uan_no = fields.Char('UAN No.',track_visibility='always')
    pan_upload = fields.Binary('Upload(PAN)',track_visibility='always')
    aadhar_no = fields.Char('Aadhar Card No.',track_visibility='always')
    aadhar_upload = fields.Binary('Upload(Aadhar)',track_visibility='always')
    passport_upload = fields.Binary('Upload(Passport)',track_visibility='always')
    bank_name = fields.Char(string='Bank Name')
    bank_account_number = fields.Char(string='Bank Account number')
    ifsc_code = fields.Char(string='IFSC Code')

    _sql_constraints = [
        ('pan_uniq', 'unique (pan_no)', 'Pan No must be unique!'),
        ('aadhar_uniq', 'unique (aadhar_no)', 'Aadhar no must be unique!'),
        ('passport_uniq', 'unique (passport_id)', 'Passport no must be unique!'),
    ]




    @api.multi
    def create_user(self):
        return {
            'name': 'Create User',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('groups_inherit.view_createuser_wizard').id,
            'res_model': 'createuser.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                # 'default_employee_id': self.id,
                'default_res_model': self._name,
                'default_res_id': self.id,
                'default_name': self.name,
                'default_login': self.identify_id,
                }
        }
    