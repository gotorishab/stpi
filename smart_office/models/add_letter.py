from odoo import models, api, fields,_
from datetime import datetime, date, timedelta
import requests
import json

class AddLetter(models.Model):
    _inherit = "muk_dms.file"
    _rec_name = "name"
    _description = "Add Document/Letter"

    current_owner_id = fields.Many2one('res.users', 'Current Owner')

    tracker_ids = fields.One2many('muk.letter.tracker', 'letter_id')


    @api.model
    def create(self, vals):
        if self._context.get('smart_office_incoming_letter', False):
            vals['directory'] = self.env.ref('smart_office.smart_office_directory').id
            vals['responsible_user_id'] = self.env.user.id
        # if 'code' not in vals or vals['code'] == _('New'):
        #     vals['name'] = self.env['ir.sequence'].next_by_code('muk.dms.letter') or _('New')
        res = super(AddLetter, self).create(vals)
        if self._context.get('smart_office_incoming_letter', False):
            self.env['muk.letter.tracker'].create(dict(
                type='create',
                # from_id=False,
                to_id=self.env.user.id,
                letter_id=res.id
            ))
            res.directory.doc_file_preview = res.content
        return res

    # @api.constrains('name')
    # def _check_name(self):
    #     pass

    # Letter Information
    responsible_user_id = fields.Many2one('res.users', default=lambda self:self.env.user.id)
    document_type = fields.Selection([('letter', 'Letter'),
                                      ('document', 'Document')], default='letter')
    # doc_no = fields.Char()

    # doc_tags = fields.Text('Tags')
    doc_enclosure = fields.Selection([('book', 'Book'),
                                     ('service_book', 'Service Book'),
                                     ('cd_dvd', 'CD or DVD')])
    doc_enclosure_detail = fields.Text('Enclosure Details')

    file_track_ids = fields.One2many('file.tracking.information', 'create_let_id', string = "files")
    pdf_file = fields.Binary(related='content')
    folder_id = fields.Many2one('folder.master', string="Folder Name")

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
    doc_letter_details = fields.Text('Letter Details')
    file_holder = fields.Many2one('res.users', string = "File holder")

    # doc_letter_category = fields.Selection([('salary', 'Salary'),
    #                                         ('employee_details', 'Employee Details'),
    #                                         ('forest_conservation', 'Forest Conservation'),
    #                                         ('legislative_sec', 'Legislative Sec'),
    #                                         ('view_sec', 'View Sec'),
    #                                         (('lr_sec', 'LR Sec'))], default='salary')

    reference_ids = fields.Many2many('muk_dms.file', 'muk_dms_file_rel', 'field1', 'field2', 'Reference Letter', domain="[('id', '!=', id)]")

    forward_from_id = fields.Many2one('res.users', 'Forward From', default=lambda self:self.env.user.id)
    forward_to_id = fields.Many2one('res.users', 'Forward To')


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
