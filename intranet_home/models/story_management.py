from odoo import api, fields, models, _
from odoo.http import request


class VardhmanStoryCategory(models.Model):
    _name = "vardhman.create.blogpost"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Vardhman Create Blog Post"

    tag_ids = fields.Many2many('blog.tag', string='Story Category')
    name = fields.Char('Title')
    description = fields.Html('Description')
    post_id = fields.Many2one('blog.post', string='Story')
    front_type = fields.Selection([
        ('news', 'News'),
        ('story', 'Story'),
        ('announcement', 'Announcement'),
        ('idea', 'Idea'),
        ('calendar_1', 'Calendar Image First'),
        ('calendar_2', 'Calendar Image Second'),
        ('calendar_3', 'Calendar Image Third'),
    ], string='Front Type',default='story')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending_approval', 'Approval Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='state', default='draft')


    def button_send_for_approval(self):
        for rec in self:
            rec.write({'state': 'pending_approval'})


    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})


    def button_approved(self):
        for rec in self:
            bl_id = 1
            blog_id = self.env['blog.blog'].sudo().search(
                [
                    ('front_type', '=', rec.front_type)
                ], limit=1)
            if blog_id:
                for bl in blog_id:
                    bl_id = bl.id
            grp = self.env['blog.post'].create({
                'name': str(rec.name),
                'front_type': rec.front_type,
                'blog_id': bl_id,
            })
            for user in self.tag_ids:
                grp.tag_ids = [(4, user.id)]
            rec.post_id = grp.id
            grp.is_published = True
            rec.write({'state': 'approved'})



class VardhmanAnnouncement(models.Model):
    _name = "vardhman.create.announcement"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Vardhman Create Blog Post"

    tag_ids = fields.Many2many('blog.tag', string='Announcement Category')
    name = fields.Char('Title')
    description = fields.Html('Description')
    post_id = fields.Many2one('blog.post', string='Story')
    front_type = fields.Selection([
        ('news', 'News'),
        ('story', 'Story'),
        ('announcement', 'Announcement'),
        ('idea', 'Idea'),
        ('calendar_1', 'Calendar Image First'),
        ('calendar_2', 'Calendar Image Second'),
        ('calendar_3', 'Calendar Image Third'),
    ], string='Front Type',default='announcement')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending_approval', 'Approval Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='state', default='draft')


    def button_send_for_approval(self):
        for rec in self:
            rec.write({'state': 'pending_approval'})


    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})


    def button_approved(self):
        for rec in self:
            bl_id = 1
            blog_id = self.env['blog.blog'].sudo().search(
                [
                    ('front_type', '=', rec.front_type)
                ], limit=1)
            if blog_id:
                for bl in blog_id:
                    bl_id = bl.id
            grp = self.env['blog.post'].create({
                'name': str(rec.name),
                'front_type': rec.front_type,
                'blog_id': bl_id,
            })
            for user in self.tag_ids:
                grp.tag_ids = [(4, user.id)]
            rec.post_id = grp.id
            grp.is_published = True
            rec.write({'state': 'approved'})



class VardhmanIdeaShare(models.Model):
    _name = "vardhman.create.blogidea"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Share Ideas and Suggestions"

    ideasugg_id = fields.Many2one('blog.tag', string='Idea/Suggestion Type')
    subtype_id = fields.Many2one('blog.tag', string='Idea/Suggestion SubType')
    name = fields.Char('Title')
    post_id = fields.Many2one('blog.post', string='Idea/Suggestion')
    front_type = fields.Selection([
        ('news', 'News'),
        ('story', 'Story'),
        ('announcement', 'Announcement'),
        ('idea', 'Idea'),
        ('calendar_1', 'Calendar Image First'),
        ('calendar_2', 'Calendar Image Second'),
        ('calendar_3', 'Calendar Image Third'),
    ], string='Front Type',default='idea')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending_approval', 'Approval Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='state', default='draft')


    def button_send_for_approval(self):
        for rec in self:
            rec.write({'state': 'pending_approval'})


    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})


    def button_approved(self):
        for rec in self:
            bl_id = 1
            blog_id = self.env['blog.blog'].sudo().search(
                [
                    ('front_type', '=', rec.front_type)
                ], limit=1)
            if blog_id:
                for bl in blog_id:
                    bl_id = bl.id
            grp = self.env['blog.post'].create({
                'name': str(rec.name),
                'front_type': rec.front_type,
                'blog_id': bl_id,
            })
            grp.tag_ids = [(4, rec.ideasugg_id.id)]
            grp.tag_ids = [(4, rec.subtype_id.id)]
            rec.post_id = grp.id
            grp.is_published = True
            rec.write({'state': 'approved'})
