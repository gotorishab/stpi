from odoo import api, fields, models,_


class Reason_wizard(models.TransientModel):
    _name = 'Child.block.year.wizard'

    ltc_id=fields.Many2one('employee.ltc.advance', 'LTC')
    block_year=fields.Many2one('block.year', 'Block year')
    child_block_year=fields.Many2one('child.block.year', 'Child Block year')


    def button_confirm(self):
        self.ltc_id.child_block_year = self.child_block_year.id