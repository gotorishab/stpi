from odoo import fields, models, api, _


class InheritResCity(models.Model):
    _inherit = 'res.city'
    _description = 'Res City'

    metro = fields.Boolean('Metro City?')
    city_tier = fields.Selection([('a', 'A'),
                                  ('a1', 'A1'),
                                  ('other', 'Other'),
                                  ], string='City Tier', store=True)
    employee_hra_cat = fields.Selection([('x', 'X'),
                                         ('y', 'Y'),
                                         ('z', 'Z'),
                                         ], string='HRA Category')