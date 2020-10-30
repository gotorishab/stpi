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