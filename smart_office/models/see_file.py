from odoo import fields, models, api
from datetime import datetime
import requests
import json

class FolderMaster(models.Model):
    _name = 'see.file'

    my_url = fields.Text()
    url_attach = fields.Html()

    @api.onchange('my_url')
    def onchange_my_url(self):
        if self.my_url:
            self.url_attach = '<img id="img" src="%s"/>' % self.my_url