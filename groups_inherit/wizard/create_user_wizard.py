from odoo import api, fields, models,_


class createuser_wizard(models.TransientModel):
    _name = 'createuser.wizard'

    @api.model
    def _get_branch(self):
        return self.env.user.default_branch_id

    res_id = fields.Integer('ID')
    res_model = fields.Char('Model')

    name = fields.Char('Name')
    login = fields.Char('Login')
    groups_id = fields.Many2many('res.groups',string='Groups', domain="[('stpi', '=', True)]")
    branch_ids = fields.Many2many('res.branch', default=_get_branch)
    default_branch_id = fields.Many2one('res.branch', string='Default branch',default=_get_branch)

    def button_confirm(self):
        for rec in self:
            model_id = rec.env[rec.res_model].browse(rec.res_id)
            Users = rec.env['res.users'].with_context({'no_reset_password': True, 'mail_create_nosubscribe': True})
            user = Users.create({
                'name': rec.name,
                'login': rec.login,
                'email': model_id.work_email,
                'notification_type': 'inbox',
                'default_branch_id':rec.default_branch_id.id,
                'sel_groups_1_9_10':1,
                'branch_ids': [(6, 0, rec.branch_ids.ids)]
            })
            for group in rec.groups_id:
                group.users += user
            comp_model = self.env['res.users'].search([('login', '=', rec.login)], limit=1)
            _body = (_(
                (
                    "<ul><b>User Created: {0} </b></ul> ").format(rec.login)))
            model_id.message_post(body=_body)
            model_id.user_id = comp_model.id



