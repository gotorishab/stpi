# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class HrLoan(models.Model):
    _name = 'hr.loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Loan Request"

    @api.model
    def default_get(self, field_list):
        result = super(HrLoan, self).default_get(field_list)
        if result.get('user_id'):
            ts_user_id = result['user_id']
        else:
            ts_user_id = self.env.context.get('user_id', self.env.user.id)
            result['employee_id'] = self.env['hr.employee'].search([('user_id', '=', ts_user_id)], limit=1).id
        return result

    @api.multi
    @api.depends('loan_lines.paid')
    def _compute_loan_amount(self):
        total_paid = 0.0
        for loan in self:
            for line in loan.loan_lines:
                if line.paid:
                    total_paid += line.amount
                    print("-----------",total_paid)
                loan.total_interest += line.monthly_interest_amount
                loan.total_paid_amount = total_paid
                loan.total_amount = loan.loan_amount
                balance_amount = (loan.total_interest + loan.total_amount) - loan.total_paid_amount
                loan.balance_amount = balance_amount


                
#     @api.multi
#     @api.depends('loan_lines.paid')
#     def _compute_loan_amount(self):
#         total_paid = 0.0
#         for loan in self:
#             for line in loan.loan_lines:
#                 if line.paid:
#                     total_paid += line.amount
#             balance_amount = loan.loan_amount - total_paid
#             self.total_amount = loan.loan_amount
#             self.balance_amount = balance_amount
#             print("_____________-------------------",self.balance_amount)
#             self.total_paid_amount = total_paid


    name = fields.Char(string="Loan Name", default="Loan Request", readonly=True)
    date = fields.Date(string="Requested Date", default=fields.Date.today(), readonly=True)
    employee_id = fields.Many2one('hr.employee', string="Employee")
    employee_id_related = fields.Many2one('hr.employee', related="employee_id", string="Employee")
    department_id = fields.Many2one('hr.department', related="employee_id.department_id", readonly=True,
                                    string="Department", store=True)
    type_id =fields.Many2one('loan.type',string="Type")
    installment = fields.Integer(string="No Of Installments", default= 0)
    approve_date = fields.Date(string="Approve Date")
    payment_date = fields.Date(string="Payment Start Date", default=fields.Date.today())
    loan_lines = fields.One2many('hr.loan.line', 'loan_id', string="Loan Line", index=True)

    company_id = fields.Many2one('res.company', 'Company', readonly=True,
                                 default=lambda self: self.env.user.company_id,
                                 states={'draft': [('readonly', False)]})
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    job_position = fields.Many2one('hr.job', related="employee_id.job_id", readonly=True, string="Job Position")
    loan_amount = fields.Float(string="Loan Amount")
    interest= fields.Float(related='type_id.interest',string="Interest Rate%")
    total_amount = fields.Float(string="Total Amount", readonly=True, compute='_compute_loan_amount')
    balance_amount = fields.Float(string="Balance Amount", compute='_compute_loan_amount',store=True)
    total_paid_amount = fields.Float(string="Total Paid Amount", compute='_compute_loan_amount')
    payslip_id = fields.Many2one('hr.payslip', string="Payslip Ref.")
    paid = fields.Boolean(string="Paid")
    total_interest = fields.Float(string="Total Interest", compute='_compute_loan_amount')

    # treasury_account_id = fields.Many2one('account.account', string="Treasury Account")
    # emp_account_id = fields.Many2one('account.account', string="Loan Account")
    # journal_id = fields.Many2one('account.journal', string="Journal")
    max_emi = fields.Integer(string="Max No.EMI")
    action_app = fields.Boolean('Action Approve bool', invisible=1)
    action_clos = fields.Boolean('Action Loan Close bool', invisible=1)


    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval_1', 'Submitted'),
        ('waiting_approval_2', 'Waiting Approval'),
        ('approve', 'Approved'),
        ('refuse', 'Refused'),
        ('cancel', 'Canceled'),
    ], string="Status", default='draft', track_visibility='onchange', copy=False, )

    @api.model
    def create(self, values):
        loan_count = self.env['hr.loan'].search_count([('employee_id', '=', values['employee_id']), ('state', '=', 'approve'),
                                                       ('balance_amount', '!=', 0)])
        if loan_count:
            raise ValidationError(_("The employee has already a pending installment"))
        else:
            values['name'] = self.env['ir.sequence'].get('hr.loan.seq') or ' '
            res = super(HrLoan, self).create(values)
            return res


    @api.constrains('type_id')
    @api.onchange('type_id')
    def onchange_type_id_get_emi(self):
        for record in self:
            if record.type_id:
                if record.type_id.max_emi:
                    record.max_emi = record.type_id.max_emi


    @api.constrains('installment')
    def check_installment(self):
        if self.installment > 0:
            if self.installment > self.type_id.max_emi:
                raise UserError(_('Please enter valid no. of installments %d') %self.type_id.max_emi)


    @api.constrains('loan_amount')
    def check_loan_amount(self):
        if self.loan_amount > 0.00:
            max_all = self.env['allowed.loan.amount'].search([('pay_level_id', '=', self.employee_id.job_id.pay_level_id.id)], limit=1)
            if max_all.amount and self.loan_amount > max_all.amount:
                raise UserError(_('You are not allowed to take loan more than Rs. %s/-') %max_all.amount)
    #

    @api.multi
    def action_reset_to_draft(self):
        for loan in self:
            loan.loan_lines.unlink()
            loan.write({'state': 'draft'})

    @api.multi
    def action_refuse(self):
        return self.write({'state': 'refuse'})


    @api.multi
    def action_submit(self):
        for line in self:
            line.sudo().compute_installment()
        self.write({'state': 'waiting_approval_1'})
        return True

    @api.multi
    def action_cancel(self):
        self.ensure_one()
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        ctx = dict(
            default_composition_mode='comment',
            default_res_id=self.id,

            default_model='hr.loan',
            default_is_log='True',
            custom_layout='mail.mail_notification_light'
        )
        mw = {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
        self.write({'state': 'cancel'})
        self.sudo().action_reset_to_draft()
        return mw
    #
    #
    # @api.multi
    # def action_approve(self):
    #     for data in self:
    #         if not data.loan_lines:
    #             raise ValidationError(_("Please Compute installment"))
    #         else:
    #             self.write({'state': 'approve'})

    @api.multi
    def unlink(self):
        for loan in self:
            if loan.state not in ('draft', 'cancel'):
                raise UserError(
                    'You cannot delete a loan which is not in draft or cancelled state')
        return super(HrLoan, self).unlink()


    # if type_id and installment and loan_amount:
    @api.multi
    def compute_installment(self):
        """This automatically create the installment the employee need to pay to
        company based on payment start date and the no of installments.
            """
        for loan in self:
            loan.loan_lines.unlink()
            date_start = datetime.strptime(str(loan.payment_date), '%Y-%m-%d')
            if loan.installment <=0:
                raise UserError(_('Please enter Number of Installment grater than Zero'))
            if loan.loan_amount <=0:
                raise UserError(_('Please enter Loan Amount grater than Zero'))

            amount = loan.loan_amount / loan.installment

            for i in range(1, loan.installment + 1):
                cb_interest= 0.0
                for j in  range (0,i):
                    # print('-----j',j)
                    cb_interest += ((loan.loan_amount-(amount * (j))) * (self.interest/100))/12

                closing_balance = loan.loan_amount-amount * i
                year_interest =(loan.loan_amount-(amount * (i-1)))* (self.interest/100)
                monthly_interest = year_interest/12
                self.env['hr.loan.line'].create({
                    'date': date_start,
                    'principle_recovery_installment': amount,
                    'closing_blance_principle': closing_balance,
                    'yearly_interest_amount':year_interest,
                    'monthly_interest_amount':monthly_interest ,
                    'cb_interest':cb_interest,
                    'pending_amount': closing_balance + monthly_interest,
                    'amount': amount + monthly_interest,
                    'employee_id': loan.employee_id.id,
                    'loan_id': loan.id})
                date_start = date_start + relativedelta(months=1)
        return True

    @api.multi
    def action_approve(self):
        self.approve_date = date.today()
        if self.approve_date.day <= 10:
            self.payment_date = self.approve_date.replace(day=1)
        else:
            self.payment_date = self.approve_date.replace(day=1) + relativedelta(months=1)
        payment_date = self.payment_date
        for id in sorted(self.loan_lines.ids):
            i = self.env["hr.loan.line"].browse(id)
            i.approval_d = payment_date
            i.date = payment_date
            payment_date = payment_date + relativedelta(months=1)
        # loan_approve = self.env['ir.config_parameter'].sudo().get_param('account.loan_approve')
        contract_obj = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])
        if not contract_obj:
            raise UserError('You must Define a contract for employee')
        if not self.loan_lines:
            raise UserError('You must compute installment before Approved')
        # if loan_approve:
        #     self.write({'state': 'waiting_approval_2'})
        # else:
        self.write({'state': 'approve'})
        return True


