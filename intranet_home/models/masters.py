from odoo import api, fields, models, _
from odoo.http import request


class VardhmanStoryCategory(models.Model):
    _name = "vardhman.story.category"
    _description = "Vardhman Story Category"

    name = fields.Char('Name')


class VardhmanSuggestionType(models.Model):
    _name = "vardhman.suggestion.type"
    _description = "Vardhman Suggestion Type"

    name = fields.Char('Ideas/ Suggestion Type :')
    subname = fields.Char('Idea/Suggestion Sub Type :')


class VardhmanEventCategory(models.Model):
    _name = "vardhman.event.category"
    _description = "Vardhman event Category"

    name = fields.Char('Event Category :')
    subname = fields.Char('Event Sub Category :')



class VardhmanStoryRejection(models.Model):
    _name = "vardhman.story.rejection"
    _description = "Vardhman Story Rejection"

    name = fields.Char('Story Rejection Reason :')


class VardhmanIdeaRejection(models.Model):
    _name = "vardhman.idea.rejection"
    _description = "Vardhman Idea Rejection"

    name = fields.Char('Idea Rejection Reason :')


class VardhmanUnitMaster(models.Model):
    _name = "vardhman.unit.master"
    _description = "Vardhman unit master"

    name = fields.Char('Unit Name:')
    Description = fields.Char('Description')
