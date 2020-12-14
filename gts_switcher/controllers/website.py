from odoo import http
from odoo.addons.http_routing.models.ir_http import unslug
from odoo.http import request
import jwt
import odoo
from odoo import models, fields, api, _

# key = 'chalhatpagle'
key = ",jy`\;4Xpe7%KKL$.VNJ'.s6)wErQa"


class IntermediateWebsitePage(http.Controller):

    @http.route(['/login/intermediate'], type='http', auth="user", website=True)
    def intermediate_detail(self, user_id=None, **post):
        user_id = request.env.user
        connection_rec=request.env['server.connection'].search([], limit=1)
        base_url= http.request.env["ir.config_parameter"].sudo().get_param("web.base.url").strip()
        url=str(connection_rec.url).strip()
        encoded_jwt = jwt.encode({'token': user_id.token}, key)
        if user_id:
            partner_sudo = request.env['res.users'].sudo().browse(user_id)
            if partner_sudo.exists():
                values = {
                    'login_user': partner_sudo,
                    'access_type': user_id.access_type,
                    'edit_page': True,
                    'url': url,
                    'base_url': base_url,
                    'login':request.env.user.login,
                    'instance_type':connection_rec.instance_type,
                    'password':str(encoded_jwt.decode("utf-8"))
                }
                return request.render("gts_switcher.intermediate_page", values)
        return request.not_found()