class InstallmentLine(models.Model):
    _name = "hr.loan.line"
    _description = "Installment Line"


    date = fields.Date(string="Installment Date")

    # Added this field by RGupta @Dexciss
    approval_d = fields.Date('EMI Date')
    # installment_month = fields.Char('Installment Month')

    principle_recovery_installment=fields.Float(string="Principle Recovery Installment")
    closing_blance_principle=fields.Float(string="Closing Balance Principle")
    yearly_interest_amount=fields.Float(string="Yearly Interest Amount")
    monthly_interest_amount = fields.Float(string="Monthly Interest Amount")
    cb_interest=fields.Float(string="C/B Interest")

    employee_id = fields.Many2one('hr.employee', string="Requested By")
    pending_amount = fields.Float(string="Total Pending Recovery")
    amount = fields.Float(string="EMI")
    paid = fields.Boolean(string="Paid")
    loan_id = fields.Many2one('hr.loan', string="Loan Ref.")
    payslip_id = fields.Many2one('hr.payslip', string="Payslip Ref.")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval_1', 'Submitted'),
        ('waiting_approval_2', 'Waiting Approval'),
        ('approve', 'Approved'),
        ('refuse', 'Refused'),
        ('cancel', 'Canceled'),
    ], string="State", related='loan_id.state')






class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.one
    def _compute_employee_loans(self):
        """This compute the loan amount and total loans count of an employee.
            """
        self.loan_count = self.env['hr.loan'].search_count([('employee_id', '=', self.id)])

    loan_count = fields.Integer(string="Loan Count", compute='_compute_employee_loans')
