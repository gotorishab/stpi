from odoo import api, fields, models, _
from odoo.http import request
from datetime import date
from datetime import datetime


class KnowledgeCreateTasks(models.Model):
    _name = "knowledge.create.task"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Knowledge Create Task"


    task_title = fields.Char('Enter Task Title :')
    kaizen_code = fields.Char('Kaizen Code :')
    target_date = fields.Date('Task Target Date :')
    description = fields.Char('Enter Task Description :')
    # user_ids = fields.Many2many('res.users',string='Assigned To')
    task_user_ids = fields.One2many('knowledge.users.task','create_task_id',string='Assigned To')

    state = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Submitted'), ('cancelled', 'Cancelled')
         ], required=True, default='draft', string='Status', track_visibility='always')


    def button_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})


    def button_submit(self):
        for rec in self:
            for line in rec.task_user_ids:
                self.env['knowledge.assigned.task'].create({
                    'state': 'draft',
                    'user_id': line.user_id.id,
                    'main_task': rec.id,
                    'task_title': rec.task_title,
                    'kaizen_code': rec.kaizen_code,
                    'target_date': rec.target_date,
                    'description': rec.description,
                })
            rec.write({'state': 'submitted'})

    def button_cancel(self):
        for rec in self:
            rec.write({'state': 'cancelled'})


class KnowledgeUsersTasks(models.Model):
    _name = "knowledge.users.task"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Knowledge Users Task"

    create_task_id = fields.Many2one('knowledge.create.task')
    unit_id = fields.Many2one('vardhman.unit.master',string='Unit')
    department_id = fields.Many2one('vhr.department',string='Department')
    user_id = fields.Many2one('res.users', string='Assigned To')


    @api.onchange('unit_id','department_id')
    def onchange_user(self):
        for rec in self:
            if rec.department_id.id and not rec.unit_id.id:
                return {'domain': {'user_id': [('department_id', '=', rec.department_id.id)]}}
            elif rec.unit_id.id and not rec.department_id.id:
                return {'domain': {'user_id': [('unit_id', '=', rec.unit_id.id)]}}
            elif rec.unit_id.id and rec.department_id.id:
                return {'domain': {'user_id': [('unit_id', '=', rec.unit_id.id),('department_id', '=', rec.department_id.id)]}}
            else:
                return {'domain': {'user_id': [('id', '!=', 0)]}}

    @api.onchange('user_id')
    def onchange_emp_get_eve(self):
        for rec in self:
            if not rec.department_id.id:
                rec.department_id = rec.user_id.department_id.id
            if not rec.unit_id.id:
                rec.unit_id = rec.user_id.unit_id.id
                
                
class KnowledgeAssignedTasks(models.Model):
    _name = "knowledge.assigned.task"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Knowledge Assigned Task"

    task_title = fields.Char('Enter Task Title :')
    kaizen_code = fields.Char('Kaizen Code :')
    target_date = fields.Date('Task Target Date :')
    description = fields.Char('Enter Task Description :')
    main_task = fields.Many2one('knowledge.create.task',string='Main Task')
    user_id = fields.Many2one('res.users',string='Assigned To')

    state = fields.Selection(
        [('draft', 'Draft'), ('working', 'Working'), ('completed', 'Completed'), ('overdue', 'Overdue'), ('cancelled', 'Cancelled')
         ], required=True, default='draft', string='Status', track_visibility='always')

    def button_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    def button_submit(self):
        for rec in self:
            rec.write({'state': 'working'})

    def button_complete(self):
        for rec in self:
            rec.write({'state': 'completed'})

    def button_overdue(self):
        for rec in self:
            rec.write({'state': 'overdue'})

    def button_cancel(self):
        for rec in self:
            rec.write({'state': 'cancelled'})


    def knowledge_assigned_task_cron(self):
        active_ads = self.env['knowledge.assigned.task'].search(
            [('state', 'in', ['draft','working']), ('target_date', '<=', datetime.now().date())])
        for rec in active_ads:
            rec.sudo().button_overdue()