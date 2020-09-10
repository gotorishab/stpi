from odoo import models, fields, api,_
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class PfWidthdrawl(models.Model):
    _name = "pf.widthdrawl"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "PF"
    # _rec_name = 'employee_id'


    def _default_employee(self):
        return self.env['hr.employee'].sudo().search([('user_id', '=', self.env.uid)], limit=1)

    name = fields.Char(string='Name')
    date = fields.Date(string="Requested Date", default=fields.Date.today())
    employee_id=fields.Many2one('hr.employee', string="Request By", default=_default_employee,track_visibility='always',)
    advance_amount=fields.Float(string="Advance Amount",track_visibility='always',)
    interest=fields.Float(string="Interest",track_visibility='always',)
    designation=fields.Many2one('hr.job', string="Designation",track_visibility='always',)
    center=fields.Char(string="Work Location",track_visibility='always',)
    present_pay=fields.Float(string="Present Pay", compute='_compute_present_pay')
    bank_account_number=fields.Char(string="Bank Account",track_visibility='always',)
    cepf_vcpf = fields.Boolean('CEPF + VCPF')
    cpf = fields.Boolean('CPF')
    rule=fields.Selection([('A','23(1)(A)'),
                           ('B','23(1)(B)'),
                           ('E','23(1)(E)')],string="Rules",track_visibility='always',)
    pf_type = fields.Many2one('pf.type',string="PF Withdrawal Type",track_visibility='always')
    maximum_withdrawal = fields.Float(string='Eligible Amount')
#     purpose=fields.Selection([('a','Purchase of dwelling sight/flat/ construction of house/ renovation of house'),
#                               ('b','Repayment of loans'),
#                               ('e','For marriage and Education')],
    purpose = fields.Text(string="Purpose",track_visibility='always',related="pf_type.purpose")
#     attachment_document=fields.Selection([('ai',""""""'1) Declaration form for purchase of dwelling site.'
#                                                 '2) Declaration & Undertaking for non-encumbrance.'
#                                                 '3) Agreement of sale/Copy of Sale Deed/Allotment Letter.'
#                                                 '4) Copy of prior intimation under rule 18(2) of CCS Conduct Rules, 1964.'
#                                                 '5) Estimate of Repairs, Renovation, Construction.'""""""),
#                                  ('bi','1) Certificate of Home Loan Sanctioned. 2) Copy of Sale Deed.3) Certificate of Outstanding Home Loan. 4) Copy of prior intimation under rule 18(2) of CCS Conduct Rules, 1964.'),
#                                  ('ei','Marriage 1) Copy of invitation card. Education 1) Admission letter/Fee Details/Other')],
#                                 string='Attach Documents',track_visibility='always',)
    attachment_document = fields.Text(string="Attachment Document",track_visibility='always',related="pf_type.attachment_document")
