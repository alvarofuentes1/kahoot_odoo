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


    @http.route('/survey/set_response_time', type='json', auth='user')
    def set_response_time(self, **kwargs):
        question_id = kwargs.get('question_id')
        response_time = kwargs.get('response_time')

        _logger.info(f"Recibiendo tiempo de respuesta: {response_time} para la línea de entrada: {question_id}")

        if not question_id or response_time is None:
            return {"status": "error", "message": "Datos incompletos"}

        input_line = request.env['survey.user_input_line'].sudo().browse(int(question_id))
        if input_line.exists():
            input_line.write({'response_time': float(response_time)})
            return {"status": "ok"}
        else:
            return {"status": "error", "message": "Respuesta no encontrada"}
        
    
    @http.route('/survey/<int:survey_id>/ranking', type='json', auth='public', methods=['GET'])
    def get_ranking(self, survey_id):
        # Obtener el ranking del TOP 10 para la encuesta
        rankings = self.env['survey.session.ranking'].search([
            ('survey_id', '=', survey_id)
        ], order='rank_position asc', limit=10)

        # Formatear la respuesta
        ranking_data = []
        for rank in rankings:
            ranking_data.append({
                'user_name': rank.user_id.name,
                'total_score': rank.total_score,
                'rank_position': rank.rank_position,
            })
        
        return {'ranking': ranking_data}