# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.http import request
from datetime import datetime
from odoo.exceptions import ValidationError, UserError


class BlogBlog(models.Model):
    _inherit = "blog.blog"

    front_type = fields.Selection([
        ('news', 'News'),
        ('story', 'Story'),
        ('announcement', 'Announcement'),
        ('idea', 'Idea'),
        ('cmd', 'CMD Message'),
    ], string='Front Type')

    @api.constrains('front_type')
    def unique_front_type(self):
        for rec in self:
            count = 0
            search_id = self.env['blog.blog'].sudo().search(
                [
                    ('front_type', '=', rec.front_type),
                    ('id', '!=', rec.id)
                ])
            if search_id:
                raise ValidationError("You have already applied for this front type")