#     attachment_ids=fields.Many2many('abc.ab',string="Attachment")
    attachment_ids = fields.Many2many('ir.attachment', string='Files',track_visibility='always')
    branch_id = fields.Many2one('res.branch',string="Branch",track_visibility='onchange')
    department_id = fields.Many2one('hr.department','Department',track_visibility='onchange')
    
    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], required=True, default='draft',string="Status",track_visibility='always',)


    @api.onchange('pf_type','employee_id')
    @api.constrains('pf_type','employee_id')
    def onchange_pf_type(self):
        for rec in self:
            pf_employee = self.env['pf.employee'].sudo().search([('employee_id', '=', rec.employee_id.id)])
            amt = 0.00
            max_all = 0.00
            maximum_allowed = 0.00
            if pf_employee:
                for pf_emp in pf_employee:
                    pf_emp.amount = pf_emp.amount - self.advance_amount
                    pf_emp.pf_withdrwal_amount = pf_emp.amount
                    if rec.pf_type.cepf_vcpf == True and rec.pf_type.cpf == True:
                        max_all = pf_emp.cepf_vcpf + pf_emp.cpf
                    elif rec.pf_type.cepf_vcpf == True and rec.pf_type.cpf == False:
                        max_all = pf_emp.cepf_vcpf
                    elif rec.pf_type.cepf_vcpf == False and rec.pf_type.cpf == True:
                        max_all = pf_emp.cpf
                    elif rec.pf_type.cepf_vcpf == False and rec.pf_type.cpf == False:
                        max_all = 0
            contract_obj = self.env['hr.contract'].sudo().search([('employee_id', '=', rec.employee_id.id)], limit=1)
            maximum_allowed = contract_obj.updated_basic * rec.pf_type.months
            if max_all < maximum_allowed:
                amt = max_all
            else:
                amt = maximum_allowed
            rec.maximum_withdrawal = amt

    @api.multi
    def button_to_approve(self):
        for rec in self:
            rec.write({'state': 'to_approve'})

    @api.multi
    def button_approved(self):
        for rec in self:
            rec.write({'state': 'approved'})
            pf_balance = self.env['pf.employee'].sudo().search([('employee_id', '=', rec.employee_id.id)],limit=1)
            #         print("////////////////////////",pf_balance)
            if pf_balance:
                pf_balance.get_pf_details()
            pf_withd = []
            amt = 0
            pf_employee = self.env['pf.employee'].sudo().search([('employee_id','=',rec.employee_id.id)])
            if pf_employee:
                for pf_emp in pf_employee:
                    pf_emp.amount = pf_emp.amount - self.advance_amount
                    pf_emp.pf_withdrwal_amount = pf_emp.amount
                    if rec.pf_type.cepf_vcpf == True and rec.pf_type.cpf == True:
                        amt = pf_emp.cepf_vcpf + pf_emp.cpf
                    elif rec.pf_type.cepf_vcpf == True and rec.pf_type.cpf == False:
                        amt = pf_emp.cepf_vcpf
                    elif rec.pf_type.cepf_vcpf == False and rec.pf_type.cpf == True:
                        amt = pf_emp.cpf
                    elif rec.pf_type.cepf_vcpf == False and rec.pf_type.cpf == False:
                        amt = 0
            if rec.advance_amount > amt:
                raise ValidationError("You are not able to  take advance amount more than %s" % rec.maximum_withdrawal)
            if rec.pf_type.min_years < (rec.employee_id.birthday - datetime.now().date()).days:
                raise ValidationError("You are not able to  apply as minimum age for PF should be atlest %s" % rec.pf_type.min_years)

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})

    @api.multi
    def button_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})


    @api.model
    def create(self, vals):
        res =super(PfWidthdrawl, self).create(vals)
        sequence = ''
        seq = self.env['ir.sequence'].next_by_code('pf.widthdrawl')
        sequence = 'PF - ' + str(seq)
        res.name = sequence
        contract_obj = self.env['hr.contract'].sudo().search([('employee_id', '=', res.employee_id.id)], limit=1)
        maximum_allowed = contract_obj.updated_basic * res.pf_type.months
        if res.advance_amount > maximum_allowed:
            raise ValidationError("You are not able to  take advance amount more than %s" % res.maximum_withdrawal)
        pf_count = self.env['pf.widthdrawl'].sudo().search(
            [('employee_id', '=', res.employee_id.id), ('state', '!=', 'approved'), ('id', '!=', res.id),
             ])
        if pf_count:
            raise ValidationError(_("The employee has already a PF pending"))
        return res

    @api.multi
    @api.depends('name')
    def name_get(self):
        res = []
        for record in self:
            if record.name:
                name = record.name
            else:
                name = 'PF'
            res.append((record.id, name))
        return res

    @api.multi
    def unlink(self):
        for pf in self:
            if pf.state not in ('draft'):
                raise UserError(
                    'You cannot delete a PF which is not in draft or cancelled state')
        return super(PfWidthdrawl, self).unlink()


