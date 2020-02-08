from odoo import models,fields,api,_


class HrPayslipLinesIn(models.Model):
    _inherit = 'hr.payslip.line'

    taxable_amount = fields.Float('Taxable Amount', compute='_compute_taxable_amount')

    @api.depends('total')
    def _compute_taxable_amount(self):
        for record in self:
            record.taxable_amount = (record.total * record.salary_rule_id.taxable_percentage) / 100


