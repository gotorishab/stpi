from odoo import api, fields, models, _
from odoo.http import request


class VardhmanStoryCategory(models.Model):
    _name = "vardhman.block.user"
    _description = "Vardhman Story Block User"

    user_id = fields.Many2one('res.users', string='User')

    activity = fields.Selection([
        ('story', 'Story'),
        ('idea', 'Idea')
    ], string='Activity')




class VardhmanIdeaSuggestion(models.Model):
    _name = "vardhman.handle.ideasugg"
    _description = "Handle Idea/Suggestion Block User"

    ideasugg_id = fields.Many2one('blog.tag', string='Idea/Suggestion Type')
    subtype_id = fields.Many2one('blog.tag', string='Idea/Suggestion SubType')
    user_ids = fields.Many2many('res.users', string='User')
    group_id = fields.Many2one('res.groups', string='Select Role')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
    ], string='state', default='draft')

    def button_submit(self):
        for res in self:
            if res.group_id:
                for user in res.user_ids:
                    res.group_id.users = [(4, user.id)]
            res.write({'state': 'submitted'})





class VardhmanRenderSurvey(models.Model):
    _name = "vardhman.render.survey"
    _description = "Render access to create survey"

    user_id = fields.Many2one('res.users', string='User')
    group_id = fields.Many2one('res.groups', string='Group')

class VardhmanLikePosts(models.Model):
    _name = "vardhman.like.blogforum"
    _description = "Likes and Comments for post stories"

    enable_like = fields.Boolean('Enable Likes')
    enable_comments = fields.Boolean('Enable Comments')