#     @api.constrains('rule')
#     @api.onchange('rule')
#     def _onchange_rule(self):
#         for e in self:
#             if e.rule == 'A':
#                 e.purpose = 'a'
#             elif e.rule == 'B':
#                 e.purpose = 'b'
#             elif e.rule == 'E':
#                 e.purpose = 'e'

#     @api.constrains('purpose')
#     @api.onchange('purpose')
#     def _onchange_purpose(self):
#         for e in self:
#             if e.purpose== 'a':
#                 e.attachment_document='ai'
#             elif e.purpose=='b':
#                 e.attachment_document='bi'
#             elif e.purpose=='e':
#                 e.attachment_document='ei'


    @api.constrains('employee_id')
    @api.onchange('employee_id')
    def _onchange_basic_details(self):
        for rec in self:
            rec.designation = rec.employee_id.job_id.id
            rec.bank_account_number = rec.employee_id.bank_account_number
            rec.center = rec.employee_id.work_location
            rec.branch_id = rec.employee_id.branch_id.id
            rec.department_id = rec.employee_id.department_id.id
            

    @api.depends('employee_id')
    def _compute_present_pay(self):
        for rec in self:
            contract_obj = self.env['hr.contract'].sudo().search([('employee_id', '=', self.employee_id.id)], limit=1)
            if contract_obj:
                for contract in contract_obj:
                    rec.present_pay = contract.updated_basic

    @api.constrains('advance_amount')
    @api.onchange('advance_amount')
    def _onchange_advance_amount(self):
        for rec in self:
            max_balance = self.env['pf.employee'].sudo().search([('employee_id', '=', self.employee_id.id)], limit=1)
            if max_balance:
                for empbal in max_balance:
                    if rec.advance_amount > empbal.amount:
                        raise ValidationError("You aare not able to  take advance amount more than %s"%empbal.amount +"/-")
                    if empbal.pf_start_data and rec.pf_type.min_years:
                        if rec.date <= (empbal.pf_start_data + relativedelta(years=rec.pf_type.min_years)):
                            raise ValidationError(
                                "You are not able to withdraw PF before %s" % empbal.pf_start_data + relativedelta(years=rec.pf_type.min_years))


