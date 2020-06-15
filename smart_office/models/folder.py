from odoo import fields, models, api, _
from datetime import datetime, date, timedelta
import requests
import json
from odoo.exceptions import UserError

class FolderMaster(models.Model):
    _name = 'folder.master'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'folder.master'
    _rec_name ='number'

    folder_name = fields.Char(string = 'File Name',track_visibility='always')
    old_file_number = fields.Char(string = 'Old File Number',track_visibility='always')


    current_owner_id = fields.Many2one('res.users', 'Current Owner',track_visibility='always')
    last_owner_id = fields.Many2one('res.users', 'Last Owner',track_visibility='always')

    sec_owner = fields.Many2many('res.users', string='Secondary Owners',track_visibility='always')

    previous_owner = fields.Many2many('res.users', string='Previous/Current Owners',track_visibility='always')

    date = fields.Date(string='Date', default = fields.Date.today(),track_visibility='always')
    subject = fields.Many2one('code.subject', string='Subject',track_visibility='always')
    tags = fields.Many2many('muk_dms.tag', string='Tags',track_visibility='always')
    number = fields.Char(string = 'Number',track_visibility='always')
    status = fields.Selection([('normal', 'Normal'),
                               ('important', 'Important'),
                               ('urgent', 'Urgent')
                               ], string='Status',track_visibility='always')
    sequence = fields.Integer(string = 'Sequence')
    first_doc_id = fields.Integer(string = 'First Doc Id')
    type = fields.Many2many('folder.type', string = "Type",track_visibility='always')
    description = fields.Text(string = 'Description',track_visibility='always')
    file_ids = fields.One2many('muk_dms.file','folder_id', string = 'Files',track_visibility='always')
    iframe_dashboard = fields.Text()
    folder_track_ids = fields.One2many('folder.tracking.information', 'create_let_id', string = "Files")
    my_view = fields.Text()
    my_dash = fields.Html('My Dash Html')
    dashboard_view = fields.Many2one('ir.ui.view')
    state = fields.Selection(
        [('draft', 'Draft'), ('in_progress', 'In Progress'), ('closed', 'Closed')
         ], required=True, default='draft', string='Status',track_visibility='always')
    # green_ids = fields.Many2many('green.sheets','folder_id', string = 'Green Sheets')


    @api.model
    def create(self, vals):
        res = super(FolderMaster, self).create(vals)
        vals['last_owner_id'] = self.env.user.id
        vals['current_owner_id'] = self.env.user.id
        res.current_owner_id = self.env.user.id
        res.last_owner_id = self.env.user.id
        name = ''
        count = 0
        current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        sur_usr = current_employee.branch_id.name
        d_id = current_employee.department_id.stpi_doc_id
        fy = self.env['date.range'].search(
            [('type_id.name', '=', 'Fiscal Year'), ('date_start', '<=', datetime.now().date()),
             ('date_end', '>=', datetime.now().date())], limit=1)
        files = self.env['muk_dms.file'].search(
            [('create_date', '>=', fy.date_start), ('create_date', '<=', fy.date_end)])
        for file in files:
            count += 1
        name = (res.subject.code) + '(' + str(count) + ')/' + str(d_id) + '/' + str(sur_usr) + '/' + str(
                fy.name)
        res.number = str(name)
        self.env['file.tracker.report'].create({
            'name': str(res.folder_name),
            'number': str(res.number),
            'type': 'File',
            'created_by': str(current_employee.user_id.name),
            'created_by_dept': str(current_employee.department_id.name),
            'created_by_jobpos': str(current_employee.job_id.name),
            'created_by_branch': str(current_employee.branch_id.name),
            'create_date': datetime.now().date(),
            'action_taken': 'file_created',
            'remarks': res.description,
            'details': "File created on {}".format(datetime.now().date())
        })
        res.sudo().create_file()
        return res

    @api.multi
    def create_file(self):
        for res in self:
            seq = self.env['ir.sequence'].next_by_code('folder.master')
            res.sequence = int(seq)
            data = {
                        'assign_name': res.folder_name,
                        'assign_no': res.sequence,
                        'assign_date': res.date,
                        'assign_subject': (res.subject.subject),
                        'remarks': res.description,
                        'created_by': 1,
                        'doc_flow_id': 0,
                        'wing_id': 1,
                        'section_id': 0,
                        'designation_id': 78,
                        'document_ids': res.first_doc_id,
                    }
            req = requests.post('http://103.92.47.152/STPI/www/web-service/add-assignment/', data=data,
                                json=None)
            try:
                pastebin_url = req.text
                # print('============Patebin url=================', pastebin_url)
                dictionary = json.loads(pastebin_url)
                res.iframe_dashboard = str(dictionary["response"][0]['notesheet']) + str('?type=STPI&user_id=1')
                req.raise_for_status()
                status = req.status_code
                if int(status) in (204, 404):
                    response = False
                else:
                    response = req.json()
                return (status, response)
            except Exception as e:
                print('=============Error==========',e)


    @api.multi
    def deal_with_file(self):
        req = requests.post('http://35.244.32.228:8369/letterlist?jsonrpc=2.0&params={}',
                            json=None)
        print('===================================================',req)
        print('===================================================',req.text)
        if self.iframe_dashboard:
            self.write({'state': 'in_progress'})
            total_iframe = self.iframe_dashboard.replace('800', '100%').replace('"600"', '"100%"').replace(
                'allowtransparency', '')
            file_ids = self.env['see.file'].sudo().search([])
            for id in file_ids:
                id.unlink()
            html = '''
                    <html>
                    <body>
                    <iframe marginheight="0" marginwidth="0" frameborder = "0" 
                    src="{0}" width="100%" height="1000"/>
                    </body>
                    </html>
                    '''.format(total_iframe)
            self.env['see.file'].sudo().create({
                "my_url":self.iframe_dashboard,
                "my_url_text":html
            })
            return  {
                'name': 'Notesheet',
                'view_type': 'form',
                'view_mode': 'kanban',
                'res_model': 'see.file',
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('smart_office.see_file_view1_kanban').id
            }
        else:
            raise UserError(_('URL not defined'))


    @api.multi
    @api.depends('number')
    def name_get(self):
        res = []
        name = ''
        for record in self:
            if record.number:
                name = record.number
            else:
                count = 0
                current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                sur_usr = current_employee.branch_id.name
                d_id = current_employee.department_id.stpi_doc_id
                fy = self.env['date.range'].search(
                    [('type_id.name', '=', 'Fiscal Year'), ('date_start', '<=', datetime.now().date()),
                     ('date_end', '>=', datetime.now().date())], limit=1)
                files = self.env['muk_dms.file'].search(
                    [('create_date', '>=', fy.date_start), ('create_date', '<=', fy.date_end)])
                for file in files:
                    count += 1
                if self.subject:
                    name = (self.subject.code) + '(' + str(count) + ')/' + str(d_id) + '/' + str(sur_usr) + '/' + str(
                        fy.name)
                else:
                    name = 'File'
            res.append((record.id, name))
        return res

    @api.multi
    def button_submit(self):
        for rec in self:
            rec.write({'state': 'in_progress'})

    @api.multi
    def button_close(self):
        for rec in self:
            current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            rec.env['file.tracker.report'].create({
                'name': str(rec.folder_name),
                'number': str(rec.number),
                'type': 'File',
                'closed_by': str(current_employee.user_id.name),
                'closed_by_dept': str(current_employee.department_id.name),
                'closed_by_jobpos': str(current_employee.job_id.name),
                'closed_by_branch': str(current_employee.branch_id.name),
                'close_date': datetime.now().date(),
                'action_taken': 'file_closed',
                'remarks': rec.description,
                'details': "File closed on {}".format(datetime.now().date())
            })
            rec.write({'state': 'closed'})

    @api.multi
    def button_reset_to_draft(self):
        for rec in self:
            current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            rec.env['file.tracker.report'].create({
                'name': str(rec.folder_name),
                'number': str(rec.number),
                'type': 'File',
                'repoen_by': str(current_employee.user_id.name),
                'repoen_by_dept': str(current_employee.department_id.name),
                'repoen_by_jobpos': str(current_employee.job_id.name),
                'repoen_by_branch': str(current_employee.branch_id.name),
                'repoen_date': datetime.now().date(),
                'action_taken': 'file_repoened',
                'remarks': rec.description,
                'details': "File repoen on {}".format(datetime.now().date())
            })
            rec.write({'state': 'draft'})



    @api.multi
    def action_cancel(self):
        for rec in self:
            rec.sudo().button_reset_to_draft()
    @api.multi
    def action_refuse(self):
        for rec in self:
            rec.sudo().button_reset_to_draft()




class FolderType(models.Model):
    _name = 'folder.type'
    _description = 'Folder Type'

    name = fields.Char(string = 'Name')

class SubjectMainHeads(models.Model):
    _name = 'code.subject'
    _description = 'Code Subject'
    _rec_name = 'subject'

    code = fields.Char(string='Code')
    subject = fields.Char(string = 'Subject')