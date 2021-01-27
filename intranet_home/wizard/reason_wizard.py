from odoo import api, fields, models,_


class Reason_wizard(models.TransientModel):
    _name = 'rejectstory.wizard'


    res_id = fields.Integer('ID')
    res_model = fields.Char('Model')
    reason_des = fields.Many2one('vardhman.story.rejection', string='Reason for Rejection')

    def button_confirm(self):
        model_id = self.env[self.res_model].browse(self.res_id)
        _body = (_(
            (
                "Reason of Rejection: <ul><b>{0}</b></ul> ").format(self.reason_des.name)))
        model_id.message_post(body=_body)
        model_id.write({'reason_des':self.reason_des.id})
        model_id.write({'state':'rejected'})
