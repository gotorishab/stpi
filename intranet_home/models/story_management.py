from odoo import api, fields, models, _
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo import http


class VardhmanStoryCategory(models.Model):
    _name = "vardhman.create.blogpost"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Create Story Post"


    def _default_unit(self):
        return self.env['vardhman.unit.master'].sudo().search([('id', '=', self.env.user.unit_id.id)], limit=1)


    unit_id = fields.Many2one('vardhman.unit.master',string='Unit', default=_default_unit)
    tag_ids = fields.Many2many('blog.tag', string='Story Category')
    name = fields.Char('Title')
    description = fields.Html('Description')
    post_id = fields.Many2one('blog.post', string='Story')
    reason_des = fields.Many2one('vardhman.story.rejection', string='Reason for Rejection')
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
        ('pending_approval1', 'Reviewed by Unit Level Moderator'),
        ('pending_approval2', 'Reviewed by Central Level Moderator'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='state', default='draft', track_visibility='always')


    def button_send_for_approval(self):
        for rec in self:
            cout = 0
            max_word_limit_idea = 0
            blog_id = self.env['res.company'].sudo().search(
                [
                    ('id', '=', rec.env.user.company_id.id),
                ], limit=1)
            print('=======================================', blog_id)
            # for numb in blog_id:
            if blog_id:
                for numb in blog_id:
                    print('=======================================', blog_id)
                    if numb.enable_story_post == True:
                        max_word_limit_idea = blog_id.max_word_limit_story
                        for ct in rec.description:
                            cout += 1
                        if cout > max_word_limit_idea:
                            raise ValidationError(
                                _('Word Limit Exceeded'))
                        else:
                            bg_id = self.env['vardhman.block.user'].sudo().search(
                                [
                                    ('user_id', '=', rec.env.user.id),
                                    ('activity', '=', 'story'),
                                ], limit=1)
                            if bg_id:
                                raise ValidationError(
                                    _('You are blocked from posting.'))
                            else:
                                rec.write({'state': 'pending_approval'})
                    else:
                        raise ValidationError(
                            _('Story Posting is not allowed'))



    def button_review_unit(self):
        for rec in self:
            rec.write({'state': 'pending_approval1'})



    def button_review_central(self):
        for rec in self:
            rec.write({'state': 'pending_approval2'})


    def button_reject(self):
        for rec in self:
            rc = {
                'name': 'Reason for Rejection',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('intranet_home.view_reason_revert_story_wizard').id,
                'res_model': 'rejectstory.wizard',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': {
                    'default_res_model': self._name,
                    'default_res_id': self.id,
                }
            }
            return rc
            # rec.write({'state': 'rejected'})


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
                'content': rec.description,
                'blog_id': bl_id,
            })
            for user in self.tag_ids:
                grp.tag_ids = [(4, user.id)]
            rec.post_id = grp.id
            grp.is_published = True
            rec.write({'state': 'approved'})

    def delete_story(self):
        for rec in self:
            rec.post_id.sudo().unlink()
            rec.sudo().unlink()
            return {
                'name': 'Story - Approved',
                'view_mode': 'tree,form',
                'res_model': 'vardhman.create.blogpost',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': [('state', '=', 'approved')],
            }


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
    indent_user_type = fields.Selection([
        ('all', 'All Individual Users'),
        ('specific', 'Specific Group of users'),
    ], string='Intended User Type',default='all')
    group_ids = fields.Many2many('res.groups',string='Groups')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending_approval', 'Approval Pending'),
        ('approved', 'Published'),
        ('rejected', 'Rejected'),
    ], string='state', default='draft')


    def button_send_for_approval(self):
        for rec in self:
            rec.write({'state': 'pending_approval'})

    #
    # def button_send_for_approval(self):
    #     for rec in self:
    #         blog_id = self.env['vardhman.block.user'].sudo().search(
    #             [
    #                 ('user_id', '=', rec.env.user.id),
    #                 ('activity', '=', 'blog'),
    #             ], limit=1)
    #         if blog_id:
    #             raise ValidationError(
    #                 _('You are blocked from posting.'))
    #         else:
    #             rec.write({'state': 'pending_approval'})
    #

    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})

    # def publish_announcement(self):
    #     for rec in self:
    #         if rec.indent_user_type == 'specific':
    #             for line in self.env['res.users'].search([('groups_id', 'in', rec.group_ids.ids), ('id', '!=', self.env.user.id)]):
    #                 template = self.env.ref('intranet_home.email_template_edi_announcement', raise_if_not_found=False)
    #                 if template:
    #                     ctx = {'description': rec.description, 'name': rec.name, 'partner_name': line.name,}
    #                     template.with_context(ctx).send_mail(line.id, force_send=False, raise_exception=False)




    def button_approved(self):
        for rec in self:
            if rec.indent_user_type == 'specific':
                user_ids = self.env['res.users'].search([('groups_id', 'in', rec.group_ids.ids), ('id', '!=', self.env.user.id)])
            elif rec.indent_user_type == 'all':
                user_ids = self.env['res.users'].search([('id', '!=', self.env.user.id)])
            for line in user_ids:
                template = self.env.ref('intranet_home.email_template_edi_announcement', raise_if_not_found=False)
                if template:
                    ctx = {'description': rec.description, 'rec':rec, 'name': rec.name, 'partner_name': line.name}
                    template.with_context(ctx).send_mail(line.id, force_send=False, raise_exception=False)
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
                'announcement_id': rec.id,
                'content': rec.description,
            })
            rec.post_id = grp.id
            grp.is_published = True
            rec.write({'state': 'approved'})



    def create_notification(self):
        return {

            'effect': {

                'fadeout': 'slow',

                'message': 'Enter your custom message here',

                'type': 'rainbow_man',

            }

        }
    #
    # def create_notification(self):
    #    message = {
    #
    #        'type': 'ir.actions.client',
    #
    #        'tag': 'display_notification',
    #
    #        'params': {
    #
    #            'title': _('Announcement!'),
    #
    #            'message': 'You have an announcement. Please open latest appointment to see',
    #
    #            'sticky': False,
    #
    #        }
    #
    #    }
    #
    #    return message

