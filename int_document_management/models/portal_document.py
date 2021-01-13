# -*- coding: utf-8 -*-
# Part of Synconics. See LICENSE file for full copyright and licensing details.

import base64
from PIL import Image
from odoo import models, fields
from odoo.tools.mimetypes import guess_mimetype


class PortalDocuments(models.Model):
    _name = 'intranett.portal.documents'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _parent_store = True
    _description = 'Portal Documents'

    name = fields.Char(string='Name', track_visibility='always')
    document_ids = fields.One2many('documents.attachment', 'parent_id', string='Document')
    description = fields.Text(string='Discription', track_visibility='always')
    is_published = fields.Boolean(string='Is Published', Default=False)
    document = fields.Binary(string='Document', attachment=True, track_visibility='always')
    # child_ids = fields.Many2many('intranett.portal.documents', 'chield_directory_rel')
    # parent_id = fields.Many2one('intranett.portal.documents', 'Parent Directory')

    parent_id = fields.Many2one('intranett.portal.documents', string='Parent Directory', index=True, ondelete="cascade")
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many('intranett.portal.documents', 'parent_id', string='Children Directory')

    state = fields.Selection(
        [('draft', 'Draft'), ('verification_pending', 'Verification Pending'), ('to_publish', 'To Publish'), ('published', 'Published'), ('cancelled', 'Cancelled')
         ], required=True, default='draft', string='Status', track_visibility='always')

    def _get_image(self):
        image_base64 = base64.b64decode(self.document)
        mimetype = guess_mimetype(image_base64)
        imgext = '.' + mimetype.split('/')[1]
        final_name = 'file_%s.png' % imgext.replace('.', '')
        return final_name

    def _get_size(self):
        image_base64 = base64.b64decode(self.document)
        return round(len(image_base64) / 1000000, 2)

    def button_submit(self):
        for rec in self:
            rec.write({'state': 'verification_pending'})

    def button_verify(self):
        for rec in self:
            rec.write({'state': 'to_publish'})

    def button_publish(self):
        for rec in self:
            rec.is_published = True
            rec.write({'state': 'published'})

    def button_unpublish(self):
        for rec in self:
            rec.is_published = False
            rec.write({'state': 'draft'})

    def button_cancel(self):
        for rec in self:
            rec.write({'state': 'cancelled'})

    def get_path(self):
        folders = self.env['intranett.portal.documents']
        most_parent = False
        category_id = self
        if category_id:
            while not most_parent:
                if category_id.parent_id:
                    folders += category_id
                    category_id = category_id.parent_id
                else:
                    most_parent = category_id
                    folders += category_id
        print('>>>>>>>>>>>>>>>>>>>', folders)
        return folders.sorted()


class Documents(models.Model):
    _name = 'documents.attachment'

    name = fields.Char(string='Name')
    document = fields.Binary(string='Document', attachment=True, track_visibility='always')
    parent_id = fields.Many2one('intranett.portal.documents', string='Parent Directory')


    def _get_image(self):
        image_base64 = base64.b64decode(self.document)
        mimetype = guess_mimetype(image_base64)
        imgext = '.' + mimetype.split('/')[1]
        final_name = 'file_%s.png' % imgext.replace('.', '')
        return final_name

    def _get_size(self):
        image_base64 = base64.b64decode(self.document)
        return round(len(image_base64) / 1000000, 2)






