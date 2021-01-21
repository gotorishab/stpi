from odoo import api, fields, models, _
from odoo.http import request


class VardhmanStoryCategory(models.Model):
    _name = "vardhman.create.disforum"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Vardhman Create Blog Post"

    discussion_group_type = fields.Selection([
        ('Private', 'Private'),
        ('Public', 'Public'),
        ('Isolated', 'Isolated')
    ], string='Discussion Group Type')
    name = fields.Char('Title')
    description = fields.Text('Description')
    department_id = fields.Many2one('hr.department',string='Department')
    unit_id = fields.Many2one('vardhman.unit.master',string='Unit')
    # tag_ids = fields.Many2many('blog.tag', string='Story Category')

    forum_id = fields.Many2one('forum.post', string='Story')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending_approval', 'Approval Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='state', default='draft')

    front_type = fields.Selection([
        ('discussion_forum', 'Discussion Forum')
    ], string='Front Type',default='discussion_forum')



    def button_send_for_approval(self):
        for rec in self:
            rec.write({'state': 'pending_approval'})


    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})


    def button_approved(self):
        for rec in self:
            bl_id = 1
            blog_id = self.env['forum.forum'].sudo().search(
                [
                    ('front_type', '=', rec.front_type)
                ], limit=1)
            if blog_id:
                for bl in blog_id:
                    bl_id = bl.id
            grp = self.env['forum.post'].create({
                'name': str(rec.name),
                'forum_id': bl_id,
            })
            # for user in self.tag_ids:
            #     grp.tag_ids = [(4, user.id)]
            rec.forum_id = grp.id
            grp.state='active'
            rec.write({'state': 'approved'})
