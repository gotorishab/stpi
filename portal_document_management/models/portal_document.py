# -*- coding: utf-8 -*-
# Part of Synconics. See LICENSE file for full copyright and licensing details.

import base64
from PIL import Image
from odoo import models, fields
from odoo.tools.mimetypes import guess_mimetype


class PortalDocuments(models.Model):
    _name = 'portal.documents'
    _description = 'Portal Documents'

    name = fields.Char(string='Name')
    type_id = fields.Char(string='Type')
    document = fields.Binary(string='Document',attachment=True)
    description = fields.Text(string='Discription')
    is_published = fields.Boolean(string='Is Published', Default=False)

    def _get_image(self):
        image_base64 = base64.b64decode(self.document)
        mimetype = guess_mimetype(image_base64)
        imgext = '.' + mimetype.split('/')[1]
        final_name = 'file_%s.png' % imgext.replace('.', '')
        return final_name

    def _get_size(self):
        image_base64 = base64.b64decode(self.document)
        return round(len(image_base64) / 1000000, 2)

class DocumentsType(models.Model):
    _name = 'documents.type'

    name = fields.Char(string='Name')





