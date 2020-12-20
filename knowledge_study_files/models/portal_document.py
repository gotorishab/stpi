# -*- coding: utf-8 -*-
# Part of Synconics. See LICENSE file for full copyright and licensing details.

import base64
from PIL import Image
from odoo import models, fields
from odoo.tools.mimetypes import guess_mimetype


class PortalDocuments(models.Model):
    _name = 'portal.study.files'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Portal Documents'

    name = fields.Char(string='Name', track_visibility='always')
    type_id = fields.Many2one('documents.study.type',string='Type', track_visibility='always')
    document = fields.Binary(string='Document',attachment=True, track_visibility='always')
    description = fields.Text(string='Discription', track_visibility='always')
    is_published = fields.Boolean(string='Is Published', Default=False)

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


class DocumentsType(models.Model):
    _name = 'documents.study.type'

    name = fields.Char(string='Name')





