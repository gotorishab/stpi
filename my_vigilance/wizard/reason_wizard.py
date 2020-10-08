from odoo import api, fields, models,_


class Reason_wizard(models.TransientModel):
    _name = 'revert.vigilance.wizard'


    res_id = fields.Integer('ID')
    res_model = fields.Char('Model')
    reason_des = fields.Text('Remarks: ')
    penalty = fields.Many2one('vigilance.penalty', string='Penalty: ')

    def button_confirm(self):

        model_id = self.env[self.res_model].browse(self.res_id)
        _body = (_(
            (
                "Action Taken: <ul><b>{0}</b></ul> ").format(self.reason_des)))
        model_id.message_post(body=_body)
        model_id.write({'state': 'closed'})
