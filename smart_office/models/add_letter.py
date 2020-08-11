from odoo import models, api, fields,_
from datetime import datetime, date, timedelta
import requests
import json
from PyPDF2 import PdfFileMerger, PdfFileReader
from odoo.exceptions import UserError

class AddLetter(models.Model):
    _inherit = "muk_dms.file"
    _rec_name = "name"
    _description = "Add Document/Letter"

    current_owner_id = fields.Many2one('res.users', 'Current Owner')
    last_owner_id = fields.Many2one('res.users', 'Last Owner')
    sec_owner_one = fields.Many2one('res.users', 'Secondary Owner 1')
    sec_owner_two = fields.Many2one('res.users', 'Secondary Owner 2')
    sec_owner_three = fields.Many2one('res.users', 'Secondary Owner 3')

    sec_owner = fields.Many2many('res.users', string='Secondary Owners')
    srch_id = fields.Many2many('res.users', string='My Search')
    dispatch_id = fields.Many2one('dispatch.document')
    previous_owner = fields.Many2many('res.users', string='Previous/Current Owners')
    previous_owner_emp = fields.Many2many('hr.employee', string='Previous/Current Owners')
    content_binary = fields.Text('Content Binary')
    tracker_ids = fields.One2many('muk.letter.tracker', 'letter_id')

    @api.onchange('name')
    @api.constrains('name')
    def get_directory_name(self):
        for rec in self:
            directory = self.env['muk_dms.directory'].search([('name', '=', 'Incoming Files')], limit=1)
            rec.directory = directory.id


    @api.model
    def create(self, vals):
        res = super(AddLetter, self).create(vals)
        print('==============================res.content=============================', res.content)
        res.content_binary = res.content
        if not res.dispatch_id:
            print('============================self.env.user.id===============================',self.env.user.id)
            print('============================current_owner_id===============================',self.env.user.id)
            directory = self.env['muk_dms.directory'].sudo().search([('name', '=', 'Incoming Files')], limit=1)
            vals['directory'] = directory.id
            # if self._context.get('smart_office_incoming_letter', False):
            #     vals['directory'] = self.env.ref('smart_office.smart_office_directory').id
            vals['responsible_user_id'] = self.env.user.id
            vals['last_owner_id'] = self.env.user.id
            vals['current_owner_id'] = self.env.user.id
            # if 'code' not in vals or vals['code'] == _('New'):
            #     vals['name'] = self.env['ir.sequence'].next_by_code('muk.dms.letter') or _('New')
            seq = self.env['ir.sequence'].next_by_code('muk_dms.file')
            date = datetime.now().date()
            sequence = str(date.strftime('%Y%m%d')) + '/' + str(seq)
            res.letter_number = sequence
            current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
            enclosure_details = str(res.sender_enclosures) + ' *****' + str(res.name)
            data = {
                'document_type': res.document_type,
                'name': int(seq),
                'enclosure_details': enclosure_details,
                'user_id': current_employee.user_id.id,
                'attachment[]': res.content
            }
            print('==============================name=============================', int(seq))
            print('==============================enclosure_details=============================', enclosure_details)
            print('==============================user_id=============================', current_employee.user_id.id)
            # print('==============================res.content=============================', res.content)
            req = requests.post('http://206.189.129.190/STPI/www/web-service/add-letter/', data=data,
                                json=None)
            try:
                print('=====================================================', req)
                pastebin_url = req.text
                print('===========================pastebin_url==========================', pastebin_url)
                dictionary = json.loads(pastebin_url)
                res.php_letter_id = str(dictionary["response"]["letterData"]["id"])
            except Exception as e:
                print('=============Error==========', e)
            current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            self.env['file.tracker.report'].create({
                'name': str(res.name),
                'number': str(res.letter_number),
                'type': 'Correspondence',
                'created_by': str(current_employee.user_id.name),
                'created_by_dept': str(current_employee.department_id.name),
                'created_by_jobpos': str(current_employee.job_id.name),
                'created_by_branch': str(current_employee.branch_id.name),
                'create_date': datetime.now().date(),
                'action_taken': 'correspondence_created',
                'remarks': res.sender_remarks,
                'details': "Correspondence created on {}".format(datetime.now().date())
            })
            if self._context.get('smart_office_incoming_letter', False):
                self.env['muk.letter.tracker'].create(dict(
                    type='create',
                    # from_id=False,
                    to_id=self.env.user.id,
                    letter_id=res.id
                ))
                res.directory.doc_file_preview = res.content
            return res
        else:
            # print('============================self.env.user.id===============================', self.env.user.id)
            print('============================dispatch_id.current_user_id===============================',
                  res.dispatch_id.current_user_id.id)
            directory = self.env['muk_dms.directory'].sudo().search([('name', '=', 'Incoming Files')], limit=1)
            vals['directory'] = directory.id
            vals['responsible_user_id'] = res.dispatch_id.current_user_id.id
            vals['last_owner_id'] = res.dispatch_id.current_user_id.id
            vals['current_owner_id'] = res.dispatch_id.current_user_id.id
            vals['create_uid'] = res.dispatch_id.current_user_id.id
            vals['write_uid'] = res.dispatch_id.current_user_id.id
            seq = self.env['ir.sequence'].next_by_code('muk_dms.file')
            date = datetime.now().date()
            sequence = str(date.strftime('%Y%m%d')) + '/' + str(seq)
            res.letter_number = sequence
            current_employee = self.env['hr.employee'].search([('user_id', '=', res.dispatch_id.current_user_id.id)], limit=1)
            enclosure_details = str(res.sender_enclosures) + ' *****' + str(res.name)
            data = {
                'document_type': res.document_type,
                'name': int(seq),
                'enclosure_details': enclosure_details,
                'user_id': current_employee.user_id.id,
                'attachment[]': res.content
            }
            print('==============================name=============================', int(seq))
            print('==============================enclosure_details=============================', enclosure_details)
            print('==============================user_id=============================', current_employee.user_id.id)
            # print('==============================res.content=============================', res.content)
            req = requests.post('http://206.189.129.190/STPI/www/web-service/add-letter/', data=data,
                                json=None)
            try:
                print('=====================================================', req)
                pastebin_url = req.text
                print('===========================pastebin_url==========================', pastebin_url)
                dictionary = json.loads(pastebin_url)
                res.php_letter_id = str(dictionary["response"]["letterData"]["id"])
            except Exception as e:
                print('=============Error==========', e)
            current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            self.env['file.tracker.report'].create({
                'name': str(res.name),
                'number': str(res.letter_number),
                'type': 'Correspondence',
                'created_by': str(current_employee.user_id.name),
                'created_by_dept': str(current_employee.department_id.name),
                'created_by_jobpos': str(current_employee.job_id.name),
                'created_by_branch': str(current_employee.branch_id.name),
                'create_date': datetime.now().date(),
                'action_taken': 'correspondence_created',
                'remarks': res.sender_remarks,
                'details': "Correspondence created on {}".format(datetime.now().date())
            })
            if self._context.get('smart_office_incoming_letter', False):
                self.env['muk.letter.tracker'].create(dict(
                    type='create',
                    # from_id=False,
                    to_id=self.env.user.id,
                    letter_id=res.id
                ))
                res.directory.doc_file_preview = res.content
            return res


    # Letter Information
    responsible_user_id = fields.Many2one('res.users', default=lambda self:self.env.user.id)
    document_type = fields.Selection([('letter', 'Letter'),
                                      ('document', 'Document')], default='document')

    sender_type = fields.Many2one('doc.sender.type',' Sender Type')
    delivery_mode = fields.Many2one('doc.delivery.mode', 'Delivery Mode')
    language_of_letter = fields.Many2one('doc.letter.language', 'Correspondence Language')
    letter_type = fields.Many2one('doc.letter.type', 'Correspondence Type')
    php_letter_id = fields.Char('PHP Letter ID')
    # doc_no = fields.Char()

    # doc_tags = fields.Text('Tags')
    doc_enclosure = fields.Selection([('book', 'Book'),
                                     ('service_book', 'Service Book'),
                                     ('cd_dvd', 'CD or DVD')])
    doc_enclosure_detail = fields.Text('Enclosure Details')

    file_track_ids = fields.One2many('file.tracking.information', 'create_let_id', string = "files")
    pdf_file = fields.Binary(related='content')
    folder_id = fields.Many2one('folder.master', string="File Assigned")

    letter_number = fields.Char('Correspondence Number')

    sender_type_related = fields.Char(related='sender_type.name')
    delivery_mode_related = fields.Char(related='delivery_mode.name')
    language_of_letter_related = fields.Char(related='language_of_letter.name')
    letter_type_related = fields.Char(related='letter_type.name')
    other_st = fields.Char('Other (Sender Type)')
    other_dm = fields.Char('Other (Delivery Mode)')
    other_lol = fields.Char('Other (Correspondence Language')
    other_lt = fields.Char('Other (Correspondence Type)')

    # Receipt Information
    doc_receive_m2o = fields.Many2one('doc.rf', string='Doc receive from')
    doc_recieve_from = fields.Selection([('private', 'Private'),
                                         ('govt', 'Government')], default='private')
    doc_type_m2o = fields.Many2one('doc.type', string='Doc Type')
    doc_type = fields.Selection([('organization', 'Organization'),
                                 ('individual', 'Individual'),
                                 ('state', 'State'),
                                 ('central', 'Central')], default='organization')

    doc_organisation_id = fields.Many2one('muk.doc.organisation', 'Organisation')
    doc_sender_id = fields.Many2one('muk.doc.sender', 'Sender Name')
    reciept_mode = fields.Selection([('hand_to_hand', 'Hand to Hand'),
                                     ('email', 'Email'),
                                     ('post', 'Post'),
                                     ('fax', 'Fax'),
                                     ('spl_mess', 'Spl. Messenger')], default='post')
    doc_reciept_date = fields.Date('Receipt Date', default=fields.Date.context_today)
    doc_subject = fields.Char('Subject')
    doc_remark = fields.Text('Remark')
    doc_state = fields.Many2one('res.country.state', 'State')
    doc_department_id = fields.Many2one('muk.doc.department', 'Department')
    doc_letter_details = fields.Text('Correspondence Details')
    file_holder = fields.Many2one('res.users', string = "File holder")

    sender_ministry = fields.Many2one('doc.sender.minstry',"Ministry")
    sender_department = fields.Many2one('doc.sender.department',"Department")
    sender_name = fields.Char("Name")
    sender_designation = fields.Many2one('doc.sender.designation',"Designation")
    sender_organisation = fields.Char("Organisation")
    sender_address = fields.Many2one('doc.sender.address',"Address")
    sender_address_text = fields.Text("Sender Address")

    sender_city = fields.Many2one('res.city', string="City")
    sender_state = fields.Many2one('res.country.state', string="State")
    sender_country = fields.Many2one('res.country', string="Country")
    sender_pincode = fields.Char("Pin Code")
    sender_landline = fields.Char("Landline")
    sender_mobile = fields.Char("Mobile")
    sender_fax = fields.Char("FAX")
    sender_email = fields.Char("Email")
    sender_enclosures = fields.Char("Enclosure")
    sender_remarks = fields.Char("Remarks")


    # doc_letter_category = fields.Selection([('salary', 'Salary'),
    #                                         ('employee_details', 'Employee Details'),
    #                                         ('forest_conservation', 'Forest Conservation'),
    #                                         ('legislative_sec', 'Legislative Sec'),
    #                                         ('view_sec', 'View Sec'),
    #                                         (('lr_sec', 'LR Sec'))], default='salary')

    reference_ids = fields.Many2many('muk_dms.file', 'muk_dms_file_rel', 'field1', 'field2', 'Reference Correspondence', domain="[('id', '!=', id)]")

    forward_from_id = fields.Many2one('res.users', 'Forward From', default=lambda self:self.env.user.id)
    forward_to_id = fields.Many2one('res.users', 'Forward To')




    @api.multi
    def action_view_file(self):
        form_view = self.env.ref('smart_office.foldermaster_form_view')
        tree_view = self.env.ref('smart_office.foldermaster_tree_view1')
        value = {
            'domain': str([('id', '=', self.folder_id.id)]),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'folder.master',
            'view_id': False,
            'views': [(form_view and form_view.id or False, 'form'),
                      (tree_view and tree_view.id or False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': self.folder_id.id,
            'target': 'current',
            'nodestroy': True
        }
        return value



    @api.multi
    def tracker_view_letter(self):
        for rec in self:
            views_domain = []
            dmn = self.env['file.tracker.report'].search(['|', ('name', '=', rec.name), ('number', '=', rec.letter_number)])
            for id in dmn:
                views_domain.append(id.id)
            return {
                'name': 'File Tracking Report',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'file.tracker.report',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': [('id', 'in', views_domain)]
            }



    @api.onchange('sender_ministry')
    def change_sender_minstry(self):
        if self.sender_ministry == False:
            self.sender_address = False
        else:
            return {'domain': {'sender_address': [('minstry', '=', self.sender_ministry.id)]}}



    @api.onchange('sender_address')
    @api.constrains('sender_address')
    def change_sender_address(self):
        for rec in self:
            if rec.sender_address:
                rec.sender_address_text = rec.sender_address.name


    def smart_office_create_file(self):
        files = [(6, 0, self.ids)]
        return {
            # 'name': 'Print Invoice',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'muk_dms.directory',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'form_view_ref': 'smart_office.view_add_files_doc_form',
                        'default_files': files},
        }




    @api.onchange('doc_receive_m2o')
    @api.constrains('doc_receive_m2o')
    def get_doc_receive(self):
        for rec in self:
            rec.doc_type_m2o = False
            if rec.doc_receive_m2o.name == 'Private':
                rec.doc_recieve_from = 'private'
            elif rec.doc_receive_m2o.name == 'Government':
                rec.doc_recieve_from = 'govt'
            else:
                rec.doc_recieve_from = ''

    @api.onchange('doc_type_m2o')
    @api.constrains('doc_type_m2o')
    def get_doc_type(self):
        for rec in self:
            if rec.doc_type_m2o.name == 'Organisation':
                rec.doc_type = 'organization'
            elif rec.doc_type_m2o.name == 'Individual':
                rec.doc_type = 'individual'
            elif rec.doc_type_m2o.name == 'Central':
                rec.doc_type = 'central'
            elif rec.doc_type_m2o.name == 'State':
                rec.doc_type = 'state'
            else:
                rec.doc_type = ''



class Organisation(models.Model):
    _name = "muk.doc.organisation"
    _description = "Organisation"

    name = fields.Char('Organisation Name')


class Sender(models.Model):
    _name = "muk.doc.sender"
    _description = "("

    name = fields.Char('Organisation Name')


class Department(models.Model):
    _name = "muk.doc.department"
    _description = "Department"

    name = fields.Char('Organisation Name')


class DocReceive(models.Model):
    _name = 'doc.rf'
    _description='Doc Receive From'

    name = fields.Char('Doc Receive From')


class DocType(models.Model):
    _name = 'doc.type'
    _description='Doc Receive From'

    name = fields.Char('Doc Type')
    doc_receive_id = fields.Many2one('doc.rf')


class SenderType(models.Model):
    _name = 'doc.sender.type'
    _description='Sender Type'

    name = fields.Char('Name')


class DeliveryMode(models.Model):
    _name = 'doc.delivery.mode'
    _description='Delivery Mode'

    name = fields.Char('Name')


class LanguageLetter(models.Model):
    _name = 'doc.letter.language'
    _description='Language of Letter'

    name = fields.Char('Name')


class LetterType(models.Model):
    _name = 'doc.letter.type'
    _description='Letter Type'

    name = fields.Char('Name')



class SenderMinistry(models.Model):
    _name = 'doc.sender.minstry'
    _description='Sender Minstry'

    name = fields.Char('Name')


class SenderDepartment(models.Model):
    _name = 'doc.sender.department'
    _description='Sender Department'

    name = fields.Char('Department Name')

class SenderDesignation(models.Model):
    _name = 'doc.sender.designation'
    _description='Sender Designation'

    name = fields.Char('Department Name')

class SenderAddress(models.Model):
    _name = 'doc.sender.address'
    _description='Sender Address'
    _rec_name='minstry'

    minstry = fields.Many2one('doc.sender.minstry')
    name = fields.Char('Address')
