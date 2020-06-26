from odoo import fields, models, api, _
from datetime import datetime, date, timedelta
import base64


class DispatchDocument(models.Model):
    _name = 'dispatch.document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Dispatch Document'
    _rec_name = 'name'

    name = fields.Float('Number')
    cooespondence_ids = fields.Many2many('muk_dms.file', string='Correspondence', track_visibility='always')
    current_user_id = fields.Many2one('res.users', track_visibility='always')
    branch_id = fields.Many2one('res.branch', 'Branch', track_visibility='always')
    department_id = fields.Many2one('hr.department', 'Department', track_visibility='always')
    job_id = fields.Many2one('hr.job', 'Job Position', track_visibility='always')
    created_on = fields.Date(string='Date', default = fields.Date.today(), track_visibility='always')
    select_template = fields.Many2one('select.template.html', track_visibility='always')
    template_html = fields.Html('Template', track_visibility='always')
    basic_version = fields.Float('Basic Version')
    print_heading = fields.Char('Heading')
    dispatch_mode_ids = fields.One2many('dispatch.document.mode','dispatch_id',string='Dispatch Mode')

    version = fields.Many2one('dispatch.document', string='Version', track_visibility='always')
    previousversion = fields.Many2one('dispatch.document', string='Previous  Version', track_visibility='always')

    folder_id = fields.Many2one('folder.master', string="File", track_visibility='always')
    dispatch_mode = fields.Selection(
        [('hand_to_hand', 'Hand to Hand'),('email', 'Email'), ('fax', 'Fax'), ('splmess', 'Spl. Messenger'), ('post', 'Post')
         ], string='Dispatch Mode', track_visibility='always')
    enter_mode = fields.Char('Enter Mode of Dispatch')
    state = fields.Selection(
        [('draft', 'Draft'),('obsolete', 'Obsolete'), ('reject', 'Reject'), ('ready_for_dispatched', 'Ready for Dispatch'), ('dispatched', 'Dispatched')
         ], required=True, default='draft', string='Status', track_visibility='always')



    @api.multi
    def button_edit(self):
        for rec in self:
            cout = 0
            current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            dis_name = self.env['dispatch.document'].sudo().search([('folder_id', '=', self.folder_id.id),('basic_version', '=', self.basic_version)])
            m_name = self.env['dispatch.document'].sudo().search([('folder_id', '=', self.folder_id.id)])
            for ct in m_name:
                cout+=1
            if cout <1:
                name = 1
            else:
                name = rec.name
            dd = self.env['dispatch.document'].create({
                'name': name + 0.001,
                'basic_version': int(rec.name),
                'previousversion': rec.id,
                'dispatch_mode': rec.dispatch_mode,
                'template_html': rec.template_html,
                'select_template': rec.select_template.id,
                'current_user_id': current_employee.user_id.id,
                'department_id': current_employee.department_id.id,
                'job_id': current_employee.job_id.id,
                'branch_id': current_employee.branch_id.id,
                'created_on': datetime.now().date(),
                'folder_id': rec.folder_id.id,
                'state': 'draft',
                'cooespondence_ids': rec.cooespondence_ids.ids,
            })
            dd.version = dd.id
            # rec.sudo().button_obsellete()
            form_view = self.env.ref('smart_office.document_dispatch_form_view')
            tree_view = self.env.ref('smart_office.dispatch_document_tree_view1')
            value = {
                'domain': str([('id', '=', dd.id)]),
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'dispatch.document',
                'view_id': False,
                'views': [(form_view and form_view.id or False, 'form'),
                          (tree_view and tree_view.id or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': dd.id,
                'target': 'new',
                'nodestroy': True
            }
            return value


    @api.multi
    def button_obsellete(self):
        for rec in self:
            rec.write({'state': 'obsolete'})

    @api.multi
    def button_ready_for_dispatch(self):
        for rec in self:
            dis_name = self.env['dispatch.document'].sudo().search([('id', '!=', rec.id),('folder_id', '=', rec.folder_id.id),('basic_version', '=', rec.basic_version)])
            for dd in dis_name:
                dd.sudo().button_obsellete()
            rec.write({'state': 'ready_for_dispatched'})



    @api.multi
    def print_dispatch_document(self):
        pdf = self.env.ref('smart_office.dispatch_document_status_print').get_pdf(self)
        print('================a==================', pdf)
        report_name = "smart_office.dispatch_document_status_print"
        # pdf = self.env['smart_office.dispatch_document_status_print'].sudo().get_pdf([self.id], report_name)
        report_file = base64.encodestring(pdf)
        print('================report_file==================', report_file)
        # print('============================================,self.env.ref('smart_office.dispatch_document_status_print').report_action(self))
        return self.env.ref('smart_office.dispatch_document_status_print').report_action(self)



    @api.multi
    def button_dispatch(self):
        for rec in self:
            rec.write({'state': 'dispatched'})

    @api.multi
    def button_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'reject'})


class DispatchDocumentMode(models.Model):
    _name = 'dispatch.document.mode'
    _description = 'Dispatch Document'

    dispatch_id = fields.Many2one('dispatch.document', string='Dispatch Document')
    dispatch_mode = fields.Selection(
        [('hand_to_hand', 'Hand to Hand'),('email', 'Email'), ('fax', 'Fax'), ('splmess', 'Spl. Messenger'), ('post', 'Post')
         ], string='Dispatch Mode', track_visibility='always')
    enter_mode = fields.Char('Dispatch Details')
    dispatch_number = fields.Char('Dispatch Number')