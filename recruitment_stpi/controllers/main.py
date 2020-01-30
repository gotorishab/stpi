from odoo import http, tools, SUPERUSER_ID, _
from odoo.addons.website.controllers.main import Website
from odoo.http import request
import json, sys, base64, pytz
from datetime import datetime, date, timedelta
from functools import reduce
from odoo import http
import logging

_logger = logging.getLogger(__name__)

class Maincontroller(Website):

    @http.route('/website_form/submit/form', type='http', auth="public", website=True, csrf=False)
    def create_hr_applicant_data_form(self, **kw):
        # if not request.session.uid:
        #     return request.redirect('/web/login')
        request.env.cr.autocommit(False)
        try:
            od = {}
            qw = {}
            for key in sorted(kw):
                if not ('_' in key and key.split("_")[len(key.split("_")) - 1] == '0'):
                    od.update({key: kw[key]})
                else:
                    qw.update({key[:len(key) - 2]: kw[key]})
            one2manyrooms = []

            temp_list = []
            for rec in qw.keys():
                if sorted([res for res in od.keys() if rec in res]):
                    temp_list.append(sorted([res for res in od.keys() if rec in res]))
            if temp_list:
                for i in range(0, len(temp_list[0])):
                    dict = {}
                    for booking in temp_list:
                        dict.update({booking[i]: kw[booking[i]]})
                    one2manyrooms.append(dict)

            education_ids = []
            experience_ids = []
            document_ids = []

            for rec in one2manyrooms:

                name_school = self.get_key_name(rec, 'name_school_')
                university_board = self.get_key_name(rec, 'university_board_')
                edu_from_date = self.get_key_name(rec, 'edu_from_date_')
                edu_to_date = self.get_key_name(rec, 'edu_to_date_')
                degree = self.get_key_name(rec, 'degree_')
                expe_employers_name = self.get_key_name(rec, 'expe_employers_name_')
                positions_held = self.get_key_name(rec, 'positions_held_')
                experience_from_date = self.get_key_name(rec, 'experience_from_date_')
                experience_to_date = self.get_key_name(rec, 'experience_to_date_')
                reasons = self.get_key_name(rec, 'reasons_')
                name_of_doc = self.get_key_name(rec, 'name_of_doc_')
                upload_doc = self.get_key_name(rec, 'upload_doc_')

                if name_school or university_board or edu_from_date or edu_to_date or degree:
                    education_ids.append((0, 0, {
                        'from_date':'' if not edu_from_date else kw.get(edu_from_date[0]),
                        'to_date':'' if not edu_to_date else kw.get(edu_to_date[0]),
                        'school_name':'' if not name_school else kw.get(name_school[0]),
                        'grade':'' if not university_board else kw.get(university_board[0]),
                    }))
                if expe_employers_name or positions_held or experience_from_date or experience_to_date or reasons:
                    experience_ids.append((0, 0, {
                        'organization':'' if not expe_employers_name else kw.get('expe_employers_name'),
                        'from_date':'' if not experience_from_date else kw.get(experience_from_date[0]),
                        'to_date':'' if not experience_to_date else kw.get(experience_to_date[0]),
                        'position':'' if not positions_held else kw.get(positions_held[0]),
                        'reasons':'' if not reasons else kw.get(reasons[0]),
                    }))
                if name_of_doc or upload_doc:
                    document_ids.append((0, 0, {
                        'organization':'' if not name_of_doc else kw.get('name_of_doc'),
                        'doc_attachment_id':'' if not upload_doc else kw.get('upload_doc'),
                    }))
            print('==============================',kw.get('nation'))
            print('================kw==============',kw)

            request.env['hr.applicant'].sudo().create({
                'name': kw.get('partner_name'),
                'partner_name': kw.get('partner_name'),
                'job_id': kw.get('job'),
                # partner_name=kw.get('partner_name'),
                # categ_ids=[(6, 0, [self.env.ref('hr_recruitment.tag_applicant_sales').id])],
                'email_from': kw.get('email_from'),
                'personal_email': kw.get('email_from'),
                'date_of_birth': kw.get('dob'),
                'father_name': kw.get('father_name'),
                'mother_name': kw.get('mother_name'),
                'ex_serviceman': kw.get('ex_serviceman'),
                'goverment_employee': kw.get('goverment_employee'),
                'gender': kw.get('gender'),
                'category_id': kw.get('category'),
                'religion_id': kw.get('religion'),
                'country_id': kw.get('nationality'),
                'place_of_birth': kw.get('pob'),
                'partner_phone': kw.get('partner_phone'),
                'aadhar_no': kw.get('aadhar_no'),
                'pan_no': kw.get('pan_no'),
                'blood_group': kw.get('blood_group'),
                'partner_mobile': kw.get('partner_phone_per'),
                'education_ids': education_ids,
                'prev_occu_ids': experience_ids,
                'address_ids': [(0, 0, {
                    'street': kw.get('street'),
                    'street2': kw.get('street2'),
                    'zip': kw.get('zip'),
                    'city': kw.get('city'),
                    'state_id': kw.get('state_id'),
                    'country_id': kw.get('country_id'),
                    'address_type': 'permanent_add'
                })]
            })
            request.env.cr.commit()
            return request.redirect('/job-thank-you')
        except:
            request.env.cr.rollback()
        finally:
            request.env.cr.autocommit(True)


        return

    def get_key_name(self, record, key):
        return [k for k in record.keys() if key in k]