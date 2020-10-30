from odoo import fields, models, api
from datetime import datetime
import requests
import json

class CreateFolder(models.TransientModel):
    _name = 'part.file.wizard'
    _description = 'Wizard of Part File'


    deffolderid = fields.Many2one('folder.master')
    folder_id = fields.Many2many('folder.master', string="Select File")
    description = fields.Text(string = 'Description')


    def confirm_button(self):
        if self:
            for file in self.folder_id:
                file.sudo().button_close()
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