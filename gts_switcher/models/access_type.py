from odoo import models, tools, fields, api, _

class AccessType(models.Model):
    _name = 'access.type'

    name = fields.Char("Access")
