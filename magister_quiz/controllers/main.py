from odoo import http
from odoo.http import request
from werkzeug.utils import redirect
import logging
import json

_logger = logging.getLogger(__name__)

class SurveyRedirectController(http.Controller):

    @http.route(['/play/<string:survey_name>'], type='http', auth='public')
    def redirect_to_survey(self, survey_name):
        
        # Buscar el formulario por nombre (título)
        survey = request.env['survey.survey'].sudo().search([('title', 'ilike', survey_name)], limit=1)
        _logger.info(f"Intentando redirigir a: {survey.title}")

        if survey:
            # Redirigir a la URL original de Odoo
            return redirect(f'/survey/start/{survey.access_token}')
        else:
            return request.render('website.404')
        
    @http.route('/quiz/timer/<string:survey_name>', type='http', auth='public')
    def get_timer_config(self, survey_name):
        survey = request.env['survey.survey'].sudo().search([('title', 'ilike', survey_name)], limit=1)
        data = {
            'is_question_timed': survey.is_question_timed,
            'time_per_question': survey.time_per_question,
        }
        return request.make_response(json.dumps(data), headers={'Content-Type': 'application/json'})
