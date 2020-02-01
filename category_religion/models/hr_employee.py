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

