from odoo import fields, models, api, _


class InheritResCity(models.Model):
    _inherit = 'res.city'
    _description = 'Res City'

    metro = fields.Boolean('Metro City?')
    employee_hra_cat = fields.Selection([('x', 'X'),
                                         ('y', 'Y'),
                                         ('z', 'Z'),
                                         ], string='HRA Category')