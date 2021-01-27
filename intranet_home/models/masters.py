from odoo import api, fields, models, _
from odoo.http import request


class VardhmanStoryCategory(models.Model):
    _name = "vardhman.story.category"
    _description = "Vardhman Story Category"

    name = fields.Text('Name')

class BlogTag(models.Model):
    _inherit = "blog.tag"

    front_type = fields.Selection([
        ('news', 'News'),
        ('story', 'Story'),
        ('announcement', 'Announcement'),
        ('idea', 'Idea'),
        ('subidea', 'Idea SubIdea'),
        ('calendar_1', 'Calendar Image First'),
        ('calendar_2', 'Calendar Image Second'),
        ('calendar_3', 'Calendar Image Third'),
    ], string='Front Type')

    parent_tag_id = fields.Many2one('blog.tag', string='Idea Category')


class HrDepartment(models.Model):
    _inherit = "hr.department"

    unit_id = fields.Many2one('vardhman.unit.master',string='Unit')


class VardhmanSuggestionType(models.Model):
    _name = "vardhman.suggestion.type"
    _description = "Vardhman Idea/Suggestion Type"

    name = fields.Text('Ideas/ Suggestion Type :')

class VardhmanSuggestionSubType(models.Model):
    _name = "vardhman.suggestion.subtype"
    _description = "Vardhman Idea/Suggestion Type"

    name = fields.Many2one('vardhman.suggestion.type',string='Ideas/ Suggestion Type :')
    subname = fields.Text('Idea/Suggestion Sub Type :')


class VardhmanEventCategory(models.Model):
    _name = "vardhman.event.category"
    _description = "Vardhman event Category"

    name = fields.Char('Event Category :')


class VardhmanEventSubCategory(models.Model):
    _name = "vardhman.event.subcategory"
    _description = "Vardhman Suggestion Type"

    event = fields.Many2one('vardhman.event.category',string='Event Type :')
    name = fields.Char('Event Sub Type :')


class VardhmanStoryRejection(models.Model):
    _name = "vardhman.story.rejection"
    _description = "Vardhman Story Rejection"

    name = fields.Text('Story Rejection Reason :')

class VardhmanStoryPostSetting(models.Model):
    _name = "vardhman.story.postuser"
    _description = "Vardhman Story Post for user"

    user_id = fields.Many2one('res.users',string='User :')
    enable_security = fields.Boolean('Enable Story Post')
    word_limit = fields.Integer('Word Limit(Text)')

class VardhmanIdeaSharing(models.Model):
    _name = "vardhman.idea.reason"
    _description = "Vardhman Idea/Suggestion Sharing"

    user_id = fields.Many2one('res.users',string='User :')
    enable_security = fields.Boolean('Enable Idea/Suggestion Sharing')
    word_limit = fields.Integer('Word Limit for Idea(Text)')


class VardhmanIdeaRejection(models.Model):
    _name = "vardhman.idea.rejection"
    _description = "Vardhman Idea/Suggestion Rejection Reason"

    name = fields.Char('Idea Rejection Reason :')


class VardhmanUnitMaster(models.Model):
    _name = "vardhman.unit.master"
    _description = "Vardhman unit master"

    name = fields.Char('Unit Name:')
    Description = fields.Char('Description')


class VardhmanDepartmentMaster(models.Model):
    _name = "vardhman.department.master"
    _description = "Vardhman Department master"

    name = fields.Char('Department Name:')
    unit_id = fields.Many2one('vardhman.unit.master','Unit:')



class VardhmanDisForum(models.Model):
    _name = "vardhman.disfor.group"
    _description = "Discussion Forum Group Type"

    name = fields.Char('Discussion Forum Group Type')
    user_ids = fields.Many2many('res.users', string='Users:')
    group_id = fields.Many2one('res.groups', string='Group:')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('group_created', 'Group Created'),
    ], string='state', default='draft')

    def create_group(self):
        for rec in self:
            grp = self.env['res.groups'].create({
                'name': str(rec.name),
            })
            for user in self.user_ids:
                grp.users = [(4, user.id)]
            rec.group_id = grp.id
            rec.write({'state': 'group_created'})


class VardhmanEventPhotograph(models.Model):
    _name = "vardhman.event.photograph"
    _description = "Event Photograph"

    documents_binary_min_size = fields.Integer(
        string="Minimum Size",
        help="Defines the minimum upload size in MB.")

    documents_binary_max_size = fields.Integer(
        string="Maximum Size",
        help="Defines the maximum upload size in MB.")




class VardhmanLimitPhotograph(models.Model):
    _name = "vardhman.limit.photograph"
    _description = "Limit of Photograph"

    user_id = fields.Many2one('res.users',string='User')
    documents_binary_max_size = fields.Integer(
        string="Maximum Photo Limit",
        help="Defines the maximum upload size in MB.")


