from odoo import api, fields, models, _
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo import http

class VardhmanIdeaShare(models.Model):
    _name = "vardhman.create.blogidea"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Share Ideas and Suggestions"
    _order = 'active desc'

    ideasugg_id = fields.Many2one('blog.tag', string='Idea Category')
    active = fields.Boolean('Active')
    subtype_id = fields.Many2one('blog.tag', string='Idea Sub-Category')
    name = fields.Text('Ideas and Suggestions')
    idea_description = fields.Text('Idea Description')
    tan_nontan = fields.Selection([
        ('Tangible', 'Tangible'),
        ('non_tan', 'Non-Tangible'),
    ], string='Benefit Type')
    benefits = fields.Text('Benefit')
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


    def toggle_active(self):
        """ Inverse the value of the field ``active`` on the records in ``self``. """
        for record in self:
            record.active = not record.active
            if record.post_id:
                if record.active == True:
                    record.post_id.is_published = True
                else:
                    record.post_id.is_published = False



    def button_send_for_approval(self):
        for rec in self:
            cout = 0
            max_word_limit_idea = 0
            blog_id = self.env['res.company'].sudo().search(
                [
                    ('id', '=', rec.env.user.company_id.id),
                ],limit=1)
            print('=======================================',blog_id)
            # for numb in blog_id:
            if blog_id:
                for numb in blog_id:
                    print('=======================================', blog_id)
                    if numb.enable_idea_post == True:
                        max_word_limit_idea = blog_id.max_word_limit_idea
                        for ct in rec.name:
                            cout+=1
                        if cout > max_word_limit_idea:
                            raise ValidationError(
                                _('Word Limit Exceeded'))
                        else:
                            bg_id = self.env['vardhman.block.user'].sudo().search(
                                [
                                    ('user_id', '=', rec.env.user.id),
                                    ('activity', '=', 'idea'),
                                ], limit=1)
                            if bg_id:
                                raise ValidationError(
                                    _('You are blocked from posting.'))
                            else:
                                rec.write({'state': 'pending_approval'})
                            # rec.write({'state': 'pending_approval'})
                    else:
                        raise ValidationError(
                            _('Idea sharing is not allowed'))


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
                'content': str(rec.name),
                'front_type': rec.front_type,
                'blog_id': bl_id,
            })
            grp.tag_ids = [(4, rec.ideasugg_id.id)]
            grp.tag_ids = [(4, rec.subtype_id.id)]
            rec.post_id = grp.id
            grp.is_published = True
            rec.write({'state': 'approved'})
            rec.active = True
