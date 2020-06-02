from odoo import fields, models, api, _
from datetime import datetime, date, timedelta
import requests
import json
from odoo.exceptions import UserError

class FolderMaster(models.Model):
    _name = 'folder.master'
    _description = 'folder.master'
    _rec_name ='folder_name'

    folder_name = fields.Char(string = 'File Name')


    current_owner_id = fields.Many2one('res.users', 'Current Owner')
    last_owner_id = fields.Many2one('res.users', 'Last Owner')

    sec_owner = fields.Many2many('res.users', string='Secondary Owners')

    previous_owner = fields.Many2many('res.users', string='Previous/Current Owners')




    date = fields.Date(string='Date', default = fields.Date.today())
    subject = fields.Many2one('code.subject', string='Subject')
    tags = fields.Many2many('muk_dms.tag', string='Tags')
    number = fields.Char(string = 'Number')
    status = fields.Selection([('normal', 'Normal'),
                               ('important', 'Important'),
                               ('urgent', 'Urgent')
                               ], string='Status')
    sequence = fields.Integer(string = 'Sequence')
    type = fields.Many2many('folder.type', string = "Type")
    description = fields.Text(string = 'Description')
    file_ids = fields.One2many('muk_dms.file','folder_id', string = 'Files')
    iframe_dashboard = fields.Text()
    my_view = fields.Text()
    my_dash = fields.Html('My Dash Html')
    dashboard_view = fields.Many2one('ir.ui.view')
    # green_ids = fields.Many2many('green.sheets','folder_id', string = 'Green Sheets')


    @api.model
    def create(self, vals):
        res = super(FolderMaster, self).create(vals)
        vals['last_owner_id'] = self.env.user.id
        vals['current_owner_id'] = self.env.user.id
        res.sudo().create_file()
        return res

    @api.multi
    def create_file(self):
        for res in self:
            data = {
                        'assign_name': res.folder_name,
                        'assign_no': res.number,
                        'assign_date': res.date,
                        'assign_subject': res.description,
                        'remarks': res.description,
                        'created_by': 1,
                        'doc_flow_id': 0,
                        'wing_id': 1,
                        'section_id': 0,
                        'designation_id': 78,


                    }
            req = requests.post('http://103.92.47.152/STPI/www/web-service/add-assignment/', data=data,
                                json=None)
            try:
                pastebin_url = req.text
                print('============Patebin url=================', pastebin_url)
                dictionary = json.loads(pastebin_url)
                res.iframe_dashboard = str(dictionary["response"][0]['notesheet']) + str('?type=STPI&user_id=1')
                # res.my_dash = '<img id="img" src="%s"/>' % res.iframe_dashboard
                # res.iframe_dashboard = 'http://103.92.47.152/STPI/www/assignment/note-sheet/717?type=STPI&user_id=1'
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
        if self.iframe_dashboard:
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
    @api.depends('subject')
    def name_get(self):
        res = []
        name = ''
        for record in self:
            count = 0
            sur_usr = self.env.user.branch_id.name
            fy = self.env['date.range'].search([('type_id.name', '=', 'Fiscal Year'),('date_start', '<=', datetime.now().date()),('date_end', '>=', datetime.now().date())], limit=1)
            files = self.env['muk_dms.file'].search([('create_date', '>=', fy.date_start),('create_date', '<=', fy.date_end)])
            for file in files:
                count+=1
            if record.subject:
                name = (record.subject.code) + '/' + str(count) + '/'  + str(record.env.user.branch_id.name) + '/'  + str(fy.name)
            else:
                name = 'File'
            res.append((record.id, name))
        return res


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