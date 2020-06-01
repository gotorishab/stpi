from odoo import http, tools, SUPERUSER_ID, _
from odoo.addons.website.controllers.main import Website
from odoo.http import request
import json, sys, base64, pytz
from datetime import datetime, date, timedelta
from functools import reduce
from odoo import http
import logging, uuid, werkzeug
import base64


_logger = logging.getLogger(__name__)


class Maincontroller(Website):

    @http.route('/getEligibilityCritirea', type='http', auth="public", website=True, csrf=False)
    def getEligibilityCritirea(self, **kw):
        if kw.get('courses_id'):
            course_id = request.env['op.admission.register'].sudo().search(
                [('id', '=', int(kw.get('courses_id')))])
            eligibility_citirea = ""
            if course_id:
                eligibility_citirea = course_id.batch_id.course_id.eligibility_citirea
            return json.dumps(dict(eligibility_citirea=str(eligibility_citirea)))
