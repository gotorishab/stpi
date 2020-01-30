from odoo import _, api, fields, models

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    branch_id = fields.Many2one('res.branch', 'Branch', 
                                default=lambda self: self.env['res.users']._get_default_branch())
#   