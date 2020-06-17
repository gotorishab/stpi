from odoo import fields, models, api
from datetime import datetime

class AddReference(models.TransientModel):
    _name = 'write.correspondence'
    _description = 'Add Reference'



    cooespondence_ids = fields.Many2many('muk_dms.file', string='Correspondence')
    current_user_id = fields.Many2one('res.users')
    branch_id = fields.Many2one('res.branch', 'Branch')
    department_id = fields.Many2one('hr.department', 'Department')
    created_on = fields.Date(string='Date', default = fields.Date.today())
    select_template = fields.Many2one('select.template.html')
    template_html = fields.Html('Template')
    version = fields.Many2one('dispatch.document', string='Version')
    previousversion = fields.Many2one('dispatch.document', string = 'Previous Version')
    folder_id = fields.Many2one('folder.master', string="Select File")

    @api.onchange('select_template')
    def get_template(self):
        if self.select_template:
            self.template_html = self.select_template.template


    def confirm_button(self):
        if self:
            current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            letter_id = []
            for letter in self.folder_id.file_ids:
                letter_id.append(letter.id)
            dd = self.env['dispatch.document'].create({
                'name': 1,
                'template_html': self.template_html,
                'select_template': self.select_template.id,
                'current_user_id': (current_employee.user_id.id),
                'department_id': (current_employee.department_id.id),
                'job_id': (current_employee.job_id.id),
                'branch_id': (current_employee.branch_id.id),
                'created_on': datetime.now().date(),
                'folder_id': self.folder_id.id,
                'state': 'draft',
            })
            dd.version = dd.id
            dd.previousversion = dd.id
            dd.cooespondence_ids = [(6, 0, letter_id)]
            form_view = self.env.ref('smart_office.foldermaster_form_view')
            tree_view = self.env.ref('smart_office.foldermaster_tree_view1')
            value = {
                'domain': str([('id', '=', self.folder_id.id)]),
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'folder.master',
                'view_id': False,
                'views': [(form_view and form_view.id or False, 'form'),
                          (tree_view and tree_view.id or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': self.folder_id.id,
                'target': 'current',
                'nodestroy': True
            }
            return value



class SelectTemplate(models.Model):
    _name = 'select.template.html'
    _description = 'Select Template'

    name = fields.Char('Name')
    template = fields.Html('Template')