from odoo import fields, models, api
from addons.board.controllers.main import Board
from datetime import datetime
import requests
import json

class FolderMaster(models.Model):
    _name = 'see.file'

    my_url = fields.Text()
