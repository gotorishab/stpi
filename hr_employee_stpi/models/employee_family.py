from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime

class Employeefamily(models.Model):
    _inherit='employee.relative'
    _description = 'Employee Relative'

    salutation = fields.Many2one('res.partner.title',string='Salutation')
    relative_type = fields.Selection([('Aunty', 'Aunty'),
                                      ('Brother', 'Brother'),
                                      ('Daughter', 'Daughter'),
                                      ('Father', 'Father'),
                                      ('Husband', 'Husband'),
                                      ('Mother', 'Mother'),
                                      ('Sister', 'Sister'),
                                      ('Son', 'Son'), ('Uncle', 'Uncle'),
                                      ('Wife', 'Wife'), ('Other', 'Other')],
                                     string='Relative Type')

    relate_type = fields.Many2one('relative.type', string="Relative Type")
    relate_type_name = fields.Char(related='relate_type.name')


    name = fields.Char(string = 'Name',)

    medical = fields.Boolean('Medical',default=False)
    tuition = fields.Boolean('Tuition',default=False)
    ltc = fields.Boolean('LTC',default=False)
    status = fields.Selection([('dependant','Dependant'),
                               ('non_dependant','Non-Dependant')
                               ],string='Status')
    prec_pf =fields.Float('PF%')
    prec_gratuity =fields.Float('Gratuity%')
    prec_pension =fields.Float('Pension%')

    age= fields.Float('Age')


    @api.onchange('prec_pf')
    def check_pf_prect(self):
        prect = self.env['employee.relative'].search([('employee_id','=',self.employee_id.id)]).mapped('prec_pf')
        total = 0
        print('-------------------prect',prect,self.employee_id.name)
        for val in prect:
            total+=val
        total+=self.prec_pf
        print("---------total-",total)
        if total>100 and self.prec_pf > 0:
            self.update({'prec_pf':0})
            raise UserError(_('you have already distributed your PF out of 100%'))

    @api.onchange('prec_gratuity')
    def check_gratuity(self):
        prect = self.env['employee.relative'].search([('employee_id','=',self.employee_id.id)]).mapped('prec_gratuity')
        total =0
        for val in prect:
            total+=val
        total +=self.prec_gratuity
        if total>100 and self.prec_gratuity > 0:
            self.update({'prec_pf':0})
            raise UserError(_('you have already distributed your Gratuity out of 100%'))

    @api.onchange('prec_pension')
    def check_pension(self):
        prect = self.env['employee.relative'].search([('employee_id','=',self.employee_id.id)]).mapped('prec_pension')
        total =0
        for val in prect:
            total+=val
        total +=self.prec_pension
        if total>100 and self.check_pension > 0:
            self.update({'prec_pf':0})
            raise UserError(_('you have already distributed your Pension out of 100%'))


    @api.onchange('birthday')
    def get_age(self):
        if self.birthday:
            day=(datetime.now().date() - self.birthday).days
            self.age = day/365
            self.tuition =False


    @api.onchange('tuition')
    def child_count(self):
        count =0
        prect = self.env['employee.relative'].search([('employee_id', '=', self.employee_id.id)]).mapped('tuition')
        for ch in prect:
            if ch:
                count+=1
        # print('-----------count',count)
        if self.tuition and count >= 2:
            self.update({'tuition': False})
            raise UserError(_('Only Two Child allowed for Tuition'))

    @api.onchange('relative_type')
    def onchange_relative_type(self):
        pass


    @api.multi
    @api.depends('name','relate_type','age')
    def name_get(self):
        res = []
        for record in self:
            if record.name and record.relate_type and record.age:
                name = str(record.name) + ' [' + str(record.relate_type.name) + ':' + str(int(record.age)) + ']'
            else:
                name = 'Relative'
            res.append((record.id, name))
        return res
