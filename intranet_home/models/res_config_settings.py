# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    work_anniversary_year = fields.Integer('Work Anniversary Years ', default=1, config_parameter='intranet_home.work_anniversary_year')