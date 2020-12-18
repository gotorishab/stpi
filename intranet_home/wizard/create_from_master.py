from odoo import fields, models, api
from datetime import datetime

class CreateStoryCategory(models.TransientModel):
    _name = 'wizard.story.category'
    _description = "Vardhman Story Category"

    name = fields.Char('Name')


    def confirm_button(self):
        if self:
            master_id = self.env['vardhman.story.category'].create({
                'name': self.name,

            })
            form_view = self.env.ref('intranet_home.view_vardhman_story_form')
            tree_view = self.env.ref('intranet_home.view_vardhman_story_list')
            value = {
                'domain': str([('id', '=', master_id.id)]),
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'vardhman.story.category',
                'view_id': False,
                'views': [(form_view and form_view.id or False, 'form'),
                          (tree_view and tree_view.id or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': master_id.id,
                'target': 'current',
                'nodestroy': True
            }
            return value



class VardhmanSuggestionType(models.Model):
    _name = "wizard.suggestion.type"
    _description = "wizard Suggestion Type"

    name = fields.Char('Ideas/ Suggestion Type :')
    subname = fields.Char('Idea/Suggestion Sub Type :')


    def confirm_button(self):
        if self:
            master_id = self.env['vardhman.suggestion.category'].create({
                'name': self.name,
                'subname': self.subname,

            })
            form_view = self.env.ref('intranet_home.foldermaster_form_view')
            tree_view = self.env.ref('intranet_home.foldermaster_tree_view1')
            value = {
                'domain': str([('id', '=', master_id.id)]),
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'vardhman.suggestion.category',
                'view_id': False,
                'views': [(form_view and form_view.id or False, 'form'),
                          (tree_view and tree_view.id or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': master_id.id,
                'target': 'current',
                'nodestroy': True
            }
            return value


class VardhmanEventCategory(models.Model):
    _name = "wizard.event.category"
    _description = "wizard event Category"

    name = fields.Char('Event Category :')
    subname = fields.Char('Event Sub Category :')


    def confirm_button(self):
        if self:
            master_id = self.env['vardhman.event.category'].create({
                'name': self.name,
                'subname': self.subname,

            })
            form_view = self.env.ref('intranet_home.foldermaster_form_view')
            tree_view = self.env.ref('intranet_home.foldermaster_tree_view1')
            value = {
                'domain': str([('id', '=', master_id.id)]),
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'vardhman.event.category',
                'view_id': False,
                'views': [(form_view and form_view.id or False, 'form'),
                          (tree_view and tree_view.id or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': master_id.id,
                'target': 'current',
                'nodestroy': True
            }
            return value


class VardhmanStoryRejection(models.Model):
    _name = "wizard.story.rejection"
    _description = "wizard Story Rejection"

    name = fields.Char('Story Rejection Reason :')


    def confirm_button(self):
        if self:
            master_id = self.env['vardhman.story.rejection'].create({
                'name': self.name,

            })
            form_view = self.env.ref('intranet_home.foldermaster_form_view')
            tree_view = self.env.ref('intranet_home.foldermaster_tree_view1')
            value = {
                'domain': str([('id', '=', master_id.id)]),
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'vardhman.story.rejection',
                'view_id': False,
                'views': [(form_view and form_view.id or False, 'form'),
                          (tree_view and tree_view.id or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': master_id.id,
                'target': 'current',
                'nodestroy': True
            }
            return value

class wizardIdeaRejection(models.Model):
    _name = "wizard.idea.rejection"
    _description = "wizard Idea Rejection"

    name = fields.Char('Idea Rejection Reason :')



    def confirm_button(self):
        if self:
            master_id = self.env['vardhman.idea.rejection'].create({
                'name': self.name,

            })
            form_view = self.env.ref('intranet_home.foldermaster_form_view')
            tree_view = self.env.ref('intranet_home.foldermaster_tree_view1')
            value = {
                'domain': str([('id', '=', master_id.id)]),
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'vardhman.idea.rejection',
                'view_id': False,
                'views': [(form_view and form_view.id or False, 'form'),
                          (tree_view and tree_view.id or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': master_id.id,
                'target': 'current',
                'nodestroy': True
            }
            return value


class wizardUnitMaster(models.Model):
    _name = "wizard.unit.master"
    _description = "wizard unit master"

    name = fields.Char('Unit Name:')
    Description = fields.Char('Description')

    def confirm_button(self):
        if self:
            master_id = self.env['vardhman.unit.master'].create({
                'name': self.name,
                'Description': self.Description,

            })
            form_view = self.env.ref('intranet_home.foldermaster_form_view')
            tree_view = self.env.ref('intranet_home.foldermaster_tree_view1')
            value = {
                'domain': str([('id', '=', master_id.id)]),
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'unit.master',
                'view_id': False,
                'views': [(form_view and form_view.id or False, 'form'),
                          (tree_view and tree_view.id or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': master_id.id,
                'target': 'current',
                'nodestroy': True
            }
            return value
