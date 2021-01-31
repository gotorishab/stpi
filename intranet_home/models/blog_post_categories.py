# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.http import request
from datetime import datetime
from odoo.exceptions import ValidationError, UserError


class BlogPost(models.Model):
    _inherit = "blog.post"


    def _get_user_vote(self):
        votes = self.env['blog.post.vote'].search_read([('blog_id', 'in', self._ids), ('user_id', '=', self._uid)], ['vote', 'blog_id'])
        mapped_vote = dict([(v['blog_id'][0], v['vote']) for v in votes])
        for vote in self:
            vote.user_vote = mapped_vote.get(vote.id, 0)

    @api.depends('vote_ids.vote')
    def _get_vote_count(self):
        read_group_res = self.env['blog.post.vote'].read_group([('blog_id', 'in', self._ids)], ['blog_id', 'vote'], ['blog_id', 'vote'], lazy=False)
        result = dict.fromkeys(self._ids, 0)
        for data in read_group_res:
            result[data['blog_id'][0]] += data['__count'] * int(data['vote'])
        for post in self:
            post.vote_count = result[post.id]

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

    # vote
    vote_ids = fields.One2many('blog.post.vote', 'blog_id', string='Votes')
    user_vote = fields.Integer('My Vote', compute='_get_user_vote')
    vote_count = fields.Integer('Total Votes', compute='_get_vote_count', store=True)
    can_upvote = fields.Boolean('Can Upvote', compute='_get_post_karma_rights', compute_sudo=False)
    can_downvote = fields.Boolean('Can Downvote', compute='_get_post_karma_rights', compute_sudo=False)
    date_from = fields.Date(strign="From Date", default=fields.Date.today())
    date_to = fields.Date(strign="To Date", default=fields.Date.today())


    @api.depends_context('uid')
    def _get_post_karma_rights(self):
        user = self.env.user
        is_admin = self.env.is_admin()
        # sudoed recordset instead of individual posts so values can be
        # prefetched in bulk
        for post, post_sudo in zip(self, self.sudo()):
            is_creator = post.create_uid == user
            post.can_upvote = is_admin or user.karma >= 1 or post.user_vote == -1
            post.can_downvote = is_admin or user.karma >= 1 or post.user_vote == 1

    def vote(self, upvote=True):
        Vote = self.env['blog.post.vote']
        vote_ids = Vote.search([('blog_id', 'in', self._ids), ('user_id', '=', self._uid)])
        new_vote = '1' if upvote else '-1'
        voted_blog_ids = set()
        if vote_ids:
            for vote in vote_ids:
                if upvote:
                    new_vote = '0' if vote.vote == '-1' else '1'
                else:
                    new_vote = '0' if vote.vote == '1' else '-1'
                vote.vote = new_vote
                voted_blog_ids.add(vote.blog_id.id)
        for blog_id in set(self._ids) - voted_blog_ids:
            for blog_id in self._ids:
                Vote.create({'blog_id': blog_id, 'vote': new_vote})
        return {'vote_count': self.vote_count, 'user_vote': new_vote}
    

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


class BlogVote(models.Model):
    _name = 'blog.post.vote'
    _description = 'Blog Vote'
    _order = 'create_date desc, id desc'

    blog_id = fields.Many2one('blog.post', string='Post', ondelete='cascade', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self._uid)
    vote = fields.Selection([('1', '1'), ('-1', '-1'), ('0', '0')], string='Vote', required=True, default='1')
    create_date = fields.Datetime('Create Date', index=True, readonly=True)
    blog_blog_id = fields.Many2one('blog.blog', string='Blog', related="blog_id.blog_id", store=True, readonly=False)
    recipient_id = fields.Many2one('res.users', string='To', related="blog_id.create_uid", store=True, readonly=False)

    _sql_constraints = [
        ('vote_uniq', 'unique (blog_id, user_id)', "Vote already exists !"),
    ]