class PfEmployee(models.Model):
    _name = "pf.employee"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "PF Employee"
    _rec_name = 'employee_id'

    def _default_employee(self):
        return self.env['hr.employee'].sudo().search([('user_id', '=', self.env.uid)], limit=1)

    pf_start_data = fields.Date('PF Start Date')
    employee_id=fields.Many2one('hr.employee', string="Request By", default=_default_employee)
    branch_id = fields.Many2one('res.branch',string="Branch",track_visibility='onchange')
    advance_amount = fields.Float('Advance Amount Taken')
    advance_left = fields.Float('Amount Left', compute='_compute_amount')
    amount = fields.Float('Amount', compute='_compute_amount')
    cepf_vcpf = fields.Float('CEPF + VCPF', compute='_compute_amount')
    cpf = fields.Float('CPF', compute='_compute_amount')
    pf_details_ids=fields.One2many('pf.employee.details', 'pf_details_id', string="Employee")
    currency_id = fields.Many2one('res.currency', string='Currency',
                              default=lambda self: self.env.user.company_id.currency_id)
    # @api.depends('employee_id')
    # def _compute_amount(self):
    #     for rec in self:
    #         sum = 0.00
    #         pf_employee_obj = self.env['pf.employee.details'].search([('pf_details_id', '=', rec.id)])
    #         if pf_employee_obj:
    #             for details in pf_employee_obj:
    #                 sum += details.amount
    #         rec.amount = sum


    @api.constrains('employee_id')
    @api.onchange('employee_id')
    def _onchange_basic_detailsss(self):
        for rec in self:
            rec.branch_id = rec.employee_id.branch_id.id

    @api.multi
    def button_transfer_pf(self):
        pass


    @api.depends('pf_details_ids')
    def _compute_amount(self):
        for rec in self:
            sum = 0.00
            sum1 = 0.00
            cv = 0.00
            cpf = 0.00
            for details in rec.pf_details_ids:
                sum += details.amount
                if details.pf_code == 'CEPF + VCPF' or details.pf_code == 'VCPF' or details.pf_code == 'CEPF':
                    if details.type == 'Deposit':
                        cv += details.amount
                    elif details.type == 'Withdrawal':
                        cv -= details.amount
                if details.pf_code == 'CPF':
                    if details.type == 'Deposit':
                        cpf += details.amount
                    elif details.type == 'Withdrawal':
                        cpf -= details.amount
            rec.cepf_vcpf = cv
            rec.cpf = cpf

            pf_advance = self.env['pf.widthdrawl'].sudo().search(
                [('employee_id', '=', rec.employee_id.id),
                 ('state', '=', 'approved')], limit=1)
            for ad in pf_advance:
                sum1 += ad.advance_amount
            rec.amount = sum
            # rec.advance_amount = sum1
            rec.advance_left = rec.amount - rec.advance_amount



    # @api.model
    # def create(self, values):
    #     res = super(PfEmployee, self).create(values)
    #     count = 0
    #     print('=================================================')
    #     search_id = self.env['pf.employee'].search(
    #         [('employee_id', '=', res.employee_id.id)])
    #     print('======================1===========================')
    #     if search_id:
    #         for emp in search_id:
    #             count += 1
    #             print('===================2==============================')
    #         if count > 1:
    #             print('===================3==============================')
    #             raise ValidationError("You are not apply for more thn one")
    #     print('===================4==============================')


    @api.multi
    def get_pf_details(self):
        pf_details_ids = []
        for rec in self:
            advance_amount = 0.00
            rec.pf_details_ids.unlink()
            if rec.employee_id:
                pay_rules = self.env['hr.payslip.line'].sudo().search(
                    [('slip_id.employee_id', '=', rec.employee_id.id),
                     ('slip_id.state', '=', 'done'),
                     ('salary_rule_id.pf_register', '=', True),
                     ])
                if pay_rules:
                    for i in pay_rules:
                        pf_details_ids.append((0, 0, {
                            'pf_details_id': rec.id,
                            'employee_id': rec.employee_id.id,
                            'type': 'Deposit',
                            'pf_code': i.code,
                            'description': i.name,
                            'date': datetime.now().date(),
                            'amount': i.total,
                            'reference': i.slip_id.number,
                        }))
                pf_advance = self.env['pf.widthdrawl'].sudo().search(
                    [('employee_id', '=', rec.employee_id.id),
                     ('state', '=', 'approved')])
                if pf_advance:
                    for i in pf_advance:
                        pf_details_ids.append((0, 0, {
                            'pf_details_id': rec.id,
                            'employee_id': rec.employee_id.id,
                            'type': 'Withdrawal',
                            'pf_code': i.pf_type.name,
                            'description': ' ',
                            'date': i.date,
                            'amount': i.advance_amount,
                            'reference': i.name,
                        }))
                rec.pf_details_ids = pf_details_ids
                for lines in rec.pf_details_ids:
                    if lines.type == 'Withdrawal':
                        advance_amount += lines.amount
                rec.advance_amount = advance_amount


class PfEmployeeDetails(models.Model):
    _name = "pf.employee.details"
    _description = "PF"


    pf_details_id = fields.Many2one('pf.employee', string="Employee")
    employee_id=fields.Many2one('hr.employee')
    date = fields.Date('Date')
    type = fields.Selection([
                            ('Deposit', 'Deposit'),
                            ('Withdrawal', 'Withdrawal'),
                            ], string="Type")
    pf_code = fields.Char(string='PF code')
    description = fields.Char(string='Description')
    amount = fields.Float('Amount')
    reference = fields.Char('Reference')

class AbcAb(models.Model):
    _name = "abc.ab"
    _description = "abc ab"

    name=fields.Binary(string="Upload File")
