from odoo import fields, models, api
from datetime import datetime
import requests
import json

class FolderMaster(models.Model):
    _name = 'folder.master'
    _description = 'folder.master'
    _rec_name ='folder_name'

    folder_name = fields.Char(string = 'File Name')

    date = fields.Date(string='Date', default = fields.Date.today())
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
            pastebin_url = req.text
            dictionary = json.loads(pastebin_url)
            res.iframe_dashboard = str(dictionary["response"][0]['notesheet']) + str('?type=STPI&user_id=1')
            res.my_dash = '<img id="img" src="%s"/>' % res.iframe_dashboard
            # res.iframe_dashboard = 'http://103.92.47.152/STPI/www/assignment/note-sheet/717?type=STPI&user_id=1'
            req.raise_for_status()
            status = req.status_code
            if int(status) in (204, 404):
                response = False
            else:
                response = req.json()
            return (status, response)

    @api.multi
    def deal_with_file(self):
        print('=================================iframe=======================', self.iframe_dashboard)
        # self.iframe_dashboard = str(self.iframe_dashboard) + str('?type=STPI&user_id=1')
        total_iframe = self.iframe_dashboard.replace('800', '100%').replace('"600"', '"100%"').replace(
            'allowtransparency', '')
        total_form = '''<form string="Embedded Webpage" version="7.0" edit="false" create="false">

                      <div style="position:absolute; left:0; top:0; width:100%; height:100%;">
                      <iframe marginheight="0" marginwidth="0" frameborder = "0" 
                src="{0}" width="100%" height="1000"/>                       
                         
                      </div>

                  </form>'''.format(total_iframe)
        self.my_view = total_form
        # print('=====================total form====================', total_form)
        print('=====================My view====================', self.my_view)
        # data = {
        #     'username': 'admin',
        #     'password': 'password',
        # }
        # req = requests.post(self.iframe_dashboard, data=data,
        #                     json=None)
        ab =  {
            'name': 'Notesheet',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'see.file',
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref('smart_office.see_file_view1').id,
            'context': {
                                'default_my_url': self.iframe_dashboard}
            # 'arch': self.my_view,
        }
        print('==============ab================', ab)
        return ab



class FolderType(models.Model):
    _name = 'folder.type'
    _description = 'Folder Type'

    name = fields.Char(string = 'Name')