class VardhmanIdeaShare(models.Model):
    _name = "vardhman.create.blogidea"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Share Ideas and Suggestions"

    ideasugg_id = fields.Many2one('blog.tag', string='Idea Category')
    subtype_id = fields.Many2one('blog.tag', string='Idea Sub-Category')
    name = fields.Text('Ideas and Suggestions')
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
                'front_type': rec.front_type,
                'content': rec.description,
                'blog_id': bl_id,
            })
            grp.tag_ids = [(4, rec.ideasugg_id.id)]
            grp.tag_ids = [(4, rec.subtype_id.id)]
            rec.post_id = grp.id
            grp.is_published = True
            rec.write({'state': 'approved'})


class VardhmanNewsCategory(models.Model):
    _name = "vardhman.create.newspost"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Create news Post"


    def _default_unit(self):
        return self.env['vardhman.unit.master'].sudo().search([('id', '=', self.env.user.unit_id.id)], limit=1)


    unit_id = fields.Many2one('vardhman.unit.master',string='Unit', default=_default_unit)
    # tag_ids = fields.Many2many('blog.tag', string='Story Category')
    name = fields.Char('Title')
    description = fields.Html('Description')
    post_id = fields.Many2one('blog.post', string='News')
    # reason_des = fields.Many2one('vardhman.story.rejection', string='Reason for Rejection')
    front_type = fields.Selection([
        ('news', 'News'),
        ('story', 'Story'),
        ('announcement', 'Announcement'),
        ('idea', 'Idea'),
        ('calendar_1', 'Calendar Image First'),
        ('calendar_2', 'Calendar Image Second'),
        ('calendar_3', 'Calendar Image Third'),
    ], string='Front Type',default='news')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('deleted', 'Deleted'),
    ], string='state', default='draft', track_visibility='always')


    def button_publish(self):
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
                'content': rec.description,
            })
            rec.post_id = grp.id
            grp.is_published = True
            rec.write({'state': 'published'})


    def button_delete(self):
        for rec in self:
            rec.post_id.sudo().unlink()
            rec.write({'state': 'deleted'})
            rec.sudo().unlink()
            return {
                'name': 'Story - Approved',
                'view_mode': 'tree,form',
                'res_model': 'vardhman.create.newspost',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': [('state', '=', 'approved')],
            }


class VardhmanCmdCategory(models.Model):
    _name = "vardhman.create.cmdpost"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Create cmd Post"


    def _default_unit(self):
        return self.env['vardhman.unit.master'].sudo().search([('id', '=', self.env.user.unit_id.id)], limit=1)


    unit_id = fields.Many2one('vardhman.unit.master',string='Unit', default=_default_unit)
    # tag_ids = fields.Many2many('blog.tag', string='Story Category')
    name = fields.Char('Title')
    description = fields.Html('Description')
    post_id = fields.Many2one('blog.post', string='cmd')
    # reason_des = fields.Many2one('vardhman.story.rejection', string='Reason for Rejection')
    front_type = fields.Selection([
        ('news', 'News'),
        ('story', 'Story'),
        ('announcement', 'Announcement'),
        ('idea', 'Idea'),
        ('calendar_1', 'Calendar Image First'),
        ('calendar_2', 'Calendar Image Second'),
        ('calendar_3', 'Calendar Image Third'),
    ], string='Front Type',default='calendar_1')
    date_from = fields.Date(strign="From Date")
    date_to = fields.Date(strign="To Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('deleted', 'Deleted'),
    ], string='state', default='draft', track_visibility='always')


    def button_publish(self):
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
                'content': rec.description,
                'date_from': rec.date_from,
                'date_to': rec.date_to,
            })
            rec.post_id = grp.id
            grp.is_published = True
            rec.write({'state': 'published'})


    def button_delete(self):
        for rec in self:
            rec.post_id.sudo().unlink()
            rec.write({'state': 'deleted'})
            rec.sudo().unlink()
            return {
                'name': 'Story - Approved',
                'view_mode': 'tree,form',
                'res_model': 'vardhman.create.cmdpost',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': [('state', '=', 'approved')],
            }

