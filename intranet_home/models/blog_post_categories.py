# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.http import request
from datetime import datetime
from odoo.exceptions import ValidationError, UserError


class BlogPost(models.Model):
    _inherit = "blog.post"

    front_type = fields.Selection([
        ('news', 'News'),
        ('story', 'Story'),
        ('announcement', 'Announcement'),
        ('idea', 'Idea'),
        ('cmd', 'CMD Message'),
    ], string='Front Type')

    @api.onchange('blog_id')
    @api.constrains('blog_id')
    def get_front_type(self):
        for rec in self:
            if rec.blog_id:
                if rec.blog_id.front_type:
                    rec.front_type = rec.blog_id.front_type

    def button_publish(self):
        for rec in self:
            rec.is_published = True

    def button_unpublish(self):
        for rec in self:
            rec.is_published = False