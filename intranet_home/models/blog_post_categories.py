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
        ('calendar_1', 'Calendar Image First'),
        ('calendar_2', 'Calendar Image Second'),
        ('calendar_3', 'Calendar Image Third'),
    ], string='Front Type')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending_approval', 'Approval Pending'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('unpublished', 'Unpublished'),
    ], string='state',default='draft')


    @api.onchange('blog_id')
    @api.constrains('blog_id')
    def get_front_type(self):
        for rec in self:
            if rec.blog_id:
                if rec.blog_id.front_type:
                    rec.front_type = rec.blog_id.front_type


    def button_send_for_approval(self):
        for rec in self:
            rec.write({'state': 'pending_approval'})


    def button_approved(self):
        for rec in self:
            rec.write({'state': 'approved'})



    def button_publish(self):
        for rec in self:
            rec.is_published = True
            rec.write({'state': 'approved'})


    def button_unpublish(self):
        for rec in self:
            rec.is_published = False