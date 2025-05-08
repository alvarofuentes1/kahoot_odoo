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

        # Procesar el cuerpo de la solicitud manualmente
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
        except json.JSONDecodeError:
            return {"status": "error", "message": "Cuerpo de la solicitud no es un JSON válido"}      

        question_id = data.get('question_id')
        response_time = data.get('response_time')
        user_input_token = data.get('user_input_token')
        
        if not (question_id and response_time and user_input_token):
            return {"status": "error", "message": "Datos incompletos"}    
        
        user_input = request.env['survey.user_input'].sudo().search([
            ('access_token', '=', user_input_token),
        ], limit=1)
        
        if not user_input:
            return {"status": "error", "message": "Token de usuario no encontrado"}

        input_line = request.env['survey.user_input.line'].sudo().search([
            ('question_id', '=', int(question_id)),
            ('user_input_id', '=', user_input.id),
        ],order="create_date desc", limit=1)
        
        if input_line.exists():
            input_line.write({'response_time': float(response_time)})
            input_line._compute_score() #Funcion para asignar puntuación en base al tiempo de respuesta
            _logger.info("User input line actualizado: %s", input_line.read())
            
            
            return {"status": "ok"}
        else:
            return {"status": "error", "message": "Respuesta no encontrada"}
    
    def _prepare_question_html(self, survey_sudo, answer_sudo, **post):
            """ Survey page navigation is done in AJAX. This function prepare the 'next page' to display in html
            and send back this html to the survey_form widget that will inject it into the page.
            Background url must be given to the caller in order to process its refresh as we don't have the next question
            object at frontend side."""
            survey_data = self._prepare_survey_data(survey_sudo, answer_sudo, **post)
            
            last_answer_line = answer_sudo.user_input_line_ids.sorted('create_date')[-1:]  # Última respuesta
            conditional_question = None

            if last_answer_line:
                suggested = last_answer_line.suggested_answer_id
                if suggested and suggested.is_conditional_answer and suggested.next_question_id:
                    conditional_question = suggested.next_question_id

            if conditional_question:
                survey_data['question'] = conditional_question

            if answer_sudo.state == 'done':
                survey_content = request.env['ir.qweb']._render('survey.survey_fill_form_done', survey_data)
            else:
                survey_content = request.env['ir.qweb']._render('survey.survey_fill_form_in_progress', survey_data)

            survey_progress = False
            if answer_sudo.state == 'in_progress' and not survey_data.get('question', request.env['survey.question']).is_page:
                if survey_sudo.questions_layout == 'page_per_section':
                    page_ids = survey_sudo.page_ids.ids
                    survey_progress = request.env['ir.qweb']._render('survey.survey_progression', {
                        'survey': survey_sudo,
                        'page_ids': page_ids,
                        'page_number': page_ids.index(survey_data['page'].id) + (1 if survey_sudo.progression_mode == 'number' else 0)
                    })
                elif survey_sudo.questions_layout == 'page_per_question':
                    page_ids = (answer_sudo.predefined_question_ids.ids
                                if not answer_sudo.is_session_answer and survey_sudo.questions_selection == 'random'
                                else survey_sudo.question_ids.ids)
                    survey_progress = request.env['ir.qweb']._render('survey.survey_progression', {
                        'survey': survey_sudo,
                        'page_ids': page_ids,
                        'page_number': page_ids.index(survey_data['question'].id)
                    })

            background_image_url = survey_sudo.background_image_url
            if 'question' in survey_data:
                background_image_url = survey_data['question'].background_image_url
            elif 'page' in survey_data:
                background_image_url = survey_data['page'].background_image_url

            return {
                'has_skipped_questions': any(answer_sudo._get_skipped_questions()),
                'survey_content': survey_content,
                'survey_progress': survey_progress,
                'survey_navigation': request.env['ir.qweb']._render('survey.survey_navigation', survey_data),
                'background_image_url': background_image_url
            }