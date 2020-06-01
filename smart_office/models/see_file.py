from odoo import fields, models, api
from addons.board.controllers.main import Board
from datetime import datetime
import requests
import json

class FolderMaster(models.Model):
    _name = 'see.file'

    my_url = fields.Text()
    url_attach = fields.Html()

    # @api.onchange('my_url')
    # def onchange_my_url(self):
    #     if self.my_url:
    #         self.url_attach = '<img id="img" src="%s"/>' % self.my_url

    desc = fields.Char(required=True)
    url = fields.Char(required=True)
    height = fields.Integer(default=300)

    @api.model
    def create(self, vals):
        rec = super(FolderMaster, self).create(vals)
        # add kanban view to users dashboard

        context_to_save = {
            "uid": rec.create_uid._context["uid"],
            "dashboard_merge_domains_contexts": False,
            "tz": rec.create_uid._context["tz"],
            "params": {"action": rec.create_uid._context["params"]["action"]},
            "group_by": [],
            "lang": rec.create_uid._context["lang"]
        }

        B = Board()
        B.add_to_dashboard(context_to_save=context_to_save,
                           domain=[['id', '=', rec.id], ['id', '=', rec.id]],
                           action_id=context_to_save["params"]["action"],
                           name=vals["desc"],
                           view_mode='kanban')
        return rec
