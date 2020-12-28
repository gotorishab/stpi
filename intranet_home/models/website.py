# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.http import request
from datetime import datetime
from odoo.exceptions import ValidationError, UserError


class Website(models.Model):
    _inherit = "website"

    front_title = fields.Char('Title')
    front_icon = fields.Binary('Icon')
    front_url = fields.Char('URL')
    front_description = fields.Text('Description')