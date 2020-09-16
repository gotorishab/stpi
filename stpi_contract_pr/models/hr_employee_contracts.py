from odoo import fields, models, api, _
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError

class InheritContractss(models.Model):
    _inherit = 'hr.contract'
    _description = 'HR Contract'

    recruitment_type = fields.Selection([('absorption', 'Absorption'),
                                     ('compassion', 'Compassionate Appt.'),
                                     ('deputation', 'Deputation'),
                                     ('deput_absorp', 'Deputation & Absorption'),
                                     ('direct', 'Direct recruitment'),
                                     ('drabsorp', 'DR & Absorption'),
                                     ('promo', 'Promotion'),
                                    ],string='Mode of Promotion')

    employee_type = fields.Selection([('regular', 'Regular Employee'),
                                      ('contractual_with_agency', 'Contractual with Agency'),
                                      ('contractual_with_stpi', 'Contractual with STPI')], string='Employment Type'
                                     )

    basicinc = fields.Float(string='Basic Increment %')
    da = fields.Float(string='DA %')
    supplementary_allowance = fields.Float(string='Supplementary Allowance')
    voluntary_provident_fund = fields.Float(string='Voluntary Provident Fund (%)')
    xnohra = fields.Boolean(string='Rent Recovery?')
    pf_deduction = fields.Boolean(string='PF Deduction')
    transport_deduction = fields.Boolean(string='Transport Deduction')
    updated_basic = fields.Float(string='Basic + DA', compute='_compute_updated_basic_f_da')

    pay_level_id = fields.Many2one('hr.payslip.paylevel', string='Pay Level')
    pay_level = fields.Many2one('payslip.pay.level', string='Pay Band')
    
    #added by Sangita to rename the core field name
    struct_id = fields.Many2one('hr.payroll.structure', string='Salary Type')
    #added by sangita to rename the expired stage to Past Service
    state = fields.Selection([
        ('draft', 'New'),
        ('open', 'Running'),
        ('pending', 'To Renew'),
        ('close', 'Past Service'),
        ('cancel', 'Cancelled')
    ], string='Status', group_expand='_expand_states',
       track_visibility='onchange', help='Status of the contract', default='draft')
    
    #added by sangita to rename End of Trial Period to End of Probation Period
    trial_date_end = fields.Date('End of Probation Period',
        help="End date of the trial period (if there is one).")



    city_id = fields.Many2one('res.city', string='City', store=True, compute='compute_hra_tier')

    employee_hra_cat = fields.Selection([('x', 'X'),
                                     ('y', 'Y'),
                                     ('z', 'Z'),
                                    ],string='HRA Category', compute='compute_hra_tier', store=True)
    city_tier = fields.Selection([('a', 'A'),
                                     ('a1', 'A1'),
                                     ('other', 'Other'),
                                    ],string='City Tier', compute='compute_hra_tier', store=True)


    misc_deduction = fields.Monetary(string="Misc. Deducation")
    license_dee = fields.Monetary(string=" License Fee")




    @api.multi
    @api.depends('employee_id')
    def compute_hra_tier(self):
        for rec in self:
            rec.city_id = rec.employee_id.branch_id.city_id.id
            rec.employee_hra_cat = rec.employee_id.branch_id.city_id.employee_hra_cat
            rec.city_tier = rec.employee_id.branch_id.city_id.city_tier

    @api.multi
    @api.depends('wage','da')
    def _compute_updated_basic_f_da(self):
        for rec in self:
            rec.updated_basic = rec.wage * (1 + rec.da/100)



    @api.model
    def create(self, vals):
        res =super(InheritContractss, self).create(vals)
        pf_count = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', res.employee_id.id), ('state', '!=', 'cancel'),
             ])
        if pf_count:
            raise ValidationError(_("You already have a contract created"))
        return res


    #
    # @api.constrains('employee_id')
    # @api.onchange('employee_id')
    # def _get_add_city(self):
    #     for rec in self:
    #         # if rec.employee_id:
    #         #     rec.employee_type = rec.employee_id.employee_type
    #         #     rec.mode_of_promotion = rec.employee_id.mode_of_promotion
    #         if rec.city_id.name:
    #             if rec.city_id.name == 'Hyderabad' or rec.city_id.name == 'Delhi' or rec.city_id.name == 'Banglore' or rec.city_id.name == 'Mumbai' or rec.city_id.name == 'Chennai' or rec.city_id.name == 'Kolkata':
    #                 rec.city_tier = 'a1'
    #             elif rec.city_id.name == 'Ahmedabad' or rec.city_id.name == 'Surat' or rec.city_id.name == 'Kanpur' or rec.city_id.name == 'Patna' or rec.city_id.name == 'Kochi' or rec.city_id.name == 'Indore' or rec.city_id.name == 'Nagpur' or rec.city_id.name == 'Pune' or rec.city_id.name == 'Lucknow':
    #                 rec.city_tier = 'a'
    #             else:
    #                 rec.city_tier = 'other'


    # @api.constrains('pay_level')
    # @api.onchange('pay_level')
    # def _get_pay_wage(self):
    #     for rec in self:
    #         rec.wage = rec.pay_level.entry_pay


    def process_contract_cron(self):
        emp_contract = self.env['hr.contract'].search([('employee_type','=','regular'),('state', '=', 'open')])
        for employee in emp_contract:
            expiry_date = employee.date_start + relativedelta(years=1)
            todays_date = datetime.now().date()
            if expiry_date == todays_date:
                employee.state = 'close'
                create_contract = self.env['hr.contract'].create(
                    {
                        'state': 'open',
                        'name': employee.name,
                        'employee_id': employee.employee_id.id,
                        'department_id': employee.department_id.id,
                        'job_id': employee.job_id.id,
                        'pay_level_id': employee.pay_level_id.id,
                        'pay_level': employee.pay_level.id,
                        'struct_id': employee.struct_id.id,
                        'type_id': employee.type_id.id,
                        'date_start': datetime.now().date(),
                        'employee_type': 'regular',
                        'recruitment_type': employee.recruitment_type,
                        'wage': employee.wage,
                    }
                )
