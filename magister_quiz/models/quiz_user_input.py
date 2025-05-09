
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

        
class QuizUserInput(models.Model):
    _inherit = "survey.user_input"
    
    session_ranking_ids = fields.One2many("survey.session_ranking", "user_input_id")

    def has_selected_the_trigger_answer_for(self, question):
        """Check if the user selected an answer that triggers this question."""
        self.ensure_one()
        for line in self.user_input_line_ids:
            # Revisamos si la respuesta marcada tiene como siguiente esta pregunta
            answer = line.suggested_answer_id
            if answer and answer.next_conditional_question_id == question:
                return True
        return False
    
    def _save_lines(self, question, answer, comment=None, overwrite_existing=True):
        """ Sobrescribimos el método para capturar response_time desde el contexto """
        input_line = super()._save_lines(question, answer, comment, overwrite_existing)

        response_time_map = self._context.get('response_time_map') or {}
        response_time = response_time_map.get(str(question.id))  # viene como string desde el JS

        if response_time and input_line:
            input_line.write({'response_time': float(response_time)})

        return input_line
    
    @api.model
    def create_session_ranking(self):
        for user_input in self:
            # Obtener la encuesta asociada
            survey = user_input.survey_id

            # Obtener la puntuación total del usuario para la encuesta
            total_score = round(sum(user_input.user_input_line_ids.mapped('score')), 2)

            # Crear el ranking para este usuario y encuesta
            self.env['survey.session_ranking'].create({
                'user_input_id': user_input.id,
                'survey_id': survey.id,
                'user_id': user_input.partner_id.id,  # Suponiendo que el usuario es el 'partner_id' de la entrada
                'total_score': total_score,
            })
            
            _logger.info("Nuevo Session Ranking creado")
            _logger.info("user_id: %s", user_input.partner_id.name)
            _logger.info("user_id: %s", user_input.partner_id.id)
            
    def _mark_done(self):
        res = super()._mark_done()
        self.create_session_ranking()
        return res

class QuizUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    response_time = fields.Float("Response Time", help="Time taken to answer the question in seconds")
    score = fields.Float("Puntuación")
    
    def _compute_score(self):
        for line in self:
            question = line.question_id
            survey = line.survey_id
            response_time = line.response_time
            selected_answer = line.suggested_answer_id

            # Validaciones básicas
            if not question or not survey or response_time is None or not selected_answer or survey.survey_type != 'quiz' or not survey.is_question_timed:
                line.score = 0.0
                continue

            # Solo asignar puntaje si la respuesta es correcta
            if selected_answer.is_correct:
                points = question.points
                time_limit = survey.time_per_question

                # Fórmula ajustada
                total_score = (1 - ((response_time / time_limit) / 2)) * points
                total_score = max(round(total_score, 2), 0)  # Evitar puntajes negativos

                line.score = total_score
            else:
                line.score = 0.0
            
           
                            
                    