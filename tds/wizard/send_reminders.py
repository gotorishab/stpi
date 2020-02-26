from odoo import api, fields, models,_


class SendTdsReminder(models.TransientModel):
    _name = 'send.tds.reminder'
    _description = 'Send Reminder'



    def send_reminder_action_button(self):
        self.ensure_one()
        template = self.env.ref(
            'tds.email_template_tds',
            False,
        )
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        ctx = dict(
            default_composition_mode='comment',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_model='send.tds.reminder',
        )
        mw = {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
        return mw
