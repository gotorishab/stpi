# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class Religion(models.Model):
    _name = 'employee.religion'
    _description = 'Employee Religion'
    _rec_name ='name'

    name = fields.Char('Religion')


class Category(models.Model):
    _name = 'employee.category'
    _description = 'Employee category'
    _rec_name = 'name'

    name = fields.Char('Category')

class relativ_type(models.Model):
    _name = 'relative.type'
    _description = 'Relative Description'

    name = fields.Char('Name')


class EmployeeBranch(models.Model):
    _inherit = 'hr.employee'

    branch_id = fields.Many2one('res.branch', string='Branch', store=True)


    @api.onchange('job_id')
    @api.constrains('job_id')
    def get_branch_from_job(self):
        for rec in self:
            rec.branch_id = rec.job_id.branch_id.id

