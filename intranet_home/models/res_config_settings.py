# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    work_anniversary_year = fields.Integer('Work Anniversary Years ', default=1, config_parameter='intranet_home.work_anniversary_year')
    enable_story_post = fields.Boolean('Enable Story Post ', default=False, config_parameter='intranet_home.enable_story_post')
    max_word_limit_story = fields.Integer('Maximum word limit ', default=1, config_parameter='intranet_home.max_word_limit_story')
    enable_idea_post = fields.Boolean('Enable Idea/Suggestion Post ', default=False, config_parameter='intranet_home.enable_idea_post')
    max_word_limit_idea = fields.Integer('Maximum word limit ', default=1, config_parameter='intranet_home.max_word_limit_idea')
    enable_like_stories = fields.Boolean('Enable Likes ', config_parameter='intranet_home.enable_like')
    enable_comments_stories = fields.Boolean('Enable Comments ', config_parameter='intranet_home.enable_comments')