# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _
import base64
from PIL import Image
from odoo.tools.mimetypes import guess_mimetype
from odoo.exceptions import ValidationError, UserError



class Events(models.Model):
    _inherit = "event.event"


    image = fields.Image()

    @api.model
    def create(self, vals):
        res = super(Events, self).create(vals)
        print('------------------')
        size = 0
        if self.image:
            image_base64 = base64.b64decode(self.image)
            size = round(len(image_base64) / 1000000, 2)
            serch_id = self.env['vardhman.event.photograph'].sudo().search([], limit=1)
            print('=======================',serch_id)
            print('============size===========',size)
            print('==========documents_binary_min_size=============',serch_id.documents_binary_min_size)
            print('==========documents_binary_max_size=============',serch_id.documents_binary_max_size)

            if serch_id.documents_binary_min_size > size or serch_id.documents_binary_max_size < size:
                raise ValidationError("Size Invalid")
        return res



class EventTag(models.Model):
    _inherit = "event.tag"

    front_type = fields.Selection([
        ('event', 'Event'),
        ('subevent', 'SubEvent'),
    ], string='Front Type')

    parent_tag_id = fields.Many2one('event.tag', string='Event Category')

    @api.onchange('name')
    @api.constrains('name')
    def get_category_f_name(self):
        for rec in self:
            votes = self.env['event.tag.category'].search([('name', '=', 'Activity')], limit=1
                                                           )
            print('============================',votes)
            if votes:
                for isss in votes:
                    rec.category_id=isss.id


    def name_get(self):
        return [(tag.id, "%s" % (tag.name)) for tag in self]