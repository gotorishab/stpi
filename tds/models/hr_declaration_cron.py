from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta

class HrDeclarationCron(models.Model):
    _inherit = 'hr.declaration'


    def hr_declaration_cron(self):
        search_id = self.env['hr.declaration'].search(
            [('state', 'not in', ['approved', 'rejected'])])
        for rec in search_id:
            sum = 0
            dstart = rec.date_range.date_start
            dend = rec.date_range.date_end
            proll = self.env['hr.payslip.line'].sudo().search([('slip_id.employee_id', '=', rec.employee_id.id),
                                                               ('slip_id.state', '=', 'done'),
                                                               ('salary_rule_id.taxable_percentage', '>', 0),
                                                               ('slip_id.date_from', '>=', dstart),
                                                               ('slip_id.date_to', '<=', dend)])
            for i in proll:
                sum += i.taxable_amount
            rec.tax_salary_final = sum
            # rec.income_after_rebate = rec.tax_salary_final - rec.net_allowed_rebate
            age = 0
            if rec.employee_id.birthday:
                age = ((datetime.now().date() - rec.employee_id.birthday).days) / 365

            inc_tax_slab = self.env['income.tax.slab'].sudo().search([('salary_from', '<=', rec.tax_salary_final),
                                                                      ('salary_to', '>=', rec.tax_salary_final),
                                                                      ('age_from', '<=', age),
                                                                      ('age_to', '>=', age)], order="create_date desc",
                                                                     limit=1)
            for tax_slab in inc_tax_slab:
                t1 = (tax_slab.tax_rate * (rec.tax_salary_final / 100))
                t2 = (t1 * (1 + tax_slab.surcharge / 100))
                t3 = (t2 * (1 + tax_slab.cess / 100))
                rec.tax_payable = t3
            if rec.tax_payable <= 0.00:
                rec.tax_payable_zero = False
                rec.tax_payable = 0.00
            else:
                rec.tax_payable_zero = True
            rec.std_ded_ids.unlink()
            rec.exemption_ids.unlink()
            rec.rebate_ids.unlink()
            rec.slab_ids.unlink()
            ex_std_id = self.env['saving.master'].sudo().search(
                [('saving_type', '=', 'Std. Deduction'), ('it_rule', '=', 'mus10ale')], limit=1)
            my_investment = 0.00
            if ex_std_id:
                my_investment = 0.00
                my_allowed_rebate = 0.00
                if rec.tax_salary_final >= ex_std_id.rebate:
                    my_investment = ex_std_id.rebate
                else:
                    my_investment = rec.tax_salary_final

                if my_investment <= ex_std_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_std_id.rebate
                std_ded_ids = []
                std_ded_ids.append((0, 0, {
                    'std_ded_id': rec.id,
                    'it_rule': 'mus10ale',
                    'saving_master': ex_std_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                }))
                rec.std_ded_ids = std_ded_ids
            ex_child_id = self.env['saving.master'].sudo().search(
                [('saving_type', '=', 'Child Education Allowance & Hostel Expenditure Allowance'),
                 ('it_rule', '=', 'mus10ale')], limit=1)
            child_id = self.env['employee.relative'].sudo().search(
                [('employee_id', '=', rec.employee_id.id)])
            count = 0
            my_investment = 0.00
            my_allowed_rebate = 0.00
            for cc in child_id:
                if cc.relate_type_name == 'Son' or cc.relate_type_name == 'Daughter':
                    count += 1
            if ex_child_id:
                if rec.employee_id.date_of_join and rec.date_range.date_start < rec.employee_id.date_of_join <= rec.date_range.date_end:
                    nm = ((rec.date_range.date_end - rec.employee_id.date_of_join).days) / 30
                    my_investment = count * 100 * nm
                else:
                    my_investment = count * 100 * 12
                if my_investment <= ex_child_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_child_id.rebate
                exemption_ids = []
                exemption_ids.append((0, 0, {
                    'exemption_id': rec.id,
                    'it_rule': 'mus10ale',
                    'saving_master': ex_child_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                }))
                rec.exemption_ids = exemption_ids
            ex_hra_id = self.env['saving.master'].sudo().search(
                [('saving_type', '=', 'HRA Exemption'), ('it_rule', '=', 'mus10ale')], limit=1)
            prl_id = self.env['hr.payslip.line'].sudo().search(
                [('slip_id.employee_id', '=', rec.employee_id.id), ('slip_id.state', '=', 'done'), ('code', '=', 'HRA'),
                 ('slip_id.date_from', '>', rec.date_range.date_start),
                 ('slip_id.date_to', '<', rec.date_range.date_end)])
            sum_bs = 0.00
            sum_rent = 0.00
            sum_prl = 0.00
            sum = 0.00
            my_investment = 0.00
            my_allowed_rebate = 0.00
            for cc in prl_id:
                sum_prl += cc.amount
            if rec.employee_id.address_home_id.city_id.metro == True:
                sum_bs = ((rec.basic_salary + rec.da_salary) * 50) / 100
            else:
                sum_bs = ((rec.basic_salary + rec.da_salary) * 40) / 100
            sum_rent = rec.rent_paid - ((rec.basic_salary + rec.da_salary) * 10) / 100
            if sum_prl <= sum_bs and sum_prl <= sum_rent:
                sum = sum_prl
            elif sum_bs <= sum_prl and sum_bs <= sum_rent:
                sum = sum_bs
            else:
                sum = sum_rent
            if ex_hra_id:
                my_investment = sum
                if my_investment <= ex_hra_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_hra_id.rebate

                exemption_ids = []
                exemption_ids.append((0, 0, {
                    'exemption_id': rec.id,
                    'it_rule': 'mus10ale',
                    'saving_master': ex_hra_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                }))
                rec.exemption_ids = exemption_ids
            ex_lunch_id = self.env['saving.master'].sudo().search(
                [('saving_type', '=', 'Lunch Subsidy Allowance'), ('it_rule', '=', 'mus10ale')], limit=1)
            reimbursement_id = self.env['reimbursement'].sudo().search(
                [('employee_id', '=', rec.employee_id.id), ('name', '=', 'lunch'),
                 ('from_date', '>', rec.date_range.date_start), ('to_date', '<', rec.date_range.date_end),
                 ('state', '=', 'approved')])
            sum = 0.00
            my_investment = 0.00
            my_allowed_rebate = 0.00
            for cc in reimbursement_id:
                sum += float(cc.lunch_tds_amt)
            if ex_lunch_id:
                my_investment = sum
                if my_investment <= ex_lunch_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_lunch_id.rebate
                exemption_ids = []
                exemption_ids.append((0, 0, {
                    'exemption_id': rec.id,
                    'it_rule': 'mus10ale',
                    'saving_master': ex_lunch_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                }))
                rec.exemption_ids = exemption_ids
            ex_rebate_id = self.env['saving.master'].sudo().search(
                [('saving_type', '=', 'Revised Rebate under Section 87A (2019-20)'), ('it_rule', '=', 'section87a')],
                limit=1)
            my_investment = 0.00
            my_allowed_rebate = 0.00
            if rec.tax_salary_final <= 50000 and rec.tax_payable >= 12500:
                my_investment = 12500
            elif rec.tax_salary_final <= 50000 and rec.tax_payable <= 12500:
                my_investment = 10000
            elif rec.tax_salary_final >= 50000:
                my_investment = 0
            if ex_rebate_id:
                if my_investment <= ex_rebate_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_rebate_id.rebate
                rebate_ids = []
                rebate_ids.append((0, 0, {
                    'rebate_id': rec.id,
                    'it_rule': ex_rebate_id.it_rule,
                    'saving_master': ex_rebate_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                }))
                rec.rebate_ids = rebate_ids
            ex_80_c_id = self.env['saving.master'].sudo().search(
                [('saving_type', '=', 'Investment in PPF &  Employee’s share of PF contribution'),
                 ('it_rule', '=', '80_c')], limit=1)
            prl_80c_id = self.env['hr.payslip.line'].sudo().search(
                [('slip_id.employee_id', '=', rec.employee_id.id),
                 ('slip_id.state', '=', 'done'),
                 ('salary_rule_id.pf_register', '=', True),
                 ('slip_id.date_from', '>', rec.date_range.date_start),
                 ('slip_id.date_to', '<', rec.date_range.date_end)])
            sum = 0
            for sr in prl_80c_id:
                if sr.code == 'CEPF' or sr.code == 'VCPF':
                    sum += sr.amount
            my_investment = 0.00
            my_allowed_rebate = 0.00
            if ex_80_c_id:
                my_investment = sum
                if my_investment <= ex_80_c_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_80_c_id.rebate
                slab_ids = []
                slab_ids.append((0, 0, {
                    'slab_id': rec.id,
                    'it_rule': '80_c',
                    'saving_master': ex_80_c_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                }))
                rec.slab_ids = slab_ids
            exempt_am = 0.00
            std_am = 0.00
            sum_pt = 0.00
            for std in rec.std_ded_ids:
                std_am += std.allowed_rebate
            for ex in rec.exemption_ids:
                exempt_am += ex.allowed_rebate
            pr_pt_id = self.env['hr.payslip.line'].sudo().search(
                [('slip_id.employee_id', '=', rec.employee_id.id), ('slip_id.state', '=', 'done'), ('code', '=', 'PTD'),
                 ('slip_id.date_from', '>', rec.date_range.date_start),
                 ('slip_id.date_to', '<', rec.date_range.date_end)])
            for pt in pr_pt_id:
                sum_pt += pt.amount
            if (rec.tax_salary_final + rec.previous_employer_income - exempt_am) > 0.00:
                rec.income_after_exemption = rec.tax_salary_final + rec.previous_employer_income - exempt_am
            else:
                rec.income_after_exemption = 0.00
            if rec.income_after_exemption - std_am > 0.00:
                rec.income_after_std_ded = rec.income_after_exemption - std_am
            else:
                rec.income_after_std_ded = 0.00
            if rec.income_after_std_ded - sum_pt > 0.00:
                rec.income_after_pro_tax = rec.income_after_std_ded - sum_pt
            else:
                rec.income_after_pro_tax = 0.00
            if (rec.income_after_pro_tax - rec.total_tds_paid - (
                    rec.allowed_rebate_under_80c + rec.allowed_rebate_under_80b + rec.allowed_rebate_under_80d + rec.allowed_rebate_under_80dsa + rec.allowed_rebate_under_80e + rec.allowed_rebate_under_80ccg + rec.allowed_rebate_under_tbhl + rec.allowed_rebate_under_80ee + rec.allowed_rebate_under_24 + rec.allowed_rebate_under_80cdd + rec.allowed_rebate_under_80mesdr)) > 0.00:
                rec.taxable_income = rec.income_after_pro_tax - rec.total_tds_paid - (
                        rec.allowed_rebate_under_80c + rec.allowed_rebate_under_80b + rec.allowed_rebate_under_80d + rec.allowed_rebate_under_80dsa + rec.allowed_rebate_under_80e + rec.allowed_rebate_under_80ccg + rec.allowed_rebate_under_tbhl + rec.allowed_rebate_under_80ee + rec.allowed_rebate_under_24 + rec.allowed_rebate_under_80cdd + rec.allowed_rebate_under_80mesdr)
            else:
                rec.taxable_income = 0.00
            rec.tax_computed_bool = True
            rec.sudo().button_payment_tax()
        